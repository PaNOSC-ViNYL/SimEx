##########################################################################
#                                                                        #
# Copyright (C) 2016 Carsten Fortmann-Grote                              #
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

"""
    @file Module that holds the EMCOrientationParameters class.

    @author : CFG
    @institution : XFEL
    @creation 20160721

"""
import os
import copy
import numpy
import math
import tempfile
from scipy.constants import physical_constants
from scipy.constants import Avogadro

from SimEx.Parameters.AbstractCalculatorParameters import AbstractCalculatorParameters
from SimEx.Utilities.EntityChecks import checkAndSetInstance


class EMCOrientationParameters(AbstractCalculatorParameters):
    """
    Class representing parameters for the EMCOrientation analyzer.
    """

    def __init__(self,
                initial_number_of_quaternions=None,
                max_number_of_quaternions=None,
                max_number_of_iterations=None,
                min_error=None,
                beamstop=None,
                detailed_output=None,
                parameters_dictionary=None,
                ):
        """
        Constructor for the EMCOrientationParameters.
        @param initial_number_of_quaternions : Number of quaternions to start the EMC algorithm.
        @type : int (0<n<10)
        @default : 1

        @param max_number_of_quaternions : Maximum number of quaternions for the EMC algorithm.
        @type : int (initial_number_of_quaternions < n <= 10)
        @default : initial_number_of_quaternions + 1

        @param min_error : Relative convergence criterion (Go to next quaternion is relative error gets below this value.)
        @type : float (>0)
        @default : 1.e-6

        @param max_number_of_iterations : Stop the EMC algorithm after this number of iterations.
        @type : int ( >0 )
        @default : 100

        @param beamstop : Whether to apply a "center + strip" beamstop to the pixel map.
        @type : bool
        @default : True

        @param detailed_output : Whether to write detailed info to log.
        @type : bool
        @default : True

        """
        # Legacy support for dictionaries.
        if parameters_dictionary is not None:
            self.initial_number_of_quaternions = parameters_dictionary['initial_number_of_quaternions']
            self.max_number_of_quaternions = parameters_dictionary['max_number_of_quaternions']
            self.min_error = parameters_dictionary['min_error']
            self.max_number_of_iterations = parameters_dictionary['max_number_of_iterations']
            self.beamstop = parameters_dictionary['beamstop']
            self.detailed_output = parameters_dictionary['detailed_output']

        else:
            # Check all parameters.
            self.initial_number_of_quaternions = initial_number_of_quaternions
            self.max_number_of_quaternions = max_number_of_quaternions
            self.min_error = min_error
            self.max_number_of_iterations = max_number_of_iterations
            self.beamstop = beamstop
            self.detailed_output = detailed_output

    ### Setters and queries.
    @property
    def initial_number_of_quaternions(self):
        """ Query for the 'initial_number_of_quaternions' parameter. """
        return self.__initial_number_of_quaternions
    @initial_number_of_quaternions.setter
    def initial_number_of_quaternions(self, value):
        """ Set the 'initial_number_of_quaternions' parameter to a given value.
        @param value : The value to set 'initial_number_of_quaternions' to.
        """
        initial_number_of_quaternions = checkAndSetInstance( int, value, 1 )

        if all([initial_number_of_quaternions > 0, initial_number_of_quaternions < 10]):
            self.__initial_number_of_quaternions = initial_number_of_quaternions
        else:
            raise ValueError( "Parameter 'initial_number_of_quaternions' must be an integer (0 < n < 10)")

    @property
    def max_number_of_quaternions(self):
        """ Query for the 'max_number_of_quaternions' parameter. """
        return self.__max_number_of_quaternions
    @max_number_of_quaternions.setter
    def max_number_of_quaternions(self, value):
        """ Set the 'max_number_of_quaternions' parameter to a given value.
        @param value : The value to set 'max_number_of_quaternions' to.
        """
        max_number_of_quaternions = checkAndSetInstance( int, value, self.__initial_number_of_quaternions+1 )

        if all([ max_number_of_quaternions <= 10, max_number_of_quaternions > self.initial_number_of_quaternions]):
            self.__max_number_of_quaternions = max_number_of_quaternions
        else:
            raise ValueError( "Parameter 'max_number_of_quaternions' must be an integer (initial_number_of_quaternions < n <= 10)")

    @property
    def max_number_of_iterations(self):
        """ Query for the 'max_number_of_iterations' parameter. """
        return self.__max_number_of_iterations
    @max_number_of_iterations.setter
    def max_number_of_iterations(self, value):
        """ Set the 'max_number_of_iterations' parameter to a given value.
        @param value : The value to set 'max_number_of_iterations' to.
        """
        max_number_of_iterations = checkAndSetInstance( int, value, 100 )

        if max_number_of_iterations > 0:
            self.__max_number_of_iterations = max_number_of_iterations
        else:
            raise ValueError( "The parameter 'max_number_of_iterations' must be a positive integer.")

    @property
    def min_error(self):
        """ Query for the 'min_error' parameter. """
        return self.__min_error
    @min_error.setter
    def min_error(self, value):
        """ Set the 'min_error' parameter to a given value.
        @param value : The value to set 'min_error' to.
        """
        min_error = checkAndSetInstance( float, value, 1.e-5 )

        if min_error > 0:
            self.__min_error = min_error
        else:
            raise ValueError( "The parameter 'min_error' must be a positive float.")

    @property
    def beamstop(self):
        """ Query for the 'beamstop' parameter. """
        return self.__beamstop
    @beamstop.setter
    def beamstop(self, value):
        """ Set the 'beamstop' parameter to a given value.
        @param value : The value to set 'beamstop' to.
        """
        self.__beamstop = checkAndSetInstance( bool, value, True )

    @property
    def detailed_output(self):
        """ Query for the 'detailed_output' parameter. """
        return self.__detailed_output
    @detailed_output.setter
    def detailed_output(self, value):
        """ Set the 'detailed_output' parameter to a given value.
        @param value : The value to set 'detailed_output' to.
        """
        self.__detailed_output = checkAndSetInstance( bool, value, True )

