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
from SimEx.Parameters.AbstractCalculatorParameters import AbstractCalculatorParameters
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
        self.assertRaises( AttributeError, XCSITPhotonDetectorParameters )

    def testShapedConstruction(self):
        """ Testing the construction with parameters of the class. """

        # Check construction with detector type.
        detector_parameters = XCSITPhotonDetectorParameters(detector_type='AGIPDSPB')
        self.assertIsInstance( detector_parameters, AbstractCalculatorParameters)
        self.assertIsInstance( detector_parameters, XCSITPhotonDetectorParameters)

        # Check defaults for other fields.

        # Check all parameters are set as intended.
        self.assertEqual( detector_parameters.plasma_search_flag, "BLANK")
        self.assertEqual( detector_parameters.plasma_simulation_flag, "BLANKPLASMA")
        self.assertEqual( detector_parameters.point_simulation_method, "FULL")

    def testSettersAndQueries(self):
        """ Testing the default construction of the class using a dictionary. """

        # Construct with defaults.
        parameters = XCSITPhotonDetectorParameters( detector_type="AGIPDSPB")

        # Reset detector type to non-sense value
        self.assertRaises( TypeError, parameters.detector_type, None)
        self.assertRaises( TypeError, parameters.detector_type, 1)
        self.assertRaises( TypeError, parameters.detector_type, 1.4)
        is_true = False
        try:
            parameters.detector_type="BigFatDetector"
        except ValueError:
            is_true = True
        except:
            is_true = False
        self.assertTrue(is_true)
        self.assertRaises( TypeError, parameters.detector_type, ["AGIPDSPB", "LPD"])

        # Set to different detector.
        parameters.detector_type = "LPD"
        self.assertEqual(parameters.detector_type, "LPD")

        # Reset plasma_search_flag to non-sense value
        self.assertRaises( TypeError,  parameters.plasma_search_flag, None)
        self.assertRaises( TypeError,  parameters.plasma_search_flag, 1)
        self.assertRaises( TypeError,  parameters.plasma_search_flag, 1.4)
        is_true = False
        try:
            parameters.plasma_search_flag="XXX"
        except ValueError:
            is_true = True
        except:
            is_true = False
        self.assertTrue(is_true)
        self.assertRaises( TypeError,  parameters.plasma_search_flag, ["BLANK", "BLANK"])

        # Set to different detector.
        parameters.plasma_search_flag = "BLANK"
        self.assertEqual(parameters.plasma_search_flag, "BLANK")

        # Reset plasma_simulation_flag to non-sense value
        self.assertRaises( TypeError,  parameters.plasma_simulation_flag, None)
        self.assertRaises( TypeError,  parameters.plasma_simulation_flag, 1)
        self.assertRaises( TypeError,  parameters.plasma_simulation_flag, 1.4)
        is_true = False
        try:
            parameters.plasma_simulation_flag="XXX"
        except ValueError:
            is_true = True
        except:
            is_true = False
        self.assertTrue(is_true)
        self.assertRaises( TypeError,  parameters.plasma_simulation_flag, ["BLANKPLASMA", "BLANKPLASMA"])

        # Set to different detector.
        parameters.plasma_simulation_flag = "BLANKPLASMA"
        self.assertEqual(parameters.plasma_simulation_flag, "BLANKPLASMA")
        parameters.plasma_search_flag = "BLANK"
        self.assertEqual(parameters.plasma_search_flag, "BLANK")
        
        # Reset point_simulation_method to non-sense value
        self.assertRaises( TypeError,  parameters.point_simulation_method, None)
        self.assertRaises( TypeError,  parameters.point_simulation_method, 1)
        self.assertRaises( TypeError,  parameters.point_simulation_method, 1.4)
        is_true = False
        try:
            parameters.point_simulation_method="XXX"
        except ValueError:
            is_true = True
        except:
            is_true = False
        self.assertTrue(is_true)
        self.assertRaises( TypeError,  parameters.point_simulation_method, ["FANO", "FULL"])

        # Set to different detector.
        parameters.point_simulation_method = "FANO"
        self.assertEqual(parameters.point_simulation_method, "FANO")

if __name__ == '__main__':
    unittest.main()
