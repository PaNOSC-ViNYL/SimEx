##########################################################################
#                                                                        #
# Copyright (C) 2016 Carsten Fortmann-Grote                              #
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

""" Test module for the WavePropagatorParameters class.

    @author : CFG
    @institution : XFEL
    @creation 20161003 (Germany's national holiday, but I'm in Trieste, Italy for the SOS workshop.)

"""
import paths
import os
import shutil
import wpg
from wpg.beamline import Beamline

# Include needed directories in sys.path.
import unittest

from TestUtilities import TestUtilities
from SimEx.Parameters.AbstractCalculatorParameters import AbstractCalculatorParameters
from SimEx.Parameters.WavePropagatorParameters import WavePropagatorParameters
from SimEx.Utilities.WPGBeamlines import setup_S2E_SPI_beamline


class WavePropagatorParametersTest(unittest.TestCase):
    """
    Test class for the WavePropagatorParameters class.
    """

    @classmethod
    def setUpClass(cls):
        pass


    @classmethod
    def tearDownClass(cls):
        """ Tearing down the test class. """
        pass


    def setUp(self):
        """ Setting up a test. """
        self.__files_to_remove = []
        self.__dirs_to_remove = []

        self.__beamline = setup_S2E_SPI_beamline()


    def tearDown(self):
        """ Tearing down a test. """
        for f in self.__files_to_remove:
            if os.path.isfile(f):
                os.remove(f)
        for d in self.__dirs_to_remove:
            if os.path.isdir(d):
                shutil.rmtree(d)

        del self.__beamline


    def testDefaultConstruction(self):
        """ Testing the default construction."""

        # Attempt to construct an instance of the class.
        parameters = WavePropagatorParameters()

        # Check instance and inheritance.
        self.assertIsInstance( parameters, WavePropagatorParameters )
        self.assertIsInstance( parameters, AbstractCalculatorParameters )

        # Check all parameters are set to default values.
        self.assertFalse( parameters.use_opmd )
        self.assertIsInstance( parameters.beamline, Beamline )


    def testShapedConstruction(self):
        """ Testing the construction of the class with non-default parameters. """

        # Attempt to construct an instance of the class.
        parameters = WavePropagatorParameters(use_opmd=True, beamline=setup_S2E_SPI_beamline())

        # Check instance and inheritance.
        self.assertIsInstance( parameters, WavePropagatorParameters )
        self.assertIsInstance( parameters, AbstractCalculatorParameters )

        # Check all parameters are set to default values.
        self.assertTrue( parameters.use_opmd )
        self.assertIsInstance( parameters.beamline, Beamline )

if __name__ == '__main__':
    unittest.main()

