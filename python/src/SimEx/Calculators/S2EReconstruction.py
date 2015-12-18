""" Module that holds the S2EReconstruction class.

    @author : CFG
    @institution : XFEL
    @creation 20151104

"""
import os
from SimEx.Calculators.AbstractPhotonAnalyzer import AbstractPhotonAnalyzer

from EMCOrientation import EMCOrientation
from DMPhasing import DMPhasing


class S2EReconstruction(AbstractPhotonAnalyzer):
    """
    Class representing photon data analysis for electron density reconstruction from 2D diffraction patterns.
    Uses the EMC orientation module and the DM phasing module.
    """

    def __init__(self,  parameters=None, input_path=None, output_path=None):
        ### TODO
        """
        Constructor for the reconstruction analyser.

        @param  parameters : Dictionary of reconstruction parameters.
        @type : dict
        @example : parameters={}
        """

        # Initialize base class.
        super(S2EReconstruction, self).__init__(parameters,input_path,output_path)


        self.__provided_data = ['/data/electronDensity',
                                '/params/info',
                                '/history',
                                '/info',
                                '/misc',
                                '/version',
                                ]

        self.__expected_data = ['/-input_dir'
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

        emc_parameters = None
        dm_parameters = None

        # Construct emc and dm calculators.
        if self.parameters != {}:
            emc_parameters = self.parameters['EMC_Parameters']
            dm_parameters = self.parameters['DM_Parameters']

        if os.path.isdir( self.output_path ):
            intermediate_output_path = os.path.join( self.output_path, 'orient_out.h5' )
        else:
            intermediate_output_path  = 'orient_out.h5'

        self.__emc = EMCOrientation(emc_parameters, self.input_path, intermediate_output_path )
        self.__dm = DMPhasing(dm_parameters, intermediate_output_path, self.output_path)



    def expectedData(self):
        """ Query for the data expected by the Analyzer. """
        return self.__expected_data

    def providedData(self):
        """ Query for the data provided by the Analyzer. """
        return self.__provided_data

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



    def backengine(self):

        emc_status = self.__emc.backengine()
        if  emc_status!= 0:
            return emc_status
        dm_status = self.__dm.backengine()

        return dm_status
