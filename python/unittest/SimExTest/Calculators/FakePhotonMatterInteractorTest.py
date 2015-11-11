""" Test module for the FakePhotonMatterInteractor.

    @author : CFG
    @institution : XFEL
    @creation 20151111

"""
import paths
import unittest


# Import the class to test.
from SimEx.Calculators.FakePhotonMatterInteractor import FakePhotonMatterInteractor
from TestUtilities import TestUtilities

class FakePhotonMatterInteractorTest(unittest.TestCase):
    """
    Test class for the FakePhotonMatterInteractor class.
    """

    @classmethod
    def setUpClass(cls):
        """ Setting up the test class. """
        cls.input_h5 = TestUtilities.generateTestFilePath('prop_out.h5')

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
        diffractor = FakePhotonMatterInteractor(parameters=None, input_path=self.input_h5, output_path='pmi_out.h5')

        self.assertIsInstance(diffractor, FakePhotonMatterInteractor)

    def testDataInterfaceQueries(self):
        """ Check that the data interface queries work. """

        # Get test instance.
        test_interactor = FakePhotonMatterInteractor(parameters=None, input_path=self.input_h5, output_path='pmi_out.h5')

        # Get expected and provided data descriptors.
        expected_data = test_interactor.expectedData()
        provided_data = test_interactor.providedData()

        # Check types are correct.
        self.assertIsInstance(expected_data, list)
        self.assertIsInstance(provided_data, list)
        for d in expected_data:
            self.assertIsInstance(d, str)
            self.assertEqual(d[0], '/')
        for d in provided_data:
            self.assertIsInstance(d, str)
            self.assertEqual(d[0], '/')


if __name__ == '__main__':
    unittest.main()

