""" :module GaussWavefrontParametersTest: Test module for the GaussWavefrontParameters class.  """
##########################################################################
#                                                                        #
# Copyright (C) 2020 Carsten Fortmann-Grote                              #
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
import shutil
import io

# Include needed directories in sys.path.
import unittest

from SimEx.Parameters.GaussWavefrontParameters import GaussWavefrontParameters
from SimEx.Utilities.Units import meter, electronvolt, joule, radian
from TestUtilities import TestUtilities

class GaussWavefrontParametersTest(unittest.TestCase):
    """
    Test class for the GaussWavefrontParameters class.
    """

    @classmethod
    def setUpClass(cls):
        cls.beam = GaussWavefrontParameters(photon_energy=8.6e3*electronvolt,
                                    beam_diameter_fwhm=1.0e-6*meter,
                                    pulse_energy=1.0e-3*joule,
                                    photon_energy_relative_bandwidth=0.001,
                                    divergence=2.0e-6*radian,
                                    photon_energy_spectrum_type="Gauss",
                                    number_of_transverse_grid_points=400,
                                    number_of_time_slices=10,
                                    )
    @classmethod
    def tearDownClass(cls):
        """ Tearing down the test class. """
        pass

    def setUp(self):
        """ Setting up a test. """
        self.__files_to_remove = []
        self.__dirs_to_remove = []

    def tearDown(self):
        """ Tearing down a test. """
        for f in self.__files_to_remove:
            if os.path.isfile(f):
                os.remove(f)
        for d in self.__dirs_to_remove:
            if os.path.isdir(d):
                shutil.rmtree(d)

    def testDefaultConstruction(self):
        """ Testing the default construction. """

        # Attempt to construct an instance of the class.
        self.assertRaises(TypeError, GaussWavefrontParameters)

    def testShapedConstruction(self):
        """ Testing the construction of the class with parameters. """

        # Attempt to construct an instance of the class.
        parameters = GaussWavefrontParameters(
                photon_energy=4.96e3*electronvolt,
                photon_energy_relative_bandwidth=2e-2,
                photon_energy_spectrum_type="Gauss",
                pulse_energy = 2e-3*joule,
                beam_diameter_fwhm = 2e-6*meter,
                divergence = 1e-6*radian,
                number_of_transverse_grid_points=400,
                number_of_time_slices=10,
                )

        # Check all parameters are set as intended.
        self.assertEqual(parameters.photon_energy, 4.96e3*electronvolt)
        self.assertEqual(parameters.photon_energy_relative_bandwidth, 2e-2)
        self.assertEqual(parameters.photon_energy_spectrum_type, "Gauss")
        self.assertEqual(parameters.pulse_energy, 2e-3*joule)
        self.assertEqual(parameters.beam_diameter_fwhm, 2e-6*meter)
        self.assertEqual(parameters.divergence, 1e-6*radian)
        self.assertEqual(parameters.number_of_transverse_grid_points, 400)
        self.assertEqual(parameters.number_of_time_slices, 10)

    def testSettersAndQueries(self):
        """ Testing the default construction of the class using a dictionary. """
        # Attempt to construct an instance of the class.
        parameters = GaussWavefrontParameters(
                photon_energy=4.96e3*electronvolt,
                pulse_energy = 2e-3*joule,
                beam_diameter_fwhm = 2e-6*meter,
                number_of_transverse_grid_points=400,
                number_of_time_slices=10,
                )

        # Set via methods.
        parameters.photon_energy = 8.0e3*electronvolt
        parameters.pulse_energy = 2.5e-3*joule
        parameters.beam_diameter_fwhm = 100e-9*meter
        parameters.photon_energy_relative_bandwidth = 1e-3
        parameters.divergence = 5e-6*radian
        parameters.photon_energy_spectrum_type="Gauss"
        parameters.number_of_transverse_grid_points = 400
        parameters.number_of_time_slices = 10

        # Check all parameters are set as intended.
        self.assertEqual(parameters.photon_energy, 8.0e3*electronvolt)
        self.assertEqual(parameters.photon_energy_relative_bandwidth, 1e-3)
        self.assertEqual(parameters.pulse_energy.magnitude, 2.5e-3)
        self.assertEqual(parameters.beam_diameter_fwhm.magnitude, 1e-7)
        self.assertEqual(parameters.divergence.magnitude, 5e-6)
        self.assertEqual(parameters.photon_energy_spectrum_type, "Gauss")
        self.assertEqual(parameters.number_of_transverse_grid_points, 400)
        self.assertEqual(parameters.number_of_time_slices, 10)

if __name__ == '__main__':
    unittest.main()

