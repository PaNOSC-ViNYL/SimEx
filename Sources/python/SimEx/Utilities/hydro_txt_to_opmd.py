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
import numpy as np
import os
import sys

def convertTxtToOPMD(input):
	""" Converts the .txt files that are output by Esther simulation program.
		@param input: The folder containing the simulation output files to be converted.
		@type : string
		@example: input = "test"
	"""

	# Open density file to get header information (common to all input files).
	f_rho = open(str(input)+"/densite_massique.txt")

    # Open output file.
	h5 = h5py.File(str(input)+".h5", 'w')

	tmp = f_rho.readline() # Save header line as temp.
	tmp = tmp.split() # Split header line to obtain timesteps and zones.
	number_of_timesteps = int(tmp[0])
	number_of_zones = int(tmp[1])
	f_rho.close()

    # Extract density, pressure, temperature, and velocity.
	rho_array = np.loadtxt(str(input)+"/densite_massique.txt",skiprows=3,unpack=True)
	pres_array = np.loadtxt(str(input)+"/pression_hydrostatique.txt",skiprows=3,unpack=True)
	temp_array = np.loadtxt(str(input)+"/temperature_du_milieu.txt",skiprows=3,unpack=True)
	vel_array = np.loadtxt(str(input)+"/vitesse_moyenne.txt",skiprows=3,unpack=True)

    # Slice out the timestamps.
	time_array = rho_array[0]
	# Unit Conversions
	time_array = time_array * 1e9 	# Convert time into nanoseconds
	timestep = time_array[1] - time_array[0] # time step in ns

	#
	# Need to convert rho, pressure, temp, and vel to SI ready for OMPD
	#

    # Create h5 group.
	datagroup = h5.create_group('data')

    # Loop over all timestamps.
	for row in range(number_of_timesteps):
		# Create and save datasets
		datagroup.create_dataset(str(row)+'/rho', data=rho_array[1:,row])
		datagroup.create_dataset(str(row)+'/pres', data=pres_array[1:,row])
		datagroup.create_dataset(str(row)+'/temp', data=temp_array[1:,row])
		datagroup.create_dataset(str(row)+'/vel', data=vel_array[1:,row])

        # Save time attribute
		datagroup[str(row)].attrs["time"] = rho_array[0,row]

	h5.close()
