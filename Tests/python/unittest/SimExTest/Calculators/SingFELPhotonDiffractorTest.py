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
from SimEx.Calculators.XMDYNPhotonMatterInteractor import XMDYNPhotonMatterInteractor
from SimEx.Parameters.SingFELPhotonDiffractorParameters import SingFELPhotonDiffractorParameters
from SimEx.Parameters.DetectorGeometry import DetectorGeometry, DetectorPanel
from SimEx.Parameters.PhotonBeamParameters import PhotonBeamParameters
from SimEx.Utilities.Units import meter, electronvolt, joule, radian
from TestUtilities import TestUtilities

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

        parameters={ 'uniform_rotation': True,
                     'calculate_Compton' : False,
                     'slice_interval' : 100,
                     'number_of_slices' : 2,
                     'pmi_start_ID' : 1,
                     'pmi_stop_ID'  : 1,
                     'number_of_diffraction_patterns' : 2,
                     'beam_parameters' : self.beam,
                     'detector_geometry' : self.detector_geometry,
                   }

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

        parameters={ 'uniform_rotation': True,
                     'calculate_Compton' : False,
                     'slice_interval' : 100,
                     'number_of_slices' : 2,
                     'pmi_start_ID' : 1,
                     'pmi_stop_ID'  : 1,
                     'number_of_diffraction_patterns' : 2,
                     'beam_parameters' : self.beam,
                     'detector_geometry' : self.detector_geometry,
                   }

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
        parameters={ 'uniform_rotation': True,
                     'calculate_Compton' : False,
                     'slice_interval' : 100,
                     'number_of_slices' : 2,
                     'pmi_start_ID' : 1,
                     'pmi_stop_ID'  : 1,
                     'number_of_diffraction_patterns' : 2,
                     'beam_parameters' : None,
                     'detector_geometry' : self.detector_geometry,
                   }
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

    def testH5Output(self):
        """ Test that data, params and misc are present in hdf5 output file. """

        # Ensure proper cleanup.
        sample_file = TestUtilities.generateTestFilePath('2nip.pdb')
        #self.__dirs_to_remove.append( os.path.abspath( 'diffr' ) )

        # Set up parameters.
        parameters=SingFELPhotonDiffractorParameters(
                sample=sample_file,
                uniform_rotation = False,
                calculate_Compton = False,
                slice_interval = 100,
                number_of_slices = 3,
                pmi_start_ID = 1,
                pmi_stop_ID = 1,
                number_of_diffraction_patterns= 1,
                beam_parameters=self.beam,
                detector_geometry= self.detector_geometry,
                forced_mpi_command='mpirun -np 1'
                )

        # Construct the object.
        diffractor = SingFELPhotonDiffractor(parameters=parameters)
        diffractor.backengine()
        diffractor.saveH5()

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
        parameters={ 'uniform_rotation': True,
                     'calculate_Compton' : False,
                     'slice_interval' : 100,
                     'number_of_slices' : 2,
                     'pmi_start_ID' : 1,
                     'pmi_stop_ID'  : 1,
                     'number_of_diffraction_patterns' : 2,
                     'beam_parameters' : None,
                     'detector_geometry' : self.detector_geometry,
                     'number_of_MPI_processes' : 2,
                   }
        # Construct the object.
        diffractor = SingFELPhotonDiffractor(parameters=parameters, input_path='pmi')

        # Check type.
        self.assertIsInstance(diffractor, SingFELPhotonDiffractor)

        # Check default output_path.
        self.assertEqual( diffractor.output_path, os.path.abspath( 'diffr') )

    def testConstructionExceptions(self):
        """ Check that proper exceptions are thrown if object is constructed incorrectly. """
        # Parameter not a dict.
        self.assertRaises( TypeError, SingFELPhotonDiffractor, 1, self.input_h5, 'diffr.h5')

        # Setup parameters that are ok
        parameters={ 'uniform_rotation': True,
                     'calculate_Compton' : False,
                     'slice_interval' : 100,
                     'number_of_slices' : 2,
                     'pmi_start_ID' : 1,
                     'pmi_stop_ID'  : 1,
                     'number_of_diffraction_patterns' : 2,
                     'beam_parameters' : self.beam,
                     'detector_geometry' : self.detector_geometry,
                     }

        # Check construction with sane parameters.
        singfel = SingFELPhotonDiffractor( parameters, self.input_h5, 'diffr.h5')
        self.assertIsInstance( singfel, SingFELPhotonDiffractor )

        # uniform_rotation not a bool.
        parameters['uniform_rotation'] = 1
        self.assertRaises( TypeError, SingFELPhotonDiffractor, parameters, self.input_h5, 'diffr.h5')
        # Reset.
        parameters['uniform_rotation'] = True

        # calculate_Compton not a bool.
        parameters['calculate_Compton'] = 1
        self.assertRaises( TypeError, SingFELPhotonDiffractor, parameters, self.input_h5, 'diffr.h5')
        # Reset.
        parameters['calculate_Compton'] = False

        # slice_interval not positive integer.
        parameters['slice_interval'] = -1
        self.assertRaises( ValueError, SingFELPhotonDiffractor, parameters, self.input_h5, 'diffr.h5')
        # slice_interval not a number
        parameters['slice_interval'] = 'one'
        self.assertRaises( TypeError, SingFELPhotonDiffractor, parameters, self.input_h5, 'diffr.h5')
        # Reset.
        parameters['slice_interval'] = 1

        # number_of_slices not positive integer.
        parameters['number_of_slices'] = -1
        self.assertRaises( ValueError, SingFELPhotonDiffractor, parameters, self.input_h5, 'diffr.h5')
        # number_of_slices not a number
        parameters['number_of_slices'] = 'one'
        self.assertRaises( TypeError, SingFELPhotonDiffractor, parameters, self.input_h5, 'diffr.h5')
        # Reset.
        parameters['number_of_slices'] = 2

        # number_of_diffraction_patterns not positive integer.
        parameters['number_of_diffraction_patterns'] = -1
        self.assertRaises( ValueError, SingFELPhotonDiffractor, parameters, self.input_h5, 'diffr.h5')
        # number_of_diffraction_patterns not a number
        parameters['number_of_diffraction_patterns'] = 'one'
        self.assertRaises( TypeError, SingFELPhotonDiffractor, parameters, self.input_h5, 'diffr.h5')
        # Reset.
        parameters['number_of_diffraction_patterns'] = 2

        # pmi_start_ID not positive integer.
        parameters['pmi_start_ID'] = -1
        self.assertRaises( ValueError, SingFELPhotonDiffractor, parameters, self.input_h5, 'diffr.h5')
        # pmi_start_ID not a number
        parameters['pmi_start_ID'] = 'one'
        self.assertRaises( TypeError, SingFELPhotonDiffractor, parameters, self.input_h5, 'diffr.h5')
        # Reset.
        parameters['pmi_start_ID'] = 1

        # pmi_stop_ID not positive integer.
        parameters['pmi_stop_ID'] = -1
        self.assertRaises( ValueError, SingFELPhotonDiffractor, parameters, self.input_h5, 'diffr.h5')
        # pmi_stop_ID not a number
        parameters['pmi_stop_ID'] = 'one'
        self.assertRaises( TypeError, SingFELPhotonDiffractor, parameters, self.input_h5, 'diffr.h5')
        # Reset.
        parameters['pmi_stop_ID'] = 1

        # beam_parameters not a string.
        parameters['beam_parameters'] = 1
        self.assertRaises( TypeError, SingFELPhotonDiffractor, parameters, self.input_h5, 'diffr.h5')
        # beam_parameters not a file.
        parameters['beam_parameters'] = 'xyz.beam'
        self.assertRaises( IOError, SingFELPhotonDiffractor, parameters, self.input_h5, 'diffr.h5')
        parameters['beam_parameters'] =  self.beam

        # detector_geometry not a string.
        parameters['detector_geometry'] = 1
        self.assertRaises( TypeError, SingFELPhotonDiffractor, parameters, self.input_h5, 'diffr.h5')
        # detector_geometry not a file.
        parameters['detector_geometry'] = 'xyz.geom'
        self.assertRaises( IOError, SingFELPhotonDiffractor, parameters, self.input_h5, 'diffr.h5')
        parameters['detector_geometry'] = self.detector_geometry


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
                     beam_parameters = self.beam,
                     detector_geometry = self.detector_geometry,
                     forced_mpi_command='mpirun',
                     )

        # Construct the object.
        diffractor = SingFELPhotonDiffractor(parameters=parameters, input_path=self.input_h5, output_path='diffr')

        # Call backengine.
        status = diffractor.backengine()

        # Check successful completion.
        self.assertEqual(status, 0)

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
                     beam_parameters = None,
                     detector_geometry = self.detector_geometry,
                     )

        # Construct the object.
        diffractor = SingFELPhotonDiffractor(parameters=parameters, input_path=self.input_h5, output_path='diffr')

        # Call backengine.
        status = diffractor.backengine()

        # Check successful completion.
        self.assertEqual(status, 0)

    def testBackengineDefaultPaths(self):
        """ Test that we can start a calculation with default paths given. """

        # Prepare input.
        shutil.copytree( TestUtilities.generateTestFilePath( 'pmi_out' ), os.path.abspath( 'pmi' ) )

        # Ensure proper cleanup.
        self.__dirs_to_remove.append( os.path.abspath( 'pmi') )
        self.__dirs_to_remove.append( os.path.abspath( 'diffr' ) )

        parameters = SingFELPhotonDiffractorParameters(
                     uniform_rotation = True,
                     calculate_Compton = False,
                     slice_interval = 100,
                     number_of_slices = 2,
                     pmi_start_ID = 1,
                     pmi_stop_ID = 1,
                     number_of_diffraction_patterns= 2,
                     detector_geometry= self.detector_geometry,
                     forced_mpi_command='mpirun')

        # Construct the object.
        diffractor = SingFELPhotonDiffractor(parameters=parameters, input_path='pmi')

        # Call backengine.
        status = diffractor.backengine()

        # Check successful completion.
        self.assertEqual(status, 0)

        # Check expected files exist.
        self.assertTrue( os.path.isdir( os.path.abspath( 'diffr' ) ) )
        self.assertIn( 'diffr_out_0000001.h5', os.listdir( os.path.abspath( 'diffr' ) ) )

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
                     forced_mpi_command='mpirun -np 2 -x OMP_NUM_THREADS=2'
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

    def testBackengineInputFile(self):
        """ Test that we can start a test calculation if the input path is a single file. """

        # Cleanup.
        self.__dirs_to_remove.append('diffr')

        parameters = SingFELPhotonDiffractorParameters(
                     uniform_rotation = True,
                     calculate_Compton = False,
                     slice_interval = 100,
                     number_of_slices = 2,
                     pmi_start_ID = 1,
                     pmi_stop_ID = 1,
                     number_of_diffraction_patterns= 2,
                     detector_geometry= self.detector_geometry,
                     forced_mpi_command='mpirun')


        # Construct the object.
        diffractor = SingFELPhotonDiffractor(parameters=parameters, input_path=self.input_h5, output_path='diffr')

        # Call backengine.
        status = diffractor.backengine()

        # Check successful completion.
        self.assertEqual(status, 0)

    def testBackengineInputDir(self):
        """ Test that we can start a test calculation if the input path is a directory. """

        # Cleanup.
        self.__dirs_to_remove.append('diffr')

        parameters = SingFELPhotonDiffractorParameters(
                     uniform_rotation = True,
                     calculate_Compton = False,
                     slice_interval = 100,
                     number_of_slices = 2,
                     pmi_start_ID = 1,
                     pmi_stop_ID = 1,
                     number_of_diffraction_patterns= 2,
                     detector_geometry= self.detector_geometry,
                     forced_mpi_command='mpirun',
                     )

        # Construct the object.
        diffractor = SingFELPhotonDiffractor(parameters=parameters, input_path=TestUtilities.generateTestFilePath('pmi_out'), output_path='diffr')

        # Call backengine.
        status = diffractor.backengine()

        # Check successful completion.
        self.assertEqual(status, 0)

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
                     number_of_diffraction_patterns= 1,
                     detector_geometry= self.detector_geometry,
                   )

        photon_diffractor = SingFELPhotonDiffractor(
                parameters=diffraction_parameters,
                input_path=TestUtilities.generateTestFilePath('pmi_out'),
                output_path='diffr')

        photon_diffractor.backengine()

    def testSingleFile(self):
        """ Test that saveH5() generates only one linked hdf. """


        diffraction_parameters={ 'uniform_rotation': True,
                     'calculate_Compton' : True,
                     'slice_interval' : 100,
                     'number_of_slices' : 2,
                     'pmi_start_ID' : 1,
                     'pmi_stop_ID'  : 4,
                     'number_of_diffraction_patterns' : 2,
                     'beam_parameters' : None,
                     'detector_geometry' : self.detector_geometry,
                     'number_of_MPI_processes' : 8,
                   }

        photon_diffractor = SingFELPhotonDiffractor(
                parameters=diffraction_parameters,
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

    def testNoRotation(self):
        """ Test that we can run singfel with no-rotation option."""


        diffraction_parameters=SingFELPhotonDiffractorParameters(uniform_rotation = None,
                                                       calculate_Compton = False,
                                                       slice_interval = 100,
                                                       number_of_slices = 3,
                                                       pmi_start_ID = 1,
                                                       pmi_stop_ID  = 1,
                                                       number_of_diffraction_patterns = 1,
                                                       detector_geometry = self.detector_geometry
                                                       )

        photon_diffractor = SingFELPhotonDiffractor(
                parameters=diffraction_parameters,
                input_path=TestUtilities.generateTestFilePath('pmi_out'),
                output_path='diffr_newstyle')

        # Cleanup.
        #self.__dirs_to_remove.append(photon_diffractor.output_path)

        # Run backengine and convert files.
        photon_diffractor.backengine()
        photon_diffractor.saveH5()

        # Cleanup new style files.
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

        self.assertAlmostEqual(numpy.linalg.norm(pattern-new_pattern), 0.0, 10)

    def test_with_xmdyn_out(self):

        """ Check we can process a pmi file generated by XMDYNPhotonMatterInteractor from a non-s2e xmdyn run. """

        self.__files_to_remove.append('pmi_out_0000001.h5')
        self.__dirs_to_remove.append('diffr_out')
        # Locate xmdyn output.
        pmi_out_dir = TestUtilities.generateTestFilePath('xmdyn_run')

        # Construct PMI Calculator.
        pmi = XMDYNPhotonMatterInteractor(load_from_path=pmi_out_dir, output_path='pmi_out_0000001.h5')

        # Convert pmi out dir to hdf5.
        pmi.saveH5()

        # Setup diffraction parameters.
        diffraction_parameters=SingFELPhotonDiffractorParameters(
                uniform_rotation = None,
                calculate_Compton = False,
                slice_interval = 100,
                number_of_slices = 1,
                pmi_start_ID = 1,
                pmi_stop_ID  = 1,
                number_of_diffraction_patterns = 1,
                detector_geometry = self.detector_geometry,
                beam_parameters=None, # To be read from pmi input.
                )

        # Construct diffractor.
        diffractor = SingFELPhotonDiffractor(input_path='pmi_out_0000001.h5',
                                             output_path='diffr_out',
                                             parameters=diffraction_parameters,
                                             )

        # Run.
        diffractor.backengine()

        # Check diffr out was written.
        self.assertIn('diffr_out_0000001.h5', os.listdir('diffr_out'))


if __name__ == '__main__':
    unittest.main()

