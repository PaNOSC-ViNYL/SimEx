#!/usr/bin/env python
""" :module DiffractionAnalysis: Module that hosts the DiffractionAnalysis class.  """
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
from matplotlib.colors import Normalize

import h5py
import math
import numpy
import os
import tempfile

import pyFAI

class DiffractionAnalysis(AbstractAnalysis):
    """
    :class DiffractionAnalysis: Class that implements common data analysis tasks for diffraction data.
    """

    def __init__(self,
                 input_path=None,
                 pattern_indices=None,
                 poissonize=True,
                 mask=None
            ):
        """

        :param input_path: Name of file or directory that contains data to analyse.
        :type input_path: str

        :param pattern_indices: Identify which patterns to include in the analysis (default "all").
        :type pattern_indices: int || sequence of int || "all"
        :example pattern_indices: pattern_indices=1\n
                                  pattern_indices=[1,2,3]\n
                                  pattern_indices=range(1,10)\n
                                  pattern_indices="all"

        :param poissonize: Whether to add Poisson noise to the integer photon numbers (default True).
        :type poissonize: bool

        :param mask: Mask to multiply on each pattern.
        :type mask: numpy.array

        """

        # Initialize base class. This takes care of parameter checking.
        super(DiffractionAnalysis, self).__init__(input_path)

        # Handle patterns.
        self.__given_indices = pattern_indices
        self.pattern_indices = pattern_indices

        # Init attributes.
        self.poissonize = poissonize
        self.parameters = diffractionParameters(self.input_path)

        self.mask = mask

    @property
    def parameters(self):
        return self.__parameters

    @parameters.setter
    def parameters(self, val):
        self.__parameters = val
    @property
    def pattern_indices(self):
        """ Query pattern indices attribute. """
        return self.__pattern_indices

    @pattern_indices.setter
    def pattern_indices(self, pattern_indices):
        """ Set the pattern indices. """

        indices = pattern_indices
        if indices is None:
            indices = 'all'

        if not (isinstance(indices, int) or indices == 'all' or hasattr(indices, '__iter__')):
            raise TypeError('The parameter "pattern_indices" must be an int, iterable over ints, or "all".')

        # Convert int to list.
        if isinstance(pattern_indices, int):
            indices = [pattern_indices]

        self.__pattern_indices = indices

    @property
    def patterns_iterator(self):
        return self.patternGenerator()

    @property
    def poissonize(self):
        """ Query whether to read data with (True) or without (False) Poisson noise. """
        return self.__poissonize
    @poissonize.setter
    def poissonize(self, val):
        """ Set the 'poissonize' flag."""
        # Handle default.
        if val is None:
            val = True
        if not isinstance(val, bool):
            raise TypeError('The parameter "poissonize" must be a bool.')

        self.__poissonize = val

    @property
    def npattern(self):
        """ get the number of the selected patterns in this analysis object """
        indices = self.pattern_indices
        if indices != 'all':
            npattern = len(indices)
        else:
            npattern = totalNPattern(self.input_path)

        return npattern

    @property
    def solidAngles(self):
        """ Solid angle of each pixel """
        """ Note: the pixel is assumed to be square """

        # pixel number (py, px)
        pn = self.parameters['geom']['mask'].shape
        # initialize array
        solidAngles = numpy.zeros_like(pn)
        y, x = numpy.indices(pn)
        # pixel size (meter)
        ph = self.parameters['geom']['pixelHeight']
        pw = self.parameters['geom']['pixelWidth']
        # sample to detector distance (meter)
        s2d = self.parameters['geom']['detectorDist']

        center_x = 0.5*(pn[1]-1)
        center_y = 0.5*(pn[0]-1)
        rx = (x - center_x)*pw
        ry = (y - center_y)*ph
        r = numpy.sqrt(rx**2 + ry**2)
        pixDist = numpy.sqrt(r**2 + s2d**2)
        alpha = numpy.arctan2(pw,2*pixDist)
        solidAngles = 4*numpy.arcsin(numpy.sin(alpha)**2)

        return solidAngles

    @property
    def qMap(self):
        """ q of each pixel """
        """ q = 4*pi*sin(twotheta/2)/lmd """

        # pixel number (py, px)
        pn = self.parameters['geom']['mask'].shape
        # initialize array
        qMap = numpy.zeros_like(pn)
        y, x = numpy.indices(pn)
        # pixel size (meter)
        ph = self.parameters['geom']['pixelHeight']
        pw = self.parameters['geom']['pixelWidth']
        # sample to detector distance (meter)
        s2d = self.parameters['geom']['detectorDist']

        E0 = self.parameters['beam']['photonEnergy']
        lmd = 12398 / E0 #Angstrom

        center_x = 0.5*(pn[1]-1)
        center_y = 0.5*(pn[0]-1)
        rx = (x - center_x)*pw
        ry = (y - center_y)*ph
        r = numpy.sqrt(rx**2 + ry**2)
        twotheta = numpy.arctan2(r,s2d)
        qMap = 4*numpy.pi*numpy.sin(twotheta/2)/lmd

        return qMap

    @property
    def mask(self):
        """ Query the mask. """
        return self.__mask
    @mask.setter
    def mask(self, val):
        """ Set the 'mask' flag."""
        # Handle default.
        if val is None:
            self.__mask = 1.
            return
        if not isinstance(val, numpy.ndarray):
            raise TypeError('The parameter "mask" must be a numpy.array.')

        self.__mask = val


    def patternGenerator(self):
        """ Yield an iterator over a given pattern sequence from a diffraction file.
        """

        indices = self.pattern_indices
        path = self.input_path
        if os.path.isdir(path): # legacy format.
            dir_listing = os.listdir(path)
            dir_listing.sort()
            if indices != 'all':
                dir_listing = [d for (i,d) in enumerate(dir_listing) if i in indices]
            h5_files = [os.path.join(path, f) for f in dir_listing if f.split('.')[-1] == "h5"]
            for h5_file in h5_files:
                try:
                    with h5py.File(h5_file, 'r') as h5:
                        root_path = '/data/'
                        if self.poissonize:
                            path_to_data = root_path + 'data'
                        else:
                            path_to_data = root_path + 'diffr'

                        diffr = h5[path_to_data].value

                        yield diffr
                except:
                    continue

        else: # v0.2

            # Open file for reading
            with h5py.File(path, 'r') as h5:
                if indices is None or indices == 'all':
                    indices = [key for key in h5['data'].keys()]
                else:
                    indices = ["%0.7d" % ix for ix in indices]
                for ix in indices:
                    root_path = '/data/%s/'% (ix)
                    if self.poissonize:
                        path_to_data = root_path + 'data'
                    else:
                        path_to_data = root_path + 'diffr'

                    diffr = h5[path_to_data].value

                    yield diffr*self.mask



    def numpyPattern(self, operation=None):
        """ Return the pattern after opentation over the patterns defined in DiffractionAnalysis class.

        :param operation: Operation to apply to selected patterns (default none).
        :type operation: python function
        :note operation: Operation must accept a 3D numpy.array as first input argument and the "axis" keyword-argument. Operation must return a 2D numpy.array. Axis will always be chosen as axis=0.
        :example operation: numpy.mean, numpy.std, numpy.sum

        """
        if operation is None:
            # Get all the patterns read by DiffractionAnalysis class.
            pi = self.patterns_iterator
            if len(self.pattern_indices) == 1:
                pattern_to_dump = next(pi)
            else:
                pattern_to_dump = numpy.array([p for p in pi])

        # Handle operation
        else:
            operation = eval(operation)
            # Get pattern to dump.
            pi = self.patterns_iterator
            if len(self.pattern_indices) == 1:
                pattern_to_dump = next(pi)
            else:
                pattern_to_dump = operation(numpy.array([p for p in pi]), axis=0)

        return pattern_to_dump

    def plotRadialProjection(self, operation=None, logscale=False, offset = 1e-5, unit="q_nm^-1"):
        """ Plot the radial projection of a pattern.

        :param operation: Operation to apply to selected patterns (default numpy.sum).
        :type operation: python function
        :note operation: Operation must accept a 3D numpy.array as first input argument and the "axis" keyword-argument. Operation must return a 2D numpy.array. Axis will always be chosen as axis=0.
        :example operation: numpy.mean, numpy.std, numpy.sum

        :param logscale: Whether to plot the intensity on a logarithmic scale (z-axis) (default False).
        :type logscale: bool

        :param unit:can be "q_nm^-1", "q_A^-1", "2th_deg", "2th_rad", "r_mm".
        :type unit: str

        """
        # Handle default operation
        if operation is None:
            operation = numpy.sum

        # Get pattern to plot.
        pi = self.patterns_iterator
        if len(self.pattern_indices) == 1:
            pattern_to_plot = next(pi)
        else:
            pattern_to_plot = operation(numpy.array([p for p in pi]), axis=0)

        # Plot radial projection.
        plotRadialProjection(pattern_to_plot, self.__parameters, logscale,offset,unit)

    def plotPattern(self, operation=None, logscale=False, offset=1e-1,symlog=False,*argv,**kwargs):
        """ Plot a pattern.

        :param operation: Operation to apply to selected patterns (default numpy.sum).
        :type operation: python function
        :note operation: Operation must accept a 3D numpy.array as first input argument and the "axis" keyword-argument. Operation must return a 2D numpy.array. Axis will always be chosen as axis=0.
        :example operation: numpy.mean, numpy.std, numpy.sum

        :param logscale: Whether to plot the intensity on a logarithmic scale (z-axis) (default False).
        :type logscale: bool

        :param offset: Offset to apply if logarithmic scaling is on.
        :type offset: float

        """

        # Handle default operation
        if operation is not None and len(self.pattern_indices) == 1:
            print("WARNING: Giving an operation with a single pattern has no effect.")
            operation = None
        if operation is None and len(self.pattern_indices) > 1:
            operation = numpy.sum

        # Get pattern to plot.
        pi = self.patterns_iterator
        if len(self.pattern_indices) == 1:
            pattern_to_plot = next(pi)
        else:
            pattern_to_plot = operation(numpy.array([p for p in pi]), axis=0)

        # Plot image and colorbar.
        return  plotImage(pattern_to_plot, logscale, offset,symlog,*argv,**kwargs)

    def shannonPixelPhoton(self, resolution):
        """
        Get the average number of photons per shannon pixel

        :param resolution: The full periodic resolution (A) for shannon pixels
        :type resolution: float
        """
        # Extract parameters.
        beam = self.parameters['beam']
        geom = self.parameters['geom']

        # Photon energy and wavelength
        E0 = beam['photonEnergy']
        lmd = 1239.8 / E0

        # Pixel dimension
        apix = geom['pixelWidth']
        # Sample-detector distance
        Ddet = geom['detectorDist']
        # Number of pixels in each dimension
        Npix = geom['mask'].shape[0]

        # Find center.
        center = 0.5*(Npix-1)

        # Max. scattering angle.
        theta_max = math.atan( center * apix / Ddet )
        # Min resolution.
        d_min = 0.5*lmd/math.sin(theta_max/2.0)

        # Next integer resolution.
        d0 = 0.1*math.ceil(d_min*10.0) # 10 powers to get Angstrom

        ds = resolution/10 # nm

        # Pixel numbers corresponding to resolution rings.
        N = Ddet/apix * numpy.tan(numpy.arcsin(lmd/2./ds)*2)

        pi = self.patterns_iterator
        stack = numpy.array([p for p in pi])

        y, x = numpy.indices(stack[0].shape)
        r = numpy.sqrt((x-center)**2 + (y-center)**2)
        mask = (abs(r-N) <= 0.5)

        for i in range(len(stack)):
            stack[i] *= mask

        plt.figure()
        plt.imshow(stack[0])
        plt.title('Frame 0')

        a = mask[mask==True]
        nShannonPixel = len(a)
        # Mean number of expected photons per Shannon pixel
        photons = numpy.sum(stack,axis=(1,2))/nShannonPixel
        avg_photons = numpy.mean(photons)
        rms_photons = numpy.std(photons)

        print("*************************")
        print("nShannonPixel = %i" % (nShannonPixel))
        print("avg = %6.5e" % (avg_photons))
        print("std = %6.5e" % (rms_photons))
        print("*************************")
        

    def statistics(self):
        """ Get statistics of photon numbers per pattern (mean and rms) over selected patterns and plot a historgram. """

        pi = self.patterns_iterator
        stack = numpy.array([p for p in pi])

        photonStatistics(stack)

    def animatePatterns(self, output_path=None, logscale=False, offset=1e-1):
        """
        Make an animated gif out of the given patterns.

        :param output_path: Where to save the animated git.
        :type output_path: str
        :raises IOError: File exists or parent directory not found.

        :param logscale: Whether to apply logarithmic scaling to the z axis (color).
        :type logscale: bool

        :param offset: Offset to apply if logarithmic scaling is on.
        :type offset: float
        """

        # Handle default path for saving the animated gif.
        if output_path is None:
            output_path=os.path.join(os.getcwd(), "animated_patterns.gif")

        if not isinstance(output_path, str):
            raise TypeError('The parameter "output_path" must be a str, not %s.' % (type(output_path)) )

        parent_dir = os.path.dirname(os.path.abspath(output_path))
        if not os.path.isdir( parent_dir ):
            raise IOError('%s does not exist.' % (parent_dir))
        if os.path.isfile(output_path):
            raise IOError('%s already exists, cowardly refusing to overwrite.' % (output_path))

        self.__animation_output_path=os.path.abspath(output_path)

        # Make tempdir.
        tmp_out_dir = tempfile.mkdtemp()
        stack = numpy.array([p for p in self.patternGenerator()])

        mn, mx = stack.min(), stack.max()
        x_range, y_range = stack.shape[1:]
        for i,img in enumerate(stack):
            plotImage(img, logscale=logscale, offset=offset)

            # Save image.
            if self.pattern_indices != "all":
                png_filename = "%07d.png" % (self.pattern_indices[i])
            else:
                png_filename = "%07d.png" % (i)

            plt.savefig(os.path.join(tmp_out_dir, png_filename) )

            # Clear figure.
            plt.clf()

        # Render the animated gif.
        os.system("convert -delay 100 %s %s" %(os.path.join(tmp_out_dir, "*.png"), output_path) )

