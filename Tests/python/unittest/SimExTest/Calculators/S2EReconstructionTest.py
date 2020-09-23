""" :module: Test module for the S2EReconstruction."""
##########################################################################
#                                                                        #
# Copyright (C) 2015-2020 Carsten Fortmann-Grote                         #
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

import os, shutil
import unittest


# Import the class to test.
from SimEx.Calculators.S2EReconstruction import S2EReconstruction
from TestUtilities import TestUtilities

class S2EReconstructionTest(unittest.TestCase):
    """
    Test class for the S2EReconstruction class.
    """

    @classmethod
    def setUpClass(cls):
        """ Setting up the test class. """
        cls.input_h5 = TestUtilities.generateTestFilePath('diffr')

    @classmethod
    def tearDownClass(cls):
        """ Tearing down the test class. """
        del cls.input_h5

    def setUp(self):
        """ Setting up a test. """
        self.__files_to_remove = []
        self.__dirs_to_remove = []

    def testDefaultConstruction(self):
        """ Testing the default construction of the class. """

        # Ensure proper cleanup.
        self.__dirs_to_remove.append( 'analysis' )

        # Construct the object.
        analyzer = S2EReconstruction()
        self.assertIsInstance(analyzer, S2EReconstruction)

        # Check.
        self.assertEqual( analyzer.input_path,  os.path.abspath( 'detector' ) )
        self.assertEqual( analyzer.output_path, os.path.abspath( 'analysis' ) )

    @unittest.skipIf(TestUtilities.runs_on_travisCI(), "CI.")
    def testBackengineDefaultPath(self):
        """ Test that we can start a test calculation. """

        # Prepare path.
        shutil.copytree( TestUtilities.generateTestFilePath( 'diffr' ), 'detector' )

        # Ensure proper cleanup.
        self.__dirs_to_remove.append( 'detector' )
        self.__dirs_to_remove.append( 'analysis' )

        emc_parameters = {'initial_number_of_quaternions' : 1,
                          'max_number_of_quaternions'     : 2,
                          'max_number_of_iterations'      : 10,
                          'min_error'                     : 1.0e-6,
                          'beamstop'                      : True,
                          'detailed_output'               : False
                               }

        dm_parameters = {'number_of_trials'        : 5,
                         'number_of_iterations'    : 2,
                         'averaging_start'         : 15,
                         'leash'                   : 0.2,
                         'number_of_shrink_cycles' : 2,
                         }

        # Construct the object.
        analyzer = S2EReconstruction(parameters={'EMC_Parameters' : emc_parameters, 'DM_Parameters' : dm_parameters})

        # Call backengine.
        status = analyzer.backengine()

        # Check return value.
        self.assertEqual(status, 0)

        # Check presence of output files.
        self.assertTrue( os.path.isdir( 'analysis' ) )
        self.assertIn( 'orient_out.h5', os.listdir( 'analysis' ) )
        self.assertIn( 'phase_out.h5', os.listdir( 'analysis' ) )

    def tearDown(self):
        """ Tearing down a test. """

        for f in self.__files_to_remove:
            if os.path.isfile(f):
                os.remove(f)
        for d in self.__dirs_to_remove:
            if os.path.isdir(d):
                shutil.rmtree(d)

    def testShapedConstruction(self):
        """ Testing the default construction of the class. """

        self.__files_to_remove.append('orient_out.h5')
        self.__files_to_remove.append('recon_out.h5')
        # Construct the object.
        analyzer = S2EReconstruction(parameters=None, input_path=self.input_h5, output_path='recon_out.h5')

        self.assertIsInstance(analyzer, S2EReconstruction)

    @unittest.skipIf(TestUtilities.runs_on_travisCI(), "CI.")
    def testBackengine(self):
        """ Test that we can start a test calculation. """

        self.__files_to_remove.append('orient_out.h5')
        self.__files_to_remove.append('recon_out.h5')

        emc_parameters = {'initial_number_of_quaternions' : 1,
                          'max_number_of_quaternions'     : 2,
                          'max_number_of_iterations'      : 10,
                          'min_error'                     : 1.0e-6,
                          'beamstop'                      : True,
                          'detailed_output'               : False
                               }

        dm_parameters = {'number_of_trials'        : 5,
                         'number_of_iterations'    : 2,
                         'averaging_start'         : 15,
                         'leash'                   : 0.2,
                         'number_of_shrink_cycles' : 2,
                         }


        # Construct the object.
        analyzer = S2EReconstruction(parameters={'EMC_Parameters' : emc_parameters, 'DM_Parameters' : dm_parameters}, input_path=self.input_h5, output_path='recon_out.h5')

        # Call backengine.
        status = analyzer.backengine()

        self.assertEqual(status, 0)


if __name__ == '__main__':
    unittest.main()

