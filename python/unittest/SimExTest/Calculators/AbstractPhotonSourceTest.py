""" Test module for the AbstractPhotonSource module.

    @author : CFG
    @institution : XFEL
    @creation 20151006

"""
import os

import paths
import unittest


# Import the class to test.
from SimEx.Calculators.AbstractPhotonSource import AbstractPhotonSource
from SimEx.Calculators.AbstractBaseCalculator import AbstractBaseCalculator

from TestUtilities import TestUtilities

class TestPhotonSource(AbstractPhotonSource):

    def __init__(self):
        input_path = TestUtilities.generateTestFilePath('FELsource_out.h5')
        super(TestPhotonSource, self).__init__(parameters=None, input_path=input_path, output_path='test_out.h5')

    def backengine(self):
        pass

    def _readH5(self): pass
    def saveH5(self): pass



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
        self.test_class = TestPhotonSource()

    def tearDown(self):
        """ Tearing down a test. """
        del self.test_class

    def testConstruction(self):
        """ Testing the default construction of the class. """

        self.assertRaises(TypeError, AbstractPhotonSource )

    def testConstructionDerived(self):
        """ Test that we can construct a derived class and it has the correct inheritance. """
        test_source = self.test_class

        self.assertIsInstance( test_source, TestPhotonSource )
        self.assertIsInstance( test_source, object )
        self.assertIsInstance( test_source, AbstractBaseCalculator )
        self.assertIsInstance( test_source, AbstractPhotonSource )

    def testDataInterfaceQueries(self):
        """ Check that the data interface queries work. """

        # Get test instance.
        test_source = self.test_class

        # Get expected and provided data descriptors.
        expected_data = test_source.expectedData()
        provided_data = test_source.providedData()

        # Check types are correct.
        self.assertIsInstance(expected_data, list)
        self.assertIsInstance(provided_data, list)
        for d in expected_data:
            self.assertIsInstance(d, str)
            self.assertEqual(d[0], '/')
        for d in provided_data:
            self.assertIsInstance(d, str)
            self.assertEqual(d[0], '/')

    def testDefaultPaths(self):
        """ Check that default pathnames are chosen correctly. """

        # Attempt to setup without input path.
        class Source(AbstractPhotonSource):
            def __init__(self):
                super (Source, self).__init__(parameters=None, input_path=None, output_path=None)
            def backengine(self):
                pass
            def _readH5(self):
                pass
            def saveH5(self):
                pass

        self.assertRaises( IOError, Source )

        class Source2(AbstractPhotonSource):
            def __init__(self):
                super (Source2, self).__init__(parameters=None,
                                              input_path = TestUtilities.generateTestFilePath('FELsource_out.h5'),
                                              output_path = None)
            def backengine(self):
                pass
            def _readH5(self):
                pass
            def saveH5(self):
                pass


        # Construct with no output path given.
        source = Source2()

        self.assertEqual(source.output_path, os.path.abspath('source_out.h5'))


if __name__ == '__main__':
    unittest.main()

