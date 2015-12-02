""" Test module for the DM Phasing module.

    @author : CFG
    @institution : XFEL
    @creation 20151202

"""
import os

import paths
import unittest


# Import the class to test.
from SimEx.Calculators.DMPhasing import DMPhasing
from TestUtilities import TestUtilities

class DMPhasingTest(unittest.TestCase):
    """
    Test class for the DM Phasing class.
    """

    @classmethod
    def setUpClass(cls):
        """ Setting up the test class. """
        cls.input_h5 = TestUtilities.generateTestFilePath('orient_out_0000001.h5')

    @classmethod
    def tearDownClass(cls):
        """ Tearing down the test class. """
        del cls.input_h5

    def setUp(self):
        """ Setting up a test. """
        self.__files_to_remove = []
        self.__dirs_to_remove = []

    def tearDown(self):
        """ Tearing down a test. """
        for f in self.__files_to_remove:
            if os.path.isfile(f):
                os.remove(f)
        for d in self.__dirs_to_remove:
            if os.path.isdir(d):
                os.rmdir(d)

    def testConstruction(self):
        """ Testing the default construction of the class. """

        # Construct the object.
        analyzer = DMPhasing(parameters=None, input_path=self.input_h5, output_path='phasing_out.h5')

        self.assertIsInstance(analyzer, DMPhasing)

    def testBackengine(self):
        """ Test that we can start a test calculation. """

        self.__files_to_remove.append('phasing_out.h5')

        # Construct the object.
        analyzer = DMPhasing(parameters=None, input_path=self.input_h5, output_path='phasing_out.h5')

        # Call backengine.
        status = analyzer.backengine()

        self.assertEqual(status, 0)


if __name__ == '__main__':
    unittest.main()

