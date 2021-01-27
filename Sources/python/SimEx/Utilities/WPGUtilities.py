""":module WPGUtilities: Module for WPG data processing.  """
##########################################################################
#                                                                        #
# Copyright (C) 2020-2021 Juncheng E                                     #
# Contact: Juncheng E <juncheng.e@xfel.eu>                               #
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

import wpg
import numpy


class WPGdata:
    """
    :class WPGdata: Utilities to deal with WPG wavefront data
    """
    def __init__(self, input_path=None):
        """
        :param input_path: Name of the s2e wavefront .h5 file
        :type input_path: str
        """

        self.input_path = input_path
        wavefront = wpg.Wavefront()
        wavefront.load_hdf5(self.input_path)
        self.wavefront = wavefront

    def get_total_power(self, spectrum=False, meaningful_only=True):
        """ Method to dump meaningful/all total power.
            Temporal domain unit: x-time (s), y-power (W)
            Frequent domain unit: x-eV, y-J/eV

        :param spectrum: Whether to dump the power density in energy domain (True)
            or time domain (False, default).
        :type spectrum: bool
        :param meaningful_only: `False` to extract all the points, `True` to extract only meaningful points
        :type meaningful_only: bool
        """
        # Switch to frequency (energy) domain if requested.
        if spectrum:
            print("Switching to frequency domain.")
            wpg.srwlib.srwl.SetRepresElecField(self.wavefront._srwl_wf, 'f')
            self.intensity = self.wavefront.get_intensity()
        else:
            wpg.srwlib.srwl.SetRepresElecField(self.wavefront._srwl_wf, 't')
            self.intensity = self.wavefront.get_intensity()

        # Get dimensions.
        mesh = self.wavefront.params.Mesh
        dx = (mesh.xMax - mesh.xMin) / (mesh.nx - 1)
        dy = (mesh.yMax - mesh.yMin) / (mesh.ny - 1)

        # Get intensity by integrating over transverse dimensions.
        int0 = self.intensity.sum(axis=(0, 1))

        # Get power
        int0 = int0 * (dx * dy * 1.e6)
        int0max = int0.max()

        # Get meaningful slices.
        if meaningful_only:
            aw = [a[0] for a in numpy.argwhere(int0 > int0max * 0.01)]
        else:
            aw = numpy.arange(len(int0))
        int0_mean = int0[min(aw):max(aw) + 1]  # meaningful range of pulse
        dSlice = (mesh.sliceMax - mesh.sliceMin) / (mesh.nSlices - 1)
        # xs = numpy.arange(mesh.nSlices) * dSlice + mesh.sliceMin
        xs_mf = numpy.arange(min(aw), max(aw) + 1) * dSlice + mesh.sliceMin

        if (self.wavefront.params.wDomain == 'time'):
            print('x: Time (s)')
            print('y: Power (W)')
            dt = (mesh.sliceMax - mesh.sliceMin) / (mesh.nSlices - 1)
            print(('Pulse energy {:1.2g} J'.format(int0_mean.sum() * dt)))
            return xs_mf, int0_mean

        # frequency domain
        else:  
            print('x: eV')
            print('y: J/eV')

            # Switch back to time domain.
            wpg.srwlib.srwl.SetRepresElecField(self.wavefront._srwl_wf, 't')
            self.intensity = self.wavefront.get_intensity()

            return (xs_mf, int0_mean)
