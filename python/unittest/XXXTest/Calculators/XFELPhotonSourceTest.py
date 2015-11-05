""" Test module for the XFELPhotonSource.

    @author : CFG
    @institution : XFEL
    @creation 20151104

"""
import paths
import unittest

import numpy
import h5py

# Import the class to test.
from XXX.Calculators.XFELPhotonSource import XFELPhotonSource
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

    def testReadSave(self):
        """ Check that we can read the h5 input and get all relevant parameters for
        initializing the object. """

        # Construct an object with some input.
        xfel = XFELPhotonSource(parameters=None, input_path=self.input_h5, output_path='FELsource_out2.h5')

        xfel._readH5()
        # Get the parameters.
        photon_energy = xfel.parameters['photon_energy']

        # Check photon energy.
        self.assertAlmostEqual(photon_energy, 4960.0, 1)  # 5 keV

        # Get the data.
        data = xfel._XFELPhotonSource__data

        # Assert we have horizontal and vertical polarizations.
        self.assertEqual(data.shape[0], 2)


        xfel.saveH5()
if __name__ == '__main__':
    unittest.main()

