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

""" Test module for the ComptonScatteringCalculator.

    @author : CFG
    @institution : XFEL
    @creation 20160404

"""
import os
import numpy
import shutil
import h5py

# Include needed directories in sys.path.
import paths
import unittest

from SimEx.Parameters.PlasmaXRTSCalculatorParameters import PlasmaXRTSCalculatorParameters
from SimEx.Calculators.AbstractPhotonDiffractor import AbstractPhotonDiffractor
from SimEx.Calculators.AbstractBaseCalculator import AbstractBaseCalculator
from TestUtilities import TestUtilities

# Import the class to test.
from SimEx.Calculators.ComptonScatteringCalculator import ComptonScatteringCalculator
from SimEx.Calculators.ComptonScatteringCalculator import _fermiEnergy
from SimEx.Calculators.ComptonScatteringCalculator import _chemicalPotential

class ComptonScatteringCalculatorTest(unittest.TestCase):
    """
    Test class for the ComptonScatteringCalculator class.
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
        self.parameters = PlasmaXRTSCalculatorParameters(
                            elements=[['Be', 1, -1]],
                            photon_energy=8.00e3,
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
        del self.parameters

    def testConstruction(self):
        """ Testing the default construction of the class. """

        # Attempt to construct an instance of the class.
        calculator = ComptonScatteringCalculator(parameters=self.parameters,
                                               input_path=self.input_path,
                                               output_path='out')

        # Check instance and inheritance.
        self.assertIsInstance( calculator, ComptonScatteringCalculator )
        self.assertIsInstance( calculator, AbstractPhotonDiffractor )
        self.assertIsInstance( calculator, AbstractBaseCalculator )

        # Check attributes are initialized.
        self.assertEqual( calculator._input_data, {} )

    def testFermiEnergy(self):
        """ Test the calculation of the chemical potential using Fermi integral inversion. """

        # Fix electron density.
        ne = 1.0e29 # m**-3

        # Check reference value for Fermi energy.
        self.assertAlmostEqual( _fermiEnergy(ne), 7.85604, 5)


    def testChemicalPotentialDegenerate(self):
        """ Test the calculation of the chemical potential for theta << 1. """

        # Fix density and temperature.
        ne = 1e29 # m**-3
        Te = 1.0  # eV

        # Get  chemical potential.
        mu = _chemicalPotential( ne, Te )

        # Compare to reference value.
        self.assertAlmostEqual( mu, 7.74839, 5 )

    def testChemicalPotentialNonDegenerate(self):
        """ Test the calculation of the chemical potential for theta >> 1. """

        # Fix density and temperature.
        ne = 1e29 # m**-3
        Te = 1000.0  # eV

        # Get  chemical potential.
        mu = _chemicalPotential( ne, Te )

        # Compare to reference value.
        self.assertAlmostEqual( mu, -7554., 0 )



if __name__ == '__main__':
    unittest.main()

