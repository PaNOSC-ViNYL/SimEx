""" Test module for the WPGUtilities  """
##########################################################################
#                                                                        #
# Copyright (C) 2020-2021 Juncheng E                                     #
# Contact: Juncheng E <juncheng.e@xfel.eu>                               #
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
from TestUtilities.TestUtilities import generateTestFilePath
from SimEx.Utilities.WPGUtilities import WPGdata
from wpg import Wavefront


class WPGUtilitiesTest(unittest.TestCase):
    """ Test class for the WPGUtilities. """
    @classmethod
    def setUpClass(cls):
        """ Setting up the test class. """

    @classmethod
    def tearDownClass(cls):
        """ Tearing down the test class. """

    def setUp(self):
        """ Setting up a test. """
        self.__files_to_remove = []
        self.__paths_to_remove = []

    def tearDown(self):
        """ Tearing down a test. """
        # Clean up.
        for f in self.__files_to_remove:
            if os.path.isfile(f):
                os.remove(f)
        for p in self.__paths_to_remove:
            if os.path.isdir(p):
                shutil.rmtree(p)

    # @unittest.skip("demonstrating skipping")
    def testWPGDataSourceConstruction(self):
        """ Testing the construction of the class with the source hdf5 file. """
        file_path = generateTestFilePath("FELsource_out.h5")
        print("Testing path: ", file_path)
        FELsource_data = WPGdata(file_path)
        self.assertIsInstance(FELsource_data.wavefront, Wavefront)

    # @unittest.skip("demonstrating skipping")
    def testWPGDataPropConstruction(self):
        """ Testing the construction of the class with the prop hdf5 file. """
        file_path = generateTestFilePath("prop_out_0000001.h5")
        print("Testing path: ", file_path)
        prop_data = WPGdata(file_path)
        self.assertIsInstance(prop_data.wavefront, Wavefront)

    # def testTotal_power(slef):
    #     """ Check if one can get the total_power from FELsource"""

    #     file_path = generateTestFilePath("prop_out_0000001.h5")


if __name__ == '__main__':
    unittest.main()