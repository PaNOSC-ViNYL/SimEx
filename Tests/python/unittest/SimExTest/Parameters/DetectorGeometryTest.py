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
import StringIO

# Include needed directories in sys.path.
import paths
import unittest

from SimEx.Parameters.AbstractCalculatorParameters import AbstractCalculatorParameters
from SimEx.Parameters.DetectorGeometry import DetectorGeometry, DetectorPanel
from SimEx.Utilities.Units import meter
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
        self.__panel0 =DetectorPanel(
                dimensions                      = ["ss", "fs"],
                ranges                          = {
                                                    "fast_scan_min" : 0,
                                                    "fast_scan_max" : 511,
                                                    "slow_scan_min" : 512,
                                                    "slow_scan_max" : 1023,
                                                    },
                pixel_size                      = 2.2e-4*meter,
                adu_response                    = 1.0,
                badrow_direction                = None,
                distance_from_interaction_plane = 0.13*meter,
                distance_offset                 = 0.0*meter,
                fast_scan_xyz                   = None,
                slow_scan_xyz                   = None,
                corners                         = {"x" : -512, "y" : -256},
                saturation_adu                  = 1e4,
                mask                            = None,
                good_bit_mask                   = None,
                bad_bit_mask                    = None,
                saturation_map                  = None,
                badregion_flag                  = False,
                )

        # Copy-construct a second panel.
        self.__panel1 = self.__panel0( ranges={'fast_scan_min' : self.__panel0.ranges['fast_scan_min'],
                                 'fast_scan_max' : self.__panel0.ranges['fast_scan_max'],
                                 'slow_scan_min' : self.__panel0.ranges['slow_scan_max'] + 1,
                                 'slow_scan_max' : 2*self.__panel0.ranges['slow_scan_max'] - self.__panel0.ranges['slow_scan_min']+1},
                         corners={'x' : self.__panel0.corners['x'], 'y' : self.__panel0.corners['y'] + 512},
                       )


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

    def testShapedConstructionSinglePanel(self):

        # Get a panel
        detector_panel = self.__panel0

        # Construct the detector geometry.
        detector_geometry = DetectorGeometry(panels=detector_panel)

        # Check type and inheritance.
        self.assertIsInstance(detector_geometry, DetectorGeometry)
        self.assertIsInstance(detector_geometry, AbstractCalculatorParameters)

        # Check members.
        self.assertEqual( detector_panel, detector_geometry.panels[0] )

    def testShapedConstructionMultiPanels(self):

        # Get a panel
        panel0 = self.__panel0
        panel1 = self.__panel1

                # Construct the detector geometry.
        detector_geometry = DetectorGeometry(panels=[panel0, panel1])

        # Check members.
        self.assertEqual( panel0, detector_geometry.panels[0] )
        self.assertEqual( panel1, detector_geometry.panels[1] )

    def testSerialize(self):
        """ Test the serialization of the DetectorGeometry. """

        # Get panels
        panel0 = self.__panel0
        panel1 = self.__panel1

        # Setup the detector geometry.
        detector_geometry = DetectorGeometry(panels=[panel0, panel1])

        # Serialize to stream
        stream = StringIO.StringIO()

        detector_geometry.serialize(stream)

        reference_string=""";panel 0
panel0/min_fs        = 0
panel0/max_fs        = 511
panel0/min_ss        = 512
panel0/max_ss        = 1023
panel0/corner_x      = -512
panel0/corner_y      = -256
panel0/fast_scan_xyz = 1.0x
panel0/slow_scan_xyz = 1.0y
panel0/clen          = 1.3000000e-01
panel0/res           = 4.5454545e+03

;panel 1
panel1/min_fs        = 0
panel1/max_fs        = 511
panel1/min_ss        = 1024
panel1/max_ss        = 1535
panel1/corner_x      = -512
panel1/corner_y      = 256
panel1/fast_scan_xyz = 1.0x
panel1/slow_scan_xyz = 1.0y
panel1/clen          = 1.3000000e-01
panel1/res           = 4.5454545e+03

"""
        self.assertEqual(stream.getvalue(), reference_string)

    def testSerializeHandle(self):
        """ Test the serialization of the DetectorGeometry. """

        # Get panels
        panel0 = self.__panel0
        panel1 = self.__panel1

        # Setup the detector geometry.
        detector_geometry = DetectorGeometry(panels=[panel0, panel1])

        # Serialize to stream
        geom_file = "simex.geom"
        self.__files_to_remove.append(geom_file)

        # Open for writing.
        with open("simex.geom",'w') as stream:

            # Serialize into file handle.
            detector_geometry.serialize(stream)

        reference_string=""";panel 0
panel0/min_fs        = 0
panel0/max_fs        = 511
panel0/min_ss        = 512
panel0/max_ss        = 1023
panel0/corner_x      = -512
panel0/corner_y      = -256
panel0/fast_scan_xyz = 1.0x
panel0/slow_scan_xyz = 1.0y
panel0/clen          = 1.3000000e-01
panel0/res           = 4.5454545e+03

;panel 1
panel1/min_fs        = 0
panel1/max_fs        = 511
panel1/min_ss        = 1024
panel1/max_ss        = 1535
panel1/corner_x      = -512
panel1/corner_y      = 256
panel1/fast_scan_xyz = 1.0x
panel1/slow_scan_xyz = 1.0y
panel1/clen          = 1.3000000e-01
panel1/res           = 4.5454545e+03

"""

        # Open for reading.
        with open(geom_file, 'r') as stream:
            lines = "".join( stream.readlines() )

        self.assertEqual(lines, reference_string)

    def testSerializeFilename(self):
        """ Test the serialization of the DetectorGeometry. """

        # Get panels
        panel0 = self.__panel0
        panel1 = self.__panel1

        # Setup the detector geometry.
        detector_geometry = DetectorGeometry(panels=[panel0, panel1])

        # Serialize to stream
        geom_file = "simex.geom"
        #self.__files_to_remove.append(geom_file)

        # Serialize into file handle.
        detector_geometry.serialize(geom_file)

        reference_string=""";panel 0
panel0/min_fs        = 0
panel0/max_fs        = 511
panel0/min_ss        = 512
panel0/max_ss        = 1023
panel0/corner_x      = -512
panel0/corner_y      = -256
panel0/fast_scan_xyz = 1.0x
panel0/slow_scan_xyz = 1.0y
panel0/clen          = 1.3000000e-01
panel0/res           = 4.5454545e+03

;panel 1
panel1/min_fs        = 0
panel1/max_fs        = 511
panel1/min_ss        = 1024
panel1/max_ss        = 1535
panel1/corner_x      = -512
panel1/corner_y      = 256
panel1/fast_scan_xyz = 1.0x
panel1/slow_scan_xyz = 1.0y
panel1/clen          = 1.3000000e-01
panel1/res           = 4.5454545e+03

"""

        # Open for reading.
        with open(geom_file, 'r') as stream:
            lines = "".join( stream.readlines() )

        self.assertEqual(lines, reference_string)


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

        # Construct the panel.
        self.__panel = DetectorPanel(
                dimensions                      = ["ss", "fs"],
                ranges                          = {
                                                    "fast_scan_min" : 0,
                                                    "fast_scan_max" : 511,
                                                    "slow_scan_min" : 512,
                                                    "slow_scan_max" : 1024,
                                                    },
                pixel_size                      = 2.2e-4*meter,
                adu_response                    = 1.0,
                badrow_direction                = None,
                distance_from_interaction_plane = 0.13*meter,
                distance_offset                 = 0.0*meter,
                fast_scan_xyz                   = None,
                slow_scan_xyz                   = None,
                corners                         = {"x" : -512, "y" : -256},
                saturation_adu                  = 1e4,
                mask                            = None,
                good_bit_mask                   = None,
                bad_bit_mask                    = None,
                saturation_map                  = None,
                badregion_flag                  = False,
                )

    def tearDown(self):
        """ Tearing down a test. """
        for f in self.__files_to_remove:
            if os.path.isfile(f):
                os.remove(f)
        for d in self.__dirs_to_remove:
            if os.path.isdir(d):
                shutil.rmtree(d)

        del self.__panel

    def testDefaultConstruction(self):
        """ Testing the default construction. """

        # Attempt to construct an instance of the class.
        panel = DetectorPanel()
        self.assertIsInstance( panel, DetectorPanel )

    def testShapedConstruction(self):
        """ Testing construction with parameters. """

        # Construct the panel.
        panel = self.__panel

        # Check attributes.
        self.assertListEqual( panel.dimensions                  , ['ss', 'fs'] )
        self.assertDictEqual( panel.ranges                      , { "fast_scan_min" : 0, "fast_scan_max" : 511, "slow_scan_min" : 512, "slow_scan_max" : 1024})
        self.assertEqual( panel.pixel_size                       , 2.2e-4*meter )
        self.assertEqual( panel.adu_response                     , 1.0 )
        self.assertEqual( panel.badrow_direction                 , None )
        self.assertEqual( panel.distance_from_interaction_plane  , 0.13*meter )
        self.assertEqual( panel.distance_offset                  , 0.0*meter )
        self.assertEqual( panel.fast_scan_xyz                    , "1.0x" )
        self.assertEqual( panel.slow_scan_xyz                    , "1.0y" )
        self.assertEqual( panel.corners                          , {"x" : -512, "y" : -256})
        self.assertEqual( panel.saturation_adu                   , 1.0e4 )
        self.assertEqual( panel.mask                             , None )
        self.assertEqual( panel.good_bit_mask                    , None )
        self.assertEqual( panel.bad_bit_mask                     , None )
        self.assertEqual( panel.saturation_map                   , None )
        self.assertEqual( panel.badregion_flag                   , False )


    def testPanelSize(self):
        """ Testing construction with parameters. """

        # Construct the panel.
        panel = self.__panel

        # Check attributes.
        self.assertEqual( panel.pixel_size, 1.0e-4*meter,)
        self.assertIsInstance(panel.pixel_size, PhysicalQuantity )
        self.assertRaises( DetectorPanel, pixel_size=1.0e-4)

    def testSerialize(self):
        """ Test the _serialize() method for the panel. """
        # Construct a panel.
        panel = self.__panel

        stream = StringIO.StringIO()
        panel._serialize(stream=stream)

        reference_string = """;panel 0
panel0/min_fs        = 0
panel0/max_fs        = 511
panel0/min_ss        = 512
panel0/max_ss        = 1024
panel0/corner_x      = -512
panel0/corner_y      = -256
panel0/fast_scan_xyz = 1.0x
panel0/slow_scan_xyz = 1.0y
panel0/clen          = 1.3000000e-01
panel0/res           = 4.5454545e+03

"""

        self.assertEqual( stream.getvalue(), reference_string )

        stream.close()

    def testSerializeToFile(self):
        """ Test the _serialize() method for the panel. """
        # Setup a file for this panel.
        panel_file_name = "panel0.geom"

        self.__files_to_remove.append(panel_file_name)
        with open(panel_file_name, "w") as panel_file:

            # Construct a panel.
            panel = self.__panel

            panel._serialize(stream=panel_file)

            panel_file.close()

        # Setup reference string.
        reference_string = """;panel 0
panel0/min_fs        = 0
panel0/max_fs        = 511
panel0/min_ss        = 512
panel0/max_ss        = 1024
panel0/corner_x      = -512
panel0/corner_y      = -256
panel0/fast_scan_xyz = 1.0x
panel0/slow_scan_xyz = 1.0y
panel0/clen          = 1.3000000e-01
panel0/res           = 4.5454545e+03

"""
        # Open for reading.
        with open(panel_file_name, "r") as panel_file:
            panel_string = "".join(panel_file.readlines())

        # Compare.
        self.assertEqual( panel_string, reference_string )

    def testClone(self):
        """ Test the copy constructor. """
        # Get a panel.
        origin_panel = self.__panel

        # Make a copy.
        copy_panel = origin_panel()

        # Assert they are equal but not identical.
        self.assertEqual( origin_panel, copy_panel )
        self.assertIsNot( origin_panel, copy_panel )

    def testMutate(self):
        """ Test the copy constructor with mutation. """
        # Get a panel.
        origin_panel = self.__panel

        # Make a copy.
        copy_panel = origin_panel(distance_from_interaction_plane = 0.1324*meter )

        # Assert they are equal but not identical.
        self.assertNotEqual( origin_panel, copy_panel )
        self.assertIsNot( origin_panel, copy_panel )

        # Check mutated attribute.
        self.assertEqual( copy_panel.distance_from_interaction_plane, 0.1324*meter )

        #def test<++>(self):
        #""" <++> """
        #self.assertTrue(False)

    #def test<++>(self):
        #""" <++> """
        #self.assertTrue(False)

    #def test<++>(self):
        #""" <++> """
        #self.assertTrue(False)

    #def test<++>(self):
        #""" <++> """
        #self.assertTrue(False)

    #def test<++>(self):
        #""" <++> """
        #self.assertTrue(False)

    #def test<++>(self):
        #""" <++> """
        #self.assertTrue(False)

    #def test<++>(self):
        #""" <++> """
        #self.assertTrue(False)

    #def test<++>(self):
        #""" <++> """
        #self.assertTrue(False)

if __name__ == '__main__':
    unittest.main()

