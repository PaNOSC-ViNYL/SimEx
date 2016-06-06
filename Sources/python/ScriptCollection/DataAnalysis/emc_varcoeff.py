#!/usr/bin/env python
##########################################################################
#                                                                        #
# Copyright (C) 2015 Carsten Fortmann-Grote                              #
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

h5 = h5py.File('3d_stack.h5', 'r')

stacks = numpy.array(h5["data/oriented_diffraction_volumes"])
h5.close()

# First average over the individual reconstructions.
std = numpy.std(stacks, axis=0)
mean = numpy.mean(stacks, axis=0)

# Normalize the first std.
variation = std / mean

# Replace infs and nans by 0.
variation[numpy.where(numpy.isnan(variation))] = -1.0
variation[numpy.where(numpy.isinf(variation))] = -1.0

# Second average: over resolution shells.
nx, ny, nz = variation.shape

max_index = 45
r_grid = numpy.array([[[math.sqrt(ix**2 + iy**2 + iz**2) for iz in xrange(-max_index,max_index+1)] for iy in xrange(-max_index,max_index+1)] for ix in xrange(-max_index,max_index+1)])

radii = r_grid.flatten()



values = numpy.zeros(max_index)
squares = numpy.zeros(max_index)
norms = numpy.zeros(max_index)

for ix in range(nx):
    for iy in range(ny):
        for iz in range(nz):
            r = r_grid[ix, iy, iz]

            if r>=max_index: continue


            index = int( math.floor(r ) )

            var = variation[ix, iy, iz]

            # Filter out the zeros.
            if var == -1.0: continue
            #raw_input( (ix, iy, iz, r, index, var) )

            values[index] += var
            squares[index] += var**2
            norms[index] += 1.0


# Average each shell
averaged_values = values / norms
averaged_squares = squares / norms

std = numpy.sqrt( averaged_squares - averaged_values**2 )

#data_9fs = numpy.loadtxt('data/coeff_of_variation_9fs.dat')
#mean_9fs = data_9fs[:,1]
#std_9fs = data_9fs[:,2]

min_pixel = 5
max_pixel = 39
pyplot.errorbar( range(max_index)[min_pixel:max_pixel], averaged_values[min_pixel:max_pixel], yerr=std[min_pixel:max_pixel], fmt="s", label="3 fs" )
#pyplot.errorbar( range(max_index)[min_pixel:max_pixel], mean_9fs, yerr=std_9fs, fmt="s", label="9 fs")
pyplot.legend(loc=2)
pyplot.xlim([min_pixel-1,max_pixel+1])
pyplot.show()

