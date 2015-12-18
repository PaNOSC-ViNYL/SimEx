""" Module that holds the XFELPhotonSource class.

    @author : CFG
    @institution : XFEL
    @creation 20151104

"""
import os
import shutil
from subprocess import Popen
import numpy
import h5py

from SimEx.Calculators.AbstractPhotonSource import AbstractPhotonSource


class XFELPhotonSource(AbstractPhotonSource):
    """
    Class representing a x-ray free electron laser photon source.
    """

    def __init__(self,  parameters=None, input_path=None, output_path=None):
        """
        Constructor for the xfel photon source.

        @param parameters : Photon source parameters.
        @type : dict

        @param input_path : The path to the input data for the photon source.
        @type : string

        @param output_path : The path where to save output data.
        @type : string
        """

        # Initialize base class.
        super(XFELPhotonSource, self).__init__(parameters,input_path,output_path)


    def backengine(self):
        # Copy input to output.
        # Check if input_path is a directory.
        if os.path.isdir(self.input_path):
            # Make directory target if not existing already.
            if not os.path.isdir(self.output_path):
                os.mkdir( self.output_path )
            # Copy files.
            files_to_copy = [os.path.join(self.input_path, ff) for ff in os.listdir(self.input_path) if 'FELsource_out' in ff and ff.split('.')[-1] == 'h5']
            for f in files_to_copy:
                shutil.copy( f, self.output_path )

        # If input is a single file, just copy it to output.
        else:
            shutil.copy( self.input_path, self.output_path )

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
        Private method to save the object to a file.

        @param output_path : The file where to save the object's data.
        @type : string
        @default : None
        """

        pass




