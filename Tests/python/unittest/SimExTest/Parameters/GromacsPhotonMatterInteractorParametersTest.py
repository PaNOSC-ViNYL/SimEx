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
from SimEx.Parameters.AbstractCalculatorParameters import AbstractCalculatorParameters
from SimEx.Parameters.GromacsPhotonMatterInteractorParameters import GromacsPhotonMatterInteractorParameters


class GromacsPhotonMatterInteractorParametersTest(unittest.TestCase):
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
        pmi_parameters = GromacsPhotonMatterInteractorParameters()

        # Check if the parameters of the constructed class are correct
        self.assertIsInstance(pmi_parameters,
                              GromacsPhotonMatterInteractorParameters)
        self.assertIsInstance(pmi_parameters, AbstractCalculatorParameters)

        # The default non-rotation
        self.assertEqual(pmi_parameters.rotations, [(1, 0, 0, 0)])
        # The default all incidices
        self.assertEqual(pmi_parameters.pulse_indices, 'all')

    def testRotations(self):
        pmi_parameters = GromacsPhotonMatterInteractorParameters(
            rotations=[1, 0.75, 0.3, 0.2])

        self.assertEqual(pmi_parameters.rotations[0], [1, 0.75, 0.3, 0.2])

        pmi_parameters = GromacsPhotonMatterInteractorParameters(
            rotations=[(1, 0.75, 0.3, 0.2), (1, 0.3, 0.2, 0.1)])

        self.assertEqual(pmi_parameters.rotations[0], (1, 0.75, 0.3, 0.2))
        self.assertEqual(pmi_parameters.rotations[1], (1, 0.3, 0.2, 0.1))

    def testPulse_indices(self):
        pmi_parameters = GromacsPhotonMatterInteractorParameters(
            pulse_indices=[1, 2, 5])

        self.assertEqual(pmi_parameters.pulse_indices, [1, 2, 5])

    def testShapedConstruction(self):
        pmi_parameters = GromacsPhotonMatterInteractorParameters(
            rotations=[(1, 0.75, 0.3, 0.2)],
            pulse_indices=[1, 2, 5],
            forced_mpi_command='mpirun -np 4')

        self.assertEqual(pmi_parameters.rotations[0], (1, 0.75, 0.3, 0.2))
        self.assertEqual(pmi_parameters.pulse_indices, [1, 2, 5])
        self.assertEqual(pmi_parameters.forced_mpi_command, 'mpirun -np 4')


if __name__ == '__main__':
    unittest.main()
