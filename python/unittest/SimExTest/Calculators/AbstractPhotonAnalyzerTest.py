""" Test module for the AbstractPhotonAnalyzer module.

    @author : CFG
    @institution : XFEL
    @creation 20151006

"""
import paths
import unittest


# Import the class to test.
from SimEx.Calculators.AbstractPhotonAnalyzer import AbstractPhotonAnalyzer
from SimEx.Calculators.AbstractBaseCalculator import AbstractBaseCalculator

from TestUtilities import TestUtilities


class AbstractPhotonAnalyzerTest(unittest.TestCase):
    """
    Test class for the AbstractPhotonAnalyzer.
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

        self.assertRaises(TypeError, AbstractPhotonAnalyzer )

    def notestThis(self):
        aps = AbstractPhotonAnalyzer()

        self.assertIsInstance(aps, AbstractPhotonAnalyzer)

    def testConstructionDerived(self):
        """ Test that we can construct a derived class and it has the correct inheritance. """

        class TestPhotonAnalyzer(AbstractPhotonAnalyzer):

            def __init__(self):
                input_path = TestUtilities.generateTestFilePath('FELsource_out.h5')
                super(TestPhotonAnalyzer, self).__init__(parameters=None, input_path=input_path, output_path='test_out.h5')

            def backengine(self):
                pass

        test_source = TestPhotonAnalyzer()

        self.assertIsInstance( test_source, TestPhotonAnalyzer )
        self.assertIsInstance( test_source, object )
        self.assertIsInstance( test_source, AbstractBaseCalculator )
        self.assertIsInstance( test_source, AbstractPhotonAnalyzer )



if __name__ == '__main__':
    unittest.main()

