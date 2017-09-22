""" Test module for the XCSITPhotonDetector."""
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

import os
import h5py
import shutil
import subprocess

# Include needed directories in sys.path.
import paths
import unittest


# Import the class to test.
from SimEx.Calculators.XCSITPhotonDetector import XCSITPhotonDetector, XCSITPhotonDetectorParameters
from SimEx.Calculators.AbstractPhotonDetector import AbstractPhotonDetector
from SimEx.Parameters.PhotonBeamParameters import PhotonBeamParameters
from TestUtilities import TestUtilities

class XCSITPhotonDetectorTest(unittest.TestCase):
    """
    Test class for the XCSITPhotonDetector class.
    """

    @classmethod
    def setUpClass(cls):
        """ Setting up the test class. """
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

    def testShapedConstruction(self):
        """ Testing the construction of the class with parameters. """

        # Setup parameters.
        parameters=XCSITPhotonDetectorParameters(detector_type="AGIPDSPB")

        # Check construction fails without parameters.
        self.assertRaises( AttributeError, XCSITPhotonDetector )

        # Check construction fails without input_path.
        self.assertRaises( AttributeError, XCSITPhotonDetector, parameters )

        # Construct the object.
        diffractor = XCSITPhotonDetector(parameters=parameters, input_path=TestUtilities.generateTestFilePath("diffr"))

        # Check correct default handling for output_path:
        self.assertEqual( os.path.split(diffractor.output_path)[-1], "detector_out.h5")

        # Check type.
        self.assertIsInstance(diffractor, XCSITPhotonDetector)
        self.assertIsInstance(diffractor, AbstractPhotonDetector)

    @unittest.skip("Run this only on large memory machine.")
    def testMinimalExample(self):
        """ Check that beam parameters can be taken from a given propagation output file."""

        self.__files_to_remove.append("detector_out.h5")

        parameters = XCSITPhotonDetectorParameters(
                detector_type="AGIPDSPB",
                )

        diffractor = XCSITPhotonDetector(
                parameters=parameters,
                input_path=TestUtilities.generateTestFilePath("diffr/diffr_out_0000001.h5"),
                output_path="detector_out.h5",
                )

        diffractor._readH5()
        diffractor.backengine()
        diffractor.saveH5()

        # Assert output was created.
        self.assertTrue(os.path.isfile("detector_out.h5"))

        # Check if we can read the output.
        with h5py.File( "detector_out.h5") as h5:
            self.assertIn( "data", h5.keys() )
            self.assertIn( "data", h5["data"].keys() )
            self.assertIn( "photons", h5["data"].keys() )

if __name__ == '__main__':
    unittest.main()

