""":module SingFELPhotonDiffractor: Module that holds the SingFELPhotonDiffractor class.  """
##########################################################################
#                                                                        #
# Copyright (C) 2015-2018 Carsten Fortmann-Grote                         #
# Contact: Carsten Fortmann-Grote <carsten.grote@xfel.eu>                #
#                                                                        #
# This file is part of simex_platform.                                   #
# simex_platform is free software: you can redistribute it and/or modify #
# it under the terms of the GNU General Public License as published by   #
# the Free Software Foundation, either version 3 of the License, or      #
# (at your option) any later version.                                    #
#                                                                        #
# simex_platform is distributed in the hope that it will be useful,      #
# but WITHOUT ANY WARRANTY; without even the implied warranty of         #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          #
# GNU General Public License for more details.                           #
#                                                                        #
# You should have received a copy of the GNU General Public License      #
# along with this program.  If not, see <http://www.gnu.org/licenses/>.  #
#                                                                        #
##########################################################################

from pysingfel.FileIO import saveAsDiffrOutFile, prepH5
from pysingfel.beam import Beam
from pysingfel.detector import Detector
from pysingfel.diffraction import calculate_molecularFormFactorSq
from pysingfel.particle import Particle
from pysingfel.radiationDamage import generateRotations, rotateParticle
from pysingfel.toolbox import convert_to_poisson
import copy
import h5py
import os
import subprocess
import shlex
import sys

from SimEx.Utilities.Units import electronvolt, meter, joule
from SimEx.Calculators.AbstractPhotonDiffractor import AbstractPhotonDiffractor
from SimEx.Parameters.SingFELPhotonDiffractorParameters import SingFELPhotonDiffractorParameters
from SimEx.Utilities import ParallelUtilities
from SimEx.Utilities.EntityChecks import checkAndSetInstance
from SimEx.Utilities import IOUtilities