def plotRadialProjection(pattern, parameters, logscale=True, offset=1.e-5, unit="q_nm^-1"):
    """ Perform integration over azimuthal angle and plot as function of radius.

        :param unit:can be "q_nm^-1", "q_A^-1", "2th_deg", "2th_rad", "r_mm".
        :type unit: str

    """

    qs, intensities = azimuthalIntegration(pattern, parameters,unit=unit)

    if logscale:
        plt.semilogy(qs, intensities+offset)
    else:
        plt.plot(qs, intensities)

    if (unit=="q_nm^-1"):
        plt.xlabel("q (1/nm)")
    elif (unit=="q_A^-1"):
        plt.xlabel("q (1/A)")
    elif (unit=="2th_deg"):
        plt.xlabel("2theta (degrees)")
    elif (unit=="2th_rad"):
        plt.xlabel("2theta (radians)")
    elif (unit=="r_mm"):
        plt.xlabel("mm")
    plt.ylabel("Intensity (arb. units)")
    plt.tight_layout()

def azimuthalIntegration(pattern, parameters, unit="q_nm^-1" ):

    # Extract parameters.
    beam = parameters['beam']
    geom = parameters['geom']

    # Photon energy and wavelength
    E0 = beam['photonEnergy']
    lmd = 1239.8 / E0

    # Pixel dimension
    apix = geom['pixelWidth']
    # Sample-detector distance
    Ddet = geom['detectorDist']
    # Number of pixels in each dimension
    Npix = geom['mask'].shape[0]

    # Find center.
    center = 0.5*(Npix-1)

    azimuthal_integrator = pyFAI.AzimuthalIntegrator(
            dist=Ddet,
            pixel1=apix,
            pixel2=apix,
            wavelength=lmd*1e-9)


    azimuthal_integrator.setFit2D(
            directDist=Ddet*1e3,
            centerX=center,
            centerY=center,
            tilt=0.0,
            tiltPlanRotation=0.0,
            pixelX=apix*1e6,
            pixelY=apix*1e6,
            )
    qs, intensities = azimuthal_integrator.integrate1d(
            pattern,
            min(Npix,1024),
            unit=unit
            #unit="q_nm^-1",
            #unit="2th_deg",
            )

    return qs, intensities

