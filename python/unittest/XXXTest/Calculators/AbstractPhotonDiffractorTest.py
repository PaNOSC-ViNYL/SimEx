""" Test module for the AbstractPhotonDiffractor module.

    @author : CFG
    @institution : XFEL
    @creation 20151006

"""
import paths
import unittest


# Import the class to test.
from XXX.Calculators.AbstractPhotonDiffractor import AbstractPhotonDiffractor
from XXX.Calculators.AbstractBaseCalculator import AbstractBaseCalculator


class AbstractPhotonDiffractorTest(unittest.TestCase):
    """
    Test class for the AbstractPhotonDiffractor.
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

        self.assertRaises(TypeError, AbstractPhotonDiffractor )

    def notestThis(self):
        aps = AbstractPhotonDiffractor()

        self.assertIsInstance(aps, AbstractPhotonDiffractor)

    def testConstructionDerived(self):
        """ Test that we can construct a derived class and it has the correct inheritance. """

        class TestPhotonDiffractor(AbstractPhotonDiffractor):

            def __init__(self):
                pass

        test_source = TestPhotonDiffractor()

        self.assertIsInstance( test_source, TestPhotonDiffractor )
        self.assertIsInstance( test_source, object )
        self.assertIsInstance( test_source, AbstractBaseCalculator )
        self.assertIsInstance( test_source, AbstractPhotonDiffractor )





if __name__ == '__main__':
    unittest.main()

