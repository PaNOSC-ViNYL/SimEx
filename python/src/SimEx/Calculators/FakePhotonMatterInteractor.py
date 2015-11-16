""" Module that holds the FakePhotonMatterInteractor class.

    @author : CFG
    @institution : XFEL
    @creation 20151111

"""
import subprocess

from SimEx.Calculators.AbstractPhotonInteractor import AbstractPhotonInteractor
from TestUtilities.TestUtilities import generateTestFilePath


class FakePhotonMatterInteractor(AbstractPhotonInteractor):
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
        super(FakePhotonMatterInteractor, self).__init__(parameters,input_path,output_path)

        self.__provided_data = ['/data/snp_<7 digit index>/ff',
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

        self.__expected_data = ['/data/arrEhor',
                                '/data/arrEver',
                                '/params/Mesh/nSlices',
                                '/params/Mesh/nx',
                                '/params/Mesh/ny',
                                '/params/Mesh/qxMax',
                                '/params/Mesh/qxMin',
                                '/params/Mesh/qyMax',
                                '/params/Mesh/qyMin',
                                '/params/Mesh/sliceMax',
                                '/params/Mesh/sliceMin',
                                '/params/Mesh/xMax',
                                '/params/xMin',
                                '/params/yMax',
                                '/params/yMin',
                                '/params/zCoord',
                                '/params/beamline/printout',
                                '/params/Rx',
                                '/params/Ry',
                                '/params/dRx',
                                '/params/dRy',
                                '/params/nval',
                                '/params/photonEnergy',
                                '/params/wDomain',
                                '/params/wEFieldUnit',
                                '/params/wFloatType',
                                '/params/wSpace',
                                '/params/xCentre',
                                '/params/yCentre',
                                '/info/package_version',
                                '/info/contact',
                                '/info/data_description',
                                '/info/method_description',
                                '/misc/xFWHM',
                                '/misc/yFWHM',
                                '/version',
                                ]


    def expectedData(self):
        """ Query for the data expected by the Interactor. """
        return self.__expected_data

    def providedData(self):
        """ Query for the data provided by the Interactor. """
        return self.__provided_data

    def backengine(self):
        """ This method drives the backengine code."""
        cached_out = generateTestFilePath('pmi_out_0000001.h5')
        command_string = 'cp %s %s' % (cached_out, '.')
        proc = subprocess.Popen(command_string, shell=True)
        proc.wait()


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

        #super(FakePhotonMatterInteractor, self).__init__(parameters,self.input_path,self.output_path)

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
