""" Test module for the SingFELPhotonDiffractor.

    @author : CFG
    @institution : XFEL
    @creation 20151109

"""
import os, shutil
import subprocess

import paths
import unittest


# Import the class to test.
from SimEx.Calculators.S2EReconstruction import S2EReconstruction
from TestUtilities import TestUtilities

class S2EReconstructionTest(unittest.TestCase):
    """
    Test class for the S2EReconstruction class.
    """

    @classmethod
    def setUpClass(cls):
        """ Setting up the test class. """
        cls.input_h5 = TestUtilities.generateTestFilePath('diffr_out_0000001.h5')

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
                shutil.rmtree(d)

    def testConstruction(self):
        """ Testing the default construction of the class. """

        self.__files_to_remove.append('orient_out.h5')
        self.__files_to_remove.append('recon_out.h5')
        # Construct the object.
        analyzer = S2EReconstruction(parameters=None, input_path=self.input_h5, output_path='recon_out.h5')

        self.assertIsInstance(analyzer, S2EReconstruction)

    def testBackengine(self):
        """ Test that we can start a test calculation. """

        self.__files_to_remove.append('orient_out.h5')
        self.__files_to_remove.append('recon_out.h5')

        dm_parameters = {'number_of_trials'        : 5,
                         'number_of_iterations'    : 2,
                         'averaging_start'         : 15,
                         'leash'                   : 0.2,
                         'number_of_shrink_cycles' : 2,
                         }


        # Construct the object.
        analyzer = S2EReconstruction(parameters={'EMC_Parameters' : None, 'DM_Parameters' : dm_parameters}, input_path=self.input_h5, output_path='recon_out.h5')

        # Call backengine.
        status = analyzer.backengine()

        self.assertEqual(status, 0)


if __name__ == '__main__':
    unittest.main()

