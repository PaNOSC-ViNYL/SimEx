#!/usr/bin/env python2.7

import sys,os
import numpy, math
import h5py
from matplotlib import pyplot as plt
from matplotlib.colors import LogNorm, Normalize

def main(filename, pattern_number):
    """ """
    print "Opening %s." % (filename)
    with h5py.File(filename, 'r') as h5:
        if pattern_number == "all" or pattern_number=="saxs":
            plot_saxs(h5)
        elif pattern_number == "animate":
            os.mkdir("animation")
            os.chdir("animation")
            animate(h5)
            os.system("convert -delay 100 *.png animation.gif")
            os.chdir("..")

        elif pattern_number == "photons":
            photon_statistics(h5)

        else:
            plot_single(h5, pattern_number)

        h5.close()

    plt.savefig("%s_withRD.png" % (pattern_number))

def photon_statistics(hdf_instance):
    """ """

    keys = hdf_instance["data"].keys()
    keys.sort()
    img = hdf_instance["data"][keys[0]]["data"].value
    stack = numpy.empty((len(keys), img.shape[0], img.shape[1]))
    number_of_photons = numpy.empty((len(keys)))

    for i,key in enumerate(keys):
        print "Reading %s" % (key)
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

    root_path = '/data/'
    path_to_data = root_path + 'data'
    path_to_diffr = root_path + 'diffr'
    print 'Plotting pattern from %s' % (os.path.join(filename, path_to_data))
    diffr = h5[path_to_diffr].value
    #diffr = h5[path_to_data].value
    # Offset
    mn,mx =  1e-5, 19.00001
    if diffr.min() == 0:
        diffr = diffr.astype(float) + 1e-5
        plt.pcolor(diffr, norm=Normalize(vmin=mn, vmax=mx), cmap='viridis')
    else:
        plt.pcolor(diffr, norm=LogNorm(vmin=mn, vmax=mx), cmap='viridis')

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
    for i,img in enumerate(stack):
        plt.imshow(numpy.log(img), cmap="YlGnBu_r",zorder=1)
        plt.clim([numpy.log(mn), numpy.log(mx)])
        plot_resolution_rings()
        plt.title(keys[i])
        plt.colorbar()
        plt.savefig("%s.png" % (keys[i]))
        plt.clf()

def plot_resolution_rings():
    """ """
    # Photon energy and wavelength
    E0 = 4960.0
    lmd = 1239.8 / E0 # nm

    # Pixel dimension
    apix = 0.0012
    # Sample-detector distance
    Ddet = 0.13
    # Number of pixels in each dimension
    Npix = 80.0

    # Max. scattering angle.
    theta_max = math.atan( 0.5*Npix * apix / Ddet )
    # Min resolution.
    d_min = 0.5*lmd/math.sin(theta_max)

    print "**** Geometry ****"
    print "E0     = ", E0
    print "lmd    = ", lmd
    print "apix   = ", apix
    print "Ddet   = ", Ddet
    print "Npix   = ", Npix
    print "th_max = ", theta_max
    print "d_min  = ", d_min
    print "**** Geometry ****"

    # Next integer resolution.
    d0 = 0.1*math.ceil(d_min*10.0)
    # Array of resolution rings to plot.
    #ds = numpy.linspace(1.0, d0, 4)
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

if __name__ == "__main__":

    filename = sys.argv[1]
    pattern_number = 1
    if len(sys.argv) > 2:
        pattern_number = sys.argv[2]

    main(filename, pattern_number)

