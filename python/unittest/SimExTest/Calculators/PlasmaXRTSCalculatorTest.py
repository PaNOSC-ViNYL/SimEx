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

""" Test module for the PlasmaXRTSCalculator.

    @author : CFG
    @institution : XFEL
    @creation 20151109

"""
import os
import numpy
import shutil

# Include needed directories in sys.path.
import paths
import unittest

from SimEx.Parameters.PlasmaXRTSCalculatorParameters import PlasmaXRTSCalculatorParameters
from SimEx.Calculators.AbstractPhotonDiffractor import AbstractPhotonDiffractor
from SimEx.Calculators.AbstractBaseCalculator import AbstractBaseCalculator

# Import the class to test.
from SimEx.Calculators.PlasmaXRTSCalculator import PlasmaXRTSCalculator
from TestUtilities import TestUtilities

class PlasmaXRTSCalculatorTest(unittest.TestCase):
    """
    Test class for the PlasmaXRTSCalculator class.
    """

    @classmethod
    def setUpClass(cls):
        """ Setting up the test class. """
        cls.input_path = TestUtilities.generateTestFilePath('')

    @classmethod
    def tearDownClass(cls):
        """ Tearing down the test class. """
        del cls.input_path

    def setUp(self):
        """ Setting up a test. """
        self.__files_to_remove = []
        self.__dirs_to_remove = []

        # Setup parameters.
        self.xrts_parameters = PlasmaXRTSCalculatorParameters(
                            elements=[['Be', 1, -1]],
                            photon_energy=4.96e3,
                            electron_density=3e29,
                            electron_temperature=10.0,
                            mass_density=1.85,
                            ion_charge=2.3,
                            scattering_angle=90.,
                            )

    def tearDown(self):
        """ Tearing down a test. """
        for f in self.__files_to_remove:
            if os.path.isfile(f):
                os.remove(f)
        for d in self.__dirs_to_remove:
            if os.path.isdir(d):
                shutil.rmtree(d)
        del self.xrts_parameters

    def testConstruction(self):
        """ Testing the default construction of the class. """

        # Attempt to construct an instance of the class.
        xrts_calculator = PlasmaXRTSCalculator(parameters=self.xrts_parameters,
                                               input_path=self.input_path,
                                               output_path='xrts_out')

        # Check instance and inheritance.
        self.assertIsInstance( xrts_calculator, PlasmaXRTSCalculator )
        self.assertIsInstance( xrts_calculator, AbstractPhotonDiffractor )
        self.assertIsInstance( xrts_calculator, AbstractBaseCalculator )

    def testConstructionParameters(self):
        """ Testing the input parameter checks pass for a sane parameter dict. """

        # Construct an instance.
        xrts_calculator = PlasmaXRTSCalculator( parameters=self.xrts_parameters,
                                                input_path=self.input_path,
                                                output_path='xrts_out'
                                              )

        # Query the parameters.
        query = xrts_calculator.parameters

        # Check query is ok.
        self.assertIsInstance( query, PlasmaXRTSCalculatorParameters )


    def testBackengine(self):
        """ Check that the backengine can be executed and output is generated. """

        # Setup parameters.
        xrts_parameters = self.parameters


        # Construct an instance.
        xrts_calculator = PlasmaXRTSCalculator( parameters=xrts_parameters,
                                                input_path=self.input_path,
                                                output_path='xrts_out'
                                              )

        # Call the backengine.
        xrts_calculator.backengine()

        # Check for output.
        self.assertTrue( os.path.isdir( xrts_calculator.parameters._tmp_dir ) )
        self.assertTrue( 'xrts_out.txt' in os.listdir( xrts_calculator.parameters._tmp_dir ) )

    def testCheckAndSetParameters(self):
        """ Test the parameters check'n'set function. """


if __name__ == '__main__':
    unittest.main()

