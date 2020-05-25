""":module CrystFELPhotonDiffractor: Module that holds the CrystFELPhotonDiffractor class.  """
##########################################################################
#                                                                        #
# Copyright (C) 2017-2018 Carsten Fortmann-Grote                         #
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
import h5py
import numpy
import os, sys
import subprocess,shlex
import tempfile

from SimEx.Calculators.AbstractPhotonDiffractor import AbstractPhotonDiffractor
from SimEx.Parameters.CrystFELPhotonDiffractorParameters import CrystFELPhotonDiffractorParameters
from SimEx.Parameters.PhotonBeamParameters import propToBeamParameters
from SimEx.Parameters.DetectorGeometry import _detectorGeometryFromString
from SimEx.Utilities import ParallelUtilities
from SimEx.Utilities.EntityChecks import checkAndSetInstance
from SimEx.Utilities.Units import electronvolt, meter
from SimEx.Utilities import IOUtilities

class CrystFELPhotonDiffractor(AbstractPhotonDiffractor):
    """
    :class CrystFELPhotonDiffractor: Represents simulation of photon diffraction by crystals using CrystFEL.oattern_sim.
    """

    def __init__(self, parameters=None, input_path=None, output_path=None):
        """

        :param parameters: Parameters of the calculation (not data).
        :type parameters:  CrystFELPhotonDiffractorParameters

        :param input_path: Path to hdf5 file holding the input data.
        :type input_path: str

        :param output_path: Path to hdf5 file for output.
        :type output_path: str
        """

        # Set default parameters if no parameters given.
        if parameters is None:
            raise ValueError( "Parameters must at least specify the sample structure, e.g. in pdb format.")
        else:
            self.__parameters = checkAndSetInstance( CrystFELPhotonDiffractorParameters, parameters, None )


        # Dummy input path since none required (we don't read from a beam propgation yet.)
        if input_path is None:
            input_path = os.path.dirname(__file__)
        else:
            if parameters.beam_parameters is not None:
                raise RuntimeError("Beam parameters can only be passed through the parameters object or via the input_path argument.")
            parameters.beam_parameters = propToBeamParameters( input_path )

        if output_path is None:
            output_path = os.path.join(os.path.dirname(__file__), "diffr")

        # Init base class.
        super(CrystFELPhotonDiffractor, self).__init__(parameters,input_path,output_path)

        ### FIXME
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
        return None

    def providedData(self):
        """ Query for the data provided by the Diffractor. """
        return None


    def computeNTasks(self):
        """ Calculate the number of MPI tasks as function of available resources and
        assigned cpus per task."""


        resources=ParallelUtilities.getParallelResourceInfo()
        ncores=resources['NCores']
        nnodes=resources['NNodes']

        if nnodes > 1:
            raise RuntimeError( "Backengine does not support MPI parallelism. " )

        if self.parameters.cpus_per_task=="MAX":
            np=nnodes
        else:
            np=max(int(ncores/int(self.parameters.cpus_per_task)),1)

        return np

    def backengine(self):
        """ This method drives the backengine CrystFEL.pattern_sim."""

        # pattern_sim backengine does not support MPI.
        return self._run()

        # collect MPI arguments
        if self.parameters.forced_mpi_command=="":
            np=self.computeNTasks()
            mpicommand=ParallelUtilities.prepareMPICommandArguments(np)
        else:
            mpicommand=self.parameters.forced_mpi_command

        # Dump to a temporary file.
        fname = IOUtilities.getTmpFileName()
        self.dumpToFile(fname)

        mpicommand += " ".join([" ",sys.executable, __file__, fname])
        args = shlex.split(mpicommand)


        if 'SIMEX_VERBOSE' in os.environ and os.environ['SIMEX_VERBOSE'] == 'MPI':
            print("MPI command: "+mpicommand)

        try:
            proc = subprocess.Popen(args,universal_newlines=True)
            proc.wait()
        except:
            raise
        finally:
            os.remove(fname)

        return proc.returncode


    def _run(self):
        """ Perform the actual calls to pattern_sim. """

        # Setup directory structure as needed.
        if not os.path.isdir( self.output_path ):
            os.makedirs( self.output_path )

        output_file_base = os.path.join( self.output_path, "diffr_out")

        if self.parameters.number_of_diffraction_patterns == 1:
            output_file_base += "_0000001.h5"

        # Serialize geometry if necessary.
        if isinstance(self.parameters.detector_geometry, str) and os.path.isfile(self.parameters.detector_geometry):
            with open(self.parameters.detector_geometry) as tmp_geom_file:
                geom_string = "\n".join(tmp_geom_file.readlines())

            self.parameters.detector_geometry = _detectorGeometryFromString( geom_string )

        geom_file = tempfile.NamedTemporaryFile(suffix=".geom", delete=True)
        geom_filename = geom_file.name
        self.parameters.detector_geometry.serialize(stream=geom_filename, caller=self.parameters)

        # Setup command, minimum set first.
        # Distribute patterns over available processes in round-robin.
        command_sequence = ['pattern_sim',
                            '-p%s'                  % self.parameters.sample,
                            '--geometry=%s'         % geom_filename,
                            '--output=%s'           % (output_file_base),
                            '--number=%d'           % (self.parameters.number_of_diffraction_patterns)
                            ]
        # Handle random rotation as requested.
        if self.parameters.uniform_rotation is True:
            command_sequence.append('--random-orientation')
            command_sequence.append('--really-random')

        if self.parameters.beam_parameters is not None:
            command_sequence.append('--photon-energy=%f' % (self.parameters.beam_parameters.photon_energy.m_as(electronvolt)))
            command_sequence.append('--beam-bandwidth=%f' % (self.parameters.beam_parameters.photon_energy_relative_bandwidth))
            nphotons = self.parameters.beam_parameters.pulse_energy / self.parameters.beam_parameters.photon_energy
            command_sequence.append('--nphotons=%e' % (nphotons))
            command_sequence.append('--beam-radius=%e' % (self.parameters.beam_parameters.beam_diameter_fwhm.m_as(meter)/2.))
            command_sequence.append('--spectrum=%s' % (self.parameters.beam_parameters.photon_energy_spectrum_type.lower()))
            if self.parameters.beam_parameters.photon_energy_spectrum_type.lower() == "sase":
                command_sequence.append('--sample-spectrum=512')

        # Handle intensities list if present.
        if self.parameters.intensities_file is not None:
            command_sequence.append('--intensities=%s' % (self.parameters.intensities_file))

        # Handle powder if present.
        if self.parameters.powder is True:
            command_sequence.append('--powder=%s' % (os.path.join(self.output_path, "powder.h5")))

        # Handle size range if present.
        if self.parameters.crystal_size_min is not None:
            command_sequence.append('--min-size=%f' % (self.parameters.crystal_size_min.m_as(1e-9*meter) ))
        if self.parameters.crystal_size_max is not None:
            command_sequence.append('--max-size=%f' % (self.parameters.crystal_size_max.m_as(1e-9*meter) ))

        # Handle gpu acceleration.
        if self.parameters.gpus_per_task > 0:
            # Check if crystfel was built with opencv support.
            # Get pattern_sim's path.
            pattern_sim_path = subprocess.check_output(shlex.split("which pattern_sim"))[:-1].decode('utf-8')
            # Get list of dynamic dependencies.
            ldd = subprocess.check_output(shlex.split("ldd "+pattern_sim_path)).decode('utf-8')
            if "libOpenCL.so.1" in ldd:
                command_sequence.append('--gpu')

        if 'SIMEX_VERBOSE' in os.environ:
            print("Pattern_sim call: "+ " ".join(command_sequence))

        # Run the backengine command.
        proc = subprocess.Popen(command_sequence)
        proc.wait()

        return proc.returncode

    @property
    def data(self):
        """ Query for the field data. """
        return self.__data

    def _readH5(self):
        """ """
        """ Private method for reading the hdf5 input and extracting the parameters and data relevant to initialize the object. """
        pass

    def saveH5(self):
        """
        Method to save the output to a file. Creates links to h5 files that all contain only one pattern.
        """
        # Path where individual h5 files are located.
        path_to_files = self.output_path

        # Rename files.
        _rename_files(path_to_files)

        print("Linking all patterns into %s.h5." % (self.output_path))

        # Setup new file.
        with h5py.File( self.output_path + ".h5" , "w") as h5_outfile:

            data_group = h5_outfile.create_group("data")
            params_group = h5_outfile.create_group("params")
            beam_params_group = params_group.create_group("beam")
            geom_params_group = params_group.create_group("geom")

            beam_params_group["photonEnergy"] = self.parameters.beam_parameters.photon_energy.m_as(electronvolt)
            beam_params_group["photonEnergy"].attrs["unit_symbol"] = "eV"
            beam_params_group["photonEnergy"].attrs["unit_longname"] = "electronvolt"
            beam_params_group["focusArea"] = self.parameters.beam_parameters.beam_diameter_fwhm.m_as(meter)**2
            beam_params_group["focusArea"].attrs["unit_symbol"] = "m^2"
            beam_params_group["focusArea"].attrs["unit_longname"] = "square_metre"

            geom_params_group["detectorDist"] = self.parameters.detector_geometry.panels[0].distance_from_interaction_plane.m_as(meter)

            mask = self.parameters.detector_geometry.panels[0].mask
            if mask is None:
                mask = numpy.ones((self.parameters.detector_geometry.panels[0].number_of_pixels_slow,
                                   self.parameters.detector_geometry.panels[0].number_of_pixels_fast))
            geom_params_group["mask"] = mask
            geom_params_group["pixelHeight"] = self.parameters.detector_geometry.panels[0].pixel_size.m_as(meter)
            geom_params_group["pixelWidth"] = self.parameters.detector_geometry.panels[0].pixel_size.m_as(meter)

            # Files to read from.
            individual_files = [os.path.join( path_to_files, f ) for f in os.listdir( path_to_files ) ]
            individual_files.sort()

            # Loop over all individual files and link in the top level groups.
            for ind_file in individual_files:
                # Open file.
                with h5py.File( ind_file, 'r') as h5_infile:

                    # Get file ID.
                    file_ID = os.path.split(ind_file)[-1].split(".h5")[0].split("_")[-1]

                    # Create group
                    data_group.create_group(file_ID)

                    # Links must be relative.
                    relative_link_target = os.path.relpath(path=ind_file, start=os.path.dirname(os.path.dirname(ind_file)))

                    # Link in the data.
                    path_in_target = "/data/data"
                    path_in_origin = "data/%s/data" % (file_ID)
                    h5_outfile[path_in_origin] = h5py.ExternalLink(relative_link_target, path_in_target)

                    # Close input file.
                    h5_infile.close()

            # Close file.
            h5_outfile.close()

            # Reset output_path
            self.output_path = self.output_path+".h5"

def _rename_files(path):
    """ """
    """
    Renames all files generated by pattern_sim to simex conform filenames."""

    old_wd = os.getcwd()
    os.chdir( path )
    original_files = os.listdir(".")

    original_files.sort()

    for i,f in enumerate(original_files):
        if not f.split(".")[-1] == "h5":
            continue

        new_filename = "%s_%07d.h5" % ("".join(f.split("-")[:-1]),i+1)
        print("Renaming %s to %s." % (f, new_filename))
        os.rename(f, new_filename)

    os.chdir( old_wd )


if __name__ == '__main__':
    CrystFELPhotonDiffractor.runFromCLI()
