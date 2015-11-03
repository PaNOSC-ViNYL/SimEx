""" Test module for the AbstractPhotonPropagator module.

    @author : CFG
    @institution : XFEL
    @creation 20151006

"""
import paths
import unittest


# Import the class to test.
from XXX.Calculators.AbstractPhotonPropagator import AbstractPhotonPropagator
from XXX.Calculators.AbstractBaseCalculator import AbstractBaseCalculator


class AbstractPhotonPropagatorTest(unittest.TestCase):
    """
    Test class for the AbstractPhotonPropagator.
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

        self.assertRaises(TypeError, AbstractPhotonPropagator )

    def notestThis(self):
        aps = AbstractPhotonPropagator()

        self.assertIsInstance(aps, AbstractPhotonPropagator)

    def testConstructionDerived(self):
        """ Test that we can construct a derived class and it has the correct inheritance. """

        class TestPhotonPropagator(AbstractPhotonPropagator):

            def __init__(self):
                pass

        test_source = TestPhotonPropagator()

        self.assertIsInstance( test_source, TestPhotonPropagator )
        self.assertIsInstance( test_source, object )
        self.assertIsInstance( test_source, AbstractBaseCalculator )
        self.assertIsInstance( test_source, AbstractPhotonPropagator )





if __name__ == '__main__':
    unittest.main()

