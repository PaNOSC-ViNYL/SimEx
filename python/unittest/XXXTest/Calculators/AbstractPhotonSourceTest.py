""" Test module for the AbstractPhotonSource module.

    @author : CFG
    @institution : XFEL
    @creation 20151006

"""
import paths
import unittest


# Import the class to test.
from XXX.Calculators.AbstractPhotonSource import AbstractPhotonSource
from XXX.Calculators.AbstractBaseCalculator import AbstractBaseCalculator

from TestUtilities import TestUtilities


class AbstractPhotonSourceTest(unittest.TestCase):
    """
    Test class for the AbstractPhotonSource.
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

        self.assertRaises(TypeError, AbstractPhotonSource )

    def notestThis(self):
        aps = AbstractPhotonSource()

        self.assertIsInstance(aps, AbstractPhotonSource)

    def testConstructionDerived(self):
        """ Test that we can construct a derived class and it has the correct inheritance. """

        class TestPhotonSource(AbstractPhotonSource):

            def __init__(self):
                input_path = TestUtilities.generateTestFilePath('FELsource_out.h5')
                super(TestPhotonSource, self).__init__(parameters=None, input_path=input_path, output_path='test_out.h5')

            def backengine(self):
                pass

        test_source = TestPhotonSource()

        self.assertIsInstance( test_source, TestPhotonSource )
        self.assertIsInstance( test_source, object )
        self.assertIsInstance( test_source, AbstractBaseCalculator )
        self.assertIsInstance( test_source, AbstractPhotonSource )



if __name__ == '__main__':
    unittest.main()

