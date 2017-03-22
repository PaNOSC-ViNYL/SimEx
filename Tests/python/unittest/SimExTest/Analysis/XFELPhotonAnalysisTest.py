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

""" Test module for the XFELPhotonAnalysis.

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
from SimEx.Analysis.XFELPhotonAnalysis import XFELPhotonAnalysis

class XFELPhotonAnalysisTest(unittest.TestCase):
    """
    Test class for the XFELPhotonAnalysis class.
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

    def tearDown(self):
        """ Tearing down a test. """

        for f in self.__files_to_remove:
            if os.path.isfile(f): os.remove(f)
        for d in self.__dirs_to_remove:
            if os.path.isdir(d): shutil.rmtree(d)

        # To actually see the plots, uncomment this line.
        #plt.show()

    def testDefaultConstruction(self):
        """ Testing the default construction of the class. """

        # Constructing the object without input fails.
        self.assertRaises(ValueError, XFELPhotonAnalysis )

    def testShapedConstruction(self):
        """ Testing the construction of the class with non-default parameters. """

        # Construct the object.
        xfel_photon_analyzer = XFELPhotonAnalysis(input_path=TestUtilities.generateTestFilePath('prop_out_0000001.h5'))

        self.assertIsInstance(xfel_photon_analyzer, XFELPhotonAnalysis)
        self.assertIsInstance(xfel_photon_analyzer, AbstractAnalysis)
        self.assertIsInstance(xfel_photon_analyzer, object)

        self.assertIsInstance( xfel_photon_analyzer.wavefront, wpg.Wavefront)

    def testPlotTotalPowerVsTime(self):
        """ Test plotting the total power as function of time. """
        xfel_photon_analyzer = XFELPhotonAnalysis(input_path=TestUtilities.generateTestFilePath('prop_out_0000001.h5'))

        xfel_photon_analyzer.plotTotalPower()


    def testPlotTotalPowerVsEnergy(self):
        """ Test plotting the total power spectrum."""
        xfel_photon_analyzer = XFELPhotonAnalysis(input_path=TestUtilities.generateTestFilePath('prop_out_0000001.h5'))

        xfel_photon_analyzer.plotTotalPower(spectrum=True)


    def testPlotOnAxisPowerDensityVsTime(self):
        """ Test plotting the on-axis power as function of time. """
        xfel_photon_analyzer = XFELPhotonAnalysis(input_path=TestUtilities.generateTestFilePath('prop_out_0000001.h5'))

        xfel_photon_analyzer.plotOnAxisPowerDensity()


    def testPlotOnAxisPowerDensityVsEnergy(self):
        """ Test plotting the total power spectrum."""
        xfel_photon_analyzer = XFELPhotonAnalysis(input_path=TestUtilities.generateTestFilePath('prop_out_0000001.h5'))

        xfel_photon_analyzer.plotOnAxisPowerDensity(spectrum=True)


    def testPlotIntensityMap(self):
        """ Test plotting the intensity map."""
        xfel_photon_analyzer = XFELPhotonAnalysis(input_path=TestUtilities.generateTestFilePath('prop_out_0000001.h5'))

        xfel_photon_analyzer.plotIntensityMap()

    def testPlotIntensityMapLog(self):
        """ Test plotting the intensity map."""
        xfel_photon_analyzer = XFELPhotonAnalysis(input_path=TestUtilities.generateTestFilePath('prop_out_0000001.h5'))

        xfel_photon_analyzer.plotIntensityMap(logscale=True)

    def testPlotIntensityQMap(self):
        """ Test plotting the intensity map."""
        xfel_photon_analyzer = XFELPhotonAnalysis(input_path=TestUtilities.generateTestFilePath('prop_out_0000001.h5'))

        xfel_photon_analyzer.plotIntensityMap(qspace=True)


if __name__ == '__main__':
    unittest.main()

