""" Test module for the CrystFELPhotonDiffractorParameter class."""
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

import os
import shutil
import unittest

from SimEx.Parameters.CrystFELPhotonDiffractorParameters import CrystFELPhotonDiffractorParameters
from SimEx.Parameters.AbstractCalculatorParameters import AbstractCalculatorParameters
from SimEx.Parameters.PhotonBeamParameters import PhotonBeamParameters
from SimEx.Utilities.Units import meter, electronvolt, joule, radian
from TestUtilities import TestUtilities

class CrystFELPhotonDiffractorParametersTest(unittest.TestCase):
    """
    Test class for the CrystFELPhotonDiffractorParameters class.
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
        parameters = CrystFELPhotonDiffractorParameters( sample=TestUtilities.generateTestFilePath("2nip.pdb")
                )

        # Check instance and inheritance.
        self.assertIsInstance( parameters, CrystFELPhotonDiffractorParameters )
        self.assertIsInstance( parameters, AbstractCalculatorParameters )

        # Check all parameters are set to default values.
        self.assertEqual( parameters.sample, TestUtilities.generateTestFilePath("2nip.pdb") )
        self.assertTrue( parameters.uniform_rotation )
        self.assertEqual( parameters.beam_parameters, None )
        self.assertEqual( parameters.detector_geometry, None )
        self.assertTrue( parameters.uniform_rotation )
        self.assertEqual( parameters.number_of_diffraction_patterns, 1 )
        self.assertFalse( parameters.powder )
        self.assertEqual( parameters.intensities_file, None )
        self.assertEqual( parameters.crystal_size_min, None )
        self.assertEqual( parameters.crystal_size_max, None )
        self.assertFalse( parameters.poissonize, False )
        self.assertEqual( parameters.number_of_background_photons, 0 )
        self.assertFalse( parameters.suppress_fringes )
        self.assertEqual( parameters.beam_parameters, None )
        self.assertEqual( parameters.detector_geometry, None )

    def testShapedConstruction(self):
        """ Testing the construction with parameters of the class. """

        beam_parameters = PhotonBeamParameters(
                photon_energy=4.96e3*electronvolt,
                photon_energy_relative_bandwidth=0.01,
                beam_diameter_fwhm=2e-6*meter,
                divergence=2e-6*radian,
                pulse_energy=1e-3*joule)

        # Attempt to construct an instance of the class.
        parameters = CrystFELPhotonDiffractorParameters(
                sample=TestUtilities.generateTestFilePath("2nip.pdb"),
                powder=True,
                number_of_diffraction_patterns=10,
                number_of_background_photons=100,
                poissonize=True,
                suppress_fringes=True,
                crystal_size_min=10.0e-9*meter,
                crystal_size_max=100.0e-9*meter,
                uniform_rotation=False,
                beam_parameters=beam_parameters,
                detector_geometry=TestUtilities.generateTestFilePath('simple.geom'))


        # Check all parameters are set as intended.
        self.assertFalse( parameters.uniform_rotation )
        self.assertEqual( parameters.number_of_diffraction_patterns, 10 )
        self.assertTrue( parameters.powder )
        self.assertEqual( parameters.crystal_size_min.m_as(meter), 10.e-9 )
        self.assertEqual( parameters.crystal_size_max.m_as(meter), 100.e-9 )
        self.assertTrue( parameters.poissonize )
        self.assertEqual( parameters.number_of_background_photons, 100 )
        self.assertTrue( parameters.suppress_fringes )
        self.assertIsInstance( parameters.beam_parameters, PhotonBeamParameters )
        self.assertEqual( parameters.beam_parameters.photon_energy.m_as(electronvolt), 4.96e3 )
        self.assertEqual( parameters.detector_geometry, TestUtilities.generateTestFilePath('simple.geom') )

    def testSettersAndQueries(self):
        """ Testing the default construction of the class using a dictionary. """

        self.__files_to_remove.append("5udc.pdb")

        # Construct with defaults.
        parameters = CrystFELPhotonDiffractorParameters(TestUtilities.generateTestFilePath("2nip.pdb"))

        # Set some members to non-defaults.
        parameters.sample="5udc.pdb"
        parameters.powder=True
        parameters.number_of_diffraction_patterns=10
        parameters.number_of_background_photons=100
        parameters.poissonize=True
        parameters.suppress_fringes=True
        parameters.crystal_size_min=10.0e-9*meter
        parameters.crystal_size_max=100.0e-9*meter
        parameters.uniform_rotation=False

        # Check all parameters are set as intended.
        self.assertEqual( parameters.sample, "5udc.pdb")
        self.assertFalse( parameters.uniform_rotation )
        self.assertEqual( parameters.number_of_diffraction_patterns, 10 )
        self.assertTrue( parameters.powder )
        self.assertEqual( parameters.crystal_size_min, 10.0e-9*meter )
        self.assertEqual( parameters.crystal_size_max, 100.0e-9*meter )
        self.assertTrue( parameters.poissonize )
        self.assertEqual( parameters.number_of_background_photons, 100 )
        self.assertTrue( parameters.suppress_fringes )

    def testCrystalSizes(self):
        """ Test the various ways to set the crystal size range. """
        # Construct with only minimum size.
        parameters = CrystFELPhotonDiffractorParameters(sample=TestUtilities.generateTestFilePath("2nip.pdb"),
        powder=True,
        number_of_diffraction_patterns=10,
        number_of_background_photons=100,
        poissonize=True,
        suppress_fringes=True,
        crystal_size_min=10.0e-9*meter,
        uniform_rotation=False,
        )

        self.assertEqual( parameters.crystal_size_min, parameters.crystal_size_max )

        # Construct with only max size.
        parameters = CrystFELPhotonDiffractorParameters(sample=TestUtilities.generateTestFilePath("2nip.pdb"),
        powder=True,
        number_of_diffraction_patterns=10,
        number_of_background_photons=100,
        poissonize=True,
        suppress_fringes=True,
        crystal_size_max=10.0e-9*meter,
        uniform_rotation=False,
        )

        self.assertEqual( parameters.crystal_size_min, parameters.crystal_size_max )

        # Construct with both sizes set.
        parameters = CrystFELPhotonDiffractorParameters(
                sample=TestUtilities.generateTestFilePath("2nip.pdb"),
                powder=True,
                number_of_diffraction_patterns=10,
                number_of_background_photons=100,
                poissonize=True,
                suppress_fringes=True,
                crystal_size_min=10.0e-9*meter,
                crystal_size_max=100.0e-9*meter,
                uniform_rotation=False,
                )

        self.assertNotEqual( parameters.crystal_size_min, parameters.crystal_size_max )



if __name__ == '__main__':
    unittest.main()

