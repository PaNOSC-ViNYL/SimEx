""":module GaussianPhotonSource: Module that holds the GaussianPhotonSource class.  """
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

import os
import shutil

from SimEx.Calculators.AbstractPhotonSource import AbstractPhotonSource
from SimEx.Parameters.PhotonBeamParameters import PhotonBeamParameters

class GaussianPhotonSource(AbstractPhotonSource):
    """
    :class GaussianPhotonSource: Class representing a x-ray free electron laser photon source.
    """

    def __init__(self, parameters=None, input_path=None, output_path=None):
        """

        :param parameters : Photon source parameters.
        :type parameters: PhotonBeamParameters

        :param output_path: The path where to save output data.
        :type output: str, default FELsource_out.h5
        """

        # Initialize base class.
        super(GaussianPhotonSource, self).__init__(parameters, input_path, output_path)

        self.parameters = parameters
        self.__wavefront = None

    def backengine(self):
        # Wavelength (m)
        wavelength = 1.2398e-6/self.parameters.photon_energy

        # Beam waist.
        w0 = wavelength/(numpy.pi*beam_divergence)

        # Rayleigh length
        zR = (numpy.pi*w0**2)/wavelength

        # The rms of the amplitude distribution (Gaussian)
        amplitude_rms = w0/(2*numpy.sqrt(numpy.log(2)))

        print("Wavelength = {0:4.3e} m".format(wavelength))
        print("Beam waist at source position = {0:4.3e} m".format(w0))
        print("Rayleigh length = {0:4.3e} m".format(zR))
        print("Amplitude RMS= {0:4.3e} m".format(amplitude_rms))

        ## Set the Region Of Interest window

        # x-y range at beam waist.
        # Rule of thumb: 36 times w0
        range_xy = 36.0*w0
        print("ROI set to square of {0:4.3e} m edge length.".format(range_xy))

        ## Set number of sampling points in x and y and number of temporal slices.

        np = 400
        nslices = 20

        ## Build wavefront

        srwl_wf = build_gauss_wavefront(np, np, nslices,
                                        photon_energy/1.0e3,
                                        -range_xy/2, range_xy/2,
                                        -range_xy/2, range_xy/2,
                                        coherence_time/numpy.sqrt(2),
                                        sigmaAmp, sigmaAmp,
                                        0.0, # Position
                                        pulseEn=pulse_energy,
                                        pulseRange=8.)
        wf = Wavefront(srwl_wf)
    @property
    def data(self):
        """ Query for the field data. """
        return self.__wavefront

    def _readH5(self):
        """ """
        pass

    def saveH5(self):
        """ """
        pass
