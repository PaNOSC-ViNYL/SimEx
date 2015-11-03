""" Module for AbstractPhotonDetector

    @author : CFG
    @institution : XFEL
    @creation 20151007

"""

from abc import ABCMeta
from abc import abstractmethod

from XXX.Calculators.AbstractBaseCalculator import AbstractBaseCalculator
from XXX.Utilities.EntityChecks import checkAndSetInstance


class AbstractPhotonDetector(AbstractBaseCalculator):
    """
    Class representing an abstract photon source, serving as API for actual photon source simulation calculators.
    """

    __metaclass__  = ABCMeta

    @abstractmethod
    def __init__(self, **kwargs):
        """
        Constructor for the Abstract Photon Detector.

        @param **kwargs : Keyword arguments needed for setting up a photon source simulation.
        @type : keyword arguments variable1=value1, variable2=value2, ...
        """

        pass

def checkAndSetPhotonDetector(var=None, default=None):
    """
    Check if passed object is an AbstractPhotonDetector instance. If non is given, set to given default.

    @param var : The object to check.
    @param default : The default to use.
    @return : The checked photon source object.
    @throw : RuntimeError if no valid PhotonDetector was given.
    """

    return checkAndSetInstance(AbstractPhotonDetector, var, default)

