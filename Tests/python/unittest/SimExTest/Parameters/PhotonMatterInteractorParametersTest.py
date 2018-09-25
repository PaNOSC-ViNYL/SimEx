""" :module: Test module hosting the test for the SingFELPhotonDiffractorParameter class."""
##########################################################################
#                                                                        #
# Copyright (C) 2016-2018 Carsten Fortmann-Grote                         #
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


class PhotonMatterInteractorParametersTest(unittest.TestCase):
    """
    Test class for the PhotonMatterInteractorParameters class.
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
        parameters = PhotonMatterInteractorParameters()


if __name__ == '__main__':
    unittest.main()
