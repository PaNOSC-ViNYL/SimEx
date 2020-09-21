""" Test module for the TNSAIonMatterInteractor."""
##########################################################################
#                                                                        #
# Copyright (C) 2020 Zsolt Lecz, Juncheng E                              #
# Contact: Juncheng E <juncheng.e@xfel.eu>                               #
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
from SimEx.Calculators.TNSAIonMatterInteractor import TNSAIonMatterInteractor
from SimEx.Parameters.IonMatterInteractorParameters import IonMatterInteractorParameters
from SimEx.Calculators.AbstractIonInteractor import AbstractIonInteractor
from TestUtilities import TestUtilities
import os


class TNSAIonMatterInteractorTest(unittest.TestCase):

    def setUp(self):
        self.params = IonMatterInteractorParameters(ion_name='proton')
        self.params.xsec_file = generateTestFilePath('D_D_-_3He_n.txt')
        self.__files_to_remove = ['NeutronData.h5']

    def tearDown(self):
        """ Tearing down a test. """
        for f in self.__files_to_remove:
            if os.path.isfile(f):
                os.remove(f)


    def testConstructor(self):
        interact = TNSAIonMatterInteractor(self.params, input_path='something', output_path='')
        self.assertIsInstance(interact, TNSAIonMatterInteractor)
        self.assertIsInstance(interact, AbstractIonInteractor)

    def testRun(self):
        input_file = TestUtilities.generateTestFilePath('0010.sdf')
        mysource = TNSAIonMatterInteractor(parameters=self.params,
                                           input_path=input_file,
                                           output_path='Data/NeutronData.h5')

        self.assertEqual(mysource.backengine(), 0)
        mysource.saveH5()


if __name__ == '__main__':
    unittest.main()
