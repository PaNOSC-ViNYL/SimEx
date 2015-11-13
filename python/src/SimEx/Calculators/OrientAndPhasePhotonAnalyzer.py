""" Module that holds the OrientAndPhasePhotonAnalyzer class.

    @author : CFG
    @institution : XFEL
    @creation 20151112

"""
from SimEx.Calculators.AbstractPhotonAnalyzer import AbstractPhotonAnalyzer
from TestUtilities.TestUtilities import generateTestFilePath


class OrientAndPhasePhotonAnalyzer(AbstractPhotonAnalyzer):
    """
    Class representing photon data analyzes that combines orientation and phasing of 2D diffraction data.
    """

    def __init__(self,  parameters=None, input_path=None, output_path=None):
        """
        Constructor for the photon analyzer.

        @param  :
        @type :
        @default :
        """

        # Initialize base class.
        super(OrientAndPhasePhotonAnalyzer, self).__init__(parameters,input_path,output_path)

        self.__provided_data = []

        self.__expected_data = []


    def expectedData(self):
        """ Query for the data expected by the Analyzer. """
        return self.__expected_data

    def providedData(self):
        """ Query for the data provided by the Analyzer. """
        return self.__provided_data

    def backengine(self):
        """ This method drives the backengine code."""
        pass

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

        #super(OrientAndPhasePhotonAnalyzer, self).__init__(parameters,self.input_path,self.output_path)

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
