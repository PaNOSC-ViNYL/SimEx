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

""" Test module for the DMPhasingParameters class.

    @author : CFG
    @institution : XFEL
    @creation 20160722

"""
import paths
import os
import shutil

# Include needed directories in sys.path.
import unittest

from SimEx.Parameters.AbstractCalculatorParameters import AbstractCalculatorParameters
from SimEx.Parameters.DMPhasingParameters import DMPhasingParameters


class DMPhasingParametersTest(unittest.TestCase):
    """
    Test class for the DMPhasingParameters class.
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

    def tearDown(self):
        """ Tearing down a test. """
        for f in self.__files_to_remove:
            if os.path.isfile(f):
                os.remove(f)
        for d in self.__dirs_to_remove:
            if os.path.isdir(d):
                shutil.rmtree(d)

    def testDefaultConstruction(self):
        """ Testing the default construction of the class using a dictionary. """

        # Attempt to construct an instance of the class.
        parameters = DMPhasingParameters()

        # Check instance and inheritance.
        self.assertIsInstance( parameters, DMPhasingParameters )
        self.assertIsInstance( parameters, AbstractCalculatorParameters )

        # Check all parameters are set to default values.
        self.assertEqual( parameters.number_of_trials, 500 )
        self.assertEqual( parameters.number_of_iterations, 50 )
        self.assertEqual( parameters.averaging_start, 15 )
        self.assertEqual( parameters.leash, 0.2)
        self.assertEqual( parameters.number_of_shrink_cycles, 10 )

    def testLegacyDictionary(self):
        """ Check parameter object can be initialized via a old-style dictionary. """
        parameter_dict = {'number_of_trials' : 1,
                          'number_of_iterations'     : 9,
                          'averaging_start'      : 200,
                          'leash'                     : 1.0e-8,
                          'number_of_shrink_cycles' : 10}

        parameters = DMPhasingParameters(parameters_dictionary=parameter_dict)

        # Check all parameters are set correctly.
        self.assertEqual( parameters.number_of_trials, 1 )
        self.assertEqual( parameters.number_of_iterations, 9 )
        self.assertEqual( parameters.averaging_start, 200 )
        self.assertEqual( parameters.leash, 1.0e-8)
        self.assertEqual( parameters.number_of_shrink_cycles, 10 )


if __name__ == '__main__':
    unittest.main()

