""" :module PhotonBeamParameters: Module holding the PhotonBeamParameters class. """
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

from SimEx.Parameters.AbstractCalculatorParameters import AbstractCalculatorParameters
from SimEx.Utilities.EntityChecks import checkAndSetInstance

class PhotonBeamParameters(AbstractCalculatorParameters):
    """ Class representing photon beam parameters. """

    def __init__(self,
            photon_energy,
            beam_diameter_fwhm,
            pulse_energy,
            photon_energy_relative_bandwidth=None,
            divergence=None,
            **kwargs
            ):
        """
        Constructor of the PhotonBeamParameters class.

        :param photon_energy: The mean photon energy in units of electonvolts (eV).
        :type photon_energy: float

        :param photon_energy_relative_bandwidth: The relative energy bandwidth
        :type photon_energy_relative_bandwidth: float (>0.0).

        :param beam_diameter_fwhm: Beam diameter in units of metre (m).
        :type beam_diameter_fwhm: float

        :param pulse_energy: Total energy of the pulse in units of Joule (J).
        :type pulse_energy: float

        :param divergence: Beam divergence angle in units of radian (rad).
        :type divergence: float (0 < divergence < 2*pi)

        :param kwargs: Key-value pairs to be passed to the parent class constructor.
        :type kwargs: dict

        """

        super(PhotonBeamParameters, self).__init__(**kwargs)

        self.photon_energy = photon_energy
        self.photon_energy_relative_bandwidth = photon_energy_relative_bandwidth
        self.beam_diameter_fwhm = beam_diameter_fwhm
        self.pulse_energy = pulse_energy
        self.divergence = divergence

    def _setDefaults(self):
        """ Set default for required inherited parameters. """
        self._AbstractCalculatorParameters__cpus_per_task_default = 1


    @property
    def photon_energy(self):
        """ Query the 'photon_energy' parameter. """
        return self.__photon_energy
    @photon_energy.setter
    def photon_energy(self, val):
        """ Set the 'photon_energy' parameter to val."""
        self.__photon_energy = checkAndSetInstance( float, val, None)

    @property
    def photon_energy_relative_bandwidth(self):
        """ Query the 'photon_energy_relative_bandwidth' parameter. """
        return self.__photon_energy_relative_bandwidth
    @photon_energy_relative_bandwidth.setter
    def photon_energy_relative_bandwidth(self, val):
        """ Set the 'photon_energy_relative_bandwidth' parameter to val."""
        self.__photon_energy_relative_bandwidth = checkAndSetInstance( float, val, 0.01)

    @property
    def beam_diameter_fwhm(self):
        """ Query the 'beam_diameter_fwhm' parameter. """
        return self.__beam_diameter_fwhm
    @beam_diameter_fwhm.setter
    def beam_diameter_fwhm(self, val):
        """ Set the 'beam_diameter_fwhm' parameter to val."""
        self.__beam_diameter_fwhm = checkAndSetInstance( float, val, None)

    @property
    def divergence(self):
        """ Query the 'divergence' parameter. """
        return self.__divergence
    @divergence.setter
    def divergence(self, val):
        """ Set the 'divergence' parameter to val."""
        self.__divergence = checkAndSetInstance( float, val, 0.0)

    @property
    def pulse_energy(self):
        """ Query the 'pulse_energy' parameter. """
        return self.__pulse_energy
    @pulse_energy.setter
    def pulse_energy(self, val):
        """ Set the 'pulse_energy' parameter to val."""
        self.__pulse_energy = checkAndSetInstance( float, val, None)



