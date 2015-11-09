""" Test module for the AbstractBaseCalculator module.

    @author : CFG
    @institution : XFEL
    @creation 20151006

"""
import paths
import unittest
import exceptions
import os


# Import the class to test.
from SimEx.Calculators.AbstractBaseCalculator import AbstractBaseCalculator
from SimEx.Calculators.AbstractBaseCalculator import checkAndSetIO

# Derive a class from the abc.
class DerivedCalculator(AbstractBaseCalculator):
    def __init__(self, parameters=None, input_path=None, output_path=None):
        super(DerivedCalculator, self).__init__(parameters, input_path, output_path)
    def backengine(self):
        pass
    def _readH5(self):
        pass
    def saveH5(self):
        pass
    def providedData(self):
        return ['/params/params1', '/params/params2', '/data/dat1', '/data/dat2']
    def expectedData(self):
        return ['/data/dat1', '/data/dat2']


class AbstractBaseCalculatorTest(unittest.TestCase):
    """
    Test class for the AbstractBaseCalculator.
    """

    @classmethod
    def setUpClass(cls):
        """ Setting up the test class. """

    @classmethod
    def tearDownClass(cls):
        """ Tearing down the test class. """

    def setUp(self):
        """ Setting up a test. """
        self.__files_to_be_removed = []

        self.test_class_instance = DerivedCalculator(parameters={1 : '1'}, input_path=__file__, output_path='test.h5')

    def tearDown(self):
        """ Tearing down a test. """
        for f in self.__files_to_be_removed:
            if os.path.isfile(f): os.remove(f)

        del self.test_class_instance


    def testConstruction(self):
        """ Testing the default construction of the class. """
        self.assertRaises(TypeError, AbstractBaseCalculator )

    # Check its type.
    def testQueries(self):

        abc = self.test_class_instance
        # Check it has the required members.
        self.assertTrue( hasattr(abc, 'parameters') )
        self.assertTrue( hasattr(abc, 'input_path') )
        self.assertTrue( hasattr(abc, 'output_path') )


    def testCheckAndSetIO(self):
        """ Check that setting data io paths works correctly. """
        inp = 'test.in'
        out = 'test.out'
        # Ensure proper cleanup.
        self.__files_to_be_removed += [inp, out]


        # Setup the tuple.
        io = (inp, out)

        # Create a dummy input file.
        inp_handle = open(inp, 'w')
        inp_handle.write('xxx')
        inp_handle.close()

        # Call checker
        io_ret = checkAndSetIO(io)

        self.assertEqual(io_ret[0], os.path.abspath(inp) )
        self.assertEqual(io_ret[1], os.path.abspath(out) )

        # Check exception on wrong types.
        io = (1,2)
        self.assertRaises(exceptions.TypeError, checkAndSetIO, io )

        # Check exception on wrong second type.
        io = ('test.in', 2)
        self.assertRaises(exceptions.TypeError, checkAndSetIO, io )

        # Check exception on wrong second type.
        io = ('test.in', None)
        self.assertRaises(exceptions.TypeError, checkAndSetIO, io )

    def testProvidedData(self):
        """ Check the provided data query. """

        instance = self.test_class_instance
        provided_data = instance.providedData()
        expected_data = instance.expectedData()

        for ed in expected_data:
            self.assertTrue ( ed in provided_data)




if __name__ == '__main__':
    unittest.main()

