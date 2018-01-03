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
#                                                                        #
##########################################################################

""" Test module for the XFELPhotonSource.

    @author : CFG
    @institution : XFEL
    @creation 20151104

"""
from . import paths
import unittest

import numpy
import h5py

# Import the class to test.
from SimEx.Calculators.XFELPhotonSource import XFELPhotonSource
from TestUtilities import TestUtilities

class XFELPhotonSourceTest(unittest.TestCase):
    """
    Test class for the XFELPhotonSource class.
    """

    @classmethod
    def setUpClass(cls):
        """ Setting up the test class. """
        cls.input_h5 = TestUtilities.generateTestFilePath('FELsource_out.h5')

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
        xfel_source = XFELPhotonSource(parameters=None, input_path=self.input_h5, output_path='FELsource_out2.h5')

        self.assertIsInstance(xfel_source, XFELPhotonSource)

if __name__ == '__main__':
    unittest.main()

