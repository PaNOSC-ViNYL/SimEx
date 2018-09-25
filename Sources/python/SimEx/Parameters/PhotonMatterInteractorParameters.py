""" :module: Module that holds the PhotonMatterInteractorParameter class.  """
##########################################################################
#                                                                        #
# Copyright (C) 2016-2018 Carsten Fortmann-Grote                         #
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

import os
import numbers

from SimEx.Parameters.AbstractCalculatorParameters import AbstractCalculatorParameters
from SimEx.Parameters.PhotonBeamParameters import PhotonBeamParameters
from SimEx.Utilities.EntityChecks import checkAndSetInstance

class PhotonMatterInteractorParameters(AbstractCalculatorParameters):
    """
    Class representing parameters for the PhotonMatterInteractor calculator.
    """

    def __init__(self,
                rotation=None,
                calculate_Compton=None,
                number_of_trajectories=None,
                beam_parameters=None,
                parameters_dictionary=None,
                **kwargs
                ):
        """
        Constructor for the PhotonMatterInteractorParameters.

        :param rotation: Rotation to apply to the sample atoms' positions (Default: no rotation).
        :type random_rotation: List or tuple of length 4 (Giving the four coordinates of the rotation quaternion).

        :param calculate_Compton: Whether to calculate incoherent (Compton) scattering.
        :type calculate_Compton: bool, default False

        :param number_of_trajectories: Number of trajectories to simulate.
        :type number_of_trajectories: int, default 1

        :param beam_parameters: Parameters of the photon beam.
        :type beam_parameters: PhotonBeamParameters

        :param parameters_dictionary: A legacy parameters dictionary (Default: None).
        :type parameters_dictionary: dict

        """

        # Check all parameters.
        self.rotation                = rotation
        self.calculate_Compton              = calculate_Compton
        self.number_of_trajectories = number_of_trajectories
        self.beam_parameters = beam_parameters

        # Legacy support.
        if parameters_dictionary is not None and all([p is None for p in [rotation, calculate_Compton, number_of_trajectories]]):
            for key,value in parameters_dictionary.items():
                setattr(self, key, value)

        super(PhotonMatterInteractorParameters, self).__init__(**kwargs)

    def _setDefaults(self):
        """ Set default for required inherited parameters. """
        self._AbstractCalculatorParameters__cpus_per_task_default = 1

    @property
    def beam_parameters(self):
        """ Query for the 'beam_parameters' parameter. """
        return self.__beam_parameters
    @beam_parameters.setter
    def beam_parameters(self, value):
        """ Set the 'beam_parameters' parameter to a given value.
        :param value: The value to set 'beam_parameters' to.
        """
        if value is None:
            self.__beam_parameters = None

        if isinstance(value, PhotonBeamParameters):
            self.__beam_parameters = value

    @property
    def rotation(self):
        """ Query for the 'rotation' parameter. """
        return self.__rotation
    @rotation.setter
    def rotation(self, value):
        """ Set the 'rotation' parameter to a given value.
        :param value: The value to set 'rotation' to.
        """
        # Allow None.
        if value is None:
              value = [1, 0, 0, 0]

        # Check all conditions.
        conditions = [hasattr(value, '__iter__'),
                len(value) == 4,
                all([isinstance(q, numbers.Number) for q in value])]

        if not all(conditions):
            raise TypeError("Rotation must be None or a list or tuple of 4 numbers.")

        self.__rotation = value

    @property
    def calculate_Compton(self):
        """ Query for the 'calculate_Compton' parameter. """
        return self.__calculate_Compton
    @calculate_Compton.setter
    def calculate_Compton(self, value):
        """ Set the 'calculate_Compton' parameter to a given value.
        :param value: The value to set 'calculate_Compton' to.
        """
        self.__calculate_Compton = checkAndSetInstance( bool, value, False )

    @property
    def number_of_trajectories(self):
        """ Query for the 'number_of_trajectories_file' parameter. """
        return self.__number_of_trajectories
    @number_of_trajectories.setter
    def number_of_trajectories(self, value):
        """ Set the 'number_of_trajectories' parameter to a given value.
        :param value: The value to set 'number_of_trajectories' to.
        """
        number_of_trajectories = checkAndSetInstance( int, value, 1 )

        if number_of_trajectories > 0:
            self.__number_of_trajectories = number_of_trajectories
        else:
            raise ValueError("The parameters 'number_of_trajectories' must be a positive integer.")
