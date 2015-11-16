""" Test module for the SingFELPhotonDiffractor.

    @author : CFG
    @institution : XFEL
    @creation 20151109

"""
import paths
import unittest


# Import the class to test.
from SimEx.Calculators.SingFELPhotonDiffractor import SingFELPhotonDiffractor
from TestUtilities import TestUtilities

class SingFELPhotonDiffractorTest(unittest.TestCase):
    """
    Test class for the SingFELPhotonDiffractor class.
    """

    @classmethod
    def setUpClass(cls):
        """ Setting up the test class. """
        cls.input_h5 = TestUtilities.generateTestFilePath('pmi_out_0000001.h5')

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
        diffractor = SingFELPhotonDiffractor(parameters=None, input_path=self.input_h5, output_path='diffr_out.h5')

        self.assertIsInstance(diffractor, SingFELPhotonDiffractor)

    def testBackengine(self):
        """ Test that we can start a test calculation. """

        # Construct the object.
        diffractor = SingFELPhotonDiffractor(parameters=None, input_path=self.input_h5, output_path='diffr_out.h5')

        # Call backengine.
        diffractor.backengine()

if __name__ == '__main__':
    unittest.main()

