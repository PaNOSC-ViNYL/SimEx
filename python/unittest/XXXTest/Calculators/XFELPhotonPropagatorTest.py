""" Test module for the XFELPhotonPropagator.

    @author : CFG
    @institution : XFEL
    @creation 20151104

"""
import paths
import unittest

import numpy
import h5py

# Import the class to test.
from XXX.Calculators.XFELPhotonPropagator import XFELPhotonPropagator
from TestUtilities import TestUtilities

class XFELPhotonPropagatorTest(unittest.TestCase):
    """
    Test class for the XFELPhotonPropagator class.
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
        xfel_source = XFELPhotonPropagator(parameters=None, input_path=self.input_h5, output_path='prop_out.h5')


        self.assertIsInstance(xfel_source, XFELPhotonPropagator)

if __name__ == '__main__':
    unittest.main()

