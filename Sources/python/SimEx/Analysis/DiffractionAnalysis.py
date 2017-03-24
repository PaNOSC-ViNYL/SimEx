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
"""
    :module DiffractionAnalysis: Module that hosts the DiffractionAnalysis class."""
from SimEx.Analysis.AbstractAnalysis import AbstractAnalysis, plt, mpl
from matplotlib.colors import Normalize, LogNorm

import h5py
import math
import numpy
import os
import wpg

class DiffractionAnalysis(AbstractAnalysis):
    """
    :class DiffractionAnalysis: Class that implements common data analysis tasks for wavefront (radiation field) data.
    """

    def __init__(self, input_path=None,):
        """ Constructor for the DiffractionAnalysis class.

        :param input_path: Name of file or directory that contains data to analyse.
        :type input_path: str

        """

        # Initialize base class. This takes care of parameter checking.
        super(DiffractionAnalysis, self).__init__(input_path)

    def plotPattern(self, pattern_indices=None, logscale=False, operation=None, poissonized=True ):
        """ Plot a pattern.
        :param pattern: Identify which pattern to plot.
        :type pattern: int || sequence of int || "all"

        :param operation: Operation to apply to the given pattern(s).
        :type operation: function
        :note operation: Function must accept the "axis" keyword-argument. Axis will always be chosen as axis=0.
        :rtype operation: 2D numpy.array

        :param logscale: Whether to plot the intensity on a logarithmic scale (z-axis) (default False).
        :type logscale: bool

        """
        # Get new reference to pattern_indices.
        indices = pattern_indices
        if indices is None:
            indices = 'all'

        # Convert int to list.
        if isinstance(pattern_indices, int):
            indices = [pattern_indices]

        # Handle default operation
        if operation is None:
            operation = numpy.sum

        # Complain if operating on single pattern.
        else:
            if len(pattern_indices) == 1:
                print "WARNING: Giving an operation with a single pattern has no effect."
        # Get iterator over queried patterns.
        patterns_iterator = generate_patterns_from_file(self.input_path, indices=indices, poissonized=poissonized)

        # Get pattern to plot.
        if len(indices) == 1:
            pattern_to_plot = patterns_iterator.next()
        else:
            pattern_to_plot = operation(numpy.array([p for p in patterns_iterator]), axis=0)

        # Get beam and geometry parameters.
        parameters_dict = diffraction_parameters(self.input_path)

        # Plot image and colorbar.
        plot_image(pattern_to_plot, logscale)

        # Plot resolution rings.
        plot_resolution_rings(parameters_dict)

def plot_image(pattern, logscale=False):
    """ Workhorse function to plot an image """
    # Get limits.
    mn, mx = pattern.min(), pattern.max()

    if logscale:
        if mn == 0:
            pattern = pattern.astype(float) + 1e-5
        plt.imshow(pattern, norm=mpl.colors.LogNorm(vmin=mn, vmax=mx), cmap="viridis")
    else:
        plt.imshow(pattern, norm=Normalize(vmin=mn, vmax=mx), cmap='viridis')

    plt.xlabel(r'$x$ (pixel)')
    plt.ylabel(r'$y$ (pixel)')
    plt.colorbar()

def plot_resolution_rings(parameters):
    """ """
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

    # Max. scattering angle.
    theta_max = math.atan( 0.5*Npix * apix / Ddet )
    # Min resolution.
    d_min = 0.5*lmd/math.sin(theta_max)

    print "**** Info ****"
    print "E0     = ", E0
    print "lmd    = ", lmd
    print "apix   = ", apix
    print "Ddet   = ", Ddet
    print "Npix   = ", Npix
    print "th_max = ", theta_max
    print "d_min  = ", d_min
    print "**** Info ****"

    # Next integer resolution.
    d0 = 0.1*math.ceil(d_min*10.0) # 10 powers to get Angstrom
    # Array of resolution rings to plot.
    #ds = numpy.linspace(1.0, d0, 4)
    #ds = numpy.array([1.0, 0.5, .3, 0.2])
    ds = numpy.array([1.0, 0.5, .3])

    # Pixel numbers corresponding to resolution rings.
    Ns = Ddet/apix * numpy.arctan(numpy.arcsin(lmd/2./ds))


    for i,N in enumerate(Ns):
        x0 = 0.5*Npix
        X = numpy.linspace(x0-N,x0+N, 512)
        Y_up = x0 + numpy.sqrt(N**2 - (X-x0)**2)
        Y_dn = x0 - numpy.sqrt(N**2 - (X-x0)**2)
        plt.plot(X,Y_up,color='k')
        plt.plot(X,Y_dn,color='k')
        plt.text(0.5*Npix+0.75*N,0.5*Npix+0.75*N, "%2.1f" % (ds[i]*10.))

    plt.xlim(0,Npix)
    plt.ylim(0,Npix)

