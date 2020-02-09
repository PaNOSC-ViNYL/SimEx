""" Test module for the GaussianPhotonSource. """

##########################################################################
#                                                                        #
# Copyright (C) 2020 Carsten Fortmann-Grote                              #
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

import unittest
import os

# Import the class to test.
from SimEx.Calculators.GaussianPhotonSource import GaussianPhotonSource
from SimEx.Parameters.PhotonBeamParameters import PhotonBeamParameters
from SimEx.Utilities.Units import meter, joule, radian, electronvolt
from TestUtilities import TestUtilities

from wpg import Wavefront
from wpg.wpg_uti_wf import calc_pulse_energy, averaged_intensity, calculate_fwhm, get_intensity_on_axis
from wpg.wpg_uti_wf import integral_intensity, plot_intensity_map,plot_intensity_qmap

class GaussianPhotonSourceTest(unittest.TestCase):
    """
    Test class for the GaussianPhotonSource class.
    """

    @classmethod
    def setUpClass(cls):
        """ Setting up the test class. """

        cls.beam_parameters = PhotonBeamParameters(
            photon_energy = 8.0e3*electronvolt,
            beam_diameter_fwhm = 0.3e-6*meter,
            pulse_energy = 2.4e-6*joule,
            photon_energy_relative_bandwidth=1e-4,
            divergence=2.0e-6*radian,
            photon_energy_spectrum_type=None,
            )

    @classmethod
    def tearDownClass(cls):
        """ Tearing down the test class. """

    def setUp(self):
        """ Setting up a test. """

        self.__files_to_remove = []

    def tearDown(self):
        """ Tearing down a test. """

        for f in self.__files_to_remove:
            if os.path.isfile(f):
                os.remove(f)

    def testConstruction(self):
        """ Testing the default construction of the class. """

        # Construct the object.
        source = GaussianPhotonSource(parameters=None, input_path="", output_path='GaussianSource.h5')

        self.assertIsInstance(source, GaussianPhotonSource)

    def test_backengine(self):
        """ Test the backengine method. """

        source = GaussianPhotonSource(parameters=self.beam_parameters,
                                      input_path="",
                                      output_path="")

        source.backengine()

        self.assertIsInstance(source.data, Wavefront)

    def plot_test_wavefront(self):
        # Only for interactive session.
        source = GaussianPhotonSource(parameters=self.beam_parameters,
                                      input_path="",
                                      output_path="")

        source.backengine()

        wf = source.data
        integral_intensity(wf)
        plot_intensity_map(wf)
        plot_intensity_qmap(wf)

    def test_saveH5(self):
        """ Test saving the generated wavefront to disk. """

        source = GaussianPhotonSource(parameters=self.beam_parameters,
                                      input_path="",
                                      output_path="gauss_source.h5")

        source.backengine()

        source.saveH5()

        self.assertTrue(os.path.isfile(source.output_path))

        self.__files_to_remove.append(source.output_path)

if __name__ == '__main__':
    unittest.main()

