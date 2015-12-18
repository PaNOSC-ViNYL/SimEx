""" Module that holds the SingFELPhotonDiffractor class.

    @author : CFG
    @institution : XFEL
    @creation 20151104

"""
import os
import inspect
import subprocess
from SimEx.Calculators.AbstractPhotonDiffractor import AbstractPhotonDiffractor

from TestUtilities import TestUtilities

from SimEx.Utilities import prepHDF5

class SingFELPhotonDiffractor(AbstractPhotonDiffractor):
    """
    Class representing a x-ray free electron laser photon propagator.
    """

    def __init__(self,  parameters=None, input_path=None, output_path=None):
        """
        Constructor for the xfel photon propagator.

        @param  parameters : Dictionary of singFEL parameters.
        @type : dict
        @example : parameters={ 'uniform_rotation': True,
                     'calculate_Compton' : False,
                     'slice_interval' : 100,
                     'number_of_slices' : 2,
                     'pmi_start_ID' : 1,
                     'pmi_stop_ID'  : 1,
                     'number_of_diffraction_patterns' : 2,
                     'beam_parameter_file' : TestUtilities.generateTestFilePath('s2e.beam'),
                     'beam_geometry_file' : TestUtilities.generateTestFilePath('s2e.geom'),
                     }
        """

        # Initialize base class.
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

        self.__provided_data = ['/-input_dir'
                                '/-output_dir'
                                '/-config_file'
                                '/-b',
                                '/-g',
                                '/-uniformRotation',
                                '/-calculateCompton',
                                '/-sliceInterval',
                                '/-numSlices',
                                '/-pmiStartID',
                                '/-pmiEndID',
                                '/-dpID',
                                '/-numDP',
                                '/-USE_GPU',
                                '/version']


    def expectedData(self):
        """ Query for the data expected by the Diffractor. """
        return self.__expected_data

    def providedData(self):
        """ Query for the data provided by the Diffractor. """
        return self.__provided_data

    def backengine(self):
        """ This method drives the backengine code, in this case Chuck's singFEL."""

        # Link pmi output
        # Setup directory to pmi output.
        pmi_dir = os.path.abspath(os.path.join('.', 'pmi'))

        # Check if path is a file.
        if os.path.isfile(pmi_dir):
            raise OSError("Cannot create directory %s because a file with the same name already exists.")

        # Create if not existing.
        if not os.path.exists(pmi_dir):
            # If input is not a dir, first create pmi/
            if not os.path.isdir(self.input_path):
                os.mkdir(pmi_dir)
            # Link input to pmi/.
            ln_pmi_command = 'ln -s %s %s' % ( self.input_path, pmi_dir)
            proc = subprocess.Popen(ln_pmi_command, shell=True)
            proc.wait()

        ## Nothing to do if pmi output already in pmi subdir.
        #if not os.path.basename(self.input_path) in os.listdir(pmi_dir):
            ## If link already exists, just continue.
            #ln_pmi_command = 'ln -s %s %s' % ( self.input_path, pmi_dir)
            #proc = subprocess.Popen(ln_pmi_command, shell=True)
            #proc.wait()

        preph5_location = inspect.getsourcefile(prepHDF5)
        # Link the prepHDF5 utility that gets called from singFEL code.
        if not os.path.isfile('prepHDF5.py'):
            ln_preph5_command = 'ln -s %s' % ( preph5_location )
            proc = subprocess.Popen(ln_preph5_command, shell=True)
            proc.wait()

        # If parameters are given, map them to command line arguments.
        if 'uniform_rotation' in self.parameters.keys():
            uniform_rotation = {True : 'true', False : 'false'}[self.parameters['uniform_rotation']]
        else:
            uniform_rotation = '1'

        if 'calculate_Compton' in self.parameters.keys():
            calculate_Compton = {True : '1', False : '0'}[self.parameters['calculate_Compton']]
        else:
            calculate_Compton = '0'

        if 'slice_interval' in self.parameters.keys():
            slice_interval = str(self.parameters['slice_interval'])
        else:
            slice_interval = 100

        if 'number_of_slices' in self.parameters.keys():
            number_of_slices = str(self.parameters['number_of_slices'])

        if 'pmi_start_ID' in self.parameters.keys():
            pmi_start_ID = str(self.parameters['pmi_start_ID'])
        else:
            pmi_start_ID = 0

        if 'pmi_stop_ID' in self.parameters.keys():
            pmi_stop_ID = str(self.parameters['pmi_stop_ID'])
        else:
            pmi_stop_ID = 0

        if 'number_of_diffraction_patterns' in self.parameters.keys():
            number_of_diffraction_patterns = str(self.parameters['number_of_diffraction_patterns'])
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



        input_dir = '.'

        if number_of_diffraction_patterns > 1:
            if not os.path.isdir( self.output_path ):
                os.mkdir( self.output_path )
            output_dir = self.output_path

        else:
            output_dir = '.'

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

        # Remove the simlink
        if os.path.islink(pmi_dir):
            os.remove(pmi_dir)
        if os.path.islink('prepHDF5.py'):
            os.remove('prepHDF5.py')

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
        @type : string
        @default : None
        """
        pass # No action required since output is written in backengine.
