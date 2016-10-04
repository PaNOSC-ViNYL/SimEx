##########################################################################
#                                                                        #
# Copyright (C) 2015, 2016 Carsten Fortmann-Grote                        #
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

""" Test module for the WavePropagator.

    @author : CFG
    @institution : XFEL
    @creation 20160321

"""
import os, shutil
import paths
import unittest

import numpy
import h5py
from wpg.beamline import Beamline

# Import the class to test.
from SimEx.Calculators.WavePropagator import WavePropagator
from TestUtilities import TestUtilities

from SimEx.Utilities.WPGBeamlines import setupSPBDay1Beamline
from SimEx.Utilities.WPGBeamlines import setup_S2E_SPI_beamline
from SimEx.Parameters.WavePropagatorParameters import WavePropagatorParameters

class WavePropagatorTest(unittest.TestCase):
    """
    Test class for the WavePropagator class.
    """

    @classmethod
    def setUpClass(cls):
        """ Setting up the test class. """
        cls.input_h5 = TestUtilities.generateTestFilePath('FELsource_out/FELsource_out_0000000.h5')

        # Use this for strong testing, but takes long.
        #cls.input_h5 = TestUtilities.generateTestFilePath('0000028.h5')

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

    def testConstructionDefault(self):
        """ Test the construction with default parameters. """

        # Construct the object.
        propagator = WavePropagator(input_path=self.input_h5,
                                    output_path='wpg_out_0000000.h5')

        self.assertIsInstance(propagator, WavePropagator)
        self.assertIsInstance(propagator.parameters.beamline, Beamline )

    def testConstructionParameters1(self):
        """ Testing the default construction of the class. """

        # Define a beamline.
        beamline = setupSPBDay1Beamline()

        # Construct the object.
        propagator = WavePropagator(parameters=WavePropagatorParameters(beamline=beamline),
                                    input_path=self.input_h5,
                                    output_path='wpg_out_0000000.h5')

        self.assertIsInstance(propagator, WavePropagator)

    def testConstructionParameters2(self):
        """ Testing the construction of the class with a parameters object. """

        # Define a beamline.
        beamline = setupSPBDay1Beamline()

        parameters = WavePropagatorParameters(beamline=beamline, use_opmd=True)

        # Construct the object.
        propagator = WavePropagator(parameters=parameters,
                                         input_path=self.input_h5,
                                         output_path='wpg_out_0000000.h5')

        self.assertIsInstance(propagator, WavePropagator)


    def testConstructionFailParameters(self):
        """ Testing that faulty construction raises an exception. """

        # Define a beamline.
        beamline = setupSPBDay1Beamline()

        # Construct the object with beamline as parameter.
        self.assertRaises( TypeError, WavePropagator,
                                    parameters=beamline,
                                    input_path=self.input_h5,
                                    output_path='wpg_out_0000001.h5')

        # Construct the object with a parameters dict.
        self.assertRaises( TypeError, WavePropagator,
                parameters={'beamline' : beamline},
                            input_path=self.input_h5,
                            output_path='wpg_out_0000001.h5')



    def testReadH5ExceptionInput(self):
        """ Test exception raises if input is not a valid h5 file. """
        # Define a beamline.
        beamline = setupSPBDay1Beamline()

        parameters = WavePropagatorParameters(beamline=beamline)

        # Construct the object.
        propagator = WavePropagator(parameters=parameters,
                                    input_path='/tmp',
                                    output_path='wpg_out_0000001.h5')

        # Check exception raises when attempting to read.
        self.assertRaises( IOError, propagator._readH5 )

    def testReadCalculateWrite(self):
        """ Test a backengine run with a single input file. """
        # Define a beamline.
        beamline = setupSPBDay1Beamline()

        # Construct the object.
        propagator = WavePropagator( parameters=WavePropagatorParameters(beamline=beamline), input_path=self.input_h5, output_path='wpg_out.h5' )

        # Read the data.
        propagator._readH5()

        # Call the backengine.
        status = propagator.backengine()

        # Check backengine returned sanely.
        self.assertEqual( status, 0 )

        # Write propagated wavefront.
        propagator.saveH5()

        # Check output was written.
        self.assertTrue( os.path.isfile( propagator.output_path ) )

        # Ensure clean-up.
        self.__files_to_remove.append(propagator.output_path)


    def testOPMD(self):
        """ Test usage of the use_opmd parameter. """

        # Make sure we clean up after the fact.
        self.__files_to_remove.append('wpg_out.h5')
        self.__files_to_remove.append('wpg_out.opmd.h5')

        # Define a beamline.
        beamline = setup_S2E_SPI_beamline()

        # Construct the object.
        propagator = WavePropagator( parameters=WavePropagatorParameters(beamline=beamline, use_opmd=True), input_path=self.input_h5, output_path='wpg_out.h5' )

        # Read the data.
        propagator._readH5()

        # Call the backengine.
        status = propagator.backengine()

        # Write the data.
        propagator.saveH5()

        # Assert that opmd has been written.
        self.assertIn('wpg_out.opmd.h5', os.listdir( os.path.abspath( os.path.dirname( __file__ ) ) ) )

if __name__ == '__main__':
    unittest.main()