def diffractionParameters(path):
    """ Extract beam parameters and geometry from given file or directory.

    :param path: Path to file that holds the parameters to extract.
    :type path: str

    """

    # Check if old style.
    if os.path.isdir(path):
        h5_file = os.path.join(path, "diffr_out_0000001.h5")
    elif os.path.isfile(path):
        h5_file = path
    else:
        raise IOError("%s: no such file or directory." % (path))

    # Setup return dictionary.
    parameters_dict = {'beam':{}, 'geom':{}}

    # Open file.
    try:
        with h5py.File(h5_file, 'r') as h5:
            # Loop over entries in /params.
            for top_key in ['beam', 'geom']:
                # Loop over groups.
                for key, val in h5['params/%s' % (top_key)].items():
                    # Insert into return dictionary.
                    parameters_dict[top_key][key] = val.value
    except:
        pass
    # Return.
    return parameters_dict

def plotImage(pattern, logscale=False, offset=1e-1,symlog=False,*argv, **kwargs):
    """ Workhorse function to plot an image

    :param logscale: Whether to show the data on logarithmic scale (z axis) (default False).
    :type logscale: bool

    :param offset: Offset to apply if logarithmic scaling is on.
    :type offset: float

    :param symlog: If logscale is True, to show the data on symlogarithmic scale (z axis) (default False).
    :type symlog: bool

    :return: the handles of figure and axis
    :rtype: figure,axis

    """
    fig, ax = plt.subplots()
    # Get limits.
    mn, mx = pattern.min(), pattern.max()

    x_range, y_range = pattern.shape

    if logscale:
        if mn <= 0.0:
            mn = pattern.min()+offset
            mx = pattern.max()+offset
            pattern = pattern.astype(float) + offset

        # default plot setup
        kwargs['cmap'] = kwargs.pop('cmap',"viridis")
        if symlog:
            kwargs['norm'] = kwargs.pop('norm',mpl.colors.SymLogNorm(0.015,vmin=mn, vmax=mx))
        else:
            kwargs['norm'] = kwargs.pop('norm',mpl.colors.LogNorm(vmin=mn, vmax=mx))
        axes = kwargs.pop('axes',None)
        plt.imshow(pattern, *argv,**kwargs)
    else:
        kwargs['norm'] = kwargs.pop('norm',Normalize(vmin=mn, vmax=mx))
        kwargs['cmap'] = kwargs.pop('cmap',"viridis")
        plt.imshow(pattern, *argv,**kwargs)

    plt.xlabel(r'$x$ (pixel)')
    plt.ylabel(r'$y$ (pixel)')
    plt.xlim([0,x_range-1])
    plt.ylim([0,y_range-1])
    plt.tight_layout()
    plt.colorbar()
    return fig,ax



