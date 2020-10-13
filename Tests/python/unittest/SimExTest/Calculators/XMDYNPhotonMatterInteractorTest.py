""" Test module for the XMDYNPhotonMatterInteractor. """
##########################################################################
#                                                                        #
# Copyright (C) 2015 - 2020 Carsten Fortmann-Grote                       #
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
import numpy
import os
import shutil
import unittest

# Import the class to test.
from SimEx.Calculators.XMDYNPhotonMatterInteractor import XMDYNPhotonMatterInteractor
from SimEx.Parameters.PhotonMatterInteractorParameters import PhotonMatterInteractorParameters
from SimEx.Parameters.PhotonBeamParameters import PhotonBeamParameters
from TestUtilities import TestUtilities
from TestUtilities.TestUtilities import runs_on_travisCI
from SimEx.Utilities import Units

class XMDYNPhotonMatterInteractorTest(unittest.TestCase):
    """
    Test class for the XMDYNPhotonMatterInteractor class.
    """

    @classmethod
    def setUpClass(cls):
        """ Setting up the test class. """
        cls.input_h5 = TestUtilities.generateTestFilePath('prop_out_0000001.h5')
        cls.input_xmdyn_dir = TestUtilities.generateTestFilePath('xmdyn_run')

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

    def testConstructionRootPathNone(self):
        """ Testing the construction of the class with a given root path. """

        # Setup pmi parameters.
        pmi_parameters = {'number_of_trajectories' : 1,
                         }

        interactor = XMDYNPhotonMatterInteractor(
                parameters=pmi_parameters,
                output_path='pmi_out',
                input_path=TestUtilities.generateTestFilePath('prop_out_0000001.5'),
                sample_path=TestUtilities.generateTestFilePath('sample.h5'),
                root_path=None,
                )

        self.assertIn('root.', interactor.root_path)

    def testConstructionRootPath(self):
        """ Testing the construction of the class with a given root path. """

        # Setup pmi parameters.
        pmi_parameters = {'number_of_trajectories' : 1,
                         }

        interactor = XMDYNPhotonMatterInteractor(
                parameters=pmi_parameters,
                output_path='pmi_out',
                input_path=TestUtilities.generateTestFilePath('prop_out_0000001.5'),
                sample_path=TestUtilities.generateTestFilePath('sample.h5'),
                root_path='root.0000001',
                )
        self.assertEqual(interactor.root_path, 'root.0000001')

    def testConstructionWithDict(self):
        """ Testing the construction of the class with a parameter dictionary. """

        # Setup pmi parameters.
        pmi_parameters = {'number_of_trajectories' : 1,
                         }

        interactor = XMDYNPhotonMatterInteractor(
                parameters=pmi_parameters,
                output_path='pmi_out',
                input_path=TestUtilities.generateTestFilePath('prop_out_0000001.5'),
                sample_path=TestUtilities.generateTestFilePath('sample.h5'),
                )

        self.assertIsInstance(interactor, XMDYNPhotonMatterInteractor)

    def testConstructionWithParametersNoProp(self):
        """ Testing the construction of the class with a parameter dictionary without propagation input. """

        beam = PhotonBeamParameters(
                photon_energy = 8.6e3*Units.electronvolt,
                pulse_energy=1.5e-3*Units.joule,
                photon_energy_relative_bandwidth=1e-4,
                divergence=1.0e-3*Units.radian,
                beam_diameter_fwhm=5.0e-3*Units.meter,
                )

         # Setup pmi parameters.
        pmi_parameters = PhotonMatterInteractorParameters(
                number_of_trajectories=1,
                beam_parameters=beam,
                )

        interactor = XMDYNPhotonMatterInteractor(
                parameters=pmi_parameters,
                output_path='pmi_out',
                sample_path=TestUtilities.generateTestFilePath('sample.h5'),
                )

        self.assertIsInstance(interactor, XMDYNPhotonMatterInteractor)

    def testConstructionWithParameters(self):
        """ Testing the construction of the class with a parameter object. """

        # Setup pmi parameters.
        pmi_parameters = PhotonMatterInteractorParameters(
                number_of_trajectories=1,
                )

        interactor = XMDYNPhotonMatterInteractor(parameters=pmi_parameters,
                                                     output_path='pmi_out',
                                                     input_path=TestUtilities.generateTestFilePath('prop_out_0000001.h5'),
                                                     sample_path=TestUtilities.generateTestFilePath('sample.h5'),
                                                     )

        self.assertIsInstance(interactor, XMDYNPhotonMatterInteractor)

    @unittest.skipIf(runs_on_travisCI(), "xmdyn not available on travisCI.")
    def testBackengineMultipleProp(self):
        """ Check that the backengine method works correctly. """

        # Prepare input.
        shutil.copytree( TestUtilities.generateTestFilePath('prop_out'), os.path.abspath( 'prop' ) )
        self.__dirs_to_remove.append( 'prop' )
        self.__dirs_to_remove.append( 'pmi' )

        parameters = PhotonMatterInteractorParameters(number_of_trajectories=1)
        test_interactor = XMDYNPhotonMatterInteractor(
                parameters=parameters,
                input_path='prop',
                output_path='pmi',
                sample_path=TestUtilities.generateTestFilePath('sample.h5') )

        # Call backengine
        status = test_interactor.backengine()

        # Check that the backengine returned zero.
        self.assertEqual(status, 0)

        # Check we have generated the expected output.
        self.assertIn( 'pmi_out_0000001.h5' , os.listdir( test_interactor.output_path ) )

    @unittest.skipIf(runs_on_travisCI(), "xmdyn not available on travisCI.")
    def testBackengine(self):
        """ Check that the backengine method works correctly. """

        # Clean up.
        self.__dirs_to_remove.append('prop')
        self.__dirs_to_remove.append( 'pmi' )

        # Get test instance.
        pmi_parameters = {
                'number_of_trajectories' : 1,
                         }

        test_interactor = XMDYNPhotonMatterInteractor(parameters=pmi_parameters,
                                                          input_path=self.input_h5,
                                                          output_path='pmi',
                                                          sample_path = TestUtilities.generateTestFilePath('sample.h5') )

        #self.__dirs_to_remove.append(test_interactor.root_path)
        # Call backengine
        status = test_interactor.backengine()

        self.assertTrue(os.path.isdir(test_interactor.output_path))

        # Check that the backengine returned zero.
        self.assertEqual(status, 0)

        # Check we have generated the expected output.
        self.assertTrue( 'pmi_out_0000001.h5' in os.listdir( test_interactor.output_path ) )

    @unittest.skip("Not implemented.")
    def test_load_snapshot_from_dir(self):
        """ Test loading a xmdyn snapshot from a directory that contains xmdyn output. """

        pmi = XMDYNPhotonMatterInteractor(load_from_path=TestUtilities.generateTestFilePath('xmdyn_run'), output_path = 'pmi')

        snapshot = pmi.f_load_snp_from_dir(os.path.join(self.input_xmdyn_dir, 'snp', '1280'.zfill(8)))

        self.assertIsInstance(snapshot, dict)

        expected_keys = ['Z',
                'T',
                'uid',
                'r',
                'v',
                'm',
                'q',
                'f0',
                'Q',
                ]

        present_keys = snapshot.keys()
        for k in expected_keys:
            self.assertIn(k, present_keys)


if __name__ == '__main__':
    unittest.main()

