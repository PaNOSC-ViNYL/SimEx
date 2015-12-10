""" Module that holds the XFELPhotonPropagator class.

    @author : CFG
    @institution : XFEL
    @creation 20151104

"""
from prop import propagateSE

from SimEx.Calculators.AbstractPhotonPropagator import AbstractPhotonPropagator


class XFELPhotonPropagator(AbstractPhotonPropagator):
    """
    Class representing a x-ray free electron laser photon propagator.
    """

    def __init__(self,  parameters=None, input_path=None, output_path=None):
        """
        Constructor for the xfel photon propagator.

        @param  parameters  : Parameters steering the propagation of photons.
        @type               : dict

        @param  input_path  : Location of input data for the photon propagation.
        @type               : string

        @param  output_path : Location of output data for the photon propagation.
        @type               : string
        """

        # Initialize base class.
        super(XFELPhotonPropagator, self).__init__(parameters,input_path,output_path)


    def backengine(self):
        """ This method drives the backengine code, in this case the WPG interface to SRW."""

        propagateSE.propagate(self.input_path, self.output_path)

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
