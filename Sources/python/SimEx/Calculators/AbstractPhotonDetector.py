##########################################################################
#                                                                        #
# Copyright (C) 2015 Carsten Fortmann-Grote                              #
# Contact: Carsten Fortmann-Grote <carsten.grote@xfel.eu>                #
#                                                                        #
# This file is part of simex_platform.                                   #
# simex_platform is free software: you can redistribute it and/or modify #
# it under the terms of the GNU General Public License as published by   #
# the Free Software Foundation, either version 3 of the License, or      #
# (at your option) any later version.                                    #
#                                                                        #
# simex_platform is distributed in the hope that it will be useful,      #
# but WITHOUT ANY WARRANTY; without even the implied warranty of         #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          #
# GNU General Public License for more details.                           #
#                                                                        #
# You should have received a copy of the GNU General Public License      #
# along with this program.  If not, see <http://www.gnu.org/licenses/>.  #
#                                                                        #
##########################################################################

""" Module for AbstractPhotonDetector

    @author : CFG
    @institution : XFEL
    @creation 20151007

"""

from abc import ABCMeta
from abc import abstractmethod

from SimEx.Calculators.AbstractBaseCalculator import AbstractBaseCalculator
from SimEx.Utilities.EntityChecks import checkAndSetInstance


class AbstractPhotonDetector(AbstractBaseCalculator):
    """
    Class representing an abstract photon source, serving as API for actual photon source simulation calculators.
    """

    __metaclass__  = ABCMeta
    @abstractmethod
    def __init__(self, parameters=None, input_path=None, output_path=None):
        """
        Constructor for the Abstract Photon Detector.
        """
        # Check input path. Set to default if none given.
        input_path = checkAndSetInstance(str, input_path, 'diffr')
        # Check output path. Set default if none given.
        output_path = checkAndSetInstance(str, output_path, 'detector')


        # Initialize the base class.
        super(AbstractPhotonDetector, self).__init__(parameters, input_path, output_path)

def checkAndSetPhotonDetector(var=None, default=None):
    """
    Check if passed object is an AbstractPhotonDetector instance. If non is given, set to given default.

    @param var : The object to check.
    @param default : The default to use.
    @return : The checked photon source object.
    @throw : RuntimeError if no valid PhotonDetector was given.
    """

    return checkAndSetInstance(AbstractPhotonDetector, var, default)

