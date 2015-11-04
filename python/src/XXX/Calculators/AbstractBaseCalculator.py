""" Module for AbstractBaseCalculator

    @author : CFG
    @institution : XFEL
    @creation 20151007

"""
import exceptions
import os
from abc import ABCMeta, abstractmethod

from XXX.Utilities.EntityChecks import checkAndSetInstance


class AbstractBaseCalculator(object):
    """
    Abstract class for all simulation calculators.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, parameters=None, input_path=None, output_path=None):
        """
        Constructor for the Abstract Base Calculator.

        @param control_parameters : Dictionary for the parameters of the calculation (not data).
        @type : dict

        @param input_path: Path to hdf5 file holding the input data.
        @type : string
        @default : None

        @param output_path: Path to hdf5 file for output.
        @type : string
        @default : None
        """

        # Check parameters.
        self.__parameters = checkAndSetInstance(dict, parameters, {})

        self.__input_path, self.__output_path = checkAndSetIO((input_path, output_path))

    @abstractmethod
    def backengine(self):
        """
        Method to call the backengine for the calculator.
        To be implemented on the derived classes.
        """
        pass

    #######################################################################
    # Queries and setters
    #######################################################################
    # control_parameters

    @property
    def parameters(self):
        """ Query for the control parameters of the calculator."""
        return self.__parameters
    @parameters.setter
    def parameters(self, value):
        """ Set the control parameters for the calculation. """
        self.__parameters = checkAndSetInstance(dict, value, None)
    @parameters.deleter
    def parameters(self):
        """ Delete the control parameters.  """
        del self.__parameters

    # input
    @property
    def input_path(self):
        """ Query for the input file path(s). """
        return self.__input_path
    @input_path.setter
    def input_path(self, value):
        """ Set the io path(s) to a value. """
        self.__input_path = checkAndSetInstance( (str, list), value, None   )
    @input_path.deleter
    def input_path(self):
        """ Delete the input_path path(s). """
        del self.__input_path

    # output
    @property
    def output_path(self):
        """ Query for the output file path(s). """
        return self.__output_path
    @output_path.setter
    def output_path(self, value):
        """ Set the io path(s) to a value. """
        self.__output_path = checkAndSetInstance( (str, list), value, None   )
    @output_path.deleter
    def output_path(self):
        """ Delete the output_path path(s). """
        del self.__output_path


def checkAndSetIO(io):
    """ Check the passed io path/filenames and set appropriately. """

    # Check if it is a single file.
    # In that case, io is the path for output only, no input required.
    io = checkAndSetInstance(tuple, io)
    if len(io) != 2:
        raise exceptions.RuntimeError("The parameter 'io' can only be a string or a tuple of two strings.")

    # Check if input exists, if not, raise.
    i = checkAndSetInstance(str, io[0])
    i = os.path.abspath(i)
    if not os.path.isfile(i):
        raise exceptions.RuntimeError('Input file %s could not be found.' % (i))

    # Check if output file exists, otherwise attempt to create it.
    o = checkAndSetInstance(str, io[1])
    o = os.path.abspath(io[1])
    if not os.path.isfile( o ):
        path = os.path.dirname( o )
        if not os.path.isdir( path ):
            os.makedirs( path ) # Raises if permissions not sufficient to create the file.
    return (i, o)


def checkAndSetBaseCalculator(var=None, default=None):
    """
    Check if passed object is an AbstractBaseCalculator instance. If non is given, set to given default.

    @param var : The object to check.
    @param default : The default to use.
    @return : The checked photon source object.
    @throw : RuntimeError if no valid BaseCalculator was given.
    """

    return checkAndSetInstance(AbstractBaseCalculator, var, default)


