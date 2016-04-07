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
import os
import inspect
import subprocess
from SimEx.Calculators.AbstractPhotonDiffractor import AbstractPhotonDiffractor
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
        <br/><b>type</b>              : dict
        <br/><b>example</b> : parameters={ 'uniform_rotation'    : True,
                     'calculate_Compton'              : False,
                     'pmi_start_ID'                   : 1,
                     'pmi_stop_ID'                    : 1,
                     'number_of_diffraction_patterns' : 2,
                     'slice_interval'                 : 10,
                     'number_of_slices'               : 100,
                     'beam_parameter_file'            : 's2e.beam',
                     'beam_geometry_file'             : 's2e.geom',
                     }

        @param parameters['uniform_rotation']  : Whether or not to apply uniform sampling of the sample's rotations.
        <br/><b>type</b> : boolean

        @param parameters['calculate_Compton'] : Whether or not to calculate incoherent (Compton) scattering.
        <br/><b>type</b> : Bool

        @param parameters['pmi_start_ID'] : Index of the pmi file to start from.
        <br/><b>type</b> : int

        @param parameters['pmi_stop_ID'] : Index of the pmi file to stop at.
        <br/><b>type</b> : int

        @param parameters['number_of_diffraction_patterns'] : The number of diffraction patterns to calculate from each photon-matter interaction trajectory.
        <br/><b>type</b> : int

        @param parameters['slice_interval'] : The number of time slices to skip between two samplings of the photon-matter interaction trajectory.
        <br/><b>type</b> : int

        @param parameters['number_of_slices'] : Total number of slices in the pmi files."
        <br/><b>type</b> : int

        @param parameters['beam_parameter_file'] : Path of the beam parameter (.beam) file.
        <br/><b>type</b> : string

        @param parameters['beam_geometry_file'] : Path of the beam geometry (.geom) file.
        <br/><b>type</b> : string

        <br/><b>note</b>: The number of generated files is the number of pmi data files * number_of_diffraction_patterns.
        """

        super(SingFELPhotonDiffractor, self).__init__(parameters,input_path,output_path)

        # Check parameters.
        # Check that only accepted parameters are present.
        accepted_keys = ['uniform_rotation',
                         'calculate_Compton',
                         'slice_interval',
                         'number_of_slices',
                         'number_of_diffraction_patterns',
                         'pmi_start_ID',
                         'pmi_stop_ID',
                         'beam_parameter_file',
                         'beam_geometry_file']

        for k in self.parameters.keys():
            if k not in accepted_keys:
                raise RuntimeError( "The parameter '%s' is not a valid parameter for the SingFELPhotonDiffractor. " % (k))
        # Check each parameter individually and set defaults if not set.
        self.parameters['uniform_rotation'] = checkAndSetInstance(bool, self.parameters['uniform_rotation'], True)
        self.parameters['calculate_Compton'] = checkAndSetInstance(bool, self.parameters['calculate_Compton'], True)
        self.parameters['slice_interval'] = checkAndSetPositiveInteger(self.parameters['slice_interval'], 1)
        self.parameters['number_of_slices'] = checkAndSetPositiveInteger(self.parameters['number_of_slices'], 1)
        self.parameters['number_of_diffraction_patterns'] = checkAndSetPositiveInteger(self.parameters['number_of_diffraction_patterns'], 1)
        self.parameters['pmi_start_ID'] = checkAndSetPositiveInteger(self.parameters['pmi_start_ID'], 1)
        self.parameters['pmi_stop_ID'] = checkAndSetPositiveInteger(self.parameters['pmi_stop_ID'], 1)
        self.parameters['beam_parameter_file'] = checkAndSetInstance(str, self.parameters['beam_parameter_file'])
        if not os.path.isfile(self.parameters['beam_parameter_file']):
            raise IOError("%s is not a file." % (self.parameters['beam_parameter_file']))
        self.parameters['beam_geometry_file'] = checkAndSetInstance(str, self.parameters['beam_geometry_file'])
        if not os.path.isfile(self.parameters['beam_geometry_file']):
            raise IOError("%s is not a file." % (self.parameters['beam_geometry_file']))

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
        preph5_target =  os.path.join( input_dir, 'prepHDF5.py')
        # Link the prepHDF5 utility that gets called from singFEL code.
        if not os.path.isfile( preph5_target ):
            ln_preph5_command = 'ln -s %s %s' % ( preph5_location, preph5_target )
            proc = subprocess.Popen(ln_preph5_command, shell=True)
            proc.wait()

        # If parameters are given, map them to command line arguments.
        if 'uniform_rotation' in self.parameters.keys():
            uniform_rotation = {True : '1', False : '0'}[self.parameters['uniform_rotation']]
        else:
            uniform_rotation = 1

        if 'calculate_Compton' in self.parameters.keys():
            calculate_Compton = {True : 1, False : 0}[self.parameters['calculate_Compton']]
        else:
            calculate_Compton = 0

        if 'slice_interval' in self.parameters.keys():
            slice_interval = self.parameters['slice_interval']
        else:
            slice_interval = 100

        if 'number_of_slices' in self.parameters.keys():
            number_of_slices = self.parameters['number_of_slices']

        if 'pmi_start_ID' in self.parameters.keys():
            pmi_start_ID = self.parameters['pmi_start_ID']
        else:
            pmi_start_ID = 0

        if 'pmi_stop_ID' in self.parameters.keys():
            pmi_stop_ID = self.parameters['pmi_stop_ID']
        else:
            pmi_stop_ID = 0

        if 'number_of_diffraction_patterns' in self.parameters.keys():
            number_of_diffraction_patterns = self.parameters['number_of_diffraction_patterns']
        else:
            number_of_diffraction_patterns = 1

        if 'beam_parameter_file' in self.parameters.keys():
            beam_parameter_file = self.parameters['beam_parameter_file']
        else:
            raise RuntimeError("Beam parameter file must be given.")

        if 'beam_geometry_file' in self.parameters.keys():
            beam_geometry_file = self.parameters['beam_geometry_file']
        else:
            raise RuntimeError("Beam geometry file must be given.")


        if not os.path.isdir( self.output_path ):
            os.mkdir( self.output_path )
        output_dir = self.output_path

        config_file = '/dev/null'

        # Run the backengine command.
        command_sequence = ['mpirun',
                            '-np','2',
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
