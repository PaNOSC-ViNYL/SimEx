#!/usr/bin/env python
##########################################################################
#                                                                        #
# Copyright (C) 2016 Carsten Fortmann-Grote                              #
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

### Calculate double averaged variation coefficient over stack of 3D diffraction volumes.

import numpy
import h5py
import scipy
import math

import matplotlib
matplotlib.use('Qt4Agg')
from matplotlib import pyplot

#h5 = h5py.File('3d_stack_test.h5', 'r')
h5 = h5py.File('3d_stack.h5', 'r')

stacks = numpy.array(h5["data/oriented_diffraction_volumes"])
h5.close()

##############################################################
# First average over the individual reconstructions.
##############################################################
std = numpy.std(stacks, axis=0)
mean = numpy.mean(stacks, axis=0)

# Normalize the first std.
variation = std / mean

# Replace infs and nans by 0.
variation[numpy.where(numpy.isnan(variation))] = -1.0
variation[numpy.where(numpy.isinf(variation))] = -1.0

##############################################################
# Second average over resolution shells.
##############################################################
nx, ny, nz = variation.shape

# Index of the central voxel (assuming cubic shape). This is also the length of the results arrays.
central_index = ((nx-1)/2)
radius = float(central_index)

# This grid carries the distance of each pixel from the central pixel.
r_grid = numpy.array([[[math.sqrt((float(ix)-radius)**2 + (float(iy)-radius)**2 + (float(iz)-radius)**2) for ix in range(nx)] for iy in range(ny)] for iz in range(nz)])

# Setup arrays to hold results.
# For values.
values = numpy.zeros(central_index)
# For square of values.
squares = numpy.zeros(central_index)
# For number of elements at each index.
norms = numpy.zeros(central_index)

for iz in range(nz):
    for iy in range(ny):
        for ix in range(nx):
            r = r_grid[iz, iy, ix]

            if r>=central_index: continue

            index = int( math.floor(r ) )

            var = variation[iz, iy, ix]

            # Filter out the zeros.
            if var == -1.0: continue

            values[index] += var
            squares[index] += var**2
            norms[index] += 1.0


# Average each shell
averaged_values = values / norms
averaged_squares = squares / norms

std = numpy.sqrt( averaged_squares - averaged_values**2 )
indices = range(central_index)

out_data = numpy.array([[i, averaged_values[i],  std[i]] for i in indices])
numpy.savetxt('varcoeff.txt', out_data)

#data_9fs = numpy.loadtxt('/home/grotec/Work/XFEL/SPB_3fs/reconstruction/data/coeff_of_variation_9fs.dat')
#mean_9fs = data_9fs[:,1]
#std_9fs = data_9fs[:,2]
#min_pixel = 5
#max_pixel = 38
#pyplot.errorbar( xrange(min_pixel, max_pixel), averaged_values[min_pixel:], yerr=std[min_pixel:], fmt="s", label="9 fs (new analysis, no Compton)" )
#pyplot.errorbar( xrange(min_pixel, max_pixel), mean_9fs[:-1], yerr=std_9fs[:-1], fmt="s", label="9 fs (Yoon et al. (2016), w/ Compton)")
#pyplot.legend(loc=2)
#pyplot.xlim([min_pixel-1,max_pixel+1])
#pyplot.show()

