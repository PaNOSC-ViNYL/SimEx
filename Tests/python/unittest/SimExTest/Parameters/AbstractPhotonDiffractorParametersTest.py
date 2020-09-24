""" :module: Module for the AbstractPhotonDiffractorParameter class. """
##########################################################################
#                                                                        #
# Copyright (C) 2016-2019 Carsten Fortmann-Grote                         #
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

import os
import shutil

# Include needed directories in sys.path.
import unittest

from TestUtilities import TestUtilities
from SimEx.Parameters.AbstractCalculatorParameters import AbstractCalculatorParameters
from SimEx.Parameters.AbstractPhotonDiffractorParameters import AbstractPhotonDiffractorParameters


class AbstractPhotonDiffractorParametersTest(unittest.TestCase):
    """
    Test class for the AbstractPhotonDiffractorParameters class.
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
        """ Testing the default construction. """

        # Attempt to construct an instance of the class.
        parameters = AbstractPhotonDiffractorParameters( sample=TestUtilities.generateTestFilePath("2nip.pdb")
                )

        # Check instance and inheritance.
        self.assertIsInstance( parameters, AbstractPhotonDiffractorParameters )
        self.assertIsInstance( parameters, AbstractCalculatorParameters )

        # Check all parameters are set to default values.
        self.assertEqual( parameters.sample, TestUtilities.generateTestFilePath("2nip.pdb") )
        self.assertFalse( parameters.uniform_rotation )
        self.assertEqual( parameters.beam_parameters, None )
        self.assertEqual( parameters.detector_geometry, None )
        self.assertEqual( parameters.number_of_diffraction_patterns, 1 )


if __name__ == '__main__':
    unittest.main()

