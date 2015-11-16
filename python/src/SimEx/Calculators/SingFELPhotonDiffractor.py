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

        @param  :
        @type :
        @default :
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
                os.mkdir(pmi_dir)

        # Nothing to do if pmi output already in pmi subdir.
        if not os.path.basename(self.input_path) in os.listdir(pmi_dir):
            # If link already exists, just continue.
            ln_pmi_command = 'ln -s %s %s' % ( self.input_path, pmi_dir)
            proc = subprocess.Popen(ln_pmi_command, shell=True)
            proc.wait()

        preph5_location = inspect.getsourcefile(prepHDF5)
        # Link the prepHDF5 utility that gets called from singFEL code.
        if not os.path.isfile('prepHDF5.py'):
            ln_preph5_command = 'ln -s %s' % ( preph5_location )
            proc = subprocess.Popen(ln_preph5_command, shell=True)
            proc.wait()

        # Run the backengine command.
        command_string = 'mpirun \
-np 2 \
radiationDamageMPI \
 --inputDir . \
 --outputDir . \
 --beamFile %s \
 --geomFile %s \
 --configFile /dev/null \
 --uniformRotation 1 \
 --calculateCompton 0 \
 --sliceInterval 100\
 --numSlices 2\
 --pmiStartID 1 \
 --pmiEndID 1 \
 --numDP 2' % ( TestUtilities.generateTestFilePath('s2e.beam'), TestUtilities.generateTestFilePath('s2e.geom') )
        proc = subprocess.Popen(command_string, shell=True)
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
        pass # Nothing to be done since IO happens in backengine.

        ## Read the file.
        #file_handle = h5py.File(self.input_path, 'r')

        ## Setup empty dictionary.
        #parameters = {}

        ## Get photon energy.
        ##parameters['photon_energy'] = file_handle['params/photonEnergy'].value

        ## Read the electric field data and convert to numpy array.
        ##import ipdb; ipdb.set_trace()
        #Ehor = numpy.array(file_handle['/data/arrEhor'][:])
        #Ever = numpy.array(file_handle['/data/arrEver'][:])

        ## Store on object.
        #self.__e_field = numpy.array([Ehor, Ever])

        #super(SingFELPhotonDiffractor, self).__init__(parameters,self.input_path,self.output_path)

        #file_handle.close()

    def saveH5(self):
        """ """
        """
        Private method to save the object to a file.

        @param output_path : The file where to save the object's data.
        @type : string
        @default : None
        """
        pass # No action required since output is written in backengine.
