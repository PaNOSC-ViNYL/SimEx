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

""" Module that holds the SingFELPhotonDiffractor class.

    @author : CFG
    @institution : XFEL
    @creation 20151104

"""
import inspect
import os
import subprocess

from SimEx.Calculators.AbstractPhotonDiffractor import AbstractPhotonDiffractor
from SimEx.Parameters.SingFELPhotonDiffractorParameters import SingFELPhotonDiffractorParameters
from SimEx.Utilities.EntityChecks import checkAndSetInstance, checkAndSetPositiveInteger

import prepHDF5

class SingFELPhotonDiffractor(AbstractPhotonDiffractor):
    """
    Class representing a x-ray free electron laser photon propagator.
    """

    def __init__(self,  parameters=None, input_path=None, output_path=None):
        """
        Constructor for the xfel photon propagator.

        @param  parameters : singFEL parameters.
        <br/><b>type</b>   : SingFELPhotonDiffractorParameters instance.
        @default : None.
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

        preph5_target =  os.path.join( input_dir, 'prepHDF5.py')
        # Link the prepHDF5 utility that gets called from singFEL code.
        if not os.path.isfile( preph5_target ):
            os.symlink(preph5_location, preph5_target)

        uniform_rotation = int( self.parameters.uniform_rotation)
        calculate_Compton = int( self.parameters.calculate_Compton )
        slice_interval = self.parameters.slice_interval
        number_of_slices = self.parameters.number_of_slices
        pmi_start_ID = self.parameters.pmi_start_ID
        pmi_stop_ID = self.parameters.pmi_stop_ID
        number_of_diffraction_patterns = self.parameters.number_of_diffraction_patterns
        number_of_MPI_processes = self.parameters.number_of_MPI_processes
        beam_parameter_file = self.parameters.beam_parameter_file
        beam_geometry_file = self.parameters.beam_geometry_file

        if not os.path.isdir( self.output_path ):
            os.mkdir( self.output_path )
        output_dir = self.output_path

        config_file = '/dev/null'

        # Run the backengine command.
        command_sequence = ['mpirun',
                            '-np',                str(number_of_MPI_processes) ,
                            'radiationDamageMPI',
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
                            ]
        proc = subprocess.Popen(command_sequence)
        proc.wait()


        if os.path.islink(preph5_target):
            os.remove(preph5_target)

        # Return the return code from the backengine.
        return proc.returncode

    @property
    def data(self):
        """ Query for the field data. """
        return self.__data

    def _readH5(self):
        """ """
        """ Private method for reading the hdf5 input and extracting the parameters and data relevant to initialize the object. """
        pass # Nothing to be done since IO happens in backengine.

    def saveH5(self):
        """ """
        """
        Private method to save the object to a file.

        @param output_path : The file where to save the object's data.
        <br/><b>type</b> : string
        <br/><b>default</b> : None
        """
        pass # No action required since output is written in backengine.
