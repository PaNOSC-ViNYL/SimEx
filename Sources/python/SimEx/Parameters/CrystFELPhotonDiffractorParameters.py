""" :module CrystFELPhotonDiffractorParameters: Module that holds the CrystFELPhotonDiffractorParameters class.  """
##########################################################################
#                                                                        #
# Copyright (C) 2016-2020 Carsten Fortmann-Grote                         #
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
from SimEx.Utilities.EntityChecks import checkAndSetInstance, checkAndSetPhysicalQuantity
from SimEx.Utilities import IOUtilities
from SimEx.Utilities.Units import meter
from SimEx.Parameters.PhotonBeamParameters import PhotonBeamParameters
from SimEx.Parameters.DetectorGeometry import DetectorGeometry

class CrystFELPhotonDiffractorParameters(AbstractPhotonDiffractorParameters):
    """
    :class CrystFELPhotonDiffractorParameters: Encapsulates parameters for the CrystFELPhotonDiffractor.
    """
    def __init__(self,
                sample=None,
                uniform_rotation=None,
                number_of_diffraction_patterns=None,
                powder=None,
                intensities_file=None,
                crystal_size_min=None,
                crystal_size_max=None,
                poissonize=None,
                number_of_background_photons=None,
                suppress_fringes=None,
                beam_parameters=None,
                detector_geometry=None,
                **kwargs
                ):
        """
        :param sample: Location of file that contains the sample definition (pdb or crystfel format)
        :type sample: str

        :param uniform_rotation: Whether to perform uniform sampling of rotation space.
        :type uniform_rotation: bool, default True

        :param powder: Whether to sum all patterns to generate a simulated powder diffraction pattern.
        :type powder: bool

        :param intensities_file: Location of file that contains intensities and phases at reciprocal lattice points. See CrystFEL documentation for more info. Default: Constant intensities and phases across entire sample.
        :type intensities_file: str

        :param crystal_size_min: Minimum crystal size.
        :type crystal_size_min: PhysicalQuantity with unit of length (meter).

        :param crystal_size_max: Maximum crystal size.
        :type crystal_size_max: PhysicalQuantity with unit of length (meter).

        :param poissonize: Whether to add Poisson noise to pixel values.
        :type poissonize: bool

        :param number_of_background_photons: Add this number of Poisson distributed photons uniformly over the detector surface (default 0).
        :type number_of_background_photons: int

        :param number_of_diffraction_patterns: Number of diffraction patterns to calculate from each trajectory.
        :type number_of_diffraction_patterns: int, default 1

        :param suppress_fringes: Whether to suppress subsidiary maxima beyond first minimum of the shape transform (default False).
        :type suppress_fringes: bool

        :param beam_parameters: Path of the beam parameter file.
        :type beam_parameters: str

        :param detector_geometry: Path of the beam geometry file.
        :type detector_geometry: str

        :param kwargs: Key-value pairs to pass to the parent class.
        """

        # Check all parameters.
        self.powder = powder
        self.intensities_file = intensities_file
        self.crystal_size_min = crystal_size_min
        self.crystal_size_max = crystal_size_max
        self.poissonize = poissonize
        self.number_of_background_photons = number_of_background_photons
        self.suppress_fringes = suppress_fringes

        # Handle single size case:
        if self.crystal_size_min is None or self.crystal_size_max is None:
            if self.crystal_size_min is None:
                self.crystal_size_min = self.crystal_size_max
            else:
                self.crystal_size_max = self.crystal_size_min

        super(CrystFELPhotonDiffractorParameters, self).__init__(sample=sample,
                                                                 uniform_rotation=uniform_rotation,
                                                                 number_of_diffraction_patterns=number_of_diffraction_patterns,
                                                                 beam_parameters=beam_parameters,
                                                                 detector_geometry=detector_geometry,
                                                                 **kwargs)

    def _setDefaults(self):
        """ Set default for required inherited parameters. """
        self._AbstractCalculatorParameters__cpus_per_task_default = "MAX"

    @property
    def powder(self):
        """ Query the 'powder' parameter. """
        return self.__powder
    @powder.setter
    def powder(self, val):
        """ Set the 'powder' parameter to val."""
        self.__powder = checkAndSetInstance( bool, val, False)

    @property
    def intensities_file(self):
        """ Query the 'intensities_file' parameter. """
        return self.__intensities_file
    @intensities_file.setter
    def intensities_file(self, val):
        """ Set the 'intensities_file' parameter to val."""
        self.__intensities_file = checkAndSetInstance( str, val, None)

    @property
    def crystal_size_min(self):
        """ Query the 'crystal_size_min' parameter. """
        return self.__crystal_size_min
    @crystal_size_min.setter
    def crystal_size_min(self, val):
        """ Set the 'crystal_size_min' parameter to val."""
        # Check if iterable.
        self.__crystal_size_min = checkAndSetPhysicalQuantity(val, None, meter )

    @property
    def crystal_size_max(self):
        """ Query the 'crystal_size_max' parameter. """
        return self.__crystal_size_max
    @crystal_size_max.setter
    def crystal_size_max(self, val):
        """ Set the 'crystal_size_max' parameter to val."""
        # Check if iterable.
        self.__crystal_size_max = checkAndSetPhysicalQuantity(val, None, meter )

    @property
    def poissonize(self):
        """ Query the 'poissonize' parameter. """
        return self.__poissonize
    @poissonize.setter
    def poissonize(self, val):
        """ Set the 'poissonize' parameter to val."""
        self.__poissonize = checkAndSetInstance( bool, val, False)

    @property
    def number_of_background_photons(self):
        """ Query the 'number_of_background_photons' parameter. """
        return self.__number_of_background_photons
    @number_of_background_photons.setter
    def number_of_background_photons(self, val):
        """ Set the 'number_of_background_photons' parameter to val."""
        self.__number_of_background_photons = checkAndSetInstance( int, val, 0)

    @property
    def suppress_fringes(self):
        """ Query the 'suppress_fringes' parameter. """
        return self.__suppress_fringes
    @suppress_fringes.setter
    def suppress_fringes(self, val):
        """ Set the 'suppress_fringes' parameter to val."""
        self.__suppress_fringes = checkAndSetInstance( bool, val, False)
