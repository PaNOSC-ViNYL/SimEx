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
# Include needed directories in sys.path.                                #
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

# Import the class to test.
from SimEx.Calculators.WavePropagator import WavePropagator
from TestUtilities import TestUtilities

from SimEx.Utilities.WPGBeamlines import setupSPBDay1Beamline

class WavePropagatorTest(unittest.TestCase):
    """
    Test class for the WavePropagator class.
    """

    @classmethod
    def setUpClass(cls):
        """ Setting up the test class. """
        cls.input_h5 = TestUtilities.generateTestFilePath('FELsource_out/FELsource_out_0000000.h5')

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


    def testConstruction(self):
        """ Testing the default construction of the class. """

        # Define a beamline.
        beamline = setupSPBDay1Beamline()

        # Construct the object.
        propagator = WavePropagator(parameters={'beamline' : beamline},
                                         input_path=self.input_h5,
                                         output_path='wpg_out_0000000.h5')

        self.assertIsInstance(propagator, WavePropagator)

    def testConstructionBeamline(self):
        """ Testing the construction of the class with the beamline given instead of a dictionary. """

        # Define a beamline.
        beamline = setupSPBDay1Beamline()

        # Construct the object.
        propagator = WavePropagator(parameters=beamline,
                                         input_path=self.input_h5,
                                         output_path='wpg_out_0000000.h5')

        self.assertIsInstance(propagator, WavePropagator)


    def testConstructionFailParameters(self):
        """ Testing that faulty construction raises an exception. """


        # Construct the object without parameters.
        self.assertRaises( RuntimeError, WavePropagator,
                                    parameters=None,
                                    input_path=self.input_h5,
                                    output_path='wpg_out_0000001.h5')


    def testReadH5ExceptionInput(self):
        """ Test exception raises if input is not a valid h5 file. """
        # Define a beamline.
        beamline = setupSPBDay1Beamline()

        # Construct the object.
        propagator = WavePropagator(parameters=beamline,
                                         input_path='/tmp',
                                         output_path='wpg_out_0000001.h5')

        # Check exception raises when attempting to read.
        self.assertRaises( IOError, propagator._readH5 )


    def testReadCalculateWrite(self):
        """ Test a backengine run with a single input file. """
        # Define a beamline.
        beamline = setupSPBDay1Beamline()

        # Construct the object.
        propagator = WavePropagator( parameters=beamline, input_path=self.input_h5, output_path='wpg_out.h5' )

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



if __name__ == '__main__':
    unittest.main()

