""" :module XFELPhotonAnalysis: Module that hosts the XFELPhotonAnalysis class."""
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

from SimEx.Analysis.AbstractAnalysis import AbstractAnalysis, plt, mpl

import os,shutil
import copy
import numpy
import wpg

class XFELPhotonAnalysis(AbstractAnalysis):
    """
    :class XFELPhotonAnalysis: Class that implements common data analysis tasks for wavefront (radiation field) data.
    """

    def __init__(self, input_path=None,):
        """
        :param input_path: Name of file or directory that contains data to analyse.
        :type input_path: str
        """
        print("\n Start initialization.")
        # Initialize base class. This takes care of parameter checking.
        super(XFELPhotonAnalysis, self).__init__(input_path)

        # Get wavefront file name.
        wavefront = wpg.Wavefront()

        print("\n Loading wavefront from %s." % (self.input_path))
        wavefront.load_hdf5(self.input_path)
        print(" ... done.")

        # Init intensity.
        self.__intensity = None

        # Init wavefront, triggers assignment of intensity.
        self.wavefront = wavefront


    @property
    def intensity(self):
        """ Query for the intensity. """
        return self.__intensity
    @intensity.setter
    def intensity(self, val):
        """ Set the intensity. """
        self.__intensity = val


    @property
    def wavefront(self):
        """ Query for the wavefront. """
        return self.__wavefront
    @wavefront.setter
    def wavefront(self, val):
        """ Query for the wavefront. """
        self.__wavefront = val

        # Get intensities and mask nans
        print("\n Getting intensities.")
        self.intensity = self.__wavefront.get_intensity()
        print(" ... done.")
        print(" Data dimensions = ", self.intensity.shape)
        print("\n Masking NANs.")
        self.__nans = mask_nans(self.intensity)
        print(" ... done.")

    def animate(self, qspace=False, logscale=False):
        """ Generate an animated gif from the wavefront data. """
        intensity = self.intensity

        # Get limits.
        xmin, xmax, ymax, ymin = self.wavefront.get_limits()
        mx = intensity.max()
        mn = intensity.min()
        if logscale and mn <= 0.0:
            mn = intensity[numpy.where(intensity > 0.0)].min(),

        inp_filename = os.path.split(self.input_path)[-1]
        os.mkdir("tmp")
        number_of_slices = intensity.shape[-1]
        # Setup a figure.

        for i in range(0,number_of_slices):

            print("Processing slice #%d." % (i))

            # Plot profile as 2D colorcoded map.
            if logscale:
                plt.imshow(intensity[:,:,i], norm=mpl.colors.LogNorm(vmin=mn, vmax=mx), extent=[xmin*1.e6, xmax*1.e6, ymax*1.e6, ymin*1.e6], cmap="viridis")
            else:
                plt.imshow(intensity[:,:,i], norm=mpl.colors.Normalize(vmin=mn, vmax=mx), extent=[xmin*1.e6, xmax*1.e6, ymax*1.e6, ymin*1.e6], cmap="viridis")

            plt.savefig("tmp/%s_%07d.png" % (inp_filename, i) )
            plt.clf()

        os.system("convert -delay 10 tmp/*.png %s.gif" % (inp_filename) )
        shutil.rmtree("tmp")

    def plotIntensityMap(self, qspace=False, logscale=False):
        """ Plot the integrated intensity as function of x,y or qx, qy on a colormap.

        :param qspace: Whether to plot the reciprocal space intensity map (default False).
        :type qspace: bool

        :param logscale: Whether to plot the intensity on a logarithmic scale (z-axis) (default False).
        :type logscale: bool

        """

        print("\n Plotting intensity map.")
        # Setup new figure.
        plt.figure()

        wf = self.wavefront
        wf_intensity = self.intensity


        # Switch to q-space if requested.
        if qspace:
            print("\n Switching to reciprocal space.")
            srwl_wf_a = copy.deepcopy(self.wavefront._srwl_wf)
            wpg.srwlib.srwl.SetRepresElecField(srwl_wf_a, 'a')
            wf = wpg.Wavefront(srwl_wf_a)
            print(" ... done.")
            wf_intensity = wf.get_intensity()
            nans = mask_nans(wf_intensity)

        # Get average and time slicing.
        wf_intensity = wf_intensity.sum(axis=-1)

        nslices = wf.params.Mesh.nSlices
        if (nslices>1):
            dt = (wf.params.Mesh.sliceMax-wf.params.Mesh.sliceMin)/(nslices-1)
            t0 = dt*nslices/2 + wf.params.Mesh.sliceMin
        else:
            t0 = (wf.params.Mesh.sliceMax+wf.params.Mesh.sliceMin)/2

        # Setup a figure.
        figure = plt.figure(figsize=(10, 10), dpi=100)
        plt.axis('tight')
        # Profile plot.
        profile = plt.subplot2grid((3, 3), (1, 0), colspan=2, rowspan=2)

        # Get limits.
        xmin, xmax, ymax, ymin = wf.get_limits()
        mn, mx = wf_intensity.min(), wf_intensity.max()

        # Plot profile as 2D colorcoded map.
        if logscale:
            profile.imshow(wf_intensity, norm=mpl.colors.LogNorm(vmin=mn, vmax=mx), extent=[xmin*1.e6, xmax*1.e6, ymax*1.e6, ymin*1.e6], cmap="viridis")
        else:
            profile.imshow(wf_intensity, norm=mpl.colors.Normalize(vmin=mn, vmax=mx), extent=[xmin*1.e6, xmax*1.e6, ymax*1.e6, ymin*1.e6], cmap="viridis")


        # Get x and y ranges.
        x = numpy.linspace(xmin*1.e6, xmax*1.e6, wf_intensity.shape[1])
        y = numpy.linspace(ymin*1.e6, ymax*1.e6, wf_intensity.shape[0])

        # Labels.
        if qspace:
            profile.set_xlabel(r'$q_{x}\ \mathrm{(\mu rad)}$')
            profile.set_ylabel(r'$q_{y}\ \mathrm{(\mu rad)}$')
        else:
            profile.set_xlabel(r'$x\ \mathrm{(\mu m)}$')
            profile.set_ylabel(r'$y\ \mathrm{(\mu m)}$')

        # x-projection plots above main plot.
        x_projection = plt.subplot2grid((3, 3), (0, 0), sharex=profile, colspan=2)

        x_projection.plot(x, wf_intensity.sum(axis=0), label='x projection')

        # Set range according to input.
        profile.set_xlim([xmin*1.e6, xmax*1.e6])

        # y-projection plot right of main plot.
        y_projection = plt.subplot2grid((3, 3), (1, 2), rowspan=2, sharey=profile)
        y_projection.plot(wf_intensity.sum(axis=1), y, label='y projection')

        # Hide minor tick labels, they disturb here.
        plt.minorticks_off()

        # Set range according to input.
        profile.set_ylim([ymin*1.e6, ymax*1.e6])

        # Cleanup.
        if qspace:
            del wf


    def plotTotalPower(self, spectrum=False):
        """ Method to plot the total power.

        :param spectrum: Whether to plot the power density in energy domain (True) or time domain (False, default).
        :type spectrum: bool

        """

        """ Adapted from github:Samoylv/WPG/wpg/wpg_uti_wf.integral_intensity() """
        print("\n Plotting total power.")
        # Setup new figure.
        plt.figure()

        # Switch to frequency (energy) domain if requested.
        if spectrum:
            print("\n Switching to frequency domain.")
            wpg.srwlib.srwl.SetRepresElecField(self.wavefront._srwl_wf, 'f')
            self.intensity = self.wavefront.get_intensity()

        # Get dimensions.
        mesh = self.wavefront.params.Mesh
        dx = (mesh.xMax - mesh.xMin)/(mesh.nx - 1)
        dy = (mesh.yMax - mesh.yMin)/(mesh.ny - 1)

        # Get intensity by integrating over transverse dimensions.
        int0 = self.intensity.sum(axis=(0,1))

        # Scale to get unit W/mm^2
        int0 = int0*(dx*dy*1.e6) #  amplitude units sqrt(W/mm^2)
        int0max = int0.max()

        # Get center pixel numbers.
        center_nx = int(mesh.nx/2)
        center_ny = int(mesh.ny/2)

        # Get meaningful slices.
        aw = [a[0] for a in numpy.argwhere(int0 > int0max*0.01)]
        int0_mean = int0[min(aw):max(aw)]  # meaningful range of pulse
        dSlice = (mesh.sliceMax - mesh.sliceMin)/(mesh.nSlices - 1)
        xs = numpy.arange(mesh.nSlices)*dSlice+ mesh.sliceMin
        xs_mf = numpy.arange(min(aw), max(aw))*dSlice + mesh.sliceMin
        if(self.wavefront.params.wDomain=='time'):
            plt.plot(xs*1e15, int0) # time axis converted to fs.
            plt.plot(xs_mf*1e15, int0_mean, 'ro')
            plt.title('Power')
            plt.xlabel('time (fs)')
            plt.ylabel('Power (W)')
            dt = (mesh.sliceMax - mesh.sliceMin)/(mesh.nSlices - 1)
            print(('Pulse energy {:1.2g} J'.format(int0_mean.sum()*dt)))

        else: #frequency domain
            plt.plot(xs, int0)
            plt.plot(xs_mf, int0_mean, 'ro')
            plt.title('Spectral Energy')
            plt.xlabel('eV')
            plt.ylabel('J/eV')

            # Switch back to time domain.
            wpg.srwlib.srwl.SetRepresElecField(self.wavefront._srwl_wf, 't')
            self.intensity = self.wavefront.get_intensity()

    def plotOnAxisPowerDensity(self, spectrum=False):
        """ Method to plot the on-axis power density.

        :param spectrum: Whether to plot the power density in energy domain (True) or time domain (False, default).
        :type spectrum: bool

        """
        """ Adapted from github:Samoylv/WPG/wpg/wpg_uti_wf.integral_intensity() """

        print("\n Plotting on-axis power density.")
        # Setup new figure.
        plt.figure()

        # Switch to frequency (energy) domain if requested.
        if spectrum:
            wpg.srwlib.srwl.SetRepresElecField(self.wavefront._srwl_wf, 'f')
            self.intensity = self.wavefront.get_intensity()

        # Get dimensions.
        mesh = self.wavefront.params.Mesh
        dx = (mesh.xMax - mesh.xMin)/(mesh.nx - 1)
        dy = (mesh.yMax - mesh.yMin)/(mesh.ny - 1)

        # Get center pixel numbers.
        center_nx = int(mesh.nx/2)
        center_ny = int(mesh.ny/2)

        # Get time slices of intensity.
        intensity = self.intensity

        # Get on-axis intensity.
        int0_00 = intensity[center_ny, center_nx, :]
        int0 = intensity.sum(axis=(0,1))*(dx*dy*1.e6) #  amplitude units sqrt(W/mm^2)
        int0max = int0.max()

        # Get meaningful slices.
        aw = [a[0] for a in numpy.argwhere(int0 > int0max*0.01)]
        if aw == []:
            raise RuntimeError("No significant intensities found.")

        dSlice = (mesh.sliceMax - mesh.sliceMin)/(mesh.nSlices - 1)

        xs = numpy.arange(mesh.nSlices)*dSlice+ mesh.sliceMin
        xs_mf = numpy.arange(min(aw), max(aw))*dSlice + mesh.sliceMin

        # Plot.
        if(self.wavefront.params.wDomain=='time'):
            plt.plot(xs*1e15,int0_00)
            plt.plot(xs_mf*1e15, int0_00[min(aw):max(aw)], 'ro')
            plt.title('On-Axis Power Density')
            plt.xlabel('time (fs)')
            plt.ylabel(r'Power density (W/mm${}^{2}$)')
        else: #frequency domain
            plt.plot(xs,int0_00)
            plt.plot(xs_mf, int0_00[min(aw):max(aw)], 'ro')
            plt.title('On-Axis Spectral Fluence')
            plt.xlabel('photon energy (eV)')
            plt.ylabel(r'fluence (J/eV/mm${}^{2}$)')

            # Switch back to time domain.
            wpg.srwlib.srwl.SetRepresElecField(self.wavefront._srwl_wf, 't')
            self.intensity = self.wavefront.get_intensity()

def mask_nans(a, replacement=0.0):
    """ Find nans in an array and replace.
    :param  a: Array to mask.
    :type a: numpy.array

    :param replacement: The value to replace nans.
    :type replacement: numeric

    :return: The array of booleans indicating which values of a are nan, numpy.isnan(a)
    :rtype: numpy.array(dtype=bool)
    """
    isnan_array = numpy.isnan(a) # This can take a while ...
    if isnan_array.any():
        nans = numpy.where(isnan_array)
        print("WARNING: Found intensity=NAN at", repr(nans))
        a[nans] = 0.0 # Yes this works because a is a reference!
    return isnan_array

