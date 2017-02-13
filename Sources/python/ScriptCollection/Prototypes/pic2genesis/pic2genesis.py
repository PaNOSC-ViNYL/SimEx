##########################################################################
#                                                                        #
# Copyright (C) 2016 Carsten Fortmann-Grote, Ashutosh Sharma             #
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

""" :module pic2genesis: Script to convert openpmd output from picongpu to a genesis beam.dat file. """

import numpy
import h5py

pic_file_name = sys.argv([1])
pic_file = h5py.File( pic_file_name )

# Read in the electron data and form a 6D phase space distribution

# Setup datastructure for genesis

# Outout
genesis_beam_file_name = "beam.dat"
with open( genesis_beam_file_name, 'w' ) as g:
    # Write a header
    # Write the data
    g.write("")


    g.close()

print "Writing %s done." % (genesis_beam_file_name)
