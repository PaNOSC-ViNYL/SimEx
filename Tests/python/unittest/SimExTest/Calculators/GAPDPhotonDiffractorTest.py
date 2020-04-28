""" Test module for the GAPDPhotonDiffractor."""
##########################################################################
#
# Modified by Juncheng E in 2020                                         #
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

import os, shutil
import subprocess
import tempfile
import unittest

# Include needed directories in sys.path.
import unittest

from TestUtilities import TestUtilities
# Import the class to test.
from SimEx.Calculators.GAPDPhotonDiffractor import GAPDPhotonDiffractor
from SimEx.Parameters.GAPDPhotonDiffractorParameters import GAPDPhotonDiffractorParameters
from SimEx.Parameters.DetectorGeometry import DetectorGeometry, DetectorPanel
from SimEx.Parameters.PhotonBeamParameters import PhotonBeamParameters
from SimEx.Utilities.Units import meter, electronvolt, joule, radian


class GAPDPhotonDiffractorTest(unittest.TestCase):
    """
    Test class for the GAPDPhotonDiffractor class.
    """
    @classmethod
    def setUpClass(cls):
        """ Setting up the test class. """
        detector_panel = DetectorPanel(
            ranges={
                'fast_scan_min': 0,
                'fast_scan_max': 21,
                'slow_scan_min': 0,
                'slow_scan_max': 21
            },
            pixel_size=2.2e-4 * meter,
            photon_response=1.0,
            distance_from_interaction_plane=0.13 * meter,
            corners={
                'x': -11,
                'y': -11
            },
        )

        cls.detector_geometry = DetectorGeometry(panels=[detector_panel])

        cls.beam = PhotonBeamParameters(
            photon_energy=8.6e3 * electronvolt,
            beam_diameter_fwhm=1.0e-6 * meter,
            pulse_energy=1.0e-3 * joule,
        )

        cls.parameters = GAPDPhotonDiffractorParameters(
            detector_geometry=cls.detector_geometry,
            beam_parameters=cls.beam,
            forced_mpi_command='mpirun -np 1')

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

    def testConstructionParameters(self):
        """ Check we can construct with a parameter object. """
        parameters = GAPDPhotonDiffractorParameters(
            beam_parameters=self.beam,
            detector_geometry=self.detector_geometry,
        )

    def testGAPDAtomInput(self):
        """ GAPD atom format preparation test """

        tmp_dir = tempfile.mkdtemp(prefix='gapd_')

        # Chdir to tmp directory.
        old_pwd = os.getcwd()
        os.chdir(tmp_dir)

        calculator = GAPDPhotonDiffractor(parameters=self.parameters,
                                          input_path='3WUL.pdb',
                                          output_path='out')
        calculator.prepareAtomData()

        self.assertIn("atoms.xyz", os.listdir(tmp_dir))

        os.chdir(old_pwd)

    def testWriteParam(self):
        """ GAPD atom format preparation test """

        tmp_dir = tempfile.mkdtemp(prefix='gapd_')
        print ('WriteParam test:',tmp_dir)

        shutil.copy2(TestUtilities.generateTestFilePath("3WUL.pdb"), tmp_dir)

        # Chdir to tmp directory.
        old_pwd = os.getcwd()
        os.chdir(tmp_dir)

        calculator = GAPDPhotonDiffractor(parameters=self.parameters,
                                          input_path='3WUL.pdb',
                                          output_path='out')
        # Diffractor atom data
        calculator.prepareAtomData()

        # Diffractor detector data
        calculator.prepareDetector()

        # Diffractor beam data
        calculator.prepareBeam()

        in_param_file = "in.param"
        calculator.writeParam(in_param_file)

        self.assertIn("in.param", os.listdir(tmp_dir))

        os.chdir(old_pwd)

    def testRun(self):
        """ GAPD atom format preparation test """

        tmp_dir = tempfile.mkdtemp(prefix='gapd_')
        print ('Engine test:',tmp_dir)
        shutil.copy2(TestUtilities.generateTestFilePath("3WUL.pdb"), tmp_dir)

        # Chdir to tmp directory.
        old_pwd = os.getcwd()
        os.chdir(tmp_dir)

        calculator = GAPDPhotonDiffractor(parameters=self.parameters,
                                          input_path='3WUL.pdb',
                                          output_path='out.txt')

        calculator.backengine()

        os.chdir(old_pwd)


if __name__ == '__main__':
    unittest.main()
