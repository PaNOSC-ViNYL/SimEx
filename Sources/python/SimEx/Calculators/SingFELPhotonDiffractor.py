""" Module that holds the SingFELPhotonDiffractor class.  """
##########################################################################
#                                                                        #
# Copyright (C) 2015 Carsten Fortmann-Grote                              #
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
import inspect
import os
import subprocess,shlex

import prepHDF5

from SimEx.Calculators.AbstractPhotonDiffractor import AbstractPhotonDiffractor
from SimEx.Parameters.SingFELPhotonDiffractorParameters import SingFELPhotonDiffractorParameters
from SimEx.Utilities import ParallelUtilities
from SimEx.Utilities.EntityChecks import checkAndSetInstance, checkAndSetPositiveInteger

class SingFELPhotonDiffractor(AbstractPhotonDiffractor):
    """
    Class representing a x-ray free electron laser photon propagator.
    """

    def __init__(self,  parameters=None, input_path=None, output_path=None):
        """

        :param parameters: Parameters of the calculation (not data).
        :type parameters: dict || SingFELPhotonDiffractorParameters

        :param input_path: Path to hdf5 file holding the input data.
        :type input_path: str

        :param output_path: Path to hdf5 file for output.
        :type output_path: str
        """

        if isinstance( parameters, dict ):
            parameters = SingFELPhotonDiffractorParameters( parameters_dictionary = parameters )

        # Set default parameters if no parameters given.
        if parameters is None:
            self.__parameters = checkAndSetInstance( SingFELPhotonDiffractorParameters, parameters, SingFELPhotonDiffractorParameters() )
        else:
            self.__parameters = checkAndSetInstance( SingFELPhotonDiffractorParameters, parameters, None )


        # Init base class.
        super(SingFELPhotonDiffractor, self).__init__(parameters,input_path,output_path)

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
        resources=ParallelUtilities.getParallelResourceInfo()
        ncores=resources['NCores']
        nnodes=resources['NNodes']

        if self.parameters.cpus_per_task=="MAX":
            np=nnodes
        else:
            np=max(int(ncores/int(self.parameters.cpus_per_task)),1)

        return np

    def backengine(self):
        """ This method drives the backengine singFEL."""

        # Setup directory to pmi output.
        # Backengine expects a directory name, so have to check if
        # input_path is dir or file and handle accordingly.
        if os.path.isdir( self.input_path ):
            input_dir = self.input_path

        elif os.path.isfile( self.input_path ):
            input_dir = os.path.dirname( self.input_path )

        # Link the  python utility so the backengine can find it.
        ### Yes, this is messy.
        preph5_location = inspect.getsourcefile(prepHDF5)
        if preph5_location is None:
            raise RuntimeError("prepHDF5.py not found. Aborting the calculation.")

        uniform_rotation = self.parameters.uniform_rotation
        calculate_Compton = int( self.parameters.calculate_Compton )
        slice_interval = self.parameters.slice_interval
        number_of_slices = self.parameters.number_of_slices
        pmi_start_ID = self.parameters.pmi_start_ID
        pmi_stop_ID = self.parameters.pmi_stop_ID
        number_of_diffraction_patterns = self.parameters.number_of_diffraction_patterns
        beam_parameter_file = self.parameters.beam_parameter_file
        beam_geometry_file = self.parameters.beam_geometry_file

        if not os.path.isdir( self.output_path ):
            os.mkdir( self.output_path )
        output_dir = self.output_path

        config_file = '/dev/null'

# collect MPI arguments
        if self.parameters.forced_mpi_command=="":
            np=self.computeNTasks()
            mpicommand=ParallelUtilities.prepareMPICommandArguments(np)
        else:
            mpicommand=self.parameters.forced_mpi_command
# collect program arguments
        command_sequence = ['radiationDamageMPI',
                            '--inputDir',         str(input_dir),
                            '--outputDir',        str(output_dir),
                            '--beamFile',         str(beam_parameter_file),
                            '--geomFile',         str(beam_geometry_file),
                            '--configFile',       str(config_file),
                            '--uniformRotation',  str(uniform_rotation),
                            '--calculateCompton', str(calculate_Compton),
                            '--sliceInterval',    str(slice_interval),
                            '--numSlices',        str(number_of_slices),
                            '--pmiStartID',       str(pmi_start_ID),
                            '--pmiEndID',         str(pmi_stop_ID),
                            '--numDP',            str(number_of_diffraction_patterns),
                            '--prepHDF5File',     preph5_location,
                            ]

        # put MPI and program arguments together
        args = shlex.split(mpicommand) + command_sequence

        if 'SIMEX_VERBOSE' in os.environ:
            print("SingFELPhotonDiffractor backengine command: "+" ".join(args))

        # Run the backengine command.
        proc = subprocess.Popen(args)
        proc.wait()

        # Return the return code from the backengine.
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
        """ """
        """
        Private method to save the object to a file. Creates links to h5 files that all contain only one pattern.

        :param output_path: The file where to save the object's data.
        :type output_path: string, default b
        """

        # Path where individual h5 files are located.
        path_to_files = self.output_path

        # Setup new file.
        h5_outfile = h5py.File( self.output_path + ".h5" , "w")

        # Files to read from.
        individual_files = [os.path.join( path_to_files, f ) for f in os.listdir( path_to_files ) ]
        individual_files.sort()

        # Keep track of global parameters being linked.
        global_parameters = False
        # Loop over all individual files and link in the top level groups.
        for ind_file in individual_files:
            # Open file.
            h5_infile = h5py.File( ind_file, 'r')

            # Get file ID.
            file_ID = os.path.split(ind_file)[-1].split(".h5")[0].split("_")[-1]

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

            # Close input file.
            h5_infile.close()

        # Close file.
        h5_outfile.close()

        # Reset output path.
        self.output_path = self.output_path+".h5"





