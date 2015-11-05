""" Module for AbstractPhotonPropagator

    @author : CFG
    @institution : XFEL
    @creation 20151007

"""

from abc import ABCMeta
from abc import abstractmethod

from XXX.Calculators.AbstractBaseCalculator import AbstractBaseCalculator
from XXX.Utilities.EntityChecks import checkAndSetInstance


class AbstractPhotonPropagator(AbstractBaseCalculator):
    """
    Class representing an abstract photon propagator, serving as API for actual photon propagation calculators.
    """

    # Make this class an abstract base class.
    __metaclass__  = ABCMeta
    @abstractmethod
    def __init__(self, parameters=None, input_path=None, output_path=None):
        #"""
        #Constructor for the Abstract Photon Propagator.
        #"""
        super(AbstractPhotonPropagator, self).__init__(parameters, input_path, output_path)

    def expectedData():
        pass
    def providedData():
        pass

def checkAndSetPhotonPropagator(var=None, default=None):
    """
    Check if passed object is an AbstractPhotonPropagator instance. If non is given, set to given default.

    @param var : The object to check.
    @param default : The default to use.
    @return : The checked photon source object.
    @throw : RuntimeError if no valid PhotonPropagator was given.
    """

    return checkAndSetInstance(AbstractPhotonPropagator, var, default)

