""" :module: Test module for the FEFFPhotonMatterInteractor.  """

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

import h5py
import os
import shutil
import unittest
import io

# Import the class to test.
from SimEx.Calculators.FEFFPhotonMatterInteractor import FEFFPhotonMatterInteractor
from SimEx.Parameters.FEFFPhotonMatterInteractorParameters import FEFFPhotonMatterInteractorParameters
from SimEx.Parameters.FEFFPhotonMatterInteractorParameters import _checkAndSetAmplitudeReductionFactor
from SimEx.Parameters.FEFFPhotonMatterInteractorParameters import _checkAndSetAtoms
from SimEx.Parameters.FEFFPhotonMatterInteractorParameters import _checkAndSetEdge
from SimEx.Parameters.FEFFPhotonMatterInteractorParameters import _checkAndSetEffectivePathDistance
from SimEx.Parameters.FEFFPhotonMatterInteractorParameters import _checkAndSetPotentials

from TestUtilities import TestUtilities

class FEFFPhotonMatterInteractorTest(unittest.TestCase):
    """
    Test class for the FEFFPhotonMatterInteractor class.
    """

    @classmethod
    def setUpClass(cls):
        """ Setting up the test class. """

    @classmethod
    def tearDownClass(cls):
        """ Tearing down the test class. """

    def setUp(self):
        """ Setting up a test. """
        self.__files_to_remove = []
        self.__dirs_to_remove = []

        self.__atoms = (
                 [[ 0.00000,     0.00000,     0.00000], 'Cu',   0],
                 [[ 0.00000,     1.80500,    -1.80500], 'Cu',   1],
                 [[-1.80500,    -1.80500,     0.00000], 'Cu',   1],
                 [[ 1.80500,     0.00000,    -1.80500], 'Cu',   1],
                 [[ 0.00000,    -1.80500,     1.80500], 'Cu',   1],
                 [[ 1.80500,     1.80500,     0.00000], 'Cu',   1],
                 [[ 0.00000,    -1.80500,    -1.80500], 'Cu',   1],
                 [[-1.80500,     1.80500,     0.00000], 'Cu',   1],
                 [[ 0.00000,     1.80500,     1.80500], 'Cu',   1],
                 [[-1.80500,     0.00000,    -1.80500], 'Cu',   1],
                 [[-1.80500,     0.00000,     1.80500], 'Cu',   1],
                 [[ 1.80500,     0.00000,     1.80500], 'Cu',   1],
                 [[ 1.80500,    -1.80500,     0.00000], 'Cu',   1],
                 [[ 0.00000,    -3.61000,     0.00000], 'Cu',   1],
                 [[ 0.00000,     0.00000,    -3.61000], 'Cu',   1],
                 [[ 0.00000,     0.00000,     3.61000], 'Cu',   1],
                 [[-3.61000,     0.00000,     0.00000], 'Cu',   1],
                 [[ 3.61000,     0.00000,     0.00000], 'Cu',   1],
                 [[ 0.00000,     3.61000,     0.00000], 'Cu',   1],
                 [[-1.80500,     3.61000,     1.80500], 'Cu',   1],
                 [[ 1.80500,     3.61000,     1.80500], 'Cu',   1],
                 [[-1.80500,    -3.61000,    -1.80500], 'Cu',   1],
                 [[-1.80500,     3.61000,    -1.80500], 'Cu',   1],
                 [[ 1.80500,     3.61000,    -1.80500], 'Cu',   1],
                 [[-1.80500,    -3.61000,     1.80500], 'Cu',   1],
                 [[-3.61000,     1.80500,    -1.80500], 'Cu',   1],
                 [[ 1.80500,    -3.61000,     1.80500], 'Cu',   1],
                 [[ 3.61000,     1.80500,    -1.80500], 'Cu',   1],
                 [[-3.61000,     1.80500,     1.80500], 'Cu',   1],
                 [[-3.61000,    -1.80500,    -1.80500], 'Cu',   1],
                 [[ 3.61000,    -1.80500,     1.80500], 'Cu',   1],
                 [[ 1.80500,    -3.61000,    -1.80500], 'Cu',   1],
                 [[-3.61000,    -1.80500,     1.80500], 'Cu',   1],
                 [[ 3.61000,     1.80500,     1.80500], 'Cu',   1],
                 [[-1.80500,    -1.80500,     3.61000], 'Cu',   1],
                 [[-1.80500,    -1.80500,    -3.61000], 'Cu',   1],
                 [[ 1.80500,     1.80500,    -3.61000], 'Cu',   1],
                 [[ 1.80500,    -1.80500,    -3.61000], 'Cu',   1],
                 [[ 1.80500,    -1.80500,     3.61000], 'Cu',   1],
                 [[-1.80500,     1.80500,    -3.61000], 'Cu',   1],
                 [[-1.80500,     1.80500,     3.61000], 'Cu',   1],
                 [[ 1.80500,     1.80500,     3.61000], 'Cu',   1],
                 [[ 3.61000,    -1.80500,    -1.80500], 'Cu',   1],
                 [[ 3.61000,    -3.61000,     0.00000], 'Cu',   1],
                 [[ 3.61000,     0.00000,    -3.61000], 'Cu',   1],
                 [[ 3.61000,     0.00000,     3.61000], 'Cu',   1],
                 [[-3.61000,     3.61000,     0.00000], 'Cu',   1],
                 [[ 0.00000,     3.61000,     3.61000], 'Cu',   1],
                 [[-3.61000,     0.00000,     3.61000], 'Cu',   1],
                 [[-3.61000,    -3.61000,     0.00000], 'Cu',   1],
                 [[ 0.00000,    -3.61000,     3.61000], 'Cu',   1],
                 [[-3.61000,     0.00000,    -3.61000], 'Cu',   1],
                 [[ 3.61000,     3.61000,     0.00000], 'Cu',   1],
                 [[ 0.00000,    -3.61000,    -3.61000], 'Cu',   1],
                 [[ 0.00000,     3.61000,    -3.61000], 'Cu',   1],
                 [[ 0.00000,    -5.41500,     1.80500], 'Cu',   1],
                 [[ 1.80500,    -5.41500,     0.00000], 'Cu',   1],
                 [[ 0.00000,    -5.41500,    -1.80500], 'Cu',   1],
                 [[-1.80500,     0.00000,     5.41500], 'Cu',   1],
                 [[-5.41500,     0.00000,    -1.80500], 'Cu',   1],
                 [[ 5.41500,    -1.80500,     0.00000], 'Cu',   1],
                 [[-1.80500,     5.41500,     0.00000], 'Cu',   1],
                 [[ 5.41500,     0.00000,    -1.80500], 'Cu',   1],
                 [[-5.41500,    -1.80500,     0.00000], 'Cu',   1],
                 [[ 1.80500,     5.41500,     0.00000], 'Cu',   1],
                 [[ 5.41500,     1.80500,     0.00000], 'Cu',   1],
                 [[ 0.00000,     5.41500,    -1.80500], 'Cu',   1],
                 [[ 0.00000,    -1.80500,    -5.41500], 'Cu',   1],
                 [[ 0.00000,     5.41500,     1.80500], 'Cu',   1],
                 [[ 1.80500,     0.00000,     5.41500], 'Cu',   1],
                 [[ 0.00000,     1.80500,     5.41500], 'Cu',   1],
                 [[ 5.41500,     0.00000,     1.80500], 'Cu',   1],
                 [[ 1.80500,     0.00000,    -5.41500], 'Cu',   1],
                 [[ 0.00000,     1.80500,    -5.41500], 'Cu',   1],
                 [[ 0.00000,    -1.80500,     5.41500], 'Cu',   1],
                 [[-5.41500,     0.00000,     1.80500], 'Cu',   1],
                 [[-5.41500,     1.80500,     0.00000], 'Cu',   1],
                 [[-1.80500,     0.00000,    -5.41500], 'Cu',   1],
                 [[-1.80500,    -5.41500,     0.00000], 'Cu',   1],
                 )

        self.__potentials = None
        self.__edge = 'K'
        self.__amplitude_reduction_factor = 0.9
        self.__effective_path_distance = 5.5

        self.__parameters = FEFFPhotonMatterInteractorParameters(
                atoms=self.__atoms,
                potentials=self.__potentials,
                edge=self.__edge,
                amplitude_reduction_factor=self.__amplitude_reduction_factor,
                effective_path_distance=self.__effective_path_distance,
                )

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

        # Construct.
        self.__dirs_to_remove.append( 'pmi' )
        feff  = FEFFPhotonMatterInteractor(parameters=self.__parameters)

        # Check type.
        self.assertIsInstance( feff, FEFFPhotonMatterInteractor )

        # Get parameters and check.
        parameters = feff.parameters

        self.assertEqual( parameters.atoms, self.__atoms)
        self.assertEqual( parameters.potentials, self.__potentials)
        self.assertEqual( parameters.edge, self.__edge)
        self.assertEqual( parameters.amplitude_reduction_factor, self.__amplitude_reduction_factor)
        self.assertEqual( parameters.effective_path_distance, self.__effective_path_distance)

    def testShapedConstructionPaths(self):
        """ Testing the construction of the class with parameters. """

        # Construct.
        feff  = FEFFPhotonMatterInteractor(parameters=self.__parameters,
                                           input_path=TestUtilities.generateTestFilePath('prop'),
                                           output_path='absorption.h5')

        # Check type.
        self.assertIsInstance( feff, FEFFPhotonMatterInteractor )

        # Get parameters and check.
        parameters = feff.parameters

        self.assertEqual( parameters.atoms, self.__atoms)
        self.assertEqual( parameters.potentials, self.__potentials)
        self.assertEqual( parameters.edge, self.__edge)
        self.assertEqual( parameters.amplitude_reduction_factor, self.__amplitude_reduction_factor)
        self.assertEqual( parameters.effective_path_distance, self.__effective_path_distance)

        self.assertEqual( feff.output_path, os.path.join( os.getcwd(), 'absorption.h5' ) )


    def testWorkingDirectorySetup(self):
        """ Test the initialization of the working directory. """

        # Requirements:
        # - By default, setup tmp dir, copy executable and write serialize parameters
        # - User may specify working directory ### TODO
        # - If feff.inp already exists: backup and overwrite. ### TODO
        # - enhancement: initialize parameters from given feff.inp ### TODO

        # Test default behavior.
        self.__dirs_to_remove.append( 'pmi' )
        feff = FEFFPhotonMatterInteractor(parameters = self.__parameters)

        # Setup working directory.
        feff._setupWorkingDirectory()

        # Assert it is created.
        self.assertTrue( os.path.isdir( feff.working_directory ) )

    def testOutputPathFail(self):
        """ Test that default output path raises if file of same name exists."""

        # Cleanup.
        self.__files_to_remove.append( 'pmi' )

        # Create file of same name as default output path.
        shutil.copy2( __file__, 'pmi' )

        # Check exception.
        self.assertRaises( IOError, FEFFPhotonMatterInteractor )

    @unittest.skip(reason="Skipped becaucse backengine never returns even when FEFF is done.")
    def testOutputPath(self):
        """ Check that the default path is set correctly. """
        # Setup the calculator.
        feff = FEFFPhotonMatterInteractor(parameters = self.__parameters)
        self.__dirs_to_remove.append( 'pmi' )

        # Execute the code.
        status = feff.backengine()

        # Check that the pmi dir was created.
        self.assertTrue( os.path.isdir( 'pmi' ) )

    @unittest.skip(reason="Skipped becaucse backengine never returns even when FEFF is done.")
    def testBackengine(self):
        """ Test the backengine execution. """

        # Setup the calculator.
        feff = FEFFPhotonMatterInteractor(parameters = self.__parameters)

        self.__dirs_to_remove.append( 'pmi' )

        # Execute the code.
        status = feff.backengine()

        # Check success.
        self.assertEqual( status, 0 )

        # Check directory content.
        self.assertIn('atoms.dat', os.listdir(feff.working_directory) )
        self.assertIn('chi.dat', os.listdir(feff.working_directory) )
        self.assertIn('feff.bin', os.listdir(feff.working_directory) )
        self.assertIn('feff.inp', os.listdir(feff.working_directory) )
        self.assertIn('feff85L', os.listdir(feff.working_directory) )
        self.assertIn('fort.38', os.listdir(feff.working_directory) )
        self.assertIn('fort.39', os.listdir(feff.working_directory) )
        self.assertIn('fpf0.dat', os.listdir(feff.working_directory) )
        self.assertIn('geom.dat', os.listdir(feff.working_directory) )
        self.assertIn('global.dat', os.listdir(feff.working_directory) )
        self.assertIn('list.dat', os.listdir(feff.working_directory) )
        self.assertIn('log.dat', os.listdir(feff.working_directory) )
        self.assertIn('log1.dat', os.listdir(feff.working_directory) )
        self.assertIn('log2.dat', os.listdir(feff.working_directory) )
        self.assertIn('log4.dat', os.listdir(feff.working_directory) )
        self.assertIn('log5.dat', os.listdir(feff.working_directory) )
        self.assertIn('log6.dat', os.listdir(feff.working_directory) )
        self.assertIn('mod1.inp', os.listdir(feff.working_directory) )
        self.assertIn('mod2.inp', os.listdir(feff.working_directory) )
        self.assertIn('mod3.inp', os.listdir(feff.working_directory) )
        self.assertIn('mod4.inp', os.listdir(feff.working_directory) )
        self.assertIn('mod5.inp', os.listdir(feff.working_directory) )
        self.assertIn('mod6.inp', os.listdir(feff.working_directory) )
        self.assertIn('mpse.dat', os.listdir(feff.working_directory) )
        self.assertIn('paths.dat', os.listdir(feff.working_directory) )
        self.assertIn('phase.bin', os.listdir(feff.working_directory) )
        self.assertIn('pot.bin', os.listdir(feff.working_directory) )
        self.assertIn('s02.inp', os.listdir(feff.working_directory) )
        self.assertIn('xmu.dat', os.listdir(feff.working_directory) )
        self.assertIn('xsect.bin', os.listdir(feff.working_directory) )

    @unittest.skip(reason="Skipped becaucse backengine never returns even when FEFF is done.")
    def testSaveH5(self):
        # Setup the calculator.
        feff = FEFFPhotonMatterInteractor(parameters = self.__parameters, output_path='feff.h5')

        self.__files_to_remove.append(feff.output_path)

        # Execute the code.
        status = feff.backengine()

        # Save.
        feff.saveH5()

        # Check content of newly generated file.
        expected_sets = [
                            'data/snp_0000001/r',
                            #'data/snp_0000001/xyz',
                            #'data/snp_0000001/Z',
                            #'data/snp_0000001/T',
                            'data/snp_0000001/E',
                            'data/snp_0000001/DeltaE',
                            'data/snp_0000001/k',
                            'data/snp_0000001/mu',
                            'data/snp_0000001/mu0',
                            'data/snp_0000001/chi',
                            'data/snp_0000001/ampl',
                            'data/snp_0000001/phase',
                            'data/snp_0000001/potential_index',
                            'params/amplitude_reduction_factor',
                            'params/edge',
                            'params/effective_path_distance',
                            #'history/parent',
                            #'misc/polarization_tensor',
                            #'misc/evec',
                            #'misc/xivec',
                            #'misc/spvec',
                            #'misc/nabs',
                            #'misc/iphabs',
                            #'misc/cf_average_data',
                            #'misc/ipol',
                            #'misc/ispin',
                            #'misc/le2',
                            #'misc/elpty',
                            #'misc/angks',
                            'info/contact',
                            'info/data_description',
                            'info/interface_version',
                            'info/credits',
                            'info/package_version',
                          ]

        with h5py.File( feff.output_path, 'r') as h5:
            for st in expected_sets:
                self.assertIsInstance( h5[st], h5py.Dataset )

            # Check attributes
            self.assertEqual( h5['data/snp_0000001/r'].attrs['unit'], 'Angstrom' )
            self.assertEqual( h5['data/snp_0000001/E'].attrs['unit'], 'eV')
            self.assertEqual( h5['data/snp_0000001/DeltaE'].attrs['unit'], 'eV')
            self.assertEqual( h5['data/snp_0000001/k'].attrs['unit'], '1')
            self.assertEqual( h5['data/snp_0000001/mu'].attrs['unit'], '1/Angstrom')
            self.assertEqual( h5['data/snp_0000001/mu0'].attrs['unit'], '1/Angstrom')
            self.assertEqual( h5['data/snp_0000001/chi'].attrs['unit'], '1')
            self.assertEqual( h5['data/snp_0000001/ampl'].attrs['unit'], '1')
            self.assertEqual( h5['data/snp_0000001/phase'].attrs['unit'], 'rad')
            self.assertEqual( h5['data/snp_0000001/potential_index'].attrs['unit'], '1')
            self.assertEqual( h5['params/amplitude_reduction_factor'].attrs['unit'], '1')
            self.assertEqual( h5['params/edge'].attrs['unit'], '')
            self.assertEqual( h5['params/effective_path_distance'].attrs['unit'], 'Angstrom')

            h5.close()


