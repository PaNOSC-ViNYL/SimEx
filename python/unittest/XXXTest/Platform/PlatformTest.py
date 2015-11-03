""" Test module for module Platform from XXX
    @author : CFG
    @creation : 20151005
"""

import unittest
import paths

from XXX.Platform.Platform import Platform


class PlatformTest( unittest.TestCase):
    """ Test class for the Platform class. """

    @classmethod
    def setUpClass(cls):
        """ Setting up the test class. """

    @classmethod
    def tearDownClass(cls):
        """ Tearing down the test class. """

    def setUp(self):
        """ Setting up a test. """

    def tearDown(self):
        """ Tearing down a test. """

    def testConstruction(self):
        """ Testing something stupid."""
        experiment_simulation_platform = Platform()

        self.assertIsInstance( experiment_simulation_platform, Platform )

if __name__ == '__main__':
    unittest.main()
