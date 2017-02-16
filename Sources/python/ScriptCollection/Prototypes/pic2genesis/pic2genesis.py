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


pic_file_name = "simData_8000.h5" # relative to cwd.
timestep = 8000
pic_file_path = os.path.abspath( os.path.join( os.path.dirname(__file__), pic_file_name))
print pic_file_path
#  Check path.
if not os.path.isfile(pic_file_path):
    raise RuntimeError("%s is not a file." % (pic_file_name))

with h5py.File( pic_file_path, 'r' ) as h5_handle:

    inf0 = '/data/%d/particles/e/position/' % (timestep)
    print inf0
    inf1 = '/data/%d/particles/e/momentum/' % (timestep)

    x_data = h5_handle[inf0]['x'].value;
    x_data_unit = h5_handle[inf0]['x'].attrs['unitSI'];
    x = x_data*x_data_unit;

    y_data = h5_handle[inf0]['y'].value;
    y_data_unit = h5_handle[inf0]['y'].attrs['unitSI'];
    y = y_data*y_data_unit;

    z_data = h5_handle[inf0]['z'].value;
    z_data_unit = h5_handle[inf0]['z'].attrs['unitSI'];
    z = z_data*z_data_unit;

    px_data = h5_handle[inf1]['x'].value;
    px_data_unit = h5_handle[inf1]['x'].attrs['unitSI'];
    px = px_data*px_data_unit;

    py_data = h5_handle[inf1]['y'].value;
    py_data_unit = h5_handle[inf1]['y'].attrs['unitSI'];
    py = py_data*py_data_unit;

    pz_data = h5_handle[inf1]['z'].value;
    pz_data_unit = h5_handle[inf1]['z'].attrs['unitSI'];
    pz = pz_data*pz_data_unit;
    
    charge_group = h5_handle['/data/%d/particles/e/charge/' %(timestep)]
    
    charge_value = charge_group.attrs['value']
    charge_unit = charge_group.attrs['unitSI']
    charge = charge_value * charge_unit # 1e in As
    
    particle_patches = h5_handle['/data/%d/particles/e/particlePatches/numParticles' %(timestep)].value
    total_number_of_electrons = numpy.sum( particle_patches )
    
    total_charge = total_number_of_electrons * charge
    
    print total_charge
    
    me = 9.1E-31
    c0 = 3e8
    psquare = px**2 + py**2 + pz**2
    gamma = numpy.sqrt( 1. + psquare/((me*c0)**2))

    h5_handle.close()

out_data = numpy.vstack([ x, px, z, pz, y, gamma]).transpose()
numpy.savetxt( 'beam.dat', out_data)