class FEFFPhotonMatterInteractorParametersTest(unittest.TestCase):
    """ Test class for the FEFFPhotonMatterInteractorParameters class. """

    @classmethod
    def setUpClass(cls):
        """ Setting up the test class. """

    @classmethod
    def tearDownClass(cls):
        """ Tearing down the test class. """

    def setUp(self):
        """ Setting up a test. """
        self.__files_to_remove = []
        self.__dirs_to_remove = []

        self.__atoms = (
                 [[ 0.00000,     0.00000,     0.00000], 'Cu',   0],
                 [[ 0.00000,     1.80500,    -1.80500], 'Cu',   1],
                 [[-1.80500,    -1.80500,     0.00000], 'Cu',   1],
                 [[ 1.80500,     0.00000,    -1.80500], 'Cu',   1],
                 [[ 0.00000,    -1.80500,     1.80500], 'Cu',   1],
                 [[ 1.80500,     1.80500,     0.00000], 'Cu',   1],
                 [[ 0.00000,    -1.80500,    -1.80500], 'Cu',   1],
                 [[-1.80500,     1.80500,     0.00000], 'Cu',   1],
                 [[ 0.00000,     1.80500,     1.80500], 'Cu',   1],
                 [[-1.80500,     0.00000,    -1.80500], 'Cu',   1],
                 [[-1.80500,     0.00000,     1.80500], 'Cu',   1],
                 [[ 1.80500,     0.00000,     1.80500], 'Cu',   1],
                 [[ 1.80500,    -1.80500,     0.00000], 'Cu',   1],
                 [[ 0.00000,    -3.61000,     0.00000], 'Cu',   1],
                 [[ 0.00000,     0.00000,    -3.61000], 'Cu',   1],
                 [[ 0.00000,     0.00000,     3.61000], 'Cu',   1],
                 [[-3.61000,     0.00000,     0.00000], 'Cu',   1],
                 [[ 3.61000,     0.00000,     0.00000], 'Cu',   1],
                 [[ 0.00000,     3.61000,     0.00000], 'Cu',   1],
                 [[-1.80500,     3.61000,     1.80500], 'Cu',   1],
                 [[ 1.80500,     3.61000,     1.80500], 'Cu',   1],
                 [[-1.80500,    -3.61000,    -1.80500], 'Cu',   1],
                 [[-1.80500,     3.61000,    -1.80500], 'Cu',   1],
                 [[ 1.80500,     3.61000,    -1.80500], 'Cu',   1],
                 [[-1.80500,    -3.61000,     1.80500], 'Cu',   1],
                 [[-3.61000,     1.80500,    -1.80500], 'Cu',   1],
                 [[ 1.80500,    -3.61000,     1.80500], 'Cu',   1],
                 [[ 3.61000,     1.80500,    -1.80500], 'Cu',   1],
                 [[-3.61000,     1.80500,     1.80500], 'Cu',   1],
                 [[-3.61000,    -1.80500,    -1.80500], 'Cu',   1],
                 [[ 3.61000,    -1.80500,     1.80500], 'Cu',   1],
                 [[ 1.80500,    -3.61000,    -1.80500], 'Cu',   1],
                 [[-3.61000,    -1.80500,     1.80500], 'Cu',   1],
                 [[ 3.61000,     1.80500,     1.80500], 'Cu',   1],
                 [[-1.80500,    -1.80500,     3.61000], 'Cu',   1],
                 [[-1.80500,    -1.80500,    -3.61000], 'Cu',   1],
                 [[ 1.80500,     1.80500,    -3.61000], 'Cu',   1],
                 [[ 1.80500,    -1.80500,    -3.61000], 'Cu',   1],
                 [[ 1.80500,    -1.80500,     3.61000], 'Cu',   1],
                 [[-1.80500,     1.80500,    -3.61000], 'Cu',   1],
                 [[-1.80500,     1.80500,     3.61000], 'Cu',   1],
                 [[ 1.80500,     1.80500,     3.61000], 'Cu',   1],
                 [[ 3.61000,    -1.80500,    -1.80500], 'Cu',   1],
                 [[ 3.61000,    -3.61000,     0.00000], 'Cu',   1],
                 [[ 3.61000,     0.00000,    -3.61000], 'Cu',   1],
                 [[ 3.61000,     0.00000,     3.61000], 'Cu',   1],
                 [[-3.61000,     3.61000,     0.00000], 'Cu',   1],
                 [[ 0.00000,     3.61000,     3.61000], 'Cu',   1],
                 [[-3.61000,     0.00000,     3.61000], 'Cu',   1],
                 [[-3.61000,    -3.61000,     0.00000], 'Cu',   1],
                 [[ 0.00000,    -3.61000,     3.61000], 'Cu',   1],
                 [[-3.61000,     0.00000,    -3.61000], 'Cu',   1],
                 [[ 3.61000,     3.61000,     0.00000], 'Cu',   1],
                 [[ 0.00000,    -3.61000,    -3.61000], 'Cu',   1],
                 [[ 0.00000,     3.61000,    -3.61000], 'Cu',   1],
                 [[ 0.00000,    -5.41500,     1.80500], 'Cu',   1],
                 [[ 1.80500,    -5.41500,     0.00000], 'Cu',   1],
                 [[ 0.00000,    -5.41500,    -1.80500], 'Cu',   1],
                 [[-1.80500,     0.00000,     5.41500], 'Cu',   1],
                 [[-5.41500,     0.00000,    -1.80500], 'Cu',   1],
                 [[ 5.41500,    -1.80500,     0.00000], 'Cu',   1],
                 [[-1.80500,     5.41500,     0.00000], 'Cu',   1],
                 [[ 5.41500,     0.00000,    -1.80500], 'Cu',   1],
                 [[-5.41500,    -1.80500,     0.00000], 'Cu',   1],
                 [[ 1.80500,     5.41500,     0.00000], 'Cu',   1],
                 [[ 5.41500,     1.80500,     0.00000], 'Cu',   1],
                 [[ 0.00000,     5.41500,    -1.80500], 'Cu',   1],
                 [[ 0.00000,    -1.80500,    -5.41500], 'Cu',   1],
                 [[ 0.00000,     5.41500,     1.80500], 'Cu',   1],
                 [[ 1.80500,     0.00000,     5.41500], 'Cu',   1],
                 [[ 0.00000,     1.80500,     5.41500], 'Cu',   1],
                 [[ 5.41500,     0.00000,     1.80500], 'Cu',   1],
                 [[ 1.80500,     0.00000,    -5.41500], 'Cu',   1],
                 [[ 0.00000,     1.80500,    -5.41500], 'Cu',   1],
                 [[ 0.00000,    -1.80500,     5.41500], 'Cu',   1],
                 [[-5.41500,     0.00000,     1.80500], 'Cu',   1],
                 [[-5.41500,     1.80500,     0.00000], 'Cu',   1],
                 [[-1.80500,     0.00000,    -5.41500], 'Cu',   1],
                 [[-1.80500,    -5.41500,     0.00000], 'Cu',   1],
                 )

        self.__potentials = None
        self.__edge = 'K'
        self.__amplitude_reduction_factor = 0.9
        self.__effective_path_distance = 5.5

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


        feff_parameters = FEFFPhotonMatterInteractorParameters(
                atoms=self.__atoms,
                potentials=self.__potentials,
                edge=self.__edge,
                effective_path_distance=self.__effective_path_distance,
                amplitude_reduction_factor=self.__amplitude_reduction_factor)

        self.assertIsInstance( feff_parameters, FEFFPhotonMatterInteractorParameters )

        # Check attributes
        self.assertEqual( feff_parameters._FEFFPhotonMatterInteractorParameters__atoms, self.__atoms)
        self.assertEqual( feff_parameters._FEFFPhotonMatterInteractorParameters__potentials, self.__potentials)
        self.assertEqual( feff_parameters._FEFFPhotonMatterInteractorParameters__edge, self.__edge)
        self.assertEqual( feff_parameters._FEFFPhotonMatterInteractorParameters__amplitude_reduction_factor, self.__amplitude_reduction_factor)
        self.assertEqual( feff_parameters._FEFFPhotonMatterInteractorParameters__effective_path_distance, self.__effective_path_distance)

    def testDefaultConstruction(self):
        """ Testing that construction without arguments fails. """
        self.assertRaises( TypeError, FEFFPhotonMatterInteractorParameters )

    def testQueries(self):
        """ Test that all queries return the correct value. """

        feff_parameters = FEFFPhotonMatterInteractorParameters(
                atoms=self.__atoms,
                potentials=self.__potentials,
                edge=self.__edge,
                effective_path_distance=self.__effective_path_distance,
                amplitude_reduction_factor=self.__amplitude_reduction_factor)

        # Check queries.
        self.assertEqual( feff_parameters.atoms, self.__atoms)
        self.assertEqual( feff_parameters.potentials, self.__potentials)
        self.assertEqual( feff_parameters.edge, self.__edge)
        self.assertEqual( feff_parameters.amplitude_reduction_factor, self.__amplitude_reduction_factor)
        self.assertEqual( feff_parameters.effective_path_distance, self.__effective_path_distance)

    def testFinalization(self):
        """ That that the finalization flag is set correctly. """
        feff_parameters = FEFFPhotonMatterInteractorParameters(
                atoms=self.__atoms,
                potentials=self.__potentials,
                edge=self.__edge,
                effective_path_distance=self.__effective_path_distance,
                amplitude_reduction_factor=self.__amplitude_reduction_factor)

        # Is finalized after construction.
        self.assertTrue(feff_parameters.finalized)

        # Change a parameter
        feff_parameters.edge='L1'
        self.assertFalse(feff_parameters.finalized)

        # Finalize.
        feff_parameters.finalize()
        self.assertTrue(feff_parameters.finalized)

    def testSetters(self):
        """ Test that setting parameters works correctly. """

        # Construct the object.
        feff_parameters = FEFFPhotonMatterInteractorParameters(
                atoms=self.__atoms,
                potentials=self.__potentials,
                edge=self.__edge,
                effective_path_distance=self.__effective_path_distance,
                amplitude_reduction_factor=self.__amplitude_reduction_factor)

        # Set new parameters.
        feff_parameters.atoms = self.__atoms[:10]
        feff_parameters.potentials = None
        feff_parameters.edge = 'L2'
        feff_parameters.amplitude_reduction_factor = 0.1
        feff_parameters.effective_path_distance = 5.0

         # Check attributes
        self.assertEqual( feff_parameters._FEFFPhotonMatterInteractorParameters__atoms, self.__atoms[:10])
        self.assertEqual( feff_parameters._FEFFPhotonMatterInteractorParameters__potentials, None )
        self.assertEqual( feff_parameters._FEFFPhotonMatterInteractorParameters__edge, 'L2' )
        self.assertEqual( feff_parameters._FEFFPhotonMatterInteractorParameters__amplitude_reduction_factor, 0.1 )
        self.assertEqual( feff_parameters._FEFFPhotonMatterInteractorParameters__effective_path_distance, 5.0 )

    def testCheckAndSetAtoms(self):
        """ Test the atom check and set utility. """

        # None
        self.assertRaises( TypeError, _checkAndSetAtoms, None )
        # Wrong type
        self.assertRaises( TypeError, _checkAndSetAtoms, 1 )
        # Empty
        self.assertRaises( TypeError, _checkAndSetAtoms, [] )
        # Wrong shape
        self.assertRaises( TypeError, _checkAndSetAtoms, [1.0, 'Cu', 0] )
        # [0] not an iterable
        self.assertRaises( TypeError, _checkAndSetAtoms, [[0.0, 'Cu', 0]] )
        ## [0] not of length 3
        self.assertRaises( TypeError, _checkAndSetAtoms, [[[0.0, 0.1], 'Cu', 0]] )
        # [1] not symbol
        self.assertRaises( TypeError, _checkAndSetAtoms, [[[0.0, 0.0, 0.0], 29, 0]] )
        # [1] not a correct symbol
        self.assertRaises( ValueError, _checkAndSetAtoms, [[[0.0, 0.0, 0.0], 'Xx', 0]] )
        # [2] not integer
        self.assertRaises( TypeError, _checkAndSetAtoms, [[[0.0, 0.0, 0.0], 'Cu', 'i']] )
        # 0 not in potential indices.
        self.assertRaises( ValueError, _checkAndSetAtoms, [[[0.0, 0.0, 0.0], 'Cu', 1]] )
        # Two 0's in potential indices.
        self.assertRaises( ValueError, _checkAndSetAtoms, [[[0.0, 0.0, 0.0], 'Cu', 0],[[0.1, 0.2, 0.3], 'Cu', 0]] )
        # Index missing.
        self.assertRaises( ValueError, _checkAndSetAtoms, [[[0.0, 0.0, 0.0], 'Cu', 0],[[0.1, 0.2, 0.3], 'Cu', 2]] )

        # Ok.
        self.assertEqual( _checkAndSetAtoms ([[[0.0, 0.0, 0.0], 'Cu', 0]]), [[[0.0, 0.0, 0.0], 'Cu', 0]] )

    def testCheckAndSetPotentials(self):
        """ Test the potential check and set utility. """

        # None.
        self.assertIs( _checkAndSetPotentials( None ), None)

        # Anything but None.
        self.assertRaises( ValueError, _checkAndSetPotentials, [[0, 29, 'Cu'], [1, 29, 'Cu']] )

    def testCheckAndSetEdge(self):
        """ Test the edge check and set utility. """

        # None.
        self.assertEqual( _checkAndSetEdge(None), 'K' )

        # Not a string
        self.assertRaises( TypeError, _checkAndSetEdge, 0 )

        # Not a valid edge designator.
        self.assertRaises( ValueError, _checkAndSetEdge, 'L' )

        # Lower case works.
        self.assertEqual( _checkAndSetEdge('k'), 'K' )
        # Ok.
        self.assertEqual( _checkAndSetEdge('L1'), 'L1' )

    def testCheckAndSetAmplitudeReductionFactor(self):
        """ Test the amplitude reduction factor check and set utility. """

        # None.
        self.assertEqual( _checkAndSetAmplitudeReductionFactor( None ), 1.0 )
        # Wrong type.
        self.assertRaises( TypeError, _checkAndSetAmplitudeReductionFactor, 'a' )
        # Outside range.
        self.assertRaises( ValueError, _checkAndSetAmplitudeReductionFactor, -1.4 )
        self.assertRaises( ValueError, _checkAndSetAmplitudeReductionFactor, 2.4 )

        # Int ok.
        self.assertEqual( _checkAndSetAmplitudeReductionFactor( 1 ), 1.0 )
        self.assertEqual( _checkAndSetAmplitudeReductionFactor( 0 ), 0.0 )

        # Float ok.
        self.assertEqual( _checkAndSetAmplitudeReductionFactor( 0.5), 0.5 )

    def testCheckAndSetEffectivePathDistance(self):
        """ Test the effective path distance check and set utility. """

        # None.
        self.assertEqual( _checkAndSetEffectivePathDistance( None ), None )
        # Wrong type.
        self.assertRaises( TypeError, _checkAndSetEffectivePathDistance, 'a' )
        # Outside range.
        self.assertRaises( ValueError, _checkAndSetEffectivePathDistance, -1.4 )

        # Int ok.
        self.assertEqual( _checkAndSetEffectivePathDistance( 1 ), 1.0 )
        self.assertEqual( _checkAndSetEffectivePathDistance( 0 ), 0.0 )
        self.assertEqual( _checkAndSetEffectivePathDistance( 2 ), 2.0 )

        # Float ok.
        self.assertEqual( _checkAndSetEffectivePathDistance( 0.5), 0.5 )

    def testFinalize(self):
        # Setup parameters.
        feff_parameters = FEFFPhotonMatterInteractorParameters(
                atoms=self.__atoms,
                potentials=self.__potentials,
                edge=self.__edge,
                effective_path_distance=5.5,
                amplitude_reduction_factor=1.0,
                )

        # Get potential list.
        potential_list = feff_parameters._FEFFPhotonMatterInteractorParameters__potential_list

        self.assertEqual( potential_list, [[0,29,'Cu'],[1,29,'Cu']] )

    def testSerialize(self):
        """ Check that the serialize() method produces a valid feff.inp file."""

        # Setup parameters.
        feff_parameters = FEFFPhotonMatterInteractorParameters(
                atoms=self.__atoms,
                potentials=self.__potentials,
                edge=self.__edge,
                effective_path_distance=5.5,
                amplitude_reduction_factor=1.0,
                )

        # Setup a stream to write to.
        stream = io.StringIO()
        feff_parameters._serialize( stream = stream )

        # Compare to reference.
        reference_inp = """EDGE    K
S02     1.000000
CONTROL 1 1 1 1 1 1
PRINT   0 0 0 0 0 0
RPATH   5.500000
EXAFS

POTENTIALS
0      29      Cu
1      29      Cu

ATOMS
0.00000      0.00000      0.00000      0
0.00000      1.80500      -1.80500      1
-1.80500      -1.80500      0.00000      1
1.80500      0.00000      -1.80500      1
0.00000      -1.80500      1.80500      1
1.80500      1.80500      0.00000      1
0.00000      -1.80500      -1.80500      1
-1.80500      1.80500      0.00000      1
0.00000      1.80500      1.80500      1
-1.80500      0.00000      -1.80500      1
-1.80500      0.00000      1.80500      1
1.80500      0.00000      1.80500      1
1.80500      -1.80500      0.00000      1
0.00000      -3.61000      0.00000      1
0.00000      0.00000      -3.61000      1
0.00000      0.00000      3.61000      1
-3.61000      0.00000      0.00000      1
3.61000      0.00000      0.00000      1
0.00000      3.61000      0.00000      1
-1.80500      3.61000      1.80500      1
1.80500      3.61000      1.80500      1
-1.80500      -3.61000      -1.80500      1
-1.80500      3.61000      -1.80500      1
1.80500      3.61000      -1.80500      1
-1.80500      -3.61000      1.80500      1
-3.61000      1.80500      -1.80500      1
1.80500      -3.61000      1.80500      1
3.61000      1.80500      -1.80500      1
-3.61000      1.80500      1.80500      1
-3.61000      -1.80500      -1.80500      1
3.61000      -1.80500      1.80500      1
1.80500      -3.61000      -1.80500      1
-3.61000      -1.80500      1.80500      1
3.61000      1.80500      1.80500      1
-1.80500      -1.80500      3.61000      1
-1.80500      -1.80500      -3.61000      1
1.80500      1.80500      -3.61000      1
1.80500      -1.80500      -3.61000      1
1.80500      -1.80500      3.61000      1
-1.80500      1.80500      -3.61000      1
-1.80500      1.80500      3.61000      1
1.80500      1.80500      3.61000      1
3.61000      -1.80500      -1.80500      1
3.61000      -3.61000      0.00000      1
3.61000      0.00000      -3.61000      1
3.61000      0.00000      3.61000      1
-3.61000      3.61000      0.00000      1
0.00000      3.61000      3.61000      1
-3.61000      0.00000      3.61000      1
-3.61000      -3.61000      0.00000      1
0.00000      -3.61000      3.61000      1
-3.61000      0.00000      -3.61000      1
3.61000      3.61000      0.00000      1
0.00000      -3.61000      -3.61000      1
0.00000      3.61000      -3.61000      1
0.00000      -5.41500      1.80500      1
1.80500      -5.41500      0.00000      1
0.00000      -5.41500      -1.80500      1
-1.80500      0.00000      5.41500      1
-5.41500      0.00000      -1.80500      1
5.41500      -1.80500      0.00000      1
-1.80500      5.41500      0.00000      1
5.41500      0.00000      -1.80500      1
-5.41500      -1.80500      0.00000      1
1.80500      5.41500      0.00000      1
5.41500      1.80500      0.00000      1
0.00000      5.41500      -1.80500      1
0.00000      -1.80500      -5.41500      1
0.00000      5.41500      1.80500      1
1.80500      0.00000      5.41500      1
0.00000      1.80500      5.41500      1
5.41500      0.00000      1.80500      1
1.80500      0.00000      -5.41500      1
0.00000      1.80500      -5.41500      1
0.00000      -1.80500      5.41500      1
-5.41500      0.00000      1.80500      1
-5.41500      1.80500      0.00000      1
-1.80500      0.00000      -5.41500      1
-1.80500      -5.41500      0.00000      1
END"""

        comp = stream.getvalue()
        self.assertEqual( comp, reference_inp )

##############################
# NO TESTS BENEATH THIS LINE #
##############################
if __name__ == '__main__':
    unittest.main()

