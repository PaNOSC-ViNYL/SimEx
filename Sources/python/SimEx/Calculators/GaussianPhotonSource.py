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
import math
from scipy.constants import hbar, c

from SimEx.Calculators.AbstractPhotonSource import AbstractPhotonSource
from SimEx.Parameters.PhotonBeamParameters import PhotonBeamParameters
from SimEx.Utilities.Units import meter, joule, radian, electronvolt, second

from wpg.generators import build_gauss_wavefront
from wpg import Wavefront


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

        # The rms of the amplitude distribution (Gaussian)
        theta = self.parameters.divergence.m_as(radian)
        E = self.parameters.photon_energy
        coherence_time = 2.*math.pi*hbar*joule*second/self.parameters.photon_energy_relative_bandwidth/E
        coherence_time = coherence_time.m_as(second)


        beam_waist = 2.*hbar*c*joule*meter/theta/E
        amplitude_rms = 0.5*beam_waist/math.sqrt(math.log(2.))

        # Rule of thumb: 36 times w0
        # x-y range at beam waist.
        range_xy = 36.0*beam_waist.m_as(meter)

        # Set number of sampling points in x and y and number of temporal slices.
        np = 400 #self.parameters.number_of_transverse_grid_points
        nslices = 20 #self.parameters.number_of_time_slices

        # Build wavefront
        srwl_wf = build_gauss_wavefront(np, np, nslices,
                                        E.m_as(electronvolt)/1.0e3,
                                        -range_xy/2, range_xy/2,
                                        -range_xy/2, range_xy/2,
                                        coherence_time/math.sqrt(2),
                                        amplitude_rms.m_as(meter), amplitude_rms.m_as(meter),
                                        0.0,
                                        pulseEn=self.parameters.pulse_energy.m_as(joule),
                                        pulseRange=8.)
        # Store on class.
        self.__wavefront = Wavefront(srwl_wf)

    @property
    def data(self):
        """ Query for the field data. """
        return self.__wavefront

    def _readH5(self):
        """ """
        pass

    def saveH5(self):
        """ """
        self.data.store_hdf5(self.output_path)
