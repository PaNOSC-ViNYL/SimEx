""" :module CrystFELPhotonDiffractorParameter: Test module for the CrystFELPhotonDiffractorParameter class.  """
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

import paths
import os
import numpy
import shutil
import subprocess

# Include needed directories in sys.path.
import paths
import unittest

from TestUtilities import TestUtilities
#from SimEx.Parameters.AbstractCalculatorParameters import AbstractCalculatorParameters
from SimEx.Calculators.XCSITPhotonDetectorParameters import XCSITPhotonDetectorParameters
from SimEx.Parameters.PhotonBeamParameters import PhotonBeamParameters


class XCSITPhotonDetectorParametersTest(unittest.TestCase):
    """
    Test class for the XCSITPhotonDetectorParameters class.
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
        parameters = XCSITPhotonDetectorParameters( )

        ## Check instance and inheritance.
        #self.assertIsInstance( parameters, XCSITPhotonDetectorParameters )
        #self.assertIsInstance( parameters, AbstractCalculatorParameters )

        ## Check all parameters are set to default values.
        #self.assertEqual( parameters.sample, TestUtilities.generateTestFilePath("2nip.pdb") )
        #self.assertTrue( parameters.uniform_rotation )
        #self.assertEqual( parameters.beam_parameters, None )
        #self.assertEqual( parameters.geometry, None )
        #self.assertTrue( parameters.uniform_rotation )
        #self.assertEqual( parameters.number_of_diffraction_patterns, 1 )
        #self.assertFalse( parameters.powder )
        #self.assertEqual( parameters.intensities_file, None )
        #self.assertEqual( parameters.crystal_size_range, None )
        #self.assertFalse( parameters.poissonize, False )
        #self.assertEqual( parameters.number_of_background_photons, 0 )
        #self.assertFalse( parameters.suppress_fringes )
        #self.assertEqual( parameters.beam_parameters, None )
        #self.assertEqual( parameters.geometry, None )

    def testShapedConstruction(self):
        """ Testing the construction with parameters of the class. """

        beam_parameters = PhotonBeamParameters(
                photon_energy=4.96e3,
                photon_energy_relative_bandwidth=0.01,
                beam_diameter_fwhm=2e-6,
                divergence=2e-6,
                pulse_energy=1e3)

        # Attempt to construct an instance of the class.
        parameters = XCSITPhotonDetectorParameters(
                sample=TestUtilities.generateTestFilePath("2nip.pdb"),
                powder=True,
                number_of_diffraction_patterns=10,
                number_of_background_photons=100,
                poissonize=True,
                suppress_fringes=True,
                crystal_size_range=[10,100],
                uniform_rotation=False,
                beam_parameters=beam_parameters,
                geometry=TestUtilities.generateTestFilePath('simple.geom'))


        # Check all parameters are set as intended.
        self.assertFalse( parameters.uniform_rotation )
        self.assertEqual( parameters.number_of_diffraction_patterns, 10 )
        self.assertTrue( parameters.powder )
        self.assertEqual( parameters.crystal_size_range, (10.,100.) )
        self.assertTrue( parameters.poissonize )
        self.assertEqual( parameters.number_of_background_photons, 100 )
        self.assertTrue( parameters.suppress_fringes )
        self.assertIsInstance( parameters.beam_parameters, PhotonBeamParameters )
        self.assertEqual( parameters.beam_parameters.photon_energy, 4.96e3 )
        self.assertEqual( parameters.geometry, TestUtilities.generateTestFilePath('simple.geom') )

    def testSettersAndQueries(self):
        """ Testing the default construction of the class using a dictionary. """

        self.__files_to_remove.append("5udc.pdb")

        # Construct with defaults.
        parameters = XCSITPhotonDetectorParameters(TestUtilities.generateTestFilePath("2nip.pdb"))

        # Set some members to non-defaults.
        parameters.sample="5udc.pdb"
        parameters.powder=True
        parameters.number_of_diffraction_patterns=10
        parameters.number_of_background_photons=100
        parameters.poissonize=True
        parameters.suppress_fringes=True
        parameters.crystal_size_range=[10,100]
        parameters.uniform_rotation=False

        # Check all parameters are set as intended.
        self.assertEqual( parameters.sample, "5udc.pdb")
        self.assertFalse( parameters.uniform_rotation )
        self.assertEqual( parameters.number_of_diffraction_patterns, 10 )
        self.assertTrue( parameters.powder )
        self.assertEqual( parameters.crystal_size_range, (10.,100.) )
        self.assertTrue( parameters.poissonize )
        self.assertEqual( parameters.number_of_background_photons, 100 )
        self.assertTrue( parameters.suppress_fringes )

if __name__ == '__main__':
    unittest.main()

