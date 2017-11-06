""" :module DetectorGeometryTest: Test module for the DetectorGeometry class.  """
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
import shutil

# Include needed directories in sys.path.
import paths
import unittest

from SimEx.Parameters.AbstractCalculatorParameters import AbstractCalculatorParameters
from SimEx.Parameters.DetectorGeometry import DetectorGeometry, DetectorPanel
from SimEx.Utilities.Units import Metre
from SimEx import PhysicalQuantity

class DetectorGeometryTest(unittest.TestCase):
    """
    Test class for the DetectorGeometry class.
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
        self.assertRaises( TypeError,  DetectorGeometry )

    def testShapedConstruction(self):

        # Get a panel
        detector_panel = DetectorPanel()

        # Construct the detector geometry.
        detector_geometry = DetectorGeometry(panels=detector_panel)

        # Check type and inheritance.
        self.assertIsInstance(detector_geometry, DetectorGeometry)
        self.assertIsInstance(detector_geometry, AbstractCalculatorParameters)

        # Check members.
        self.assertEqual( detector_panel, detector_geometry.panels[0] )

class DetectorPanelTest(unittest.TestCase):
    """
    Test class for the DetectorPanel class.
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
        panel = DetectorPanel()
        self.assertIsInstance( panel, DetectorPanel )

    def testShapedConstruction(self):
        """ Testing construction with parameters. """

        # Construct the panel.
        panel = DetectorPanel(
                dimensions                      = ["ss", "fs"],
                ranges                          = [[0,511],[0,511]],
                pixel_size                      = 2.2e-4*Metre,
                adu_response                    = 1.0,
                badrow_direction                = None,
                distance_from_interaction_plane = 0.13*Metre,
                distance_offset                 = 0.0*Metre,
                fast_scan_xyz                   = None,
                slow_scan_xyz                   = None,
                corners                         = [512,512],
                saturation_adu                  = 1e4,
                mask                            = None,
                good_bit_mask                   = None,
                bad_bit_mask                    = None,
                saturation_map                  = None,
                badregion_flag                  = False,
                )

        # Check attributes.
        self.assertListsEqual( panel.dimensions,                     , ['ss', 'fs'] )
        self.assertListsEqual( panel.ranges,                         , [[0,511],[0,511]] )
        self.assertEqual( panel.pixel_size,                          , 1.0e-4*Metre )
        self.assertEqual( panel.adu_response,                        ,
        self.assertEqual( panel.badrow_direction
        self.assertEqual( panel.distance_from_interaction_plane
        self.assertEqual( panel.distance_offset
        self.assertEqual( panel.fast_scan_xyz
        self.assertEqual( panel.slow_scan_xyz
        self.assertEqual( panel.corners
        self.assertEqual( panel.saturation_adu
        self.assertEqual( panel.mask
        self.assertEqual( panel.good_bit_mask
        self.assertEqual( panel.bad_bit_mask
        self.assertEqual( panel.saturation_map
        self.assertEqual( panel.badregion_flag




    def testPanelSize(self):
        """ Testing construction with parameters. """

        # Construct the panel.
        panel = DetectorPanel(
                dimensions                      = ["ss", "fs"],
                ranges                          = [[0,511],[0,511]],
                pixel_size                      = 2.2e-4*Metre,
                adu_response                    = 1.0,
                badrow_direction                = None,
                distance_from_interaction_plane = 0.13*Metre,
                distance_offset                 = 0.0*Metre,
                fast_scan_xyz                   = None,
                slow_scan_xyz                   = None,
                corners                         = [512,512],
                saturation_adu                  = 1e4,
                mask                            = None,
                good_bit_mask                   = None,
                bad_bit_mask                    = None,
                saturation_map                  = None,
                badregion_flag                  = False,
                )

        # Check attributes.
        self.assertEqual( panel.pixel_size, 1.0e-4*Metre,)
        self.assertIsInstance(panel.pixel_size, PhysicalQuantity )
        self.assertRaises( DetectorPanel, pixel_size=1.0e-4)


if __name__ == '__main__':
    unittest.main()

