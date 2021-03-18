""" module: Hosting Test of the Units module."""

import os
import shutil
import unittest
from SimEx.Utilities.singfelSlurm import singfelSlurm, getSingfelCommand


class singfelSlurmTest(unittest.TestCase):
    """ Test class for the WPGUtilities. """
    @classmethod
    def setUpClass(cls):
        """ Setting up the test class. """

    @classmethod
    def tearDownClass(cls):
        """ Tearing down the test class. """

    def setUp(self):
        """ Setting up a test. """
        self.__files_to_remove = ['submit.slurm']
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

    # @unittest.skip("demonstrating skipping")
    def testOrientationNone(self):
        """Testing orientation command"""
        singfel_cmd = getSingfelCommand(uniform_rotation=None,
                                        back_rotation=True,
                                        number_of_diffraction_patterns=1,
                                        calculate_Compton=0,
                                        orientation=None)
        self.assertEqual(singfel_cmd.find("--orientation"), -1)

    # @unittest.skip("demonstrating skipping")
    def testOrientationIllegal(self):
        """Testing orientation command"""
        self.assertRaises(TypeError, getSingfelCommand, orientation=12)

    # @unittest.skip("demonstrating skipping")
    def testOrientationNormal(self):
        """Testing orientation command"""
        singfel_cmd = getSingfelCommand(uniform_rotation=None,
                                        back_rotation=True,
                                        number_of_diffraction_patterns=1,
                                        calculate_Compton=0,
                                        orientation=(1, 0, 0, 0))
        self.assertNotEqual(singfel_cmd.find("--orientation"), -1)

    # @unittest.skip("demonstrating skipping")
    def testSlurmConstruct(self):
        singfel_cmd = getSingfelCommand(uniform_rotation=None,
                                        back_rotation=True,
                                        number_of_diffraction_patterns=1,
                                        calculate_Compton=0,
                                        orientation=(1, 0, 0, 0))
        singfelSlurm('Test', './', singfel_cmd, nodes=2).writeScript()


if __name__ == '__main__':
    unittest.main()