def diffraction_parameters(path):
    """ Extract beam parameters and geometry from given file or directory. """
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
    with h5py.File(h5_file, 'r') as h5:
        # Loop over entries in /params.
        for top_key in ['beam', 'geom']:
            # Loop over groups.
            for key, val in h5['params/%s' % (top_key)].iteritems():
                # Insert into return dictionary.
                parameters_dict[top_key][key] = val.value

    # Return.
    return parameters_dict

def get_pattern_from_file(path, index=None, poissonized=False):
    """ Workhorse function to extract a given pattern from a diffraction file. """
    if index is None:
        index = 1
    if os.path.isdir(path):
        return get_pattern_from_v0_1(path, index, poissonized)
    # Open file for reading
    with h5py.File(path, 'r') as h5:
        root_path = '/data/%0.7d/'% (index)
        if poissonized:
            path_to_data = root_path + 'data'
        else:
            path_to_data = root_path + 'diffr'

        diffr = h5[path_to_data].value

        return diffr,path

def generate_patterns_from_file(path, indices=None, poissonized=False):
    """ Workhorse function to yield an iterator over a given pattern sequence from a diffraction file. """
    if indices is None:
        indices = 'all'
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
                    if poissonized:
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
                indices = [key for key in h5['data'].iterkeys()]
            else:
                indices = ["%0.7d" % ix for ix in indices]
            for ix in indices:
                root_path = '/data/%s/'% (ix)
                if poissonized:
                    path_to_data = root_path + 'data'
                else:
                    path_to_data = root_path + 'diffr'

                diffr = h5[path_to_data].value

                yield diffr


def get_pattern_from_v0_1(path, pattern, poissonized=False):
    """ Workhorse function to extract a given pattern from a directory containing v0.1 diffraction files. """

    # Open file for reading
    filename = os.path.join(path, "diffr_out_%07d.h5" % (pattern))
    with h5py.File(filename, 'r') as h5:

        root_path = '/data/'
        if poissonized:
            path_to_data = root_path + 'data'
        else:
            path_to_data = root_path + 'diffr'

        diffr = h5[path_to_data].value

        return diffr,filename


        ## Setup a figure.
        #figure = plt.figure(figsize=(10, 10), dpi=100)
        #plt.axis('tight')
        ## Profile plot.
        #profile = plt.subplot2grid((3, 3), (1, 0), colspan=2, rowspan=2)

        ## Plot profile as 2D colorcoded map.
        #if logscale:
            #profile.imshow(wf_intensity, norm=mpl.colors.LogNorm(vmin=mn, vmax=mx), cmap="viridis")
        #else:
            #profile.imshow(wf_intensity, norm=mpl.colors.Normalize(vmin=mn, vmax=mx), cmap="viridis")

        #profile.set_aspect('equal', 'datalim')

        ## Get x and y ranges.
        #nx, ny = pattern_to_plot.shape
        #x = numpy.arange(nx)
        #y = numpy.arange(ny)


        #profile.set_xlabel(r'$x$ (pixel)')
        #profile.set_ylabel(r'$y$ (pixel)')

        ## x-projection plots above main plot.
        #x_projection = plt.subplot2grid((3, 3), (0, 0), sharex=profile, colspan=2)
        #x_projection.plot(x, pattern_to_plot.sum(axis=0), label='x projection')

        ## Set range according to input.
        #profile.set_xlim([xmin, xmax])

        ## y-projection plot right of main plot.
        #y_projection = plt.subplot2grid((3, 3), (1, 2), rowspan=2, sharey=profile)
        #y_projection.plot(pattern_to_plot.sum(axis=1), y, label='y projection')

        ## Hide minor tick labels, they disturb here.
        #plt.minorticks_off()

        ## Set range according to input.
        #profile.set_ylim([ymin, ymax])


#def main(filename, pattern_number):
    #""" """
    #print "Opening %s." % (filename)
    #with h5py.File(filename, 'r') as h5:
        #if pattern_number == "all" or pattern_number=="saxs":
            #plot_saxs(h5)
        #elif pattern_number == "animate":
            #os.mkdir("animation")
            #os.chdir("animation")
            #animate(h5)
            #os.system("convert -delay 100 *.png animation.gif")
            #os.chdir("..")

        #elif pattern_number == "photons":
            #photon_statistics(h5)

        #else:
            #plot_single(h5, pattern_number)

        #h5.close()

    ##plt.show()
    #plt.savefig("%0.7d_woRD.png" % (int(pattern_number)))

