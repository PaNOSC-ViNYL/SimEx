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
RENDER_PLOT=True # Set to True to show plots.
""" Test module for the DiffractionAnalysis.

    @author : CFG
    @institution : XFEL
    @creation 20170322

"""
import h5py
import numpy
import os, shutil
import paths
import unittest
import wpg

from TestUtilities import TestUtilities

# Import the class to test.
from SimEx.Analysis.AbstractAnalysis import AbstractAnalysis, plt
from SimEx.Analysis.DiffractionAnalysis import DiffractionAnalysis

class DiffractionAnalysisTest(unittest.TestCase):
    """
    Test class for the DiffractionAnalysis class.
    """

    @classmethod
    def setUpClass(cls):
        """ Setting up the test class. """

    @classmethod
    def tearDownClass(cls):
        """ Tearing down the test class. """

    def setUp(self):
        """ Setting up a test. """
        self.__files_to_remove = []
        self.__dirs_to_remove = []

        self.__test_data = TestUtilities.generateTestFilePath('diffr.h5')

    def tearDown(self):
        """ Tearing down a test. """

        for f in self.__files_to_remove:
            if os.path.isfile(f): os.remove(f)
        for d in self.__dirs_to_remove:
            if os.path.isdir(d): shutil.rmtree(d)

        if RENDER_PLOT:
            plt.show()

    def testDefaultConstruction(self):
        """ Testing the default construction of the class. """

        # Constructing the object without input fails.
        self.assertRaises(ValueError, DiffractionAnalysis )

    def testShapedConstruction(self):
        """ Testing the construction of the class with non-default parameters. """

        # Construct the object.
        analyzer = DiffractionAnalysis(input_path=self.__test_data)

        self.assertIsInstance(analyzer, DiffractionAnalysis)
        self.assertIsInstance(analyzer, AbstractAnalysis)
        self.assertIsInstance(analyzer, object)

        self.assertIsInstance( analyzer.input_path, str )
        self.assertEqual( analyzer.input_path, self.__test_data)

    def testPlotOnePatternPoissonized(self):
        """ Check we can plot one diffraction pattern as a color map. """
        analyzer = DiffractionAnalysis(input_path=self.__test_data)
        analyzer.plotPattern(poissonized=True)
        plt.show()

    def testPlotOnePattern(self):
        """ Check we can plot one diffraction pattern as a color map. """
        analyzer = DiffractionAnalysis(input_path=self.__test_data)
        analyzer.plotPattern(pattern=4, operation=None)
        plt.show()

    def testPlotSumPatternLogscale(self):
        """ Check we can plot one diffraction pattern as a color map. """
        analyzer = DiffractionAnalysis(input_path=self.__test_data)
        analyzer.plotPattern(pattern="all", operation=numpy.sum, logscale=True, poissonized=False)
        plt.show()

    def testPlotOnePatternLegacy(self):
        """ Check we can plot one diffraction pattern from a v0.1 dir as a color map. """
        analyzer = DiffractionAnalysis(input_path=TestUtilities.generateTestFilePath('diffr_0.1'))
        analyzer.plotPattern(pattern=4, operation=None)
        plt.show()

    def testPlotAvgPattern(self):
        """ Check we can plot the average diffraction pattern as a color map. """
        analyzer = DiffractionAnalysis(input_path=self.__test_data)
        analyzer.plotPattern(pattern="all", operation=numpy.mean)
        plt.show()

    def testPlotRMSPattern(self):
        """ Check we can plot the rms diffraction pattern as a color map. """
        analyzer = DiffractionAnalysis(input_path=self.__test_data)
        analyzer.plotPattern(pattern="all", operation=numpy.std)
        plt.show()

if __name__ == '__main__':
    unittest.main()
