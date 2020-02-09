""" Test module for the GaussianPhotonSource. """

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

import unittest

# Import the class to test.
from SimEx.Calculators.GaussianPhotonSource import GaussianPhotonSource
from SimEx.Parameters.PhotonBeamParameters import PhotonBeamParameters
from SimEx.Utilities.Units import meter, joule, radian, electronvolt
from TestUtilities import TestUtilities

class GaussianPhotonSourceTest(unittest.TestCase):
    """
    Test class for the GaussianPhotonSource class.
    """

    @classmethod
    def setUpClass(cls):
        """ Setting up the test class. """

        cls.beam_parameters = PhotonBeamParameters(
            photon_energy = 8.0e3*electronvolt,
            beam_diameter_fwhm = 0.3e-6*meter,
            pulse_energy = 2.4e-6*joule,
            photon_energy_relative_bandwidth=0.1,
            divergence=2.0e-6*radian,
            photon_energy_spectrum_type=None,
            )

    @classmethod
    def tearDownClass(cls):
        """ Tearing down the test class. """

    def setUp(self):
        """ Setting up a test. """

    def tearDown(self):
        """ Tearing down a test. """

    def testConstruction(self):
        """ Testing the default construction of the class. """

        # Construct the object.
        source = GaussianPhotonSource(parameters=None, input_path="", output_path='GaussianSource.h5')

        self.assertIsInstance(source, GaussianPhotonSource)

if __name__ == '__main__':
    unittest.main()

