##########################################################################
#                                                                        #
# Copyright (C) 2015, 2016 Carsten Fortmann-Grote                        #
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

""" Test module for the XMDYNDemoPhotonMatterInteractor.

    @author : CFG
    @institution : XFEL
    @creation 20151215

"""
import paths
import os
import shutil
import unittest

# Import the class to test.
from SimEx.Calculators.XMDYNDemoPhotonMatterInteractor import XMDYNDemoPhotonMatterInteractor
from TestUtilities import TestUtilities

class XMDYNDemoPhotonMatterInteractorTest(unittest.TestCase):
    """
    Test class for the XMDYNDemoPhotonMatterInteractor class.
    """

    @classmethod
    def setUpClass(cls):
        """ Setting up the test class. """
        cls.input_h5 = TestUtilities.generateTestFilePath('prop_out_0000001.h5')

    @classmethod
    def tearDownClass(cls):
        """ Tearing down the test class. """

    def setUp(self):
        """ Setting up a test. """
        self.__files_to_remove = []
        self.__dirs_to_remove = []

    def tearDown(self):
        """ Tearing down a test. """
        # Clean up.
        for f in self.__files_to_remove:
            if os.path.isfile(f):
                os.remove(f)
        for p in self.__dirs_to_remove:
            if os.path.isdir(p):
                shutil.rmtree(p)

    def testShapedConstruction(self):
        """ Testing the construction of the class with parameters. """

        # Setup pmi parameters.
        pmi_parameters = {'number_of_trajectories' : 1,
                          'number_of_steps'        : 100,
                         }

        interactor = XMDYNDemoPhotonMatterInteractor(parameters=pmi_parameters,
                                                     output_path='pmi_out',
                                                     input_path='pmi_in',
                                                     sample_path=TestUtilities.generateTestFilePath('sample.h5'),
                                                     )

        self.assertIsInstance(interactor, XMDYNDemoPhotonMatterInteractor)

    def testDefaultConstruction(self):
        """ Testing the default construction of the class. """

        # Construct the object.
        interactor = XMDYNDemoPhotonMatterInteractor(sample_path = TestUtilities.generateTestFilePath('sample.h5') )

        self.assertIsInstance(interactor, XMDYNDemoPhotonMatterInteractor)


    def testDataInterfaceQueries(self):
        """ Check that the data interface queries work. """

        # Get test instance.
        # Setup pmi parameters.
        pmi_parameters = {'number_of_trajectories' : 1,
                          'number_of_steps'        : 100,
                          'sample_path' : TestUtilities.generateTestFilePath('sample.h5')
                         }
        test_interactor = XMDYNDemoPhotonMatterInteractor(parameters=pmi_parameters,
                                                          input_path=self.input_h5,
                                                          output_path='pmi_out.h5',
                                                          sample_path = TestUtilities.generateTestFilePath('sample.h5') )

        # Get expected and provided data descriptors.
        expected_data = test_interactor.expectedData()
        provided_data = test_interactor.providedData()

        # Check types are correct.
        self.assertIsInstance(expected_data, list)
        self.assertIsInstance(provided_data, list)
        for d in expected_data:
            self.assertIsInstance(d, str)
            self.assertEqual(d[0], '/')
        for d in provided_data:
            self.assertIsInstance(d, str)
            self.assertEqual(d[0], '/')

    def testBackengineDefaultPaths(self):
        """ Check that the backengine method works correctly. """

        # Prepare input.
        shutil.copytree( TestUtilities.generateTestFilePath('prop_out'), os.path.abspath( 'prop' ) )
        self.__dirs_to_remove.append( 'prop' )
        self.__dirs_to_remove.append( 'pmi' )

        test_interactor = XMDYNDemoPhotonMatterInteractor(sample_path=TestUtilities.generateTestFilePath('sample.h5') )

        # Call backengine
        status = test_interactor.backengine()

        # Check that the backengine returned zero.
        self.assertEqual(status, 0)

        # Check we have generated the expected output.
        self.assertTrue( os.path.isdir( os.path.abspath( 'prop' ) ) )
        self.assertIn( 'pmi_out_0000001.h5' , os.listdir( test_interactor.output_path ) )
        self.assertIn( 'pmi_out_0000002.h5' , os.listdir( test_interactor.output_path ) )

    def testBackengine(self):
        """ Check that the backengine method works correctly. """

        # Get test instance.
        pmi_parameters = {'number_of_trajectories' : 1,
                          'number_of_steps'        : 100,
                         }

        test_interactor = XMDYNDemoPhotonMatterInteractor(parameters=pmi_parameters,
                                                          input_path=self.input_h5,
                                                          output_path='pmi',
                                                          sample_path = TestUtilities.generateTestFilePath('sample.h5') )

        # Call backengine
        status = test_interactor.backengine()

        # Check that the backengine returned zero.
        self.assertEqual(status, 0)

        # Check we have generated the expected output.
        self.assertTrue( 'pmi_out_0000001.h5' in os.listdir( test_interactor.output_path ) )

        # Clean up.
        self.__dirs_to_remove.append('pmi')

    def testOPMD(self):
        """ Check that the input directory scanner filters out the opmd files."""
        # Setup parameters.
        pmi_parameters = {'number_of_trajectories' : 10,
                          'number_of_steps'        : 100,
                         }

        test_interactor = XMDYNDemoPhotonMatterInteractor(parameters=pmi_parameters,
                                                          input_path=TestUtilities.generateTestFilePath('prop_out'),
                                                          output_path='pmi',
                                                          sample_path=TestUtilities.generateTestFilePath('sample.h5') )

        # Call backengine
        status = test_interactor.backengine()

        self.assertEqual(status, 0 )

    def testLoadPDBFile(self):
        """ Check that the sample can be taken from a pdb directly. """

        # Get test instance.
        pmi_parameters = {'number_of_trajectories' : 10,
                          'number_of_steps'        : 100,
                         }

        pmi = XMDYNDemoPhotonMatterInteractor(parameters=pmi_parameters,
                                              input_path=self.input_h5,
                                              output_path='pmi',
                                              sample_path=TestUtilities.generateTestFilePath('2nip.pdb') )

        # Call backengine
        status = pmi.backengine()




if __name__ == '__main__':
    unittest.main()

