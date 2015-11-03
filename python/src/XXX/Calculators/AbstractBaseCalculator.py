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
    def __init__(self, control_parameters=None, io=None):
        """
        Constructor for the Abstract Base Calculator.

        @param control_parameters: Dictionary for the parameters of the calculation (not data).
        @type : dict

        @param io: Paths to input an output data
        @type : string or tuple [ipath, opath]
        @example : io='/home/user/sim/data/' (use path as directory where all io is read/written, unique filenames will be constructed for both input and output.
        @example : io=['/home/user/sim/data/sim1.in.h5', '/home/user/sim/data/sim1.out.h5'] (use these files for input and output respectively.)
        @example : io='/home/user/sim/data/sim1.h5' : File is used for input and later overwritten for output.
        """

        # Check parameters.
        #self.__control_parameters = checkAndSetInstance(dict, control_parameters, None)

        #self.__io = checkAndSetIO(io)

    def backengine(self):
        """
        Method to call the backengine for the calculator.
        To be implemented on the derived classes.
        """
        raise exceptions.RuntimeError("This method has to be implemented on the derived class.")

    #######################################################################
    # Queries and setters
    #######################################################################
    # control_parameters

    @property
    def control_parameters(self):
        """ Query for the control parameters of the calculator."""
        return self.__control_parameters
    @control_parameters.setter
    def control_parameters(self, value):
        """ Set the control parameters for the calculation. """
        self.__control_parameters = checkAndSetInstance(dict, value, None)
    @control_parameters.deleter
    def control_parameters(self):
        """ Delete the control parameters.  """
        del self.__control_parameters

    # io
    @property
    def io(self):
        """ Query for the io file path(s). """
        return self.__io
    @io.setter
    def io(self, value):
        """ Set the io path(s) to a value. """
        self.__io = checkAndSetInstance( (str, list), value, None   )
    @io.deleter
    def io(self):
        """ Delete the io path(s). """
        del self.__io

def checkAndSetIO(io):
    """ Check the passed io path/filenames and set appropriately. """

    # Check if it is a single file.
    # In that case, io is the path for output only, no input required.
    if isinstance(io, str):
        i = None
        o = io
    else:
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


