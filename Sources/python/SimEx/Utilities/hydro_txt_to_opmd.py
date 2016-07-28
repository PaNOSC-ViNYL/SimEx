##########################################################################
#                                                                        #
# Copyright (C) 2016 Richard Briggs, Carsten Fortmann-Grote              #
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

import h5py
import numpy
import os
import sys
from SimEx.Utilities import OpenPMDTools as opmd

def convertTxtToOPMD(esther_dirname=None):
    """
    Converts the esther .txt output files to opmd conform hdf5.
    @param esther_dirname: Path (absolute or relative) of the directory containing esther output.
    @type : str
    """
    # Check input.
    if not os.path.isdir( esther_dirname):
        raise IOError( "%s is not a directory or link to a directory.")

    # Get files in directory.
    dir_listing = os.listdir( esther_dirname)

    # We need these files.
    expected_files = ['densite_massique.txt', 'temperature_du_milieu.txt', 'pression_hydrostatique.txt', 'vitesse_moyenne.txt']

    if not all([f in dir_listing for f in expected_files]):
        raise IOError( "%s does not contain all relevant information (density, temperature, pressure, and velocity. Will abort now." )

    # Ok let's start reading header information.
    with open(esther_dirname+"/densite_massique.txt") as f:

        tmp = f.readline() # Save header line as temp.
        tmp = tmp.split() # Split header line to obtain timesteps and zones.
        number_of_timesteps = int(tmp[0])
        number_of_zones = int(tmp[1])

        # Close.
        f.close()

	# Load data via numpy.
	rho_array = numpy.loadtxt(str(esther_dirname)+"/densite_massique.txt",skiprows=3,unpack=True)
	pres_array = numpy.loadtxt(str(esther_dirname)+"/pression_hydrostatique.txt",skiprows=3,unpack=True)
	temp_array = numpy.loadtxt(str(esther_dirname)+"/temperature_du_milieu.txt",skiprows=3,unpack=True)
	vel_array = numpy.loadtxt(str(esther_dirname)+"/vitesse_moyenne.txt",skiprows=3,unpack=True)

    # Slice out the timestamps.
	time_array = rho_array[0]
    time_array = time_array
    time_step = time_array[1] - time_array[0]

    # Create opmd.h5 output file
    with h5py.File(str(esther_dirname)+".opmd.h5", 'w') as opmd_h5:


        # Setup the root attributes.
        opmd.setup_root_attr( opmd_h5, extension="HYDRO1D" )

        # Loop over all timestamps.
        for it in range(number_of_timesteps):
            # Write opmd
            full_meshes_path = opmd.get_basePath(opmd_h5, it) + opmd_h5.attrs["meshesPath"]

            # Setup basepath
            opmd.setup_base_path( opmd_h5, iteration=it, time=rho_array[0,it], time_step=time_step)
            opmd_h5.create_group(full_meshes_path)
            meshes = opmd_h5[full_meshes_path]


            # Create and save datasets
            meshes.create_dataset('rho',  data=rho_array[1:,it])
            meshes.create_dataset('pres', data=pres_array[1:,it])
            meshes.create_dataset('temp', data=temp_array[1:,it])
            meshes.create_dataset('vel',  data=vel_array[1:,it])

            # Assign SI units
            #                L      M     t     I     T     N     Lum
            meshes['rho'].attrs["unitDimension"] = \
                numpy.array([-3.0,  1.0,  0.0,  0.0,  0.0,  0.0,  0.0], dtype=numpy.float64) # kg m^-3
            meshes['pres'].attrs["unitDimension"] = \
                numpy.array([ 1.0, -1.0, -2.0,  0.0,  0.0,  0.0,  0.0], dtype=numpy.float64) # N m^-2 = kg m s^-2 m^-2 = kg m^-1 s^-2
            meshes['temp'].attrs["unitDimension"] = \
                numpy.array([ 0.0,  0.0,  0.0,  0.0,  1.0,  0.0,  0.0], dtype=numpy.float64) # K
            meshes['vel'].attrs["unitDimension"] = \
                numpy.array([ 1.0,  0.0, -1.0,  0.0,  0.0,  0.0,  0.0], dtype=numpy.float64) # m s^-1

            # Write common attributes.
            axis_label = ["Zones"]
            geometry = numpy.string_("other")
            grid_spacing = [numpy.float64(1.0)]
            grid_global_offset = [numpy.float64(0.0)]
            grid_unit_si = numpy.float64(1.0)
            time_offset = 0.0
            data_order = numpy.string_("C")

            # Write the common metadata to pass test
            for key in meshes.keys():
                meshes[key].attrs["unitSI"] = 1.0
                meshes[key].attrs["axisLabels"] = axis_label
                meshes[key].attrs["geometry"] = geometry
                meshes[key].attrs["gridSpacing"] = grid_spacing
                meshes[key].attrs["gridGlobalOffset"] = grid_global_offset
                meshes[key].attrs["gridUnitSI"] = grid_unit_si
                meshes[key].attrs["timeOffset"] = time_offset
                meshes[key].attrs["dataOrder"] = data_order
                meshes[key].attrs["position"] = numpy.array([0.5, 0.5], dtype=numpy.float32)

        opmd_h5.close()