def photon_statistics(hdf_instance):
    """ """

    keys = hdf_instance["data"].keys()
    keys.sort()
    img = hdf_instance["data"][keys[0]]["data"].value
    stack = numpy.empty((len(keys), img.shape[0], img.shape[1]))
    number_of_photons = numpy.empty((len(keys)))

    for i,key in enumerate(keys):
        image = hdf_instance["data"][key]['data'].value
        stack[i] = image

        # Sum over image.
        photon_number = numpy.sum( image.flatten() )

        # Log.
        print "%d: pattern %s : %4.3e photons" % ( i, key, photon_number )

        # Save on list.
        number_of_photons[i] = photon_number

        del image


    # Take average and std.
    number_of_photons_avg = numpy.mean( number_of_photons )
    number_of_photons_std = numpy.std( number_of_photons )

    print "***********************"
    print "avg = %s, std = %s" % (number_of_photons_avg, number_of_photons_std)
    print "***********************"


    ## Plot number of photons as function of frame.
    #min_number_of_photons = 150
    #max_number_of_photons = 400
    #pylab.figure(0)
    #pylab.plot( number_of_photons, 'or' )
    #pylab.plot( numpy.ones(len(number_of_photons) ) * number_of_photons_avg, '-k',linewidth=2.0 )
    #pylab.plot( numpy.ones(len(number_of_photons) ) * (number_of_photons_avg+number_of_photons_std ), '-b' )
    #pylab.plot( numpy.ones(len(number_of_photons) ) * (number_of_photons_avg-number_of_photons_std ), '-b' )
    #pylab.xlabel("Diffraction pattern ")
    #pylab.ylabel("Detected photons")
    #pylab.title("Total number of photons per diffraction pattern")
    #pylab.xlim([0,number_of_samples])
    #pylab.ylim([min_number_of_photons, max_number_of_photons])

    ## Plot histogram.
    #pylab.figure(1)
    #max_photon_number = numpy.max( number_of_photons )
    #min_photon_number = numpy.min( number_of_photons )
    #binwidth = max_photon_number - min_photon_number
    #number_of_bins = 20
    #binwidth = int( binwidth / number_of_bins )

    #pylab.hist(number_of_photons, bins=xrange(min_photon_number, max_photon_number, binwidth), facecolor='red', alpha=0.75)
    #pylab.xlim([min_number_of_photons, max_number_of_photons])
    #pylab.xlabel("Photons")
    #pylab.ylabel("Histogram")
    #pylab.title("Photon number histogram")
    ##pylab.show()

    #pylab.figure(2)
    ## Average
    #sum_over_images = 1.0*sum_over_images / number_of_samples
    ## Offset for log scale.
    ##sum_over_images += 0.01 * numpy.min(sum_over_images[numpy.where(sum_over_images > 0)])
    #sum_over_images += 1e-4
    #vmax=10.
    #vmin=1.0e-4
    #raw_input([vmin, vmax])
    #pylab.pcolor(sum_over_images,norm=LogNorm(vmax=vmax, vmin=vmin), cmap='YlGnBu_r')
    ##pylab.pcolor(sum_over_images, cmap='YlGnBu_r')
    #pylab.colorbar()

    #pylab.figure(3)
    #pylab.semilogy( numpy.sum( sum_over_images, axis=0 ), label='x axis projection')
    #pylab.semilogy( numpy.sum( sum_over_images, axis=1 ), label='y axis projection')

    #pylab.legend()
    #pylab.show()

def plot_saxs(h5):
    """ """

    root_path = '/data/'

    saxs =  numpy.zeros_like(h5[root_path]["0000001/diffr"].value)

    for i,pattern in enumerate(h5[root_path].itervalues()):
        saxs += pattern["diffr"].value

    plt.imshow(numpy.log(saxs), cmap="YlGnBu_r",zorder=1)
    plot_resolution_rings()
    plt.colorbar()

def plot_single(h5, pattern_number):
    """ """

    root_path = '/data/%0.7d/'% (int(pattern_number))
    path_to_data = root_path + 'data'
    path_to_diffr = root_path + 'diffr'
    print 'Plotting pattern from %s' % (os.path.join(filename, path_to_data))
    diffr = h5[path_to_diffr].value
    if diffr.min() == 0:
        diffr = diffr.astype(float) + 1e-5
        plt.pcolor(diffr, norm=Normalize(vmin=mn, vmax=mx), cmap='viridis')
    else:
        plt.pcolor(diffr, norm=LogNorm(vmin=mn, vmax=mx), cmap='viridis')

    print "Range = [", diffr.min(), diffr.max(),"]"
    plot_resolution_rings()
    plt.colorbar()

def animate(h5):
    root_path = '/data/'

    img = h5[root_path+'0000001/diffr'].value

    keys = h5[root_path].keys()

    rands = numpy.random.choice(range(len(keys)), 20)
    keys = [keys[i] for i in rands]
    stack = numpy.empty((len(keys), img.shape[0], img.shape[1]))

    for i,key in enumerate(keys):
        print "Reading %s" % (key)
        stack[i] = h5[root_path][key]['diffr'].value

    mn, mx = stack.min(), stack.max()
    print "Range = [", mn,",", mx,"]"
    for i,img in enumerate(stack):
        plt.pcolor(img, norm=LogNorm(vmin=mn, vmax=mx), cmap='viridis')
        plot_resolution_rings()
        plt.title(keys[i])
        plt.colorbar()
        plt.savefig("%s.png" % (keys[i]))
        plt.clf()

#if __name__ == "__main__":

    #filename = sys.argv[1]
    #pattern_number = 1
    #if len(sys.argv) > 2:
        #pattern_number = sys.argv[2]

    #main(filename, pattern_number)

