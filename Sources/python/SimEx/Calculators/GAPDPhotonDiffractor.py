""":module GAPDPhotonDiffractor: Module that holds the GAPDPhotonDiffractor class.  """
##########################################################################
#                                                                        #
# Copyright (C) 2020 Juncheng E                                          #
# Contact: Juncheng E <juncheng.e@xfel.eu>                               #
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

import copy
import h5py
import os
import subprocess
import shlex
import sys
import ase.io
import numpy as np

from SimEx.Utilities.Units import electronvolt, meter, joule
from SimEx.Calculators.AbstractPhotonDiffractor import AbstractPhotonDiffractor
from SimEx.Parameters.GAPDPhotonDiffractorParameters import GAPDPhotonDiffractorParameters
from SimEx.Utilities import ParallelUtilities
from SimEx.Utilities.EntityChecks import checkAndSetInstance
from SimEx.Utilities import IOUtilities


class GAPDPhotonDiffractor(AbstractPhotonDiffractor):
    """
    :class GAPDPhotonDiffractor: Representing scattering from a molecular sample into a detector plane.
    """
    def __init__(self, parameters=None, input_path=None, output_path=None):
        """

        :param parameters: Parameters of the calculation (not data).
        :type parameters: dict || GAPDPhotonDiffractorParameters

        :param input_path: Path to hdf5 file holding the input data.
        :type input_path: str

        :param output_path: Path to hdf5 file for output.
        :type output_path: str
        """

        if parameters is None:
            parameters_default = GAPDPhotonDiffractorParameters(),
        else:
            parameters_default = None

        self.__parameters = checkAndSetInstance(
            GAPDPhotonDiffractorParameters,
            parameters,
            parameters_default,
        )

        # Handle sample geometry provenience.
        if self.__parameters.sample is None and input_path is None:
            raise AttributeError(
                "One and only one of parameters.sample or input_path must be provided."
            )
        if self.__parameters.sample is not None:
            input_path = self.__parameters.sample

        # Init base class.
        super(GAPDPhotonDiffractor, self).__init__(parameters, input_path,
                                                   output_path)

        # expected X-ray beam data
        # TODO: define this with Aljosa
        self.__expected_prop_data = []

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
            np = max(ncores // self.parameters.cpus_per_task, 1)

        return np, ncores

    # Atom data
    def prepareAtomData(self):
        """ Prepare atomoic configuration for GAPD """

        # If the sample is passed as a pdb, convert '.pdb' into '.xyz'
        if self.input_path.split(".")[-1].lower() == 'pdb':
            if not os.path.isfile(self.input_path):
                # Attempt to query from pdb.
                pdb_path = IOUtilities.checkAndGetPDB(self.input_path)
            # Convert pdb to xyz
            a = ase.io.read(pdb_path)
            ase.io.write('atoms.xyz', a)
            self.input_path = 'atoms.xyz'

    def prepareDetector(self):
        """ Setup GAPD detector using simex objects. """

        # Read the first panel of the detector
        # We have only one panel representing a large detector here
        panel = self.parameters.detector_geometry.panels[0]

        _self.det_ny = panel.ranges["slow_scan_max"] - panel.ranges[
            "slow_scan_min"] + 1
        _self.det_nx = panel.ranges["fast_scan_max"] - panel.ranges[
            "fast_scan_min"] + 1
        _self.det_s2d = panel.distance_from_interaction_plane.m_as(
            meter) * 1000.0  # mm
        _self.det_ps = panel.pixel_size.m_as(meter) * 1e6  # um
        _self.det_conerx = detector_panel.corners['x']
        _self.det_conery = detector_panel.corners['y']

    def prepareBeam(self):
        """ Setup GAPD beam using simex objects. """

        beam = self.parameters.beam_parameters
        _self.beam_energy = beam.photon_energy.m_as(electronvolt)/1000.0 # keV
        _self.beam_diameter = beam.beam_diameter_fwhm.m_as(meter)*100 # cm
        _self.beam_fluence = beam.pulse_energy.m_as(joule)/np.pi/(_self.beam_diameter*_self.beam_diameter/4) # J/cm^2
     

    def writeParam(self, in_param_file=None):
        """ Put diffractor parameters into GAPD param file

        :param in_param_file: The stream to write the serialized geometry to (default sys.stdout).
        :type  in_param_file: File like object.

        """

        # If this is a string, open a corresponding file.
        if isinstance(in_param_file, str):
            with open(in_param_file, 'w') as fstream:

                # Detector part
                fstream.write('xyz {}'.format(_self.input_path))
                fstream.write('pn {} {}'.format(_self.det_nx, _self.det_ny))
                fstream.write('ps {}'.format(_self.det_ps))
                fstream.write('corner {} {}'.format(_self.det_conerx,
                                                    _self.det_conery))
                fstream.write('s2d {}'.format(_self.det_s2d))

                # Detector perpendicular to x-ray beam
                fstream.write('nid 0 0 -1')
                fstream.write('dx 1 0 0')

                # Beam part:
                fstream.write('beam x') # It's x-ray beam for GAPD
                fstream.write('mono e {}'.format(_self.beam_energy))
                fstream.write('fluence {}'.format(_self.beam_fluence))
                fstream.write('polarization_angle 0')
                # Beam is propograted along -z direction of the sample
                fstream.write('id 0 0 -1')

                # Output file:
                fstream.write('output_fn {}'.format(self.output_path))

        if not hasattr(in_param_file, "write"):
            raise IOError("The stream % is not writable." % (stream))

    def backengine(self):
        """ Prepare parameters and data needed to run GAPD diffractor."""

        # Diffractor parameters
        uniform_rotation = self.parameters.uniform_rotation
        calculate_Compton = int(self.parameters.calculate_Compton)
        slice_interval = self.parameters.slice_interval
        number_of_slices = self.parameters.number_of_slices
        pmi_start_ID = self.parameters.pmi_start_ID
        pmi_stop_ID = self.parameters.pmi_stop_ID
        number_of_diffraction_patterns = self.parameters.number_of_diffraction_patterns

        # Diffractor atom data
        self.prepareAtomData()

        # Diffractor detector data
        self.prepareDetector()

        # Diffractor beam data
        self.prepareBeam()

        # Diffractor output
        if not os.path.isdir(self.output_path):
            os.mkdir(self.output_path)
        self.__output_dir = self.output_path

        # Put calculator parameters into GAPD param file.
        in_param_file = "in.param"
        self.writeParam(in_param_file)

        # Setup directory to propogated beam folder
        # Backengine expects a directory name, so have to check if
        # input_path is dir or file and handle accordingly.
        if os.path.isdir(self.input_path):
            input_dir = self.input_path

        elif os.path.isfile(self.input_path):
            input_dir = os.path.dirname(self.input_path)

        # collect MPI arguments
        if self.parameters.forced_mpi_command == "":
            np, ncores = self.computeNTasks()
            mpicommand = ParallelUtilities.prepareMPICommandArguments(np)
        else:
            mpicommand = self.parameters.forced_mpi_command

        # collect program arguments
        command_sequence = ['GAPD-SimEx', '-i', str(in_param_file)]

        # put MPI and program arguments together
        args = shlex.split(mpicommand) + command_sequence

        if 'SIMEX_VERBOSE' in os.environ:
            print(
                ("GAPDPhotonDiffractor backengine command: " + " ".join(args)))

        # Run the backengine command.
        proc = subprocess.Popen(args)
        proc.wait()

        # TODO: return code running status

        # Return the return code from the backengine.
        return proc.returncode

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
            individual_files = [
                os.path.join(path_to_files, f)
                for f in os.listdir(path_to_files)
            ]
            individual_files.sort()

            # Keep track of global parameters being linked.
            global_parameters = False
            # Loop over all individual files and link in the top level groups.
            for ind_file in individual_files:
                # Open file.
                with h5py.File(ind_file, 'r') as h5_infile:

                    # Links must be relative.
                    relative_link_target = os.path.relpath(
                        path=ind_file,
                        start=os.path.dirname(os.path.dirname(ind_file)))

                    # Link global parameters.
                    if not global_parameters:
                        global_parameters = True

                        h5_outfile["params"] = h5py.ExternalLink(
                            relative_link_target, "params")
                        h5_outfile["info"] = h5py.ExternalLink(
                            relative_link_target, "info")
                        h5_outfile["misc"] = h5py.ExternalLink(
                            relative_link_target, "misc")
                        h5_outfile["version"] = h5py.ExternalLink(
                            relative_link_target, "version")

                    for key in h5_infile['data']:

                        # Link in the data.
                        ds_path = "data/%s" % (key)
                        h5_outfile[ds_path] = h5py.ExternalLink(
                            relative_link_target, ds_path)

        # Reset output path.
        self.output_path = self.output_path + ".h5"


# if __name__ == '__main__':
    # GAPDPhotonDiffractor.runFromCLI()
