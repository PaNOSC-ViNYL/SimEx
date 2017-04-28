""" Module that holds the DMPhasingParameters class.  """
##########################################################################
#                                                                        #
# Copyright (C) 2016-2017 Carsten Fortmann-Grote                         #
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

from scipy.constants import Avogadro
from scipy.constants import physical_constants
import copy
import math
import numpy
import os
import tempfile

from SimEx.Parameters.AbstractCalculatorParameters import AbstractCalculatorParameters
from SimEx.Utilities.EntityChecks import checkAndSetInstance

class DMPhasingParameters(AbstractCalculatorParameters):
    """
    Class representing parameters for the DMPhasing analyzer.
    """

    def __init__(self,
                 number_of_trials        = None,
                 number_of_iterations    = None,
                 averaging_start         = None,
                 leash                   = None,
                 number_of_shrink_cycles = None,
                 parameters_dictionary = None,
                 **kwargs
                ):
        """
        Constructor for the DMPhasingParameters.
        :param number_of_trials: How many trials to run in each iteration.
        :type number_of_trials: int>0, default 500

        :param number_of_iterations: Maximum number of DM iterations.
        :type number_of_iterations: int>0, default 50

        :param averaging_start: Start averaging after this many runs.
        :type averaging: int>0, default 15

        :param leash: DM leash parameter.
        :type leash: float>0, default 0.2

        :param number_of_shrink_cycles: DM shrink cycles.
        :type number_of_shrink_cycles: int>0, default 10
        """

        # Legacy support for dictionaries.
        if parameters_dictionary is not None:
            self.number_of_trials = parameters_dictionary['number_of_trials']
            self.number_of_iterations = parameters_dictionary['number_of_iterations']
            self.averaging_start = parameters_dictionary['averaging_start']
            self.leash = parameters_dictionary['leash']
            self.number_of_shrink_cycles = parameters_dictionary['number_of_shrink_cycles']

        else:
            # Check all parameters.
            self.number_of_trials = number_of_trials
            self.number_of_iterations = number_of_iterations
            self.averaging_start = averaging_start
            self.leash = leash
            self.number_of_shrink_cycles = number_of_shrink_cycles

    def _setDefaults(self):
        """ """
        """ Set the defaults for needed inherited parameters. """
        self._AbstractCalculatorParameters__cpus_per_task_default = "1"

    ### Setters and queries.
    @property
    def number_of_trials(self):
        """ Query for the 'number_of_trials' parameter. """
        return self.__number_of_trials
    @number_of_trials.setter
    def number_of_trials(self, value):
        """ Set the 'number_of_trials' parameter to a given value.
        :param value: The value to set 'number_of_trials' to.
        :type value: int
        """
        number_of_trials = checkAndSetInstance( int, value, 500 )

        if all([number_of_trials > 0]):
            self.__number_of_trials = number_of_trials
        else:
            raise ValueError( "Parameter 'number_of_trials' must be an integer (n > 0)")

    @property
    def number_of_iterations(self):
        """ Query for the 'number_of_iterations' parameter. """
        return self.__number_of_iterations
    @number_of_iterations.setter
    def number_of_iterations(self, value):
        """ Set the 'number_of_iterations' parameter to a given value.
        :param value: The value to set 'number_of_iterations' to.
        :type value: int
        """
        number_of_iterations = checkAndSetInstance( int, value, 50 )

        if all([ number_of_iterations > 0]):
            self.__number_of_iterations = number_of_iterations
        else:
            raise ValueError( "Parameter 'number_of_iterations' must be an integer (n > 0)")

    @property
    def leash(self):
        """ Query for the 'leash' parameter. """
        return self.__leash
    @leash.setter
    def leash(self, value):
        """ Set the 'leash' parameter to a given value.
        :param value: The value to set 'leash' to.
        :type value: float
        """
        leash = checkAndSetInstance( float, value, 0.2 )

        if leash > 0:
            self.__leash = leash
        else:
            raise ValueError( "The parameter 'leash' must be a positive integer.")

    @property
    def averaging_start(self):
        """ Query for the 'averaging_start' parameter. """
        return self.__averaging_start
    @averaging_start.setter
    def averaging_start(self, value):
        """ Set the 'averaging_start' parameter to a given value.
        :param value: The value to set 'averaging_start' to.
        :type value: int
        """
        averaging_start = checkAndSetInstance( int, value, 15 )

        if averaging_start > 0:
            self.__averaging_start = averaging_start
        else:
            raise ValueError( "The parameter 'averaging_start' must be a positive integer.")

    @property
    def number_of_shrink_cycles(self):
        """ Query for the 'number_of_shrink_cycles' parameter. """
        return self.__number_of_shrink_cycles
    @number_of_shrink_cycles.setter
    def number_of_shrink_cycles(self, value):
        """ Set the 'number_of_shrink_cycles' parameter to a given value.
        :param value : The value to set 'number_of_shrink_cycles' to.
        :type value: int
        """
        number_of_shrink_cycles = checkAndSetInstance( int, value, 10 )
        if number_of_shrink_cycles > 0:
            self.__number_of_shrink_cycles = number_of_shrink_cycles
        else:
            raise ValueError( "The parameter 'number_of_shrink_cycles' must be a positive integer.")
