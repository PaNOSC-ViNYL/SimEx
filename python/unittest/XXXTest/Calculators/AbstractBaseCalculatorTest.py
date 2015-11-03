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
from XXX.Calculators.AbstractBaseCalculator import AbstractBaseCalculator
from XXX.Calculators.AbstractBaseCalculator import checkAndSetIO


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

    def tearDown(self):
        """ Tearing down a test. """
        for f in self.__files_to_be_removed:
            if os.path.isfile(f): os.remove(f)

    def testConstruction(self):
        """ Testing the default construction of the class. """
        self.assertRaises(TypeError, AbstractBaseCalculator )

    # Check its type.
    def notestThis(self):
        self.assertIsInstance(abc, AbstractBaseCalculator)

        # Check it has the required members.
        self.assertTrue( hasattr(abc, 'control_parameters') )
        self.assertTrue( hasattr(abc, 'io') )
        self.assertTrue( hasattr(abc, 'backengine') )
        self.assertTrue( hasattr(abc, 'io_data_handles') )

        abc = AbstractBaseCalculator()
        self.assertRaises( exceptions.RuntimeError, abc.backengine )

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

        # Check exception on wrong input.
        io = ('nonexisting_file.dat', 'output.dat')
        self.assertRaises(exceptions.RuntimeError, checkAndSetIO, io )

        # Check exception on wrong types.
        io = (1,2)
        self.assertRaises(exceptions.TypeError, checkAndSetIO, io )

        # Check exception on wrong second type.
        io = ('test.in', 2)
        self.assertRaises(exceptions.TypeError, checkAndSetIO, io )

        # Check exception on wrong second type.
        io = ('test.in', None)
        self.assertRaises(exceptions.TypeError, checkAndSetIO, io )



if __name__ == '__main__':
    unittest.main()

