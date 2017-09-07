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

""" Test module for the SingFELPhotonDiffractorParameter class.

    @author : CFG
    @institution : XFEL
    @creation 20160721

"""
import paths
import os
import numpy
import shutil
import subprocess

# Include needed directories in sys.path.
import paths
import unittest

from TestUtilities import TestUtilities
from SimEx.Parameters.AbstractCalculatorParameters import AbstractCalculatorParameters
from SimEx.Parameters.SingFELPhotonDiffractorParameters import SingFELPhotonDiffractorParameters


class SingFELPhotonDiffractorParametersTest(unittest.TestCase):
    """
    Test class for the SingFELPhotonDiffractorParameters class.
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
        parameters = SingFELPhotonDiffractorParameters()

        # Check instance and inheritance.
        self.assertIsInstance( parameters, SingFELPhotonDiffractorParameters )
        self.assertIsInstance( parameters, AbstractCalculatorParameters )

        # Check all parameters are set to default values.
        self.assertEqual( parameters.uniform_rotation, None )
        self.assertFalse( parameters.calculate_Compton )
        self.assertEqual( parameters.slice_interval, 100 )
        self.assertEqual( parameters.number_of_slices, 1 )
        self.assertEqual( parameters.pmi_start_ID, 1 )
        self.assertEqual( parameters.pmi_stop_ID, 1 )
        self.assertEqual( parameters.beam_parameter_file, None )
        self.assertEqual( parameters.beam_geometry_file, None )

    def testLegacyDictionary(self):
        """ Check parameter object can be initialized via a old-style dictionary. """
        parameters_dict = { 'uniform_rotation': False,
                           'calculate_Compton' : True,
                           'slice_interval' : 12,
                           'number_of_slices' : 2,
                           'pmi_start_ID' : 4,
                           'pmi_stop_ID'  : 5,
                           'number_of_diffraction_patterns' : 2,
                           'beam_parameter_file' : TestUtilities.generateTestFilePath('s2e.beam'),
                           'beam_geometry_file' : TestUtilities.generateTestFilePath('s2e.geom'),
                           'number_of_MPI_processes' : 4, # Legacy, has no effect.
                   }


        parameters = SingFELPhotonDiffractorParameters(parameters_dictionary=parameters_dict)

        # Check all parameters are set correctly.
        self.assertFalse( parameters.uniform_rotation )
        self.assertTrue( parameters.calculate_Compton )
        self.assertEqual( parameters.slice_interval, 12 )
        self.assertEqual( parameters.number_of_slices, 2 )
        self.assertEqual( parameters.pmi_start_ID, 4 )
        self.assertEqual( parameters.pmi_stop_ID, 5 )
        self.assertEqual( parameters.beam_parameter_file, TestUtilities.generateTestFilePath('s2e.beam') )
        self.assertEqual( parameters.beam_geometry_file, TestUtilities.generateTestFilePath('s2e.geom') )


if __name__ == '__main__':
    unittest.main()

