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
import sys, os
import platform


pic_file_name = "simData_8000.h5"
pic_file_path = os.path.abspath(pic_file_name)
print pic_file_path
#  Check path.
if not os.path.isfile(pic_file_name):
    raise RuntimeError("%s is not a file." % (pic_file_name))


if platform.system() == 'Linux':
    from oct2py import octave as engine
elif platform.system() == 'Windows':
   import matlab.engine
   engine = matlab.engine.start_matlab()


#
ml_lib_path = os.path.join(os.path.dirname(__file__))
print ml_lib_path
# Add path 
if platform.system() == 'Windows':
    engine.addpath(ml_lib_path, nargout=0)
elif platform.system() == 'Linux':
    engine.addpath(ml_lib_path)
# Load .m module.
beam_file_path = engine.pic2genesis(pic_file_path) 

print beam_file_path

#engine.read_pic_data(pic_file_name)
if platform.system() == 'Windows':
        engine.quit()
# Read in the electron data and form a 6D phase space distribution
 
# Setup datastructure for genesis

# Outout
#genesis_input_file = engine.PIC_DATA(InData_GENESIS.txt) 

#print "Writing %s done." % (InData_GENESIS)
