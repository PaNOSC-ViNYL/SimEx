""" Test module for the SingFELPhotonDiffractor."""
##########################################################################
#                                                                        #
# Copyright (C) 2015-2018 Carsten Fortmann-Grote                         #
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
import numpy
import shutil

# Include needed directories in sys.path.
import unittest

# Import the class to test.
from SimEx.Calculators.SingFELPhotonDiffractor import SingFELPhotonDiffractor
from SimEx.Parameters.SingFELPhotonDiffractorParameters import SingFELPhotonDiffractorParameters
from SimEx.Parameters.DetectorGeometry import DetectorGeometry, DetectorPanel
from SimEx.Parameters.PhotonBeamParameters import PhotonBeamParameters
from SimEx.Utilities.Units import meter, electronvolt, joule, radian
from TestUtilities import TestUtilities

TRAVIS = TestUtilities.runs_on_travisCI()

class SingFELPhotonDiffractorTest(unittest.TestCase):
    """
    Test class for the SingFELPhotonDiffractor class.
    """

    @classmethod
    def setUpClass(cls):
        """ Setting up the test class. """
        cls.input_h5 = TestUtilities.generateTestFilePath('pmi_out_0000001.h5')
        detector_panel = DetectorPanel( ranges={'fast_scan_min' : 0,
                                                'fast_scan_max' : 21,
                                                'slow_scan_min' : 0,
                                                'slow_scan_max' : 21},
                                        pixel_size=2.2e-4*meter,
                                        photon_response=1.0,
                                        distance_from_interaction_plane=0.13*meter,
                                        corners={'x': -11, 'y' : -11},
                                        )

        cls.detector_geometry = DetectorGeometry(panels=[detector_panel])

        cls.beam = PhotonBeamParameters(photon_energy=8.6e3*electronvolt,
                                    beam_diameter_fwhm=1.0e-6*meter,
                                    pulse_energy=1.0e-3*joule,
                                    photon_energy_relative_bandwidth=0.001,
                                    divergence=1e-3*radian,
                                    photon_energy_spectrum_type="SASE",
                                    )

    @classmethod
    def tearDownClass(cls):
        """ Tearing down the test class. """
        del cls.input_h5
        files_to_remove = ['tmp.beam', 'tmp.geom', 'template.in']
        for f in files_to_remove:
            if os.path.isfile(f):
                os.remove(f)

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

    def testShapedConstructionDict(self):
        """ Testing the construction of the class with parameters given as a dict. """

        parameters=SingFELPhotonDiffractorParameters(uniform_rotation=True,
                                                       calculate_Compton=False,
                                                       slice_interval=100,
                                                       number_of_slices=2,
                                                       pmi_start_ID=1,
                                                       pmi_stop_ID=1,
                                                       number_of_diffraction_patterns=2,
                                                       beam_parameters=self.beam,
                                                       detector_geometry=self.detector_geometry,
                                                       )

        # Construct the object.
        diffractor = SingFELPhotonDiffractor(parameters=parameters, input_path=self.input_h5, output_path='diffr_out.h5')

        self.assertIsInstance(diffractor, SingFELPhotonDiffractor)

    def testConstructionParameters(self):
        """ Check we can construct with a parameter object. """
        parameters=SingFELPhotonDiffractorParameters(uniform_rotation=True,
                                                       calculate_Compton=False,
                                                       slice_interval=100,
                                                       number_of_slices=2,
                                                       pmi_start_ID=1,
                                                       pmi_stop_ID=1,
                                                       number_of_diffraction_patterns=2,
                                                       beam_parameters=self.beam,
                                                       detector_geometry=self.detector_geometry,
                                                       )
        diffractor = SingFELPhotonDiffractor(parameters=parameters, input_path=self.input_h5, output_path='diffr_out.h5')

        # Check instance.
        self.assertIsInstance( diffractor, SingFELPhotonDiffractor )

    def testShapedConstruction2(self):
        """ Testing the construction of the class with parameters. """

        parameters=SingFELPhotonDiffractorParameters(uniform_rotation=True,
                                                       calculate_Compton=False,
                                                       slice_interval=100,
                                                       number_of_slices=2,
                                                       pmi_start_ID=1,
                                                       pmi_stop_ID=1,
                                                       number_of_diffraction_patterns=2,
                                                       beam_parameters=self.beam,
                                                       detector_geometry=self.detector_geometry,
                                                       )

        # Construct the object.
        diffractor = SingFELPhotonDiffractor(parameters=parameters, input_path=self.input_h5, output_path='diffr_out.h5')

        self.assertIsInstance(diffractor, SingFELPhotonDiffractor)

    def testDefaultConstruction(self):
        """ Testing the default construction of the class. """

        # Prepare input.
        shutil.copytree( TestUtilities.generateTestFilePath( 'pmi_out' ), os.path.abspath( 'pmi' ) )

        # Ensure proper cleanup.
        self.__dirs_to_remove.append( os.path.abspath( 'pmi') )
        self.__dirs_to_remove.append( os.path.abspath( 'diffr' ) )

        # Set up parameters.
        parameters=SingFELPhotonDiffractorParameters(uniform_rotation=True,
                                                       calculate_Compton=False,
                                                       slice_interval=100,
                                                       number_of_slices=2,
                                                       pmi_start_ID=1,
                                                       pmi_stop_ID=1,
                                                       number_of_diffraction_patterns=2,
                                                       beam_parameters=self.beam,
                                                       detector_geometry=self.detector_geometry,
                                                       )
        # Construct the object.
        diffractor = SingFELPhotonDiffractor(parameters=parameters, input_path='pmi')

        self.assertIsInstance(diffractor, SingFELPhotonDiffractor)
        self.assertEqual( diffractor.output_path, os.path.abspath( 'diffr') )

    def testConstructionWithSample(self):
        """ Testing the construction with sample passed via parameters."""

        # Ensure proper cleanup.
        sample_file = TestUtilities.generateTestFilePath('2nip.pdb')
        self.__dirs_to_remove.append( os.path.abspath( 'diffr' ) )

        # Set up parameters.
        parameters=SingFELPhotonDiffractorParameters(
                sample=sample_file,
                uniform_rotation = False,
                calculate_Compton = False,
                slice_interval = 100,
                number_of_slices = 5,
                pmi_start_ID = 1,
                pmi_stop_ID = 1,
                number_of_diffraction_patterns= 1,
                beam_parameters=self.beam,
                detector_geometry= self.detector_geometry,
                forced_mpi_command='mpirun'
                )

        # Construct the object.
        diffractor = SingFELPhotonDiffractor(parameters=parameters)

        self.assertIsInstance(diffractor, SingFELPhotonDiffractor)
        self.assertEqual( diffractor.input_path,  os.path.abspath( sample_file ) )
        self.assertEqual( diffractor.output_path, os.path.abspath( 'diffr') )

    @unittest.skipIf(TRAVIS, "CI.")
    def testH5Output(self):
        """ Test that data, params and misc are present in hdf5 output file. """

        # Ensure proper cleanup.
        sample_file = TestUtilities.generateTestFilePath('2nip.pdb')
        self.__dirs_to_remove.append( os.path.abspath( 'diffr' ) )
        self.__files_to_remove.append( os.path.abspath( 'diffr.h5' ) )

        # Set up parameters.
        parameters=SingFELPhotonDiffractorParameters(
                sample=sample_file,
                uniform_rotation = False,
                calculate_Compton = False,
                slice_interval = 100,
                number_of_slices = 3,
                pmi_start_ID = 1,
                pmi_stop_ID = 1,
                number_of_diffraction_patterns= 2,
                beam_parameters=self.beam,
                detector_geometry= self.detector_geometry,
                forced_mpi_command='mpirun -np 2',
                )

        # Construct the object.
        diffractor = SingFELPhotonDiffractor(parameters=parameters)

        # Run and save.
        diffractor.backengine()
        diffractor.saveH5()

        # Examine content of results hdf.
        with h5py.File(diffractor.output_path, 'r') as h5:
            # Datagroups in /"
            self.assertIn("data", h5.keys())
            self.assertIn("params", h5.keys())
            self.assertIn("misc", h5.keys())

            # Data.
            data = h5["data"]
            self.assertIn("0000001", data.keys())

            # Parameters
            params = h5["params"]
            self.assertIn("beam", params.keys())
            self.assertIn("geom", params.keys())

            # Beam
            beam = h5["params/beam"]
            self.assertIn("focusArea", beam.keys())
            self.assertIn("photonEnergy", beam.keys())

            # Geometry
            geom = h5["params/geom"]
            self.assertIn("detectorDist", geom.keys())
            self.assertIn("mask", geom.keys())
            self.assertIn("pixelHeight", geom.keys())
            self.assertIn("pixelWidth", geom.keys())

    def testDefaultConstructionLegacy(self):
        """ Testing the default construction of the class with MPI parameter. """

        # Prepare input.
        shutil.copytree( TestUtilities.generateTestFilePath( 'pmi_out' ), os.path.abspath( 'pmi' ) )

        # Ensure proper cleanup.
        self.__dirs_to_remove.append( os.path.abspath( 'pmi') )
        self.__dirs_to_remove.append( os.path.abspath( 'diffr' ) )

        # Set up parameters.
        parameters=SingFELPhotonDiffractorParameters(
                sample=None,
                uniform_rotation = False,
                calculate_Compton = False,
                slice_interval = 100,
                number_of_slices = 3,
                pmi_start_ID = 1,
                pmi_stop_ID = 1,
                number_of_diffraction_patterns= 2,
                beam_parameters=self.beam,
                detector_geometry= self.detector_geometry,
                forced_mpi_command='mpirun -np 2',
                )
        # Construct the object.
        diffractor = SingFELPhotonDiffractor(parameters=parameters, input_path='pmi')

        # Check type.
        self.assertIsInstance(diffractor, SingFELPhotonDiffractor)

        # Check default output_path.
        self.assertEqual( diffractor.output_path, os.path.abspath( 'diffr') )

    def testConstructionExceptions(self):
        """ Check that proper exceptions are thrown if object is constructed incorrectly. """
        # Parameter not a parameters object.
        self.assertRaises( TypeError, SingFELPhotonDiffractor, 1, self.input_h5, 'diffr.h5')

    @unittest.skipIf(TRAVIS, "CI.")
    def testBackengine(self):
        """ Test that we can start a test calculation. """

        # Cleanup.
        self.__dirs_to_remove.append('diffr')

        parameters = SingFELPhotonDiffractorParameters(
                     uniform_rotation= True,
                     calculate_Compton = False,
                     slice_interval = 100,
                     number_of_slices = 2,
                     pmi_start_ID = 1,
                     pmi_stop_ID  = 1,
                     number_of_diffraction_patterns = 2,
                     beam_parameters=self.beam,
                     detector_geometry=self.detector_geometry,
                     forced_mpi_command='mpirun -np 2',
                     )

        # Construct the object.
        diffractor = SingFELPhotonDiffractor(parameters=parameters, input_path=self.input_h5, output_path='diffr')

        # Call backengine.
        status = diffractor.backengine()

        # Check successful completion.
        self.assertEqual(status, 0)

    @unittest.skipIf(TRAVIS, "CI.")
    def testBackengineNoBeam(self):
        """ Test that we can start a test calculation with no explicit beam parameters. """

        # Cleanup.
        self.__dirs_to_remove.append('diffr')

        parameters = SingFELPhotonDiffractorParameters(
                     uniform_rotation= True,
                     calculate_Compton = False,
                     slice_interval = 100,
                     number_of_slices = 2,
                     pmi_start_ID = 1,
                     pmi_stop_ID  = 1,
                     number_of_diffraction_patterns = 2,
                     beam_parameters=None,
                     detector_geometry=self.detector_geometry,
                     forced_mpi_command='mpirun -np 2',
                     )

        # Construct the object.
        diffractor = SingFELPhotonDiffractor(parameters=parameters, input_path=self.input_h5, output_path='diffr')

        # Call backengine.
        status = diffractor.backengine()

        # Check successful completion.
        self.assertEqual(status, 0)

    @unittest.skipIf(TRAVIS, "CI.")
    def testBackengineDefaultPaths(self):
        """ Test that we can start a calculation with default paths given. """

        # Prepare input.
        shutil.copytree( TestUtilities.generateTestFilePath( 'pmi_out' ), os.path.abspath( 'pmi' ) )

        # Ensure proper cleanup.
        self.__dirs_to_remove.append( os.path.abspath( 'pmi') )
        self.__dirs_to_remove.append( os.path.abspath( 'diffr' ) )

        parameters = SingFELPhotonDiffractorParameters(
                     uniform_rotation=True,
                     calculate_Compton=False,
                     slice_interval=100,
                     number_of_slices=2,
                     pmi_start_ID=1,
                     pmi_stop_ID=1,
                     number_of_diffraction_patterns= 2,
                     detector_geometry= self.detector_geometry,
                     forced_mpi_command='mpirun -np 2',
                     )

        # Construct the object.
        diffractor = SingFELPhotonDiffractor(parameters=parameters, input_path='pmi')

        # Call backengine.
        status = diffractor.backengine()

        # Check successful completion.
        self.assertEqual(status, 0)

        # Check expected files exist.
        self.assertTrue( os.path.isdir( os.path.abspath( 'diffr' ) ) )
        self.assertIn( 'diffr_out_0000001.h5', os.listdir( os.path.abspath( 'diffr' ) ) )

    @unittest.skipIf(TRAVIS, "CI.")
    def testBackengineWithSample(self):
        """ Test that we can start a test calculation if the sample was given via the parameters . """

        # Cleanup.
        sample_file = TestUtilities.generateTestFilePath('2nip.pdb')
        self.__dirs_to_remove.append('diffr')

        # Make sure sample file does not exist.
        if sample_file in os.listdir( os.getcwd() ):
            os.remove( sample_file )

        parameters = SingFELPhotonDiffractorParameters(
                     sample=sample_file,
                     uniform_rotation = False,
                     calculate_Compton = False,
                     number_of_diffraction_patterns=2,
                     beam_parameters=self.beam,
                     detector_geometry= self.detector_geometry,
                     forced_mpi_command='mpirun -np 2 -x OMP_NUM_THREADS=2',
                     )

        # Construct the object.
        diffractor = SingFELPhotonDiffractor(
                parameters=parameters,
                input_path=None,
                output_path='diffr'
                )

        # Call backengine.
        status = diffractor.backengine()

        # Check successful completion.
        self.assertEqual(status, 0)

        # Check expected files exist.
        self.assertTrue( os.path.isdir( os.path.abspath( 'diffr' ) ) )
        self.assertIn( 'diffr_out_0000001.h5', os.listdir( diffractor.output_path ) )
        self.assertIn( 'diffr_out_0000002.h5', os.listdir( diffractor.output_path ) )

    @unittest.skipIf(TRAVIS, "CI.")
    def testBackengineInputFile(self):
        """ Test that we can start a test calculation if the input path is a single file. """

        # Cleanup.
        self.__dirs_to_remove.append('diffr')

        parameters = SingFELPhotonDiffractorParameters(
                     uniform_rotation=True,
                     calculate_Compton=False,
                     slice_interval=100,
                     number_of_slices=2,
                     pmi_start_ID=1,
                     pmi_stop_ID=1,
                     number_of_diffraction_patterns= 2,
                     detector_geometry= self.detector_geometry,
                     forced_mpi_command='mpirun -np 2 -x OMP_NUM_THREADS=2',
                     )


        # Construct the object.
        diffractor = SingFELPhotonDiffractor(parameters=parameters, input_path=self.input_h5, output_path='diffr')

        # Call backengine.
        status = diffractor.backengine()

        # Check successful completion.
        self.assertEqual(status, 0)

    @unittest.skipIf(TRAVIS, "CI.")
    def testBackengineInputDir(self):
        """ Test that we can start a test calculation if the input path is a directory. """

        # Cleanup.
        self.__dirs_to_remove.append('diffr')

        parameters = SingFELPhotonDiffractorParameters(
                     uniform_rotation=True,
                     calculate_Compton=False,
                     slice_interval=100,
                     number_of_slices=2,
                     pmi_start_ID=1,
                     pmi_stop_ID=1,
                     number_of_diffraction_patterns= 2,
                     detector_geometry= self.detector_geometry,
                     forced_mpi_command='mpirun -np 2',
                     )

        # Construct the object.
        diffractor = SingFELPhotonDiffractor(parameters=parameters, input_path=TestUtilities.generateTestFilePath('pmi_out'), output_path='diffr')

        # Call backengine.
        status = diffractor.backengine()

        # Check successful completion.
        self.assertEqual(status, 0)

    @unittest.skipIf(TRAVIS, "CI.")
    def testBug53(self):
        """ Tests a script that was found to raise if run in parallel mode. """

        self.__dirs_to_remove.append('diffr')

        diffraction_parameters = SingFELPhotonDiffractorParameters(
                     uniform_rotation= True,
                     calculate_Compton= True,
                     slice_interval= 100,
                     number_of_slices= 2,
                     pmi_start_ID= 1,
                     pmi_stop_ID = 9,
                     number_of_diffraction_patterns=2,
                     detector_geometry= self.detector_geometry,
                     forced_mpi_command='mpirun -np 2',
                   )

        photon_diffractor = SingFELPhotonDiffractor(
                parameters=diffraction_parameters,
                input_path=TestUtilities.generateTestFilePath('pmi_out'),
                output_path='diffr')

        photon_diffractor.backengine()

    @unittest.skipIf(TRAVIS, "CI.")
    def testSingleFile(self):
        """ Test that saveH5() generates only one linked hdf. """


        parameters=SingFELPhotonDiffractorParameters(
                sample=None,
                uniform_rotation = False,
                calculate_Compton = False,
                slice_interval = 100,
                number_of_slices = 3,
                pmi_start_ID = 1,
                pmi_stop_ID = 1,
                number_of_diffraction_patterns= 8,
                beam_parameters=self.beam,
                detector_geometry= self.detector_geometry,
                forced_mpi_command='mpirun -np 8',
                )

        photon_diffractor = SingFELPhotonDiffractor(
                parameters=parameters,
                input_path=TestUtilities.generateTestFilePath('pmi_out'),
                output_path='diffr_newstyle')

        # Cleanup.
        self.__dirs_to_remove.append(photon_diffractor.output_path)

        # Run backengine and convert files.
        photon_diffractor.backengine()
        photon_diffractor.saveH5()

        # Cleanup new style files.
        self.__files_to_remove.append(photon_diffractor.output_path)

        # Check that only one file was generated.
        self.assertTrue( os.path.isfile( photon_diffractor.output_path ))

        # Open the file for reading.
        h5_filehandle = h5py.File( photon_diffractor.output_path, 'r')

        # Count groups under /data.
        number_of_patterns = len(list(h5_filehandle['data'].keys()))

        self.assertEqual( number_of_patterns, 8 )

        # Assert global metadata is present.
        self.assertIn("params", list(h5_filehandle.keys()) )
        self.assertIn("version", list(h5_filehandle.keys()) )
        self.assertIn("info", list(h5_filehandle.keys()) )

    @unittest.skipIf(TRAVIS, "CI.")
    def testNoRotation(self):
        """ Test that we can run singfel with no-rotation option."""


        diffraction_parameters=SingFELPhotonDiffractorParameters(uniform_rotation = None,
                                                       calculate_Compton = False,
                                                       slice_interval = 100,
                                                       number_of_slices = 3,
                                                       pmi_start_ID = 1,
                                                       pmi_stop_ID  = 1,
                                                       number_of_diffraction_patterns = 2,
                                                       detector_geometry = self.detector_geometry,
                                                       forced_mpi_command='mpirun -np 2',
                                                       )

        photon_diffractor = SingFELPhotonDiffractor(
                parameters=diffraction_parameters,
                input_path=TestUtilities.generateTestFilePath('pmi_out'),
                output_path='diffr_newstyle')

        # Cleanup.
        #self.__dirs_to_remove.append(photon_diffractor.output_path)

        # Run backengine and convert files.
        # Ensure removal of directory.
        self.__dirs_to_remove.append(photon_diffractor.output_path)

        photon_diffractor.backengine()
        photon_diffractor.saveH5()

        # Cleanup new style files.
        # Ensure removal of linked hdf.
        self.__files_to_remove.append(photon_diffractor.output_path)

        with h5py.File(photon_diffractor.output_path) as handle:
            pattern = handle['data/0000001/diffr'].value

        # 2nd run.
        photon_diffractor = SingFELPhotonDiffractor(
                parameters=diffraction_parameters,
                input_path=TestUtilities.generateTestFilePath('pmi_out'),
                output_path='diffr_newstyle')


        # Run backengine and convert files.
        photon_diffractor.backengine()
        photon_diffractor.saveH5()

        with h5py.File(photon_diffractor.output_path) as handle:
            new_pattern = handle['data/0000001/diffr'].value

        self.assertAlmostEqual(numpy.linalg.norm(pattern-new_pattern), 0.0, 5)


if __name__ == '__main__':
    unittest.main()

