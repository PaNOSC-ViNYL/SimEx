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
RENDER_PLOT=False # Set to True or use environment variable to show plots.

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
from SimEx.Analysis.DiffractionAnalysis import diffractionParameters, plotImage


if 'RENDER_PLOT' in os.environ:
    RENDER_PLOT=bool(os.environ['RENDER_PLOT'])


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
        analyzer = DiffractionAnalysis(input_path=self.__test_data,
                pattern_indices=[1,3,6],
                poissonize=False)

        self.assertIsInstance(analyzer, DiffractionAnalysis)
        self.assertIsInstance(analyzer, AbstractAnalysis)
        self.assertIsInstance(analyzer, object)

        self.assertIsInstance( analyzer.input_path, str )
        self.assertEqual( analyzer.input_path, self.__test_data)
        self.assertFalse( analyzer.poissonize)
        self.assertEqual( analyzer.pattern_indices, [1,3,6])

    def testShapedConstructionDefaults(self):
        """ Testing the construction of the class with non-default parameters. """

        # Construct the object.
        analyzer = DiffractionAnalysis(input_path=self.__test_data,
                )

        self.assertIsInstance(analyzer, DiffractionAnalysis)
        self.assertIsInstance(analyzer, AbstractAnalysis)
        self.assertIsInstance(analyzer, object)

        self.assertIsInstance( analyzer.input_path, str )
        self.assertEqual( analyzer.input_path, self.__test_data)
        self.assertTrue( analyzer.poissonize)
        self.assertEqual( analyzer.pattern_indices, "all")


    def testPlotOnePatternPoissonized(self):
        """ Check we can plot one diffraction pattern as a color map. """
        analyzer = DiffractionAnalysis(input_path=self.__test_data, pattern_indices=1)
        analyzer.plotPattern()
        plt.show()

    def testPlotOnePattern(self):
        """ Check we can plot one diffraction pattern as a color map. """
        analyzer = DiffractionAnalysis(input_path=self.__test_data, pattern_indices=4)
        analyzer.plotPattern()
        plt.show()

    def testPlotSumPatternLogscale(self):
        """ Check we can plot one diffraction pattern as a color map. """
        analyzer = DiffractionAnalysis(input_path=self.__test_data,
                poissonize=False)
        analyzer.plotPattern(operation=numpy.sum, logscale=True)
        plt.show()

    def testPlotOnePatternLegacy(self):
        """ Check we can plot one diffraction pattern from a v0.1 dir as a color map. """
        analyzer = DiffractionAnalysis(input_path=TestUtilities.generateTestFilePath('diffr_0.1'), pattern_indices=4)
        analyzer.plotPattern(operation=None)
        plt.show()

    def testPlotAvgPattern(self):
        """ Check we can plot the average diffraction pattern as a color map. """
        analyzer = DiffractionAnalysis(input_path=self.__test_data)
        analyzer.plotPattern(operation=numpy.mean)
        plt.show()

    def testPlotAvgPatternLegacy(self):
        """ Check we can plot the average diffraction pattern as a color map. """
        analyzer = DiffractionAnalysis(input_path=TestUtilities.generateTestFilePath('diffr_0.1'))
        analyzer.plotPattern(operation=numpy.mean)
        plt.show()


    def testPlotPatternDefault(self):
        """ Check we the sum image of all patterns is plotted by default. """
        analyzer = DiffractionAnalysis(input_path=self.__test_data)
        analyzer.plotPattern()
        plt.show()


    def testPlotRMSPattern(self):
        """ Check we can plot the rms diffraction pattern as a color map. """
        analyzer = DiffractionAnalysis(input_path=self.__test_data)
        analyzer.plotPattern(operation=numpy.std)
        plt.show()

    def testPlotAvgSequenceInt(self):
        """ Check we can plot the avg over a subset of patterns given as list of ints."""
        analyzer = DiffractionAnalysis(input_path=self.__test_data, pattern_indices=[1,3,6])
        analyzer.plotPattern(operation=numpy.mean)
        plt.show()

    def testPlotImage(self):
        """ Check we can plot an ndarray."""
        image = numpy.random.random((100, 100))
        plotImage(image)
        plt.show()

    def testDiffractionParameters(self):
        """ Test the utility to extract parameters from a h5 file."""

        # Setup test file path.
        path = self.__test_data

        # Extract.
        parameters = diffractionParameters(path)

        # Check for some keys.
        self.assertIn('beam', parameters.keys())
        self.assertIn('geom', parameters.keys())
        self.assertIn('photonEnergy', parameters['beam'].keys())
        self.assertIn('pixelWidth', parameters['geom'].keys())

    def testPlotAndStatistics(self):
        """ Check that we can get two plots (resetting the iterator works.)"""
        analyzer = DiffractionAnalysis(input_path=self.__test_data, pattern_indices="all", poissonize=True)

        analyzer.logscale = True
        analyzer.plotPattern(logscale=True)
        analyzer.statistics()

    def testRadialProjection(self):
        """ Check that we can get two plots (resetting the iterator works.)"""
        analyzer = DiffractionAnalysis(input_path=self.__test_data, pattern_indices="all", poissonize=True)

        analyzer.logscale = False
        analyzer.plotRadialProjection()
        analyzer.plotRadialProjection(logscale=True)
        analyzer.plotRadialProjection(operation=numpy.std)


    def testAnimatePatterns(self):
        """ Test the animation feature. """

        # Setup the analyser with a sequence of patterns.
        analyzer = DiffractionAnalysis(input_path=self.__test_data,
                                       pattern_indices=range(1,11),
                                      )

        # Check exceptions on faulty path.
        self.assertRaises(TypeError, analyzer.animatePatterns, output_path=["not", "a", "path"] )
        self.assertRaises(IOError, analyzer.animatePatterns, output_path="/users/home/myself/animation.gif")

        # Check default behaviour.
        analyzer.animatePatterns(output_path=None)

        # Check output is present.
        animation_out_path = 'animated_patterns.gif'
        self.__files_to_remove.append(animation_out_path)
        self.assertIn(animation_out_path, os.listdir(os.getcwd()) )

        # Check path is stored on object.
        self.assertEqual(analyzer._DiffractionAnalysis__animation_output_path, os.path.join(os.getcwd(), animation_out_path) )

        # Check exception on overwrite.
        self.assertRaises(IOError, analyzer.animatePatterns, output_path=animation_out_path)

        # Execute with parameter.
        animation_out_path = 'animation2.gif'
        self.__files_to_remove.append(animation_out_path)

        analyzer.animatePatterns(output_path=animation_out_path)

        # Check path is stored on object.
        self.assertEqual(analyzer._DiffractionAnalysis__animation_output_path, os.path.join(os.getcwd(), animation_out_path) )

        # Check file is present.
        self.assertIn(animation_out_path, os.listdir(os.getcwd()) )


if __name__ == '__main__':
    unittest.main()
