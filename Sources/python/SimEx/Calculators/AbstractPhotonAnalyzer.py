""" Module for AbstractPhotonAnalyzer """
##########################################################################
#                                                                        #
# Copyright (C) 2015-2017 Carsten Fortmann-Grote                         #
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

from abc import ABCMeta
from abc import abstractmethod
import os

from SimEx.Calculators.AbstractBaseCalculator import AbstractBaseCalculator
from SimEx.Utilities.EntityChecks import checkAndSetInstance

class AbstractPhotonAnalyzer(AbstractBaseCalculator):
    """
    Class representing an abstract photon analyzer, serving as API for actual photon analysis calculators.
    """

    __metaclass__  = ABCMeta
    @abstractmethod
    def __init__(self, parameters=None, input_path=None, output_path=None):
        """

        :param parameters: Parameters of the calculation (not data).
        :type parameters: dict || AbstractCalculatorParameters

        :param input_path: Path to hdf5 file holding the input data.
        :type input_path: str

        :param output_path: Path to hdf5 file for output.
        :type output_path: str
        """

        # Check input path. Set to default if none given.
        input_path = checkAndSetInstance(str, input_path, 'detector')
        # Check output path. Set default if none given.
        o_path = checkAndSetInstance(str, output_path, 'analysis')

        if output_path is None:
            os.makedirs( os.path.abspath( o_path) )
        output_path = o_path

        # Initialize the base class.
        super(AbstractPhotonAnalyzer, self).__init__(parameters, input_path, output_path)

def checkAndSetPhotonAnalyzer(var=None, default=None):
    """
    Check if passed object is an AbstractPhotonAnalyzer instance. If non is given, set to given default.

    :param var: The object to check.
    :param default: The default to use.
    :return: The checked photon source object.
    :raises RuntimeError: if no valid PhotonAnalyzer was given.
    """

    return checkAndSetInstance(AbstractPhotonAnalyzer, var, default)
