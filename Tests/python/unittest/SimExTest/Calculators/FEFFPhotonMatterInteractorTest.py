##########################################################################
#                                                                        #
# Copyright (C) 2015, 2016 Carsten Fortmann-Grote                        #
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
#                                                                        #
##########################################################################

""" Test module for the FEFFPhotonMatterInteractor.

    @author : CFG
    @institution : XFEL
    @creation 20151215

"""
import h5py
import os
import paths
import shutil
import unittest

# Import the class to test.
from SimEx.Calculators.FEFFPhotonMatterInteractor import FEFFPhotonMatterInteractor
from SimEx.Calculators.AbstractPhotonInteractor import AbstractPhotonInteractor

from TestUtilities import TestUtilities

class FEFFPhotonMatterInteractorTest(unittest.TestCase):
    """
    Test class for the FEFFPhotonMatterInteractor class.
    """

    @classmethod
    def setUpClass(cls):
        """ Setting up the test class. """

    @classmethod
    def tearDownClass(cls):
        """ Tearing down the test class. """

    def setUp(self):
        """ Setting up a test. """
        self.__files_to_remove = []
        self.__dirs_to_remove = []

    def tearDown(self):
        """ Tearing down a test. """
        # Clean up.
        for f in self.__files_to_remove:
            if os.path.isfile(f):
                os.remove(f)
        for p in self.__dirs_to_remove:
            if os.path.isdir(p):
                shutil.rmtree(p)

    def testShapedConstruction(self):
        """ Testing the construction of the class with parameters. """
        self.assertTrue( False )

    def testDefaultConstruction(self):
        """ Testing the default construction of the class. """

        feff = FEFFPhotonMatterInteractor()

        self.assertIsInstance( feff, AbstractPhotonInteractor )

if __name__ == '__main__':
    unittest.main()

