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

""" Test module for the EMCOrientationParameter class.

    @author : CFG
    @institution : XFEL
    @creation 20160721

"""
import paths
import os
import shutil
import unittest

from SimEx.Parameters.AbstractCalculatorParameters import AbstractCalculatorParameters
from SimEx.Parameters.EMCOrientationParameters import EMCOrientationParameters


class EMCOrientationParametersTest(unittest.TestCase):
    """
    Test class for the EMCOrientationParameters class.
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
        parameters = EMCOrientationParameters()

        # Check instance and inheritance.
        self.assertIsInstance( parameters, EMCOrientationParameters )
        self.assertIsInstance( parameters, AbstractCalculatorParameters )

        # Check all parameters are set to default values.
        self.assertTrue( parameters.beamstop )
        self.assertTrue( parameters.detailed_output )
        self.assertEqual( parameters.initial_number_of_quaternions, 1 )
        self.assertEqual( parameters.max_number_of_quaternions, 2)
        self.assertEqual( parameters.min_error, 1.e-5 )
        self.assertEqual( parameters.max_number_of_iterations, 100 )

    def testLegacyDictionary(self):
        """ Check parameter object can be initialized via a old-style dictionary. """
        parameter_dict = {'initial_number_of_quaternions' : 1,
                          'max_number_of_quaternions'     : 9,
                          'max_number_of_iterations'      : 200,
                          'min_error'                     : 1.0e-8,
                          'beamstop'                      : False,
                          'detailed_output'               : False        }


        parameters = EMCOrientationParameters(parameters_dictionary=parameter_dict)

        # Check all parameters are set to default values.
        self.assertFalse( parameters.beamstop )
        self.assertFalse( parameters.detailed_output )
        self.assertEqual( parameters.initial_number_of_quaternions, 1 )
        self.assertEqual( parameters.max_number_of_quaternions, 9)
        self.assertEqual( parameters.min_error, 1.e-8 )
        self.assertEqual( parameters.max_number_of_iterations, 200 )

    def notestNumberOfQuaternionsConsistency(self):
        """ Check that number of quaternions are checked for consistency. """
        ### FIXME.
        ## Setup default parameters.
        #parameters = EMCOrientationParameters()

        ## Check increasing initial_quaternions raises if > max_quaternions.
        #self.assertRaises( RuntimeError, lambda x:parameters.initial_number_of_quaternions = 3 )

        ## Check decreasing max_quaternions raises if < initial_quaternions.
        #self.assertRaises( RuntimeError, lambda x:parameters.max_number_of_quaternions = 1 )


if __name__ == '__main__':
    unittest.main()

