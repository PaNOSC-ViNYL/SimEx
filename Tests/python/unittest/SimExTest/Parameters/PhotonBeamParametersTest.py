""" :module PhotonBeamParametersTest: Test module for the PhotonBeamParameters class.  """
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

import paths
import os
import numpy
import shutil
import subprocess

# Include needed directories in sys.path.
import paths
import unittest

from TestUtilities import TestUtilities
from SimEx.Parameters.AbstractCalculatorParameters import AbstractCalculatorParameters
from SimEx.Parameters.PhotonBeamParameters import PhotonBeamParameters
from SimEx.Parameters.PhotonBeamParameters import propToBeamParameters

class PhotonBeamParametersTest(unittest.TestCase):
    """
    Test class for the PhotonBeamParameters class.
    """

    @classmethod
    def setUpClass(cls):
        pass

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
        self.assertRaises(TypeError, PhotonBeamParameters)

    def testShapedConstruction(self):
        """ Testing the construction of the class with parameters. """

        # Attempt to construct an instance of the class.
        parameters = PhotonBeamParameters(
                photon_energy=4.96e3,
                photon_energy_relative_bandwidth=2e-2,
                photon_energy_spectrum_type="SASE",
                pulse_energy = 2e-3,
                beam_diameter_fwhm = 2e-6,
                divergence = 1e-6,
                )

        # Check all parameters are set as intended.
        self.assertEqual( parameters.photon_energy, 4.96e3 )
        self.assertEqual( parameters.photon_energy_relative_bandwidth, 2e-2 )
        self.assertEqual( parameters.photon_energy_spectrum_type, "SASE" )
        self.assertEqual( parameters.pulse_energy, 2e-3 )
        self.assertEqual( parameters.beam_diameter_fwhm, 2e-6 )
        self.assertEqual( parameters.divergence, 1e-6 )

    def testSettersAndQueries(self):
        """ Testing the default construction of the class using a dictionary. """
        # Attempt to construct an instance of the class.
        parameters = PhotonBeamParameters(
                photon_energy=4.96e3,
                pulse_energy = 2e-3,
                beam_diameter_fwhm = 2e-6,
                )

        # Set via methods.
        parameters.photon_energy = 8.0e3
        parameters.pulse_energy = 2.5e-3
        parameters.beam_diameter_fwhm = 100e-9
        parameters.photon_energy_relative_bandwidth = 1e-3
        parameters.divergence = 5e-6
        parameters.photon_energy_spectrum_type="tophat"

        # Check all parameters are set as intended.
        self.assertEqual( parameters.photon_energy, 8.0e3 )
        self.assertEqual( parameters.photon_energy_relative_bandwidth, 1e-3 )
        self.assertEqual( parameters.pulse_energy, 2.5e-3 )
        self.assertEqual( parameters.beam_diameter_fwhm, 1e-7 )
        self.assertEqual( parameters.divergence, 5e-6 )
        self.assertEqual( parameters.photon_energy_spectrum_type, "tophat" )

    def testPropToBeamParameters(self):
        """ Test the utility function to construct a PhotonBeamParameters instance from prop output (wavefron file). """

        beam_parameters = propToBeamParameters(TestUtilities.generateTestFilePath("prop_out_0000001.h5"))

        self.assertIsInstance( beam_parameters, PhotonBeamParameters )
        self.assertAlmostEqual( beam_parameters.photon_energy, 4972.840247, 5 )
if __name__ == '__main__':
    unittest.main()

