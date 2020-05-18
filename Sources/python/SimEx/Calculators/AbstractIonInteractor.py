""":module AbstractIonInteractor: Hosts the base class for all IonInteractors. """
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
from SimEx.Parameters.IonMatterInteractorParameters import IonMatterInteractorParameters


class AbstractIonInteractor(AbstractBaseCalculator, metaclass=ABCMeta):
    """
    :class AbstractPhotonInteractor: Abstract base class for all PhotonInteractors.
    """
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

        # Check paths.
        input_path = checkAndSetInstance(str, input_path, None)
        output_path = checkAndSetInstance(str, output_path, None)

        self.__expected_data = ['Grid_Particles_',
                                'Particles_Px_',
                                'Particles_Py_',
                                'Particles_Pz_',
                                'Particles_Weight_'
                                ]

        super(AbstractIonInteractor, self).__init__(parameters, input_path, output_path)

        if isinstance(parameters, dict):
            self.parameters = IonMatterInteractorParameters()
            for k in parameters.keys():
                self.parameters.__setattr__(k,parameters[k])


    @property
    def expectedData(self):
        if self.parameters is not None:
            if isinstance(self.parameters, IonMatterInteractorParameters):
                expected_data = [name + self.parameters.ion_name for name in self.__expected_data]
            else:
                expected_data = [name + self.parameters['ion_name'] for name in self.__expected_data]
        return expected_data

    def providedData(self):
        pass

def checkAndSetIonInteractor(var=None, default=None):
    """
    Check if passed object is an AbstractPhotonInteractor instance. If non is given, set to given default.

    @param var : The object to check.
    @param default : The default to use.
    @return : The checked photon source object.
    @throw : RuntimeError if no valid PhotonInteractor was given.
    """

    return checkAndSetInstance(AbstractIonInteractor, var, default)
