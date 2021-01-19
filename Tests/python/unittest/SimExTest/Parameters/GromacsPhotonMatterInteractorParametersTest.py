""" Test module for the GromacsPhotonMatterInteractorParameters.
"""
##########################################################################
#                                                                        #
# Copyright (C) 2020, 2021 Ibrahim Dawod, Juncheng E                     #
# Contact:                                                               #
#       Ibrahim Dawod <ibrahim.dawod@physics.uu.se>                      #
#       Juncheng E <juncheng.e@xfel.eu>                                  #
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

import unittest
from SimEx.Parameters.GromacsInteractorParameters import GromacsInteractorParameters
from SimEx.Parameters.AbstractCalculatorParameters import AbstractCalculatorParameters


class GromacsInteractorParametersTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def testDefaultConstruction(self):
        parameters = GromacsInteractorParameters()
        self.assertIsInstance(parameters, GromacsInteractorParameters)
        self.assertIsInstance(parameters, AbstractCalculatorParameters)

        self.assertEqual(parameters.neutron_weight, 1.e4)
        self.assertEqual(parameters.energy_bin, 1.e4)

    def testShapedConstruction(self):
        # TODO: @Ibbe, please think about the parameters we need to pass to gromacs.  
        parameters = GromacsInteractorParameters(energy_bin=2.e4, ibeam_radius=15.e-6, target_density=6.e28)

        # Check if the parameters of the constructed class are correct
        self.assertIsInstance(parameters, GromacsInteractorParameters)
        self.assertIsInstance(parameters, AbstractCalculatorParameters)

        self.assertEqual(parameters.energy_bin, 2.e4)
        self.assertEqual(parameters.ibeam_radius, 1.5e-5)
        self.assertEqual(parameters.target_density, 6.e28)


if __name__ == '__main__':
    unittest.main()
