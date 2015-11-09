""" Test module for the entity checks.
    @author CFG
    @institution XFEL
    @creation 20151006
"""
import paths
import exceptions
import unittest

from SimEx.Utilities.EntityChecks import checkAndSetInstance

class EntityChecksTest(unittest.TestCase):
    """ Test class for the EntityChecks class. """

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

    def testCheckAndSetInstanceNoDefault(self):
        """ Test the check and set utility raises if no default nor var is given. """

        # No default given.
        self.assertRaises(exceptions.TypeError, checkAndSetInstance, int)

    def testCheckAndSetInstanceWrongType(self):
        """ Test the check and set utility raises if var is wrong type."""

        # Wrong type.
        self.assertRaises(exceptions.TypeError, checkAndSetInstance, int, 1.01, 1)

    def testCheckAndSetInstanceDerived(self):
        """ Test the check and set utility works correctly also for abstract data and derived types. """

        # Check works for a derived type.
        class my_baseclass(object):
            def __init__(self, var1, var2):
                self.__var1 = var1
                self.__var2 = var2
        class my_derived_class(my_baseclass):
            def __init__(self, var1, var2, var3):
                super(my_derived_class, self).__init__(1.0, 2.0)
                self.__var3 = var3

        mc_base = my_baseclass(1.0, 2.0)
        mc_derived = my_derived_class(1.0, 2.0, 3.0)

        check_ok = True
        try:
            checked_base_class = checkAndSetInstance(my_baseclass, mc_base)
            checked_derived_class = checkAndSetInstance(my_derived_class, mc_derived)
            checked_derived_class2 = checkAndSetInstance(my_baseclass, mc_derived)
        except:
            check_ok = False

        self.assertTrue(check_ok)

    def testCheckAndSetInstanceDefault(self):
        """ Check that setting the default works correctly. """

        # Setup default, and class.
        default = 1.0
        tp = int

        # Check raises because default not of correct type.
        self.assertRaises(exceptions.TypeError, checkAndSetInstance, tp, None, default)

        default = 1
        # Use the utility to set the variable to the default.
        var = checkAndSetInstance(tp, None, default)

        self.assertEqual(var, default)


if __name__ == '__main__':
    unittest.main()
