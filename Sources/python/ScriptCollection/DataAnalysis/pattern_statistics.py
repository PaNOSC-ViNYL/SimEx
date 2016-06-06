""" @file Script to get statistics from diffraction patterns
    @author CFG
    @date 2016.02.02
    @institution XFEL.EU
"""

import os, sys
import h5py
import numpy
import matplotlib
matplotlib.use('Qt4Agg')
import matplotlib.pyplot as pylab
from matplotlib.colors import LogNorm

# 3fs, no Compton, 200k patterns
root_path = os.path.abspath("/home/grotec/exflst_data/simS2E_data/5keV_3fs_nz35/diffr_200k_noCompton")

## 3fs, w/ Compton, 200k patterns
#root_path = os.path.abspath("/home/grotec/exflst_data/simS2E_data/5keV_3fs_nz35/diffr")

## 9fs, no Compton, 200k patterns
#root_path = os.path.abspath("/home/grotec/exflst_data/simS2E_data/sim_5kev_9fs_35_2NIP_EMC_noCompton/diffr")

## 30fs, no Compton, 200k patterns
#root_path = os.path.abspath("/home/grotec/exflst_data/simS2E_data/sim_5kev_30fs_35_2NIP_EMC_noCompton/diffr")

# 30fs, w/ Compton, 200k patterns
#root_path = os.path.abspath("/home/grotec/exflst_data/simS2E_data/sim_5kev_30fs_35_2NIP_EMC_Compton/diffr")
#root_path = os.path.abspath("/home/grotec/mnt/yoon/singfel/dataS2E/sim_5kev_30fs_35_2NIP_EMC/diffr")

if not os.path.isdir( root_path ):
    raise IOError( "Path %s does not exist." % (root_path) )
    sys.exit()

# Common part of all filenames.
basename = "diffr_out_"

# Start and stop file.
min_index = 1
max_index = 100000
number_of_samples = 2000
# Take into account 1 based indexing scheme in filenames.
file_indices = numpy.arange(min_index, max_index+1)

file_indices = numpy.random.choice(file_indices, number_of_samples, replace=False)

# Empty list to store total number of photons per frame.
number_of_photons = []
# Loop over all files.

# Take photons or fields
#data = 'diffr' # fields
data = 'data'  # photons

for i, file_index in enumerate(file_indices):

    # Aggregate file path.
    path = os.path.join( root_path, "%s%07d.h5" % (basename, file_index) )

    # Open for reading.
    try:
        hdf_instance = h5py.File(path, "r")

        # Get data (Poissonized).
        image_data = hdf_instance['data'][data]

        # Convert to numpy.
        image_data = numpy.array(image_data)

        # Sum over image.
        photon_number = numpy.sum( image_data.flatten() )

        if i == 0:
            #sum_over_images = numpy.log(1+image_data)
            sum_over_images = image_data
        else:
            #sum_over_images += numpy.log(1+image_data)
            sum_over_images += image_data

        # Log.
        print "%d, pattern #%07d : %s photons" % ( i, file_index, photon_number )

        # Save on list.
        number_of_photons.append( photon_number )

        hdf_instance.close()
        del image_data

    except:
        #raise
        continue

# Convert to numpy.
#number_of_photons = numpy.array( number_of_photons  )

## Take average and std.
#number_of_photons_avg = numpy.mean( number_of_photons )
#number_of_photons_std = numpy.std( number_of_photons )

#print "***********************"
#print "avg = %s, std = %s" % (number_of_photons_avg, number_of_photons_std)
#print "***********************"


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

pylab.figure(2)
# Average
sum_over_images = 1.0*sum_over_images / number_of_samples
# Offset for log scale.
#sum_over_images += 0.01 * numpy.min(sum_over_images[numpy.where(sum_over_images > 0)])
sum_over_images += 1e-4
vmax=10.
vmin=1.0e-4
raw_input([vmin, vmax])
pylab.pcolor(sum_over_images,norm=LogNorm(vmax=vmax, vmin=vmin), cmap='YlGnBu_r')
#pylab.pcolor(sum_over_images, cmap='YlGnBu_r')
pylab.colorbar()

pylab.figure(3)
pylab.semilogy( numpy.sum( sum_over_images, axis=0 ), label='x axis projection')
pylab.semilogy( numpy.sum( sum_over_images, axis=1 ), label='y axis projection')

pylab.legend()
pylab.show()
