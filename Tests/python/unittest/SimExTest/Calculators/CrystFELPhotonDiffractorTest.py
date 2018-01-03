""" Test module for the CrystFELPhotonDiffractor."""
##########################################################################
#                                                                        #
# Copyright (C) 2015-2017 Carsten Fortmann-Grote                         #
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
import paths
import shutil
import unittest

# Import the class to test.
from SimEx.Calculators.AbstractPhotonDiffractor import AbstractPhotonDiffractor
from SimEx.Calculators.CrystFELPhotonDiffractor import CrystFELPhotonDiffractor
from SimEx.Calculators.CrystFELPhotonDiffractor import _rename_files
from SimEx.Parameters.CrystFELPhotonDiffractorParameters import CrystFELPhotonDiffractorParameters
from SimEx.Parameters.PhotonBeamParameters import PhotonBeamParameters
from SimEx.Utilities.Units import electronvolt, joule, meter
from TestUtilities import TestUtilities

class CrystFELPhotonDiffractorTest(unittest.TestCase):
    """
    Test class for the CrystFELPhotonDiffractor class.
    """

    @classmethod
    def setUpClass(cls):
        """ Setting up the test class. """
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

    def testShapedConstruction(self):
        """ Testing the construction of the class with parameters. """

        # Setup parameters.
        parameters=CrystFELPhotonDiffractorParameters(sample="5udc.pdb")

        # Construct the object.
        diffractor = CrystFELPhotonDiffractor(parameters=parameters, input_path=None)

        # Check type.
        self.assertIsInstance(diffractor, CrystFELPhotonDiffractor)
        self.assertIsInstance(diffractor, AbstractPhotonDiffractor)

    def testConstructionWithPropInput(self):
        """ Check that beam parameters can be taken from a given propagation output file."""


        parameters = CrystFELPhotonDiffractorParameters(
                sample="5udc.pdb",
                detector_geometry=TestUtilities.generateTestFilePath("simple.geom"),
                beam_parameters=None,
                number_of_diffraction_patterns=1,
                )

        diffractor = CrystFELPhotonDiffractor(
                parameters=parameters,
                input_path=TestUtilities.generateTestFilePath("prop_out_0000001.h5"),
                output_path="diffr",
                )

        # Set spectrum type to tophat otherwise calculation will never finish.
        diffractor.parameters.beam_parameters.photon_energy_spectrum_type="tophat"

        # Check that beam parameters have been updated from prop output.
        self.assertAlmostEqual( diffractor.parameters.beam_parameters.photon_energy.m_as(electronvolt) , 4972.8402471221643, 5 )

    def testBackengineWithPropInput(self):
        """ Check that beam parameters can be taken from a given propagation output file."""

        self.__dirs_to_remove.append("diffr")
        self.__files_to_remove.append("5udc.pdb")

        parameters = CrystFELPhotonDiffractorParameters(
                sample="5udc.pdb",
                detector_geometry=TestUtilities.generateTestFilePath("simple.geom"),
                beam_parameters=None,
                number_of_diffraction_patterns=1,
                )

        diffractor = CrystFELPhotonDiffractor(
                parameters=parameters,
                input_path=TestUtilities.generateTestFilePath("prop_out_0000001.h5"),
                output_path="diffr",
                )

        # Set spectrum type to tophat otherwise calculation will never finish.
        diffractor.parameters.beam_parameters.photon_energy_spectrum_type="tophat"

        # Check that beam parameters have been updated from prop output.
        diffractor.backengine()

    def testBackengineSinglePattern(self):
        """ Check we can run pattern_sim with a minimal set of parameter. """

        # Ensure cleanup.
        self.__dirs_to_remove.append("diffr")
        self.__files_to_remove.append("5udc.pdb")

        # Get parameters.
        parameters = CrystFELPhotonDiffractorParameters(sample="5udc.pdb",
                detector_geometry=TestUtilities.generateTestFilePath("simple.geom"),
                number_of_diffraction_patterns=1)

        # Get calculator.
        diffractor = CrystFELPhotonDiffractor(parameters=parameters, input_path=None, output_path='diffr')

        # Run backengine
        status = diffractor.backengine()

        # Check return code.
        self.assertEqual(status, 0)

        # Check output dir was created.
        self.assertTrue( os.path.isdir( diffractor.output_path ) )

        # Check pattern was written.
        self.assertIn( "diffr_out_0000001.h5" , os.listdir( diffractor.output_path ))



    def testBackengineMultiplePatterns(self):
        """ Check we can run pattern_sim with a minimal set of parameter. """

        # Ensure cleanup.
        self.__dirs_to_remove.append("diffr")
        self.__files_to_remove.append("5udc.pdb")

        # Get parameters.
        parameters = CrystFELPhotonDiffractorParameters(sample="5udc.pdb",
                detector_geometry=TestUtilities.generateTestFilePath("simple.geom"),
                number_of_diffraction_patterns=2)

        # Get calculator.
        diffractor = CrystFELPhotonDiffractor(parameters=parameters, input_path=None, output_path='diffr')

        # Run backengine
        status = diffractor.backengine()

        # Check return code.
        self.assertEqual(status, 0)

        # Check output dir was created.
        self.assertTrue( os.path.isdir( diffractor.output_path ) )

        # Check pattern was written.
        self.assertIn( "diffr_out-1.h5" , os.listdir( diffractor.output_path ))
        self.assertIn( "diffr_out-2.h5" , os.listdir( diffractor.output_path ))

    def testSaveH5(self):
        """ Check that saveh5() creates correct filenames. """

        # Ensure cleanup.
        self.__dirs_to_remove.append("diffr")
        self.__files_to_remove.append("5udc.pdb")
        self.__files_to_remove.append("diffr.h5")

        # Setup beam parameters.
        beam_parameters = PhotonBeamParameters(photon_energy=5e3*electronvolt,
                pulse_energy=2e-3*joule,
                photon_energy_relative_bandwidth=1e-3,
                photon_energy_spectrum_type="tophat",
                beam_diameter_fwhm=3e-6*meter,
                )
        # Get parameters.
        parameters = CrystFELPhotonDiffractorParameters(sample="5udc.pdb",
                detector_geometry=TestUtilities.generateTestFilePath("simple.geom"),
                beam_parameters=beam_parameters,
                number_of_diffraction_patterns=2)

        # Get calculator.
        diffractor = CrystFELPhotonDiffractor(parameters=parameters, input_path=None, output_path='diffr')

        # Run backengine
        status = diffractor.backengine()

        # Check return code.
        self.assertEqual(status, 0)

        # Check output dir was created.
        self.assertTrue( os.path.isdir( diffractor.output_path ) )

        # Save correctly.
        diffractor.saveH5()

        # Check output file was created.
        self.assertTrue( os.path.isfile( diffractor.output_path ) )

        # Check pattern was written.
        self.assertIn( "diffr_out_0000001.h5" , os.listdir( "diffr" ))
        self.assertIn( "diffr_out_0000002.h5" , os.listdir( "diffr" ))

        # Open linked h5 file.
        with h5py.File(diffractor.output_path, 'r') as h5:
            self.assertIn("data" , list(h5.keys()))
            self.assertIn("0000001" , list(h5["data"].keys()))
            self.assertIn("0000002" , list(h5["data"].keys()))
            self.assertIn("data" , list(h5["data/0000001"].keys()))
            self.assertIn("data" , list(h5["data/0000002"].keys()))

            self.assertIn("params" , list(h5.keys()))
            self.assertIn("beam" , list(h5["params"].keys()))
            self.assertIn("photonEnergy" , list(h5["params/beam"].keys()))
            self.assertIn("focusArea" , list(h5["params/beam"].keys()))

        # Check metafile was created.
        self.assertIn( os.path.split(diffractor.output_path)[-1], os.listdir( os.path.dirname( diffractor.output_path) ) )

    def notestRenameFiles(self):

        _rename_files( "diffr" )

    def testBackengineWithBeamParametersObject(self):
        """ Check beam parameter logic if they are set as parameters. """

        # Ensure cleanup.
        self.__dirs_to_remove.append("diffr")
        self.__files_to_remove.append("5udc.pdb")

        # Setup beam parameters.
        beam_parameters = PhotonBeamParameters(
                photon_energy=16.0e3*electronvolt,
                photon_energy_relative_bandwidth=0.001,
                pulse_energy=2.0e-3*joule,
                beam_diameter_fwhm=100e-9*meter,
                divergence=None,
                photon_energy_spectrum_type="tophat",
                )

        # Get parameters.
        parameters = CrystFELPhotonDiffractorParameters(sample="5udc.pdb",
                detector_geometry=TestUtilities.generateTestFilePath("simple.geom"),
                beam_parameters=beam_parameters,
                number_of_diffraction_patterns=2,
                )

        # Get calculator.
        diffractor = CrystFELPhotonDiffractor(parameters=parameters, input_path=None, output_path='diffr')

        # Run backengine
        status = diffractor.backengine()

        # Check return code.
        self.assertEqual(status, 0)


if __name__ == '__main__':
    unittest.main()

