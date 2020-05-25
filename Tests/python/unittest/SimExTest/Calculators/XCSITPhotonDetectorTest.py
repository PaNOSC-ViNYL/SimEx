""" Test module for the XCSITPhotonDetector."""
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

import os
import h5py
import shutil

# Include needed directories in sys.path.
import unittest

# Import the class to test.
from SimEx.Calculators.XCSITPhotonDetector import XCSITPhotonDetector
from SimEx.Calculators.SingFELPhotonDiffractor import SingFELPhotonDiffractor
from SimEx.Parameters.XCSITPhotonDetectorParameters import XCSITPhotonDetectorParameters
from SimEx.Parameters.PhotonBeamParameters import PhotonBeamParameters
from SimEx.Parameters.DetectorGeometry import DetectorGeometry, DetectorPanel
from SimEx.Parameters.SingFELPhotonDiffractorParameters import SingFELPhotonDiffractorParameters
from SimEx.Calculators.AbstractPhotonDetector import AbstractPhotonDetector
from SimEx.Utilities import Units
from SimEx.Analysis.DiffractionAnalysis import DiffractionAnalysis, mpl
from TestUtilities import TestUtilities

@unittest.skipIf(TestUtilities.runs_on_travisCI(), "CI.")
class XCSITPhotonDetectorTest(unittest.TestCase):
    """
    Test class for the XCSITPhotonDetector class.
    """

    @classmethod
    def setUpClass(cls):
        """ Setting up the test class. """

        cls._parameters = XCSITPhotonDetectorParameters(
                detector_type="AGIPDSPB",
                )

    @classmethod
    def tearDownClass(cls):
        """ Tearing down the test class. """

        del cls._parameters

    def setUp(self):
        """ Setting up a test. """
        #self.__files_to_remove = ["detector_out.h5"]
        self.__files_to_remove = []
        self.__dirs_to_remove = []

        self._detector = XCSITPhotonDetector(
                parameters=self._parameters,
                input_path=TestUtilities.generateTestFilePath("diffr/diffr_out_0000001.h5"),
                output_path="detector_out.h5",
                )

    def tearDown(self):
        """ Tearing down a test. """
        for f in self.__files_to_remove:
            if os.path.isfile(f):
                os.remove(f)
        for d in self.__dirs_to_remove:
            if os.path.isdir(d):
                shutil.rmtree(d)

    def testShapedConstruction(self):
        """ Testing the construction of the class with parameters. """

        # Setup parameters.
        parameters=XCSITPhotonDetectorParameters(detector_type="AGIPDSPB")

        # Check construction fails without parameters.
        self.assertRaises( AttributeError, XCSITPhotonDetector )

        # Check construction fails without input_path.
        self.assertRaises( AttributeError, XCSITPhotonDetector, parameters )

        # Construct the object.
        diffractor = XCSITPhotonDetector(parameters=parameters, input_path=TestUtilities.generateTestFilePath("diffr"))

        # Check correct default handling for output_path:
        self.assertEqual( os.path.split(diffractor.output_path)[-1], "detector_out.h5")

        # Check type.
        self.assertIsInstance(diffractor, XCSITPhotonDetector)
        self.assertIsInstance(diffractor, AbstractPhotonDetector)

    def testReadH5(self):
        """ Test the readH5 method."""

        # Get a fresh detector.
        detector = self._detector
        detector.parameters.patterns = range(10)

        # Read the data.
        detector._readH5()

        # Check data shapes
        self.assertEqual(len(detector.getPhotonData()), 10)

    def testCreateXCSITInteractions(self):
        """ """

        # Get a fresh detector.
        detector = self._detector

        # Read the data.
        detector._readH5()

        # Check data shapes
        self.assertEqual(len(detector.getPhotonData()), 1)

        # Get interactions.
        detector._XCSITPhotonDetector__createXCSITInteractions()
        interactions = detector.getInteractionData()

        # Check.
        self.assertIsNotNone(interactions)

    def testCreateXCSITInteractionsMultiPatterns(self):
        """ """

        # Get a fresh detector.
        detector = self._detector
        detector.parameters.patterns = range(10)

        # Read the data.
        detector._readH5()

        # Check data shapes
        self.assertEqual(len(detector.getPhotonData()), 10)

        # Get interactions.
        detector._XCSITPhotonDetector__createXCSITInteractions()
        interactions = detector.getInteractionData()

        # Check.
        self.assertIsNotNone(interactions)

    def testBackengineIA(self):
        """ """
        # Get a fresh detector.
        detector = self._detector

        # Read the data.
        detector._readH5()

        # Check data shapes
        self.assertEqual(len(detector.getPhotonData()), 1)

        # Get interactions.
        detector._XCSITPhotonDetector__createXCSITInteractions()

        backengineIA_ret = detector._XCSITPhotonDetector__backengineIA()

        self.assertTrue(backengineIA_ret)

        self.assertEqual(len(detector.getInteractionData()), 1)

    def failingtestBackengineIAMultiPatternsFails(self):
        """ """

        # Get a fresh detector.
        detector = self._detector
        detector.parameters.patterns = range(10)

        # Read the data.
        detector._readH5()

        # Check data shapes
        self.assertEqual(len(detector.getPhotonData()), 10)

        # Get interactions.
        detector._XCSITPhotonDetector__createXCSITInteractions()

        backengineIA_ret = detector._XCSITPhotonDetector__backengineIA()

        self.assertTrue(backengineIA_ret)

        self.assertEqual(len(detector.getInteractionData()), 10)

    def testBackengineCP(self):
        """ """

        # Get a fresh detector.
        detector = self._detector

        # Read the data.
        detector._readH5()

        # Check data shapes
        self.assertEqual(len(detector.getPhotonData()), 1)

        # Get interactions.
        detector._XCSITPhotonDetector__createXCSITInteractions()

        # Simualte interactions
        self.assertTrue(detector._XCSITPhotonDetector__backengineIA())

        # Create charge matrices.
        detector._XCSITPhotonDetector__createXCSITChargeMatrix()

        # Run the charge simulation.
        self.assertTrue(detector._XCSITPhotonDetector__backengineCP())

    def testMinimalExample(self):
        """ Check that beam parameters can be taken from a given propagation output file."""

        detector = self._detector
        detector.parameters.patterns = range(1)

        detector._readH5()
        detector.backengine()
        detector.saveH5()

        # Assert output was created.
        self.assertTrue(os.path.isfile("detector_out.h5"))

        # Check if we can read the output.
        with h5py.File( "detector_out.h5") as h5:
            self.assertIn( "data", list(h5.keys()) )
            self.assertIn( "0000032", list(h5["data"].keys()) )
            self.assertIn( "data", list(h5["data/0000032"].keys()) )

    def testAGIPDQuad(self):
        """ Check numbers for 1 AGIPD Quad. """

        # Cleanup.
        self.__files_to_remove.append('5mzd.pdb')
        self.__files_to_remove.append('diffr.h5')
        self.__dirs_to_remove.append('diffr')

        # Avoid crash due to multiple instances of G4RunManager
        del self._detector

        # Setup detector geometry.
        detector_panel = DetectorPanel( ranges={'fast_scan_min' : 0,
                                                'fast_scan_max' : 511,
                                                'slow_scan_min' : 0,
                                                'slow_scan_max' : 511},
                                        pixel_size=2.2e-4*Units.meter,
                                        photon_response=1.0,
                                        distance_from_interaction_plane=0.13*Units.meter,
                                        corners={'x': -256, 'y' : -256},
                                        )

        detector_geometry = DetectorGeometry(panels=[detector_panel])

        # Setup photon beam.
        beam = PhotonBeamParameters(
                                    photon_energy=4.96e3*Units.electronvolt,
                                    beam_diameter_fwhm=1.0e-6*Units.meter,
                                    pulse_energy=1.0e-3*Units.joule,
                                    photon_energy_relative_bandwidth=0.001,
                                    divergence=1e-3*Units.radian,
                                    photon_energy_spectrum_type="SASE",
                                    )

        # Setup and run the diffraction sim.
        diffraction_parameters=SingFELPhotonDiffractorParameters(
                uniform_rotation=None,
                calculate_Compton=False,
                number_of_diffraction_patterns=1,
                detector_geometry=detector_geometry,
                beam_parameters=beam,
                sample="5mzd.pdb",
                forced_mpi_command='mpirun -np 1',
              )

        photon_diffractor = SingFELPhotonDiffractor(
                parameters=diffraction_parameters,
                output_path='diffr',
                )

        photon_diffractor.backengine()
        photon_diffractor.saveH5()

        parameters = XCSITPhotonDetectorParameters(
                detector_type="AGIPDSPB",
                patterns=[0],
                )

        detector = XCSITPhotonDetector(
                parameters=parameters,
                input_path="diffr.h5",
                output_path="detector_out.h5",
                )

        detector._readH5()
        detector.backengine()
        detector.saveH5()

        # Weak test Check we have photons in the signal.
        pattern = h5py.File("detector_out.h5", 'r')['data/0000001/data'].value


        self.assertGreater(pattern.sum(), 10)

    def plot_diffr_vs_detector(self):
        """ Compare patterns before and after detector sim. """

        # Cleanup.
        #self.__files_to_remove.append('5mzd.pdb')
        #self.__files_to_remove.append('diffr.h5')
        #self.__dirs_to_remove.append('diffr')

        # Avoid crash due to multiple instances of G4RunManager
        del self._detector

        # Setup detector geometry.
        detector_panel = DetectorPanel( ranges={'fast_scan_min' : 0,
                                                'fast_scan_max' : 511,
                                                'slow_scan_min' : 0,
                                                'slow_scan_max' : 511},
                                        pixel_size=2.2e-4*Units.meter,
                                        photon_response=1.0,
                                        distance_from_interaction_plane=0.13*Units.meter,
                                        corners={'x': -256, 'y' : -256},
                                        )

        detector_geometry = DetectorGeometry(panels=[detector_panel])

        # Setup photon beam.
        beam = PhotonBeamParameters(
                                    photon_energy=4.96e3*Units.electronvolt,
                                    beam_diameter_fwhm=1.0e-6*Units.meter,
                                    pulse_energy=1.0e-3*Units.joule,
                                    photon_energy_relative_bandwidth=0.001,
                                    divergence=1e-3*Units.radian,
                                    photon_energy_spectrum_type="SASE",
                                    )

        # Setup and run the diffraction sim.
        diffraction_parameters=SingFELPhotonDiffractorParameters(
                uniform_rotation=None,
                calculate_Compton=False,
                number_of_diffraction_patterns=1,
                detector_geometry=detector_geometry,
                beam_parameters=beam,
                sample="5mzd.pdb",
                forced_mpi_command='mpirun -np 1',
              )

        photon_diffractor = SingFELPhotonDiffractor(
                parameters=diffraction_parameters,
                output_path='diffr',
                )

        photon_diffractor.backengine()
        photon_diffractor.saveH5()

        analysis1 = DiffractionAnalysis(photon_diffractor.output_path, pattern_indices=[1], poissonize=True)
        analysis1.plotPattern(operation=None, logscale=False, )

        parameters = XCSITPhotonDetectorParameters(
                detector_type="AGIPDSPB",
                patterns=[0],
                )

        detector = XCSITPhotonDetector(
                parameters=parameters,
                input_path="diffr.h5",
                output_path="detector_out.h5",
                )

        detector._readH5()
        detector.backengine()
        detector.saveH5()

        # Weak test Check we have photons in the signal.
        pattern = h5py.File("detector_out.h5", 'r')['data/0000001/data'].value

        analysis2 = DiffractionAnalysis(detector.output_path, pattern_indices=[1], poissonize=True)
        analysis2.plotPattern(operation=None, logscale=False, )

        mpl.pyplot.show()



if __name__ == '__main__':
    unittest.main()
