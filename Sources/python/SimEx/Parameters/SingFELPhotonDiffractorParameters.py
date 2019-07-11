""" :module SingFELPhotonDiffractorParameters: Module that holds the SingFELPhotonDiffractorParameters class.  """
##########################################################################
#                                                                        #
# Copyright (C) 2016-2019 Carsten Fortmann-Grote                         #
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

from SimEx.Parameters.AbstractPhotonDiffractorParameters import AbstractPhotonDiffractorParameters
from SimEx.Parameters.DetectorGeometry import DetectorGeometry
from SimEx.Parameters.PhotonBeamParameters import PhotonBeamParameters
from SimEx.Utilities.EntityChecks import checkAndSetInstance

class SingFELPhotonDiffractorParameters(AbstractPhotonDiffractorParameters):
    """
    :class SingFELPhotonDiffractorParameters: Class representing parameters for the SingFELPhotonDiffractor calculator.
    """

    def __init__(self,
                sample=None,
                uniform_rotation=None,
                calculate_Compton=None,
                slice_interval=None,
                number_of_slices=None,
                pmi_start_ID=None,
                pmi_stop_ID=None,
                number_of_diffraction_patterns=None,
                beam_parameters=None,
                detector_geometry=None,
                number_of_MPI_processes=None,
                **kwargs
                ):
        """
        :param calculate_Compton: Whether to calculate incoherent (Compton) scattering.
        :type calculate_Compton: bool, default False

        :param slice_interval: Length of time slice interval to extract from each trajectory.
        :type slice_interval: int, default 100

        :param number_of_slices: Number of time slices to read from each trajectory.
        :type number_of_slices: int, default 1

        :param pmi_start_ID: Identifier for the first pmi trajectory to read in.
        :type pmi_start_ID: int, default 1

        :param pmi_stop_ID: Identifier for the last pmi trajectory to read in.
        :type pmi_stop_ID: int, default 1

        """
        super(SingFELPhotonDiffractorParameters, self).__init__(sample=sample,
                                                                uniform_rotation=uniform_rotation,
                                                                beam_parameters=beam_parameters,
                                                                detector_geometry=detector_geometry,
                                                                number_of_diffraction_patterns=number_of_diffraction_patterns,
                                                                **kwargs,
                                                                )

        # Check all parameters.
        self.calculate_Compton              = calculate_Compton
        self.slice_interval                 = slice_interval
        self.number_of_slices               = number_of_slices
        self.pmi_start_ID                   = pmi_start_ID
        self.pmi_stop_ID                    = pmi_stop_ID


    def _setDefaults(self):
        """ Set default for required inherited parameters. """
        self._AbstractCalculatorParameters__cpus_per_task_default = 1

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
    def number_of_slices(self):
        """ Query for the 'number_of_slices' parameter. """
        return self.__number_of_slices
    @number_of_slices.setter
    def number_of_slices(self, value):
        """ Set the 'number_of_slices' parameter to a given value.
        :param value: The value to set 'number_of_slices' to.
        """
        number_of_slices = checkAndSetInstance( int, value, 1 )

        if number_of_slices > 0:
            self.__number_of_slices = number_of_slices
        else:
            raise ValueError( "The parameter 'number_of_slices' must be a positive integer.")

    @property
    def slice_interval(self):
        """ Query for the 'slice_interval' parameter. """
        return self.__slice_interval

    @slice_interval.setter
    def slice_interval(self, value):
        """ Set the 'slice_interval' parameter to a given value.
        :param value: The value to set 'slice_interval' to.
        """
        slice_interval = checkAndSetInstance( int, value, 100 )

        if slice_interval > 0:
            self.__slice_interval = slice_interval
        else:
            raise ValueError( "The parameter 'slice_interval' must be a positive integer.")

    @property
    def pmi_start_ID(self):
        """ Query for the 'pmi_start_ID' parameter. """
        return self.__pmi_start_ID
    @pmi_start_ID.setter
    def pmi_start_ID(self, value):
        """ Set the 'pmi_start_ID' parameter to a given value.
        :param value: The value to set 'pmi_start_ID' to.
        """
        pmi_start_ID = checkAndSetInstance( int, value, 1 )
        if pmi_start_ID >= 0:
            self.__pmi_start_ID = pmi_start_ID
        else:
            raise ValueError("The parameters 'pmi_start_ID' must be a positive integer.")

    @property
    def pmi_stop_ID(self):
        """ Query for the 'pmi_stop_ID' parameter. """
        return self.__pmi_stop_ID
    @pmi_stop_ID.setter
    def pmi_stop_ID(self, value):
        """ Set the 'pmi_stop_ID' parameter to a given value.
        :param value: The value to set 'pmi_stop_ID' to.
        """
        pmi_stop_ID = checkAndSetInstance( int, value, 1 )
        if pmi_stop_ID >= 0:
            self.__pmi_stop_ID = pmi_stop_ID
        else:
            raise ValueError("The parameters 'pmi_stop_ID' must be a positive integer.")

