""" Test module for the AbstractPhotonDetector module.

    @author : CFG
    @institution : XFEL
    @creation 20151006

"""
import paths
import unittest


# Import the class to test.
from XXX.Calculators.AbstractPhotonDetector import AbstractPhotonDetector
from XXX.Calculators.AbstractBaseCalculator import AbstractBaseCalculator

from TestUtilities import TestUtilities


class AbstractPhotonDetectorTest(unittest.TestCase):
    """
    Test class for the AbstractPhotonDetector.
    """

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
        """ Testing the default construction of the class. """

        self.assertRaises(TypeError, AbstractPhotonDetector )

    def notestThis(self):
        aps = AbstractPhotonDetector()

        self.assertIsInstance(aps, AbstractPhotonDetector)

    def testConstructionDerived(self):
        """ Test that we can construct a derived class and it has the correct inheritance. """

        class TestPhotonDetector(AbstractPhotonDetector):

            def __init__(self):
                input_path = TestUtilities.generateTestFilePath('FELsource_out.h5')
                super(TestPhotonDetector, self).__init__(parameters=None, input_path=input_path, output_path='test_out.h5')

            def backengine(self):
                pass

        test_source = TestPhotonDetector()

        self.assertIsInstance( test_source, TestPhotonDetector )
        self.assertIsInstance( test_source, object )
        self.assertIsInstance( test_source, AbstractBaseCalculator )
        self.assertIsInstance( test_source, AbstractPhotonDetector )



if __name__ == '__main__':
    unittest.main()

