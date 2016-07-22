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
    @file Module that holds the SingFELPhotonDiffractorParameters class.

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


class SingFELPhotonDiffractorParameters(AbstractCalculatorParameters):
    """
    Class representing parameters for the singFELPhotonDiffractor calculator.
    """

    def __init__(self,
                uniform_rotation=None,
                calculate_Compton=None,
                slice_interval=None,
                number_of_slices=None,
                pmi_start_ID=None,
                pmi_stop_ID =None,
                number_of_diffraction_patterns=None,
                beam_parameter_file=None,
                beam_geometry_file=None,
                parameters_dictionary=None,
                ):
        """
        Constructor for the SingFELPhotonDiffractorParameters.
        @param uniform_rotation : Whether to perform uniform sampling of rotation space.
        @type : bool
        @defaul  : True

        @param calculate_Compton : Whether to calculate incoherent (Compton) scattering.
        @type : bool
        @defaul : False

        @param slice_interval : Length of time slice interval to extract from each trajectory.
        @type : int
        @default : 100

        @param number_of_slices : Number of time slices to read from each trajectory.
        @type : int
        @default : 1

        @param pmi_start_ID : Identifier for the first pmi trajectory to read in.
        @type : int
        @default : 1

        @param pmi_stop_ID : Identifier for the last pmi trajectory to read in.
        @type : int
        @default : 1

        @param number_of_diffraction_patterns : Number of diffraction patterns to calculate from each trajectory.
        @type : int
        @default : 1

        @param beam_parameter_file : Path of the beam parameter file.
        @type : str
        @default : 'beam.par'

        @param beam_geometry_file : Path of the beam geometry file.
        @type : str
        @default : 'beam.geo'
        """
        # Legacy support for dictionaries.
        if parameters_dictionary is not None:
            self.uniform_rotation = parameters_dictionary['uniform_rotation']
            self.calculate_Compton = parameters_dictionary['calculate_Compton']
            self.slice_interval = parameters_dictionary['slice_interval']
            self.number_of_slices = parameters_dictionary['number_of_slices']
            self.pmi_start_ID = parameters_dictionary['pmi_start_ID']
            self.pmi_stop_ID = parameters_dictionary['pmi_stop_ID']
            self.beam_parameter_file = parameters_dictionary['beam_parameter_file']
            self.beam_geometry_file = parameters_dictionary['beam_geometry_file']
            self.number_of_diffraction_patterns = parameters_dictionary['number_of_diffraction_patterns']

        else:
            # Check all parameters.
            self.uniform_rotation = uniform_rotation
            self.calculate_Compton = calculate_Compton
            self.slice_interval = slice_interval
            self.number_of_slices = number_of_slices
            self.pmi_start_ID = pmi_start_ID
            self.pmi_stop_ID = pmi_stop_ID
            self.beam_parameter_file = beam_parameter_file
            self.beam_geometry_file = beam_geometry_file
            self.number_of_diffraction_patterns = number_of_diffraction_patterns

    ### Setters and queries.
    @property
    def uniform_rotation(self):
        """ Query for the 'uniform_rotation' parameter. """
        return self.__uniform_rotation
    @uniform_rotation.setter
    def uniform_rotation(self, value):
        """ Set the 'uniform_rotation' parameter to a given value.
        @param value : The value to set 'uniform_rotation' to.
        """
        self.__uniform_rotation = checkAndSetInstance( bool, value, True )

    @property
    def calculate_Compton(self):
        """ Query for the 'calculate_Compton' parameter. """
        return self.__calculate_Compton
    @calculate_Compton.setter
    def calculate_Compton(self, value):
        """ Set the 'calculate_Compton' parameter to a given value.
        @param value : The value to set 'calculate_Compton' to.
        """
        self.__calculate_Compton = checkAndSetInstance( bool, value, False )

    @property
    def number_of_slices(self):
        """ Query for the 'number_of_slices' parameter. """
        return self.__number_of_slices
    @number_of_slices.setter
    def number_of_slices(self, value):
        """ Set the 'number_of_slices' parameter to a given value.
        @param value : The value to set 'number_of_slices' to.
        """
        number_of_slices = checkAndSetInstance( int, value, 1 )

        if number_of_slices > 0:
            self.__number_of_slices = number_of_slices
        else:
            raise ValueError( "The parameter 'slice_interval' must be a positive integer.")

    @property
    def slice_interval(self):
        """ Query for the 'slice_interval' parameter. """
        return self.__slice_interval
    @slice_interval.setter
    def slice_interval(self, value):
        """ Set the 'slice_interval' parameter to a given value.
        @param value : The value to set 'slice_interval' to.
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
        @param value : The value to set 'pmi_start_ID' to.
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
        @param value : The value to set 'pmi_stop_ID' to.
        """
        pmi_stop_ID = checkAndSetInstance( int, value, 1 )
        if pmi_stop_ID >= 0:
            self.__pmi_stop_ID = pmi_stop_ID
        else:
            raise ValueError("The parameters 'pmi_stop_ID' must be a positive integer.")

    @property
    def beam_parameter_file(self):
        """ Query for the 'beam_parameter_file' parameter. """
        return self.__beam_parameter_file
    @beam_parameter_file.setter
    def beam_parameter_file(self, value):
        """ Set the 'beam_parameter_file' parameter to a given value.
        @param value : The value to set 'beam_parameter_file' to.
        """
        beam_parameter_file = checkAndSetInstance( str, value, 'beam.par' )

        if os.path.isfile( beam_parameter_file):
            self.__beam_parameter_file = beam_parameter_file
        else:
            raise IOError("The beam_parameter_file (%s) is not a valid file or filename." % (beam_parameter_file) )

    @property
    def beam_geometry_file(self):
        """ Query for the 'beam_geometry_file' parameter. """
        return self.__beam_geometry_file
    @beam_geometry_file.setter
    def beam_geometry_file(self, value):
        """ Set the 'beam_geometry_file' parameter to a given value.
        @param value : The value to set 'beam_geometry_file' to.
        """
        beam_geometry_file = checkAndSetInstance( str, value, 'beam.geo' )

        if os.path.isfile( beam_geometry_file):
            self.__beam_geometry_file = beam_geometry_file
        else:
            raise IOError("The beam_parameter_file (%s) is not a valid file or filename." % (beam_geometry_file) )

    @property
    def number_of_diffraction_patterns(self):
        """ Query for the 'number_of_diffraction_patterns_file' parameter. """
        return self.__number_of_diffraction_patterns
    @number_of_diffraction_patterns.setter
    def number_of_diffraction_patterns(self, value):
        """ Set the 'number_of_diffraction_patterns' parameter to a given value.
        @param value : The value to set 'number_of_diffraction_patterns' to.
        """
        number_of_diffraction_patterns = checkAndSetInstance( int, value, 1 )

        if number_of_diffraction_patterns > 0:
            self.__number_of_diffraction_patterns = number_of_diffraction_patterns
        else:
            raise ValueError("The parameters 'number_of_diffraction_patterns' must be a positive integer.")