class SingFELPhotonDiffractor(AbstractPhotonDiffractor):
    """
    :class SingFELPhotonDiffractor: Representing scattering from a molecular sample into a detector plane.
    """

    def __init__(self, parameters=None, input_path=None, output_path=None):
        """

        :param parameters: Parameters of the calculation (not data).
        :type parameters: dict || SingFELPhotonDiffractorParameters

        :param input_path: Path to hdf5 file holding the input data.
        :type input_path: str

        :param output_path: Path to hdf5 file for output.
        :type output_path: str
        """

        if parameters is None:
            parameters_default = SingFELPhotonDiffractorParameters(),
        else:
            parameters_default = None

        self.__parameters = checkAndSetInstance(SingFELPhotonDiffractorParameters,
                                                parameters,
                                                parameters_default,
                                                )

        # Handle sample geometry provenience.
        if self.__parameters.sample is None and input_path is None:
            raise AttributeError("One and only one of parameters.sample or input_path must be provided.")
        if self.__parameters.sample is not None:
            input_path = self.__parameters.sample

        # Init base class.
        super(SingFELPhotonDiffractor, self).__init__(parameters, input_path, output_path)

        self.__expected_data = ['/data/snp_<7 digit index>/ff',
                                '/data/snp_<7 digit index>/halfQ',
                                '/data/snp_<7 digit index>/Nph',
                                '/data/snp_<7 digit index>/r',
                                '/data/snp_<7 digit index>/T',
                                '/data/snp_<7 digit index>/Z',
                                '/data/snp_<7 digit index>/xyz',
                                '/data/snp_<7 digit index>/Sq_halfQ',
                                '/data/snp_<7 digit index>/Sq_bound',
                                '/data/snp_<7 digit index>/Sq_free',
                                '/history/parent/detail',
                                '/history/parent/parent',
                                '/info/package_version',
                                '/info/contact',
                                '/info/data_description',
                                '/info/method_description',
                                '/version']

        self.__provided_data = [
                                '/data/data',
                                '/data/diffr',
                                '/data/angle',
                                '/history/parent/detail',
                                '/history/parent/parent',
                                '/info/package_version',
                                '/info/contact',
                                '/info/data_description',
                                '/info/method_description',
                                '/params/geom/detectorDist',
                                '/params/geom/pixelWidth',
                                '/params/geom/pixelHeight',
                                '/params/geom/mask',
                                '/params/beam/photonEnergy',
                                '/params/beam/photons',
                                '/params/beam/focusArea',
                                '/params/info',
                                ]

    def expectedData(self):
        """ Query for the data expected by the Diffractor. """
        return self.__expected_data

    def providedData(self):
        """ Query for the data provided by the Diffractor. """
        return self.__provided_data

    def computeNTasks(self):
        resources = ParallelUtilities.getParallelResourceInfo()
        ncores = resources['NCores']
        nnodes = resources['NNodes']

        if self.parameters.cpus_per_task == "MAX":
            np = nnodes
        else:
            np = max(ncores//self.parameters.cpus_per_task, 1)

        return np, ncores

    def backengine(self):
        """ This method drives the backengine singFEL."""

        uniform_rotation = self.parameters.uniform_rotation
        calculate_Compton = int(self.parameters.calculate_Compton)
        slice_interval = self.parameters.slice_interval
        number_of_slices = self.parameters.number_of_slices
        pmi_start_ID = self.parameters.pmi_start_ID
        pmi_stop_ID = self.parameters.pmi_stop_ID
        number_of_diffraction_patterns = self.parameters.number_of_diffraction_patterns

        if not os.path.isdir(self.output_path):
            os.mkdir(self.output_path)
        self.__output_dir = self.output_path

        # If the sample is passed as a pdb, branch out to separate backengine implementation.
        if self.input_path.split(".")[-1].lower() == 'pdb':
            if not os.path.isfile(self.input_path):
                # Attempt to query from pdb.
                self.input_path = IOUtilities.checkAndGetPDB(self.input_path)

            return self._backengineWithPdb()

        # Ok, not a pdb, proceed.
        # Serialize the geometry file.
        beam_geometry_file = "tmp.geom"
        self.parameters.detector_geometry.serialize(beam_geometry_file)

        # Setup directory to pmi output.
        # Backengine expects a directory name, so have to check if
        # input_path is dir or file and handle accordingly.
        if os.path.isdir(self.input_path):
            input_dir = self.input_path

        elif os.path.isfile(self.input_path):
            input_dir = os.path.dirname(self.input_path)

        config_file = '/dev/null'

        # collect MPI arguments
        if self.parameters.forced_mpi_command == "":
            np, ncores = self.computeNTasks()
            mpicommand = ParallelUtilities.prepareMPICommandArguments(np)
        else:
            mpicommand = self.parameters.forced_mpi_command
# collect program arguments
        command_sequence = ['radiationDamageMPI',
                            '--inputDir',         str(input_dir),
                            '--outputDir',        str(self.__output_dir),
                            '--geomFile',         str(beam_geometry_file),
                            '--configFile',       str(config_file),
                            '--uniformRotation',  str(uniform_rotation),
                            '--calculateCompton', str(calculate_Compton),
                            '--sliceInterval',    str(slice_interval),
                            '--numSlices',        str(number_of_slices),
                            '--pmiStartID',       str(pmi_start_ID),
                            '--pmiEndID',         str(pmi_stop_ID),
                            '--numDP',            str(number_of_diffraction_patterns),
                            ]

        if self.parameters.beam_parameters is not None:
            beam_parameter_file = "tmp.beam"
            self.parameters.beam_parameters.serialize(beam_parameter_file)

            command_sequence.append('--beamFile')
            command_sequence.append(str(beam_parameter_file))

        # put MPI and program arguments together
        args = shlex.split(mpicommand) + command_sequence

        if 'SIMEX_VERBOSE' in os.environ:
            print(("SingFELPhotonDiffractor backengine command: "+" ".join(args)))

        # Run the backengine command.
        proc = subprocess.Popen(args)
        proc.wait()

        # Return the return code from the backengine.
        return proc.returncode

    def _backengineWithPdb(self):
        """ """
        """
        Run the diffraction simulation if the sample is a pdb.
        Codes is based on pysingfel/tests/test_particle.test_calFromPDB
        """

        # Dump self to file.
        fname = IOUtilities.getTmpFileName()
        self.dumpToFile(fname)

        # Setup the mpi call.
        forcedMPIcommand = self.parameters.forced_mpi_command

        if forcedMPIcommand == "" or forcedMPIcommand is None:
            (np, ncores) = self.computeNTasks()
            mpicommand = ParallelUtilities.prepareMPICommandArguments(np, ncores)
        else:
            mpicommand = forcedMPIcommand

        mpicommand += " ".join(("",sys.executable, __file__, fname))

        if 'SIMEX_VERBOSE' in os.environ:
            if 'MPI' in os.environ['SIMEX_VERBOSE']:
                print(("SingFELPhotonDiffractor backengine mpicommand: "+mpicommand))

        # Launch the system command.
        args = shlex.split(mpicommand)
        with subprocess.Popen(args, universal_newlines=True) as proc:
            out, err = proc.communicate()

        # Remove the dumped class.
        os.remove(fname)

        return proc.returncode

    def _run(self):
        """ """
        """ Workhorse function to run the pysingfel backengine.
        Called if run from the command-line with dill dump.
        """
        # Local import of MPI to avoid premature call to MPI.init().
        from mpi4py import MPI

        # Initialize MPI
        mpi_comm = MPI.COMM_WORLD
        mpi_rank = mpi_comm.Get_rank()
        mpi_size = mpi_comm.Get_size()

        # Perform common work on all cores.
        initial_particle = Particle()
        initial_particle.readPDB(self.input_path, ff='WK')

        # Generate rotations.
        quaternions = generateRotations(
                self.parameters.uniform_rotation,
                'xyz',
                self.parameters.number_of_diffraction_patterns,
               )

        # Setup the pysingfel detector using the simex object.
        # TODO: only the first panel is considered for now, can loop over panels later.
        detector = Detector(None)  # read geom file
        panel = self.parameters.detector_geometry.panels[0]
        detector.set_detector_dist(panel.distance_from_interaction_plane.m_as(meter))
        detector.set_pix_width(panel.pixel_size.m_as(meter))
        detector.set_pix_height(panel.pixel_size.m_as(meter))
        detector.set_numPix(panel.ranges["slow_scan_max"] - panel.ranges["slow_scan_min"] + 1,   # y
                            panel.ranges["fast_scan_max"] - panel.ranges["fast_scan_min"] + 1,   # x
                            )
        detector.set_center_x((panel.ranges["fast_scan_max"] + panel.ranges["fast_scan_min"] + 1) / 2.)
        detector.set_center_y((panel.ranges["slow_scan_max"] + panel.ranges["slow_scan_min"] + 1) / 2.)

        # Setup the beam based on the PhotonBeamParameters instance.
        beam = Beam(None)
        simex_beam = self.parameters.beam_parameters
        beam.set_photon_energy(simex_beam.photon_energy.m_as(electronvolt))
        beam.set_focus(simex_beam.beam_diameter_fwhm.m_as(meter))
        beam.set_photonsPerPulse(simex_beam.pulse_energy.m_as(joule) /
                                 simex_beam.photon_energy.m_as(joule))    # Will update all other attributes.

        # Initialize diffraction pattern
        detector.init_dp(beam)

        # Determine which patterns to run on which core.
        number_of_patterns_per_core = self.parameters.number_of_diffraction_patterns // mpi_size
        # Remainder of the division.
        remainder = self.parameters.number_of_diffraction_patterns % mpi_size
        # Pattern indices
        pattern_indices = list(range(self.parameters.number_of_diffraction_patterns))

        # Distribute patterns over cores.
        rank_indices = pattern_indices[mpi_rank*number_of_patterns_per_core:(mpi_rank+1)*number_of_patterns_per_core]
        # Distribute remainder
        if mpi_rank < remainder:
            rank_indices.append(pattern_indices[mpi_size * number_of_patterns_per_core + mpi_rank])

        # Setup the output file.
        outputName = self.__output_dir + '/diffr_out_' + '{0:07}'.format(mpi_comm.Get_rank()+1) + '.h5'

        if os.path.exists(outputName):
            os.remove(outputName)

        output_is_ready = False
        # Loop over assigned tasks
        for pattern_index in rank_indices:

            # Setup the output hdf5 file if not already done.
            if not output_is_ready:
                prepH5(outputName)
                output_is_ready = True

            # Make local copy of the sample.
            particle = copy.deepcopy(initial_particle)

            # Rotate particle.
            quaternion = quaternions[pattern_index, :]
            rotateParticle(quaternion, particle)

            # Calculate the diffraction intensity.
            detector_intensity = calculate_molecularFormFactorSq(particle, detector)

            # Correct for solid angle
            detector_intensity *= detector.solidAngle

            # Correct for polarization
            detector_intensity *= detector.PolarCorr

            # Multiply by photon fluence.
            detector_intensity *= beam.get_photonsPerPulsePerArea()

            # Poissonize.
            detector_counts = convert_to_poisson(detector_intensity)

            # Save to h5 file.
            saveAsDiffrOutFile(
                    outputName,
                    None,
                    pattern_index,
                    detector_counts,
                    detector_intensity,
                    quaternion,
                    detector,
                    beam,
                   )

            del particle

        mpi_comm.Barrier()

        return 0

    @property
    def data(self):
        """ Query for the field data. """
        return self.__data

    def _readH5(self):
        """ """
        """
        Private method for reading the hdf5 input and extracting the parameters
        and data relevant to initialize the object.
        """

        pass

    def saveH5(self):
        """ """
        """
        Private method to save the object to a file. Creates links to h5 files that all contain only one pattern.

        :param output_path: The file where to save the object's data.
        :type output_path: string, default b
        """

        # Path where individual h5 files are located.
        path_to_files = self.output_path

        # Setup new file.
        with h5py.File(self.output_path + ".h5", "w") as h5_outfile:

            # Files to read from.
            individual_files = [os.path.join(path_to_files, f) for f in os.listdir(path_to_files)]
            individual_files.sort()

            # Keep track of global parameters being linked.
            global_parameters = False
            # Loop over all individual files and link in the top level groups.
            for ind_file in individual_files:
                # Open file.
                with h5py.File(ind_file, 'r') as h5_infile:

                    # Links must be relative.
                    relative_link_target = os.path.relpath(path=ind_file, start=os.path.dirname(os.path.dirname(ind_file)))

                    # Link global parameters.
                    if not global_parameters:
                        global_parameters = True

                        h5_outfile["params"] = h5py.ExternalLink(relative_link_target, "params")
                        h5_outfile["info"] = h5py.ExternalLink(relative_link_target, "info")
                        h5_outfile["misc"] = h5py.ExternalLink(relative_link_target, "misc")
                        h5_outfile["version"] = h5py.ExternalLink(relative_link_target, "version")

                    for key in h5_infile['data']:

                        # Link in the data.
                        ds_path = "data/%s" % (key)
                        h5_outfile[ds_path] = h5py.ExternalLink(relative_link_target, ds_path)


        # Reset output path.
        self.output_path = self.output_path+".h5"


if __name__ == '__main__':
    SingFELPhotonDiffractor.runFromCLI()
