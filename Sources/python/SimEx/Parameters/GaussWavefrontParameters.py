""" :module GaussWavefrontParameters: Contains the GaussWavefrontParameters class and associated functions."""
##########################################################################
#                                                                        #
# Copyright (C) 2015-2020 Carsten Fortmann-Grote                         #
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

from SimEx.Parameters.AbstractCalculatorParameters import AbstractCalculatorParameters
from SimEx.Utilities.EntityChecks import checkAndSetInstance, checkAndSetPhysicalQuantity
from SimEx.Utilities.Units import meter, electronvolt, joule, radian

from scipy import constants
from wpg import Wavefront, wpg_uti_wf
from wpg.srwlib import srwl
import math
import numpy
import os
import sys

class GaussWavefrontParameters(AbstractCalculatorParameters):
    def __init__(self,
            photon_energy,
            beam_diameter_fwhm,
            pulse_energy,
            photon_energy_relative_bandwidth,
            divergence,
            number_of_transverse_grid_points,
            number_of_time_slices,
            **kwargs
            ):
        """
        :class GaussWavefrontParameters: Encapsulates the parameters of a photon beam.

        :param photon_energy: The mean photon energy in units of electronvolts (eV).
        :type photon_energy: PhysicalQuantity

        :param photon_energy_relative_bandwidth: The relative energy bandwidth
        :type photon_energy_relative_bandwidth: float (>0.0).

        :param beam_diameter_fwhm: Beam diameter in units of metre (m).
        :type beam_diameter_fwhm: PhysicalQuantity

        :param pulse_energy: Total energy of the pulse in units of Joule (J).
        :type pulse_energy: PhysicalQuantity

        :param divergence: Beam divergence angle in units of radian (rad).
        :type divergence: PhysicalQuantity

        :param number_of_transverse_grid_points: The number of grid points in both horizontal (x) and
                                                 vertical (y) dimension transverse to the beam direction.t
        :type  number_of_transverse_grid_points: int

        :param number_of_time_slices: The number of time slices.
        :type number_of_time_slices: int

        :param kwargs: Key-value pairs to be passed to the parent class constructor.
        :type kwargs: dict

        """

        super(GaussWavefrontParameters, self).__init__(**kwargs)

        self.number_of_transverse_grid_points = number_of_transverse_grid_points
        self.number_of_time_slices = number_of_time_slices

    def _setDefaults(self):
        """ Set default for required inherited parameters. """
        self._AbstractCalculatorParameters__cpus_per_task_default = 1

    @property
    def photon_energy_spectrum_type(self):
        """ Query the 'photon_energy_spectrum_type' parameter. """
        return self.__photon_energy_spectrum_type
    @photon_energy_spectrum_type.setter
    def photon_energy_spectrum_type(self, val):
        """ Set the 'photon_energy_spectrum_type' parameter to val."""
        raise AttributeError("The photon_energy_spectrum_type is read-only.")

    @property
    def number_of_transverse_grid_points(self):
        """ The number of grid points in both x and y dimension (transverse to
            the beam direction)."""
        return self.__number_of_transverse_grid_points
    @number_of_transverse_grid_points.setter
    def number_of_transverse_grid_points(self, val):
        if not isinstance(val, int):
            raise TypeError('The parameter "number_of_transverse_grid_points" must\
                             be of a positive int, received {}'.format(type(val)))
        if val <= 0:
            raise ValueError('The parameter "number_of_transverse_grid_points" must\
                             be a positive int.')

    @property
    def number_of_time_slices(self):
        """ The number of time slices. """
        return self.__number_of_time_slices
    @number_of_time_slices.setter
    def number_of_time_slices(self, val):
        if not isinstance(val, int):
            raise TypeError('The parameter "number_of_time_slices" must\
                             be of a positive int, received {}'.format(type(val)))
        if val < 3:
            raise ValueError('The parameter "number_of_time_slices" must\
                             be at least 3.')


