""":module AbstractPhotonInteractor: Hosts the base class for all PhotonInteractors. """
##########################################################################
#                                                                        #
# Copyright (C) 2015-2018 Carsten Fortmann-Grote                         #
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

from SimEx.Calculators.AbstractBaseCalculator import AbstractBaseCalculator
from SimEx.Utilities.EntityChecks import checkAndSetInstance

class AbstractPhotonInteractor(AbstractBaseCalculator, metaclass=ABCMeta):
    """
    :class AbstractPhotonInteractor: Abstract base class for all PhotonInteractors.
    """
    @abstractmethod
    def __init__(self, parameters=None, input_path=None, output_path=None, sample_path=None):
        """

        :param parameters: Parameters of the calculation (not data).
        :type parameters: dict || AbstractCalculatorParameters

        :param input_path: Path to hdf5 file holding the input data.
        :type input_path: str

        :param output_path: Path to hdf5 file for output.
        :type output_path: str

        :param sample_path: Path to file containing the sample atom coordinates (at least atom type and cartesian coordinates).
        :type sample_path: str
        """

        # Check paths.
        input_path = checkAndSetInstance(str, input_path, 'prop')
        output_path = checkAndSetInstance(str, output_path, 'pmi')

        #self.sample_path = sample_path

        super(AbstractPhotonInteractor, self).__init__(parameters, input_path, output_path)


def checkAndSetPhotonInteractor(var=None, default=None):
    """
    Check if passed object is an AbstractPhotonInteractor instance. If non is given, set to given default.

    @param var : The object to check.
    @param default : The default to use.
    @return : The checked photon source object.
    @throw : RuntimeError if no valid PhotonInteractor was given.
    """

    return checkAndSetInstance(AbstractPhotonInteractor, var, default)