def plotResolutionRings(parameters,rings=(10, 5.0, 3.5),half=True):
    """
    Show resolution rings on current plot.

    :param parameters: Parameters needed to construct the resolution rings.
    :type parameters: dict
    :param rings: the rings shown on the figure
    :type rings: list
    :param half: show half period resolution (True, default) or full period resolution (False)
    :type half: bool

    """

    # Extract parameters.
    beam = parameters['beam']
    geom = parameters['geom']

    # Photon energy and wavelength
    E0 = beam['photonEnergy']
    lmd = 1239.8 / E0

    # Pixel dimension
    apix = geom['pixelWidth']
    # Sample-detector distance
    Ddet = geom['detectorDist']
    # Number of pixels in each dimension
    Npix = geom['mask'].shape[0]

    # Find center.
    center = 0.5*(Npix-1)

    # Max. scattering angle.
    theta_max = math.atan( center * apix / Ddet )
    # Min resolution.
    if (half):
        d_min = 0.5*lmd/math.sin(theta_max/2.0)/2.0
    else:
        d_min = 0.5*lmd/math.sin(theta_max/2.0)

    # Next integer resolution.
    d0 = 0.1*math.ceil(d_min*10.0) # 10 powers to get Angstrom

    # Array of resolution rings to plot.
    ds = numpy.array(rings)/10 # nm

    # Pixel numbers corresponding to resolution rings.
    if (half):
        Ns = Ddet/apix * numpy.tan(numpy.arcsin(lmd/2./ds/2.)*2)
    else:
        Ns = Ddet/apix * numpy.tan(numpy.arcsin(lmd/2./ds)*2)

    # Plot each ring and attach a label.
    for i,N in enumerate(Ns):
        x0 = center
        X = numpy.linspace(x0-N,x0+N, 512)
        Y_up = x0 + numpy.sqrt(N**2 - (X-x0)**2)
        Y_dn = x0 - numpy.sqrt(N**2 - (X-x0)**2)
        plt.plot(X,Y_up,color='k')
        plt.plot(X,Y_dn,color='k')
        plt.text(x0+0.75*N,x0+0.75*N, "%2.1f" % (ds[i]*10.), color = 'red')

    plt.xlim(0,Npix-1)
    plt.ylim(0,Npix-1)



