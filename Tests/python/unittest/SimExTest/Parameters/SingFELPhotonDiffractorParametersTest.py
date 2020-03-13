""" :module: Test module hosting the test for the SingFELPhotonDiffractorParameter class."""
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

from SimEx.Parameters.AbstractCalculatorParameters import AbstractCalculatorParameters
from SimEx.Parameters.SingFELPhotonDiffractorParameters import SingFELPhotonDiffractorParameters
from SimEx.Parameters.DetectorGeometry import DetectorGeometry, DetectorPanel
from SimEx.Parameters.PhotonBeamParameters import PhotonBeamParameters
from SimEx.Utilities.Units import meter, electronvolt, joule


from TestUtilities.TestUtilities import generateTestFilePath


class SingFELPhotonDiffractorParametersTest(unittest.TestCase):
    """
    Test class for the SingFELPhotonDiffractorParameters class.
    """

    @classmethod
    def setUpClass(cls):
        detector_panel = DetectorPanel(ranges={'fast_scan_min': 0,
                                               'fast_scan_max': 1023,
                                               'slow_scan_min': 0,
                                               'slow_scan_max': 1023},
                                       pixel_size=2.2e-4*meter,
                                       photon_response=1.0,
                                       distance_from_interaction_plane=0.13*meter,
                                       corners={'x': -512, 'y': 512},
                                       )

        cls.detector_geometry = DetectorGeometry(panels=[detector_panel])

        cls.beam = PhotonBeamParameters(
                                    photon_energy=8.6e3*electronvolt,
                                    beam_diameter_fwhm=1.0e-6*meter,
                                    pulse_energy=1.0e-3*joule,
                                    photon_energy_relative_bandwidth=0.001,
                                    divergence=None,
                                    photon_energy_spectrum_type="SASE",
                                )

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
        """ Testing the default construction of the class using a dictionary. """

        # Attempt to construct an instance of the class.
        parameters = SingFELPhotonDiffractorParameters(
                sample=generateTestFilePath("2nip.pdb")
                )

        # Check instance and inheritance.
        self.assertIsInstance(parameters, SingFELPhotonDiffractorParameters)
        self.assertIsInstance(parameters, AbstractCalculatorParameters)

        # Check all parameters are set to default values.
        self.assertEqual(parameters.uniform_rotation, False)
        self.assertFalse(parameters.calculate_Compton)
        self.assertEqual(parameters.slice_interval, 100)
        self.assertEqual(parameters.number_of_slices, 1)
        self.assertEqual(parameters.pmi_start_ID, 1)
        self.assertEqual(parameters.pmi_stop_ID, 1)
        self.assertEqual(parameters.beam_parameters, None)
        self.assertEqual(parameters.detector_geometry, None)

    def testConstructionWithGeometry(self):
        """ Testing the construction of the class with a DetectorGeometry instance. """

        # Attempt to construct an instance of the class.
        parameters = SingFELPhotonDiffractorParameters(detector_geometry=self.detector_geometry,
                                                       sample=generateTestFilePath("2nip.pdb"),
                )

        # Check instance and inheritance.
        self.assertIsInstance(parameters, SingFELPhotonDiffractorParameters)
        self.assertIsInstance(parameters, AbstractCalculatorParameters)

        # Check all parameters are set to default values.
        self.assertEqual(parameters.uniform_rotation, False)
        self.assertFalse(parameters.calculate_Compton)
        self.assertEqual(parameters.slice_interval, 100)
        self.assertEqual(parameters.number_of_slices, 1)
        self.assertEqual(parameters.pmi_start_ID, 1)
        self.assertEqual(parameters.pmi_stop_ID, 1)
        self.assertEqual(parameters.beam_parameters, None)
        self.assertEqual(parameters.detector_geometry, self.detector_geometry)

    def testConstructionWithBeamParameters(self):
        """ Testing the construction of the class with a PhotonBeamParameters instance. """

        # Attempt to construct an instance of the class.
        parameters = SingFELPhotonDiffractorParameters(detector_geometry=self.detector_geometry,
                                                       beam_parameters=self.beam,
                                                       sample=generateTestFilePath("2nip.pdb")
                                                       )

        # Check instance and inheritance.
        self.assertIsInstance(parameters, SingFELPhotonDiffractorParameters)
        self.assertIsInstance(parameters, AbstractCalculatorParameters)

        # Check all parameters are set to default values.
        self.assertEqual(parameters.uniform_rotation, False)
        self.assertFalse(parameters.calculate_Compton)
        self.assertEqual(parameters.slice_interval, 100)
        self.assertEqual(parameters.number_of_slices, 1)
        self.assertEqual(parameters.pmi_start_ID, 1)
        self.assertEqual(parameters.pmi_stop_ID, 1)
        self.assertEqual(parameters.beam_parameters, self.beam)
        self.assertEqual(parameters.detector_geometry, self.detector_geometry)

    def testConstructionWithSample(self):
        """ Testing the construction of the class with a PhotonBeamParameters instance. """

        # Attempt to construct an instance of the class.
        parameters = SingFELPhotonDiffractorParameters(
                sample=generateTestFilePath('2nip.pdb'),
                detector_geometry=self.detector_geometry,
                beam_parameters=self.beam
                )

        # Check instance and inheritance.
        self.assertIsInstance(parameters, SingFELPhotonDiffractorParameters)
        self.assertIsInstance(parameters, AbstractCalculatorParameters)

        # Check all parameters are set to default values.
        self.assertEqual(parameters.sample, generateTestFilePath('2nip.pdb'))
        self.assertEqual(parameters.uniform_rotation, False)
        self.assertFalse(parameters.calculate_Compton)
        self.assertEqual(parameters.slice_interval, 100)
        self.assertEqual(parameters.number_of_slices, 1)
        self.assertEqual(parameters.pmi_start_ID, 1)
        self.assertEqual(parameters.pmi_stop_ID, 1)
        self.assertEqual(parameters.beam_parameters, self.beam)
        self.assertEqual(parameters.detector_geometry, self.detector_geometry)

    def test_construction_exceptions(self):
        """ Test that exceptions are thrown if parameters not sane. """
        # Setup parameters that are ok
        parameters = SingFELPhotonDiffractorParameters(
                     uniform_rotation= True,
                     calculate_Compton = False,
                     slice_interval = 100,
                     number_of_slices = 2,
                     pmi_start_ID = 1,
                     pmi_stop_ID  = 1,
                     number_of_diffraction_patterns = 2,
                     beam_parameters = self.beam,
                     detector_geometry = self.detector_geometry,
                     forced_mpi_command='mpirun -np 2',
                     )

        # uniform_rotation not a bool.
        raises = False
        try:
            parameters.uniform_rotation =  1
        except TypeError:
            raises = True
        self.assertTrue(raises)
        # Reset.
        parameters.uniform_rotation = True
        raises = False

        # calculate_Compton not a bool.
        try:
            parameters.calculate_Compton= 1 
        except TypeError:
            raises = True
        self.assertTrue(raises)

        # Reset.
        parameters.calculate_Compton = False
        raises = False

        # slice_interval not positive integer.
        try:
            parameters.slice_interval= 'one'
        except TypeError:
            raises = True
        self.assertTrue(raises)
        raises = False

        try:
            parameters.slice_interval=-1 
        except ValueError:
            raises = True
        self.assertTrue(raises)
        raises = False

        # slice_interval not a number
        # Reset.
        parameters.slice_interval = 1
        # number_of_slices not positive integer.
        try:
            parameters.number_of_slices= -1
        except ValueError:
            raises = True
        self.assertTrue(raises)
        raises = False

        # number_of_slices not a number
        try:
            parameters.number_of_slices = 'one'
        except TypeError:
            raises = True
        self.assertTrue(raises)
        raises = False

        # Reset.
        parameters.number_of_slices = 2
        # number_of_diffraction_patterns not positive integer.
        try:
            parameters.number_of_diffraction_patterns = -1
        except ValueError:
            raises = True
        self.assertTrue(raises)
        raises = False

        # number_of_diffraction_patterns not a number
        try:
            parameters.number_of_diffraction_patterns = 'one'
        except TypeError:
            raises = True
        self.assertTrue(raises)
        raises = False

        # Reset.
        parameters.number_of_diffraction_patterns = 2

        # pmi_start_ID not positive integer.
        try:
            parameters.pmi_start_ID = -1
        except ValueError:
            raises = True
        self.assertTrue(raises)
        raises = False

        # pmi_start_ID not a number
        try:
            parameters.pmi_start_ID = 'one'
        except TypeError:
            raises = True
        self.assertTrue(raises)
        raises = False

        # Reset.
        parameters.pmi_start_ID = 1

        # pmi_stop_ID not positive integer.
        try:
            parameters.pmi_stop_ID = -1
        except ValueError:
            raises = True
        self.assertTrue(raises)
        raises = False

        # pmi_stop_ID not a number
        try:
            parameters.pmi_stop_ID = 'one'
        except TypeError:
            raises = True
        self.assertTrue(raises)
        raises = False

        # Reset.
        parameters.pmi_stop_ID = 1

        # beam_parameters not a string.
        try:
            parameters.beam_parameters = 1
        except TypeError:
            raises = True
        self.assertTrue(raises)
        raises = False

        # beam_parameters not a file.
        try:
            parameters.beam_parameters = 'xyz.beam'
        except IOError:
            raises = True
        self.assertTrue(raises)
        raises = False

        parameters.beam_parameters =  self.beam

        # detector_geometry not a string.
        try:
            parameters.detector_geometry = 1
        except TypeError:
            raises = True
        self.assertTrue(raises)
        raises = False

        # detector_geometry not a file.
        try:
            parameters.detector_geometry = 'xyz.geom'
        except TypeError:
            raises = True
        self.assertTrue(raises)
        raises = False

        parameters.detector_geometry = self.detector_geometry

    def testLegacyDictionary(self):
        """ Check parameter object can be initialized via a old-style dictionary. """
        parameters_dict = {'uniform_rotation'               : False,
                           'calculate_Compton'              : True,
                           'slice_interval'                 : 12,
                           'number_of_slices'               : 2,
                           'pmi_start_ID'                   : 4,
                           'pmi_stop_ID'                    : 5,
                           'number_of_diffraction_patterns' : 2,
                           'beam_parameters'                : None,
                           'detector_geometry'              : self.detector_geometry,
                           'number_of_MPI_processes'        : 4,  # Legacy, has no effect.
                           'sample'                         : generateTestFilePath('2nip.pdb')
                           }

        parameters = SingFELPhotonDiffractorParameters(**parameters_dict)

        # Check all parameters are set correctly.
        self.assertFalse(parameters.uniform_rotation)
        self.assertTrue(parameters.calculate_Compton)
        self.assertEqual(parameters.slice_interval, 12)
        self.assertEqual(parameters.number_of_slices, 2)
        self.assertEqual(parameters.pmi_start_ID, 4)
        self.assertEqual(parameters.pmi_stop_ID, 5)
        self.assertEqual(parameters.beam_parameters, None)
        self.assertEqual(parameters.detector_geometry, self.detector_geometry)
        self.assertEqual(parameters.sample, generateTestFilePath('2nip.pdb'))

if __name__ == '__main__':
    unittest.main()
