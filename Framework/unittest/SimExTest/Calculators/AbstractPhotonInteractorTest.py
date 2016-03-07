##########################################################################
#                                                                        #
# Copyright (C) 2015 Carsten Fortmann-Grote                              #
# Contact: Carsten Fortmann-Grote <carsten.grote@xfel.eu>                #
#                                                                        #
# This file is part of simex_platform.                                   #
# simex_platform is free software: you can redistribute it and/or modify #
# it under the terms of the GNU General Public License as published by   #
# the Free Software Foundation, either version 3 of the License, or      #
# (at your option) any later version.                                    #
#                                                                        #
# simex_platform is distributed in the hope that it will be useful,      #
# but WITHOUT ANY WARRANTY; without even the implied warranty of         #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          #
# GNU General Public License for more details.                           #
#                                                                        #
# You should have received a copy of the GNU General Public License      #
# along with this program.  If not, see <http://www.gnu.org/licenses/>.  #
# Include needed directories in sys.path.                                #
#                                                                        #
##########################################################################

""" Test module for the AbstractPhotonInteractor module.

    @author : CFG
    @institution : XFEL
    @creation 20151006

"""
import paths
import unittest


# Import the class to test.
from SimEx.Calculators.AbstractPhotonInteractor import AbstractPhotonInteractor
from SimEx.Calculators.AbstractBaseCalculator import AbstractBaseCalculator

from TestUtilities import TestUtilities


class AbstractPhotonInteractorTest(unittest.TestCase):
    """
    Test class for the AbstractPhotonInteractor.
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

        self.assertRaises(TypeError, AbstractPhotonInteractor )

    def notestThis(self):
        aps = AbstractPhotonInteractor()

        self.assertIsInstance(aps, AbstractPhotonInteractor)

    def testConstructionDerived(self):
        """ Test that we can construct a derived class and it has the correct inheritance. """

        class TestPhotonInteractor(AbstractPhotonInteractor):

            def __init__(self):
                input_path = TestUtilities.generateTestFilePath('FELsource_out.h5')
                super(TestPhotonInteractor, self).__init__(parameters=None, input_path=input_path, output_path='test_out.h5')

            def backengine(self):
                pass

            def _readH5(self): pass
            def saveH5(self): pass
            def expectedData(self): pass
            def providedData(self): pass

        test_source = TestPhotonInteractor()

        self.assertIsInstance( test_source, TestPhotonInteractor )
        self.assertIsInstance( test_source, object )
        self.assertIsInstance( test_source, AbstractBaseCalculator )
        self.assertIsInstance( test_source, AbstractPhotonInteractor )



if __name__ == '__main__':
    unittest.main()

