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
import h5py
import numpy
import os
import paths
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


    def testConstructionNoSample(self):
        """ Test construction w/o sample path raises. """
        # Setup pmi parameters.
        pmi_parameters = {'number_of_trajectories' : 1,
                          'number_of_steps'        : 100,
                         }

        self.assertRaises( ValueError, XMDYNDemoPhotonMatterInteractor, pmi_parameters, 'pmi_out', 'pmi_in', None)

    def testDefaultConstruction(self):
        """ Testing the default construction of the class. """

        # Construct the object.
        interactor = XMDYNDemoPhotonMatterInteractor(sample_path = TestUtilities.generateTestFilePath('sample.h5') )

        self.assertIsInstance(interactor, XMDYNDemoPhotonMatterInteractor)


    def testDataInterfaceQueries(self):
        """ Check that the data interface queries work. """

        # Get test instance.G
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


        # Clean up.
        self.__dirs_to_remove.append('pmi')

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

    def testOPMD(self):
        """ Check that the input directory scanner filters out the opmd files."""

        # Clean up.
        self.__dirs_to_remove.append('pmi')

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

        # Clean up.
        self.__dirs_to_remove.append('pmi')

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

        self.assertEqual(status, 0 )

    def testIssue53(self):
        """ Check that xmdyn_demo writes the Nph variable according to bugfix 53."""

        # Clean up.
        self.__dirs_to_remove.append('pmi')

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

        h5 = h5py.File('pmi/pmi_out_0000001.h5')
        Nph = h5['/data/snp_0000001/Nph']

        self.assertEqual(Nph.shape, (1,))

    def testRotationNone(self):
        """ Check that by default no rotation is applied and that random rotation has an effect."""

        # Clean up.
        self.__dirs_to_remove.append('pmi')

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
        # Check rotation angle.
        with h5py.File( os.path.join(test_interactor.output_path, 'pmi_out_0000001.h5'), 'r') as h5:
            angle = h5['data/angle'].value
            self.assertEqual( angle[0,0], 0. )
            self.assertEqual( angle[0,1], 0. )
            self.assertEqual( angle[0,2], 0. )
            self.assertEqual( angle[0,3], 0. )

            # Get atom positions.
            atom_positions = h5['data/snp_0000001/r'].value

        # Now do same calculation again.
        test_interactor.backengine()

        # Get atom positions from new calculation.
        with h5py.File( os.path.join(test_interactor.output_path, 'pmi_out_0000001.h5'), 'r') as h5:
            new_atom_positions = h5['data/snp_0000001/r'].value

        # They should coincide since no rotation has been applied.
        self.assertAlmostEqual( 1e10*numpy.linalg.norm(atom_positions - new_atom_positions), 0.0, 7 )

    def testRotationRandom(self):
        """ Check that by default no rotation is applied and that random rotation has an effect."""

        # Clean up.
        self.__dirs_to_remove.append('pmi')

        # Get test instance.
        pmi_parameters = {'number_of_trajectories' : 1,
                          'number_of_steps'        : 100,
                          'random_rotation'        : True,
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
        # Check rotation angle.
        with h5py.File( os.path.join(test_interactor.output_path, 'pmi_out_0000001.h5'), 'r') as h5:
            angle = h5['data/angle'].value[0]

            # Check we have a non-zero rotation.
            self.assertNotEqual( numpy.linalg.norm(angle), 0.)


if __name__ == '__main__':
    unittest.main()

