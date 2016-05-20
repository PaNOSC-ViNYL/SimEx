##########################################################################
#                                                                        #
# Copyright (C) 2015 Carsten Fortmann-Grote                              #
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
# Include needed directories in sys.path.                                #
#                                                                        #
##########################################################################

""" Test module for the SingFELPhotonDiffractor.

    @author : CFG
    @institution : XFEL
    @creation 20151109

"""
import os
import subprocess

import paths
import unittest


# Import the class to test.
from SimEx.Calculators.EMCOrientation import EMCOrientation
from TestUtilities import TestUtilities

class EMCOrientationTest(unittest.TestCase):
    """
    Test class for the EMCOrientation class.
    """

    @classmethod
    def setUpClass(cls):
        """ Setting up the test class. """
        cls.input_h5 = TestUtilities.generateTestFilePath('diffr_out_0000001.h5')

    @classmethod
    def tearDownClass(cls):
        """ Tearing down the test class. """
        del cls.input_h5

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
                os.rmdir(d)

    def testConstruction(self):
        """ Testing the default construction of the class. """

        # Construct the object.
        analyzer = EMCOrientation(parameters=None, input_path=self.input_h5, output_path='orient_out.h5')

        self.assertIsInstance(analyzer, EMCOrientation)

    def testBackengine(self):
        """ Test that we can start a test calculation. """

        self.__files_to_remove.append('orient_out.h5')

        # Construct the object.
        analyzer = EMCOrientation(parameters=None, input_path=self.input_h5, output_path='orient_out.h5')

        # Call backengine.
        status = analyzer.backengine()

        self.assertEqual(status, 0)

    def testPaths(self):
        """ Test that we can start a test calculation. """

        self.__files_to_remove.append('orient_out.h5')

        # Construct the object.
        analyzer = EMCOrientation(parameters=None, input_path=self.input_h5, output_path='orient_out.h5')

        # Call backengine.
        status = analyzer.backengine()

        # Check paths exist and are populated.
        run_files_path = analyzer.run_files_path
        tmp_files_path = analyzer.tmp_files_path

        self.assertTrue( os.isdir( run_files_path ) )
        self.assertTrue( os.isdir( tmp_files_path ) )

        expected_run_files = ["finish_intensity.dat", "quaternion.dat",
                              "detector.dat",
                              "most_likely_orientations.dat",
                              "start_intensity.dat",
                              "EMC_extended.log",
                              "mutual_info.dat",
                              "EMC.log",
                              "photons.dat",
                              ]

        for ef in expected_run_files:
            self.assertIn( ef, os.path.listdir(run_files_path) )



if __name__ == '__main__':
    unittest.main()

