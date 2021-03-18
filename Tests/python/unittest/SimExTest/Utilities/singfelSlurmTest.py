""" module: Hosting Test of the Units module."""

import os
import io
import sys
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
        self.__files_to_remove = ['submit.slurm', 'diffr.h5']
        self.__paths_to_remove = ['diffr']

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

    # @unittest.skip("demonstrating skipping")
    def testSlurmGeom(self):
        singfel_cmd = getSingfelCommand(uniform_rotation=None,
                                        back_rotation=True,
                                        number_of_diffraction_patterns=1,
                                        calculate_Compton=0,
                                        orientation=(1, 0, 0, 0),
                                        geomFile='../my.geom')
        self.assertNotEqual(singfel_cmd.find("--geomFile ../my.geom"), -1)

    # @unittest.skip("demonstrating skipping")
    def testSlurmPMISTOP(self):
        singfel_cmd = getSingfelCommand(uniform_rotation=None,
                                        back_rotation=True,
                                        number_of_diffraction_patterns=1,
                                        calculate_Compton=0,
                                        orientation=(1, 0, 0, 0),
                                        pmi_stop_ID=20)
        singfelSlurm('Test',
                     './',
                     singfel_cmd,
                     slurm_file='test.slrum',
                     nodes=2).writeScript()

    # @unittest.skip("demonstrating skipping")
    def testNotCleanup(self):
        with open('diffr.h5', 'w'):
            pass
        singfel_cmd = getSingfelCommand(uniform_rotation=None,
                                        back_rotation=True,
                                        number_of_diffraction_patterns=1,
                                        calculate_Compton=0,
                                        orientation=(1, 0, 0, 0),
                                        pmi_stop_ID=20)
        capturedOutput = io.StringIO()  # Create StringIO object
        sys.stdout = capturedOutput  #  and redirect stdout.
        singfelSlurm('Test',
                     './',
                     singfel_cmd,
                     slurm_file='test.slrum',
                     nodes=2).submit(test=True)
        sys.stdout = sys.__stdout__  # Reset redirect.
        string_out = capturedOutput.getvalue()  # Now works as before.
        self.assertNotEqual(string_out.find('diffr.h5 exists: True'), -1)
        self.assertNotEqual(string_out.find('diffr exists: False'), -1)

    # @unittest.skip("demonstrating skipping")
    def testCleanup(self):
        with open('diffr.h5', 'w'):
            pass
        os.mkdir('diffr')
        singfel_cmd = getSingfelCommand(uniform_rotation=None,
                                        back_rotation=True,
                                        number_of_diffraction_patterns=1,
                                        calculate_Compton=0,
                                        orientation=(1, 0, 0, 0),
                                        pmi_stop_ID=20)
        capturedOutput = io.StringIO()  # Create StringIO object
        sys.stdout = capturedOutput  #  and redirect stdout.
        singfelSlurm('Test',
                     './',
                     singfel_cmd,
                     slurm_file='test.slrum',
                     nodes=2,
                     is_cleanup=True).submit(test=True)
        sys.stdout = sys.__stdout__  # Reset redirect.
        string_out = capturedOutput.getvalue()  # Now works as before.
        print(string_out)
        self.assertNotEqual(string_out.find('diffr.h5 exists: True'), -1)
        self.assertNotEqual(string_out.find('diffr exists: True'), -1)
        self.assertFalse(os.path.isfile('diffr.h5'))
        self.assertFalse(os.path.isdir('diffr'))


if __name__ == '__main__':
    unittest.main()
