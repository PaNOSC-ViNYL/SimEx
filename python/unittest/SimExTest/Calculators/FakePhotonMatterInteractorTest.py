""" Test module for the FakePhotonMatterInteractor.

    @author : CFG
    @institution : XFEL
    @creation 20151111

"""
import paths
import os
import shutil
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
        self.__files_to_remove = []
        self.__paths_to_remove = []

    def tearDown(self):
        """ Tearing down a test. """
        # Clean up.
        for f in self.__files_to_remove:
            if os.path.isfile(f):
                os.remove(f)
        for p in self.__paths_to_remove:
            if os.path.isdir(p):
                shutil.rmtree(p)

    def testConstruction(self):
        """ Testing the default construction of the class. """

        # Construct the object.
        diffractor = FakePhotonMatterInteractor(parameters=None, input_path=self.input_h5, output_path='pmi')

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

    def testBackengine(self):
        """ Check that the backengine method works correctly. """

        # Get test instance.
        pmi_parameters = {'number_of_trajectories' : 10}
        test_interactor = FakePhotonMatterInteractor(parameters=pmi_parameters, input_path=self.input_h5, output_path='pmi')

        # Call backengine
        status = test_interactor.backengine()

        # Check that the backengine returned zero.
        self.assertEqual(status, 0)

        # Check that output was written to the given directory.
        self.assertTrue( os.path.isdir( test_interactor.output_path ) )
        self.assertEqual( len( os.listdir( test_interactor.output_path ) ), test_interactor.parameters['number_of_trajectories'] )

        # Call backengine again, so see that it works if directory already exists.
        status = test_interactor.backengine()

        # Check that the backengine returned zero.
        self.assertEqual(status, 0)

        # Test that exception raises if output_path is a file that already exists.
        shutil.copyfile( os.path.join( test_interactor.output_path, 'pmi_out_0000001.h5' ), 'pmi_out_0000001.h5' )
        shutil.rmtree(test_interactor.output_path)

        fake = FakePhotonMatterInteractor( parameters=pmi_parameters, input_path=self.input_h5, output_path='pmi_out_0000001.h5')
        self.assertRaises( IOError, fake.backengine )

        # Clean up.
        self.__paths_to_remove.append('pmi')
        self.__files_to_remove.append('pmi_out_0000001.h5')


if __name__ == '__main__':
    unittest.main()