def photonStatistics(stack):
    """ """

    number_of_images = stack.shape[0]
    photons = numpy.sum(stack, axis=(1,2))
    avg_photons = numpy.mean(photons)
    rms_photons =  numpy.std(photons)

    meanPerPattern = numpy.mean(stack, axis=(1,2)) 
    # average over the mean nphotons of each pattern in the stack
    avg_mean = numpy.mean(meanPerPattern)

    maxPerPattern = numpy.max(stack, axis=(1,2))
    # average over the max nphotons of each pattern in the stack
    avg_max = numpy.mean(maxPerPattern)

    minPerPattern = numpy.min(stack, axis=(1,2))
    # average over the min nphotons of each pattern in the stack
    avg_min = numpy.mean(minPerPattern)


    print("*************************")
    print ("Photon number statistics per pattern")
    print("avg = %6.5e" % (avg_photons))
    print("std = %6.5e" % (rms_photons))
    print ("Photon number statistics per pixel")
    print("avg_mean_pixel = %6.5e" % (avg_mean))
    print("avg_max_pixel = %6.5e" % (avg_max))
    print("avg_min_pixel = %6.5e" % (avg_min))
    print("*************************")


    # Plot histogram.
    plt.figure()
    max_photon_number = int(numpy.max( photons ))
    min_photon_number = int(numpy.min( photons ))
    if max_photon_number == min_photon_number:
        max_photon_number += 1

    binwidth = max_photon_number - min_photon_number
    number_of_bins = min(20, number_of_images)
    binwidth = int( binwidth / number_of_bins )

    plt.hist(photons, bins=range(min_photon_number, max_photon_number, binwidth), facecolor='red', alpha=0.75)
    plt.xlim([min_photon_number, max_photon_number])
    plt.xlabel("Photons")
    plt.ylabel("Histogram")
    plt.title("Photon number histogram")


def totalNPattern(input_path):
    """ get the number of the diffraction patterns in the h5file"""
    with h5py.File(input_path, 'r') as h5:
        npattern = len(h5['data'])
    return npattern


