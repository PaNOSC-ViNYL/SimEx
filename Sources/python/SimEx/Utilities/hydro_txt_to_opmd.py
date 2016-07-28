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

def convertTxtToOPMD(inumpyut):
	""" Converts the .txt files that are output by Esther simulation program.
		@param inumpyut: The folder containing the simulation output files to be converted.
		@type : string
		@example: inumpyut = "test"
	"""

	# Check all inumpyut files exist in the inumpyut directory

	# Open output file to obtain timesteps + number of zones
	f = open(str(inumpyut)+"/densite_massique.txt")


	tmp = f.readline() # Save header line as temp
	tmp = tmp.split() # Split header line to obtain timesteps and zones
	number_of_timesteps = int(tmp[0])
	number_of_zones = int(tmp[1])
	f.close()

	# Create h5 output file
	opmd_h5 = h5py.File(str(inumpyut)+".opmd.h5", 'w')

	# Load data
	rho_array = numpy.loadtxt(str(inumpyut)+"/densite_massique.txt",skiprows=3,unpack=True)
	pres_array = numpy.loadtxt(str(inumpyut)+"/pression_hydrostatique.txt",skiprows=3,unpack=True)
	temp_array = numpy.loadtxt(str(inumpyut)+"/temperature_du_milieu.txt",skiprows=3,unpack=True)
	vel_array = numpy.loadtxt(str(inumpyut)+"/vitesse_moyenne.txt",skiprows=3,unpack=True)

    # Slice out the timestamps.
	time_array = rho_array[0]
	# Unit Conversions
	time_array = time_array * 1e9 	# Convert time into nanoseconds
	time_step = time_array[1] - time_array[0] # time step in ns


    # Loop over all timestamps.
	for it in range(number_of_timesteps):
		# Write opmd
		# Setup the root attributes for iteration 0
		opmd.setup_root_attr( opmd_h5 )

		full_meshes_path = opmd.get_basePath(opmd_h5, it) + opmd_h5.attrs["meshesPath"]

		# Setup basepath
		opmd.setup_base_path( opmd_h5, iteration=it, time=rho_array[0,it], time_step=time_step)
		opmd_h5.create_group(full_meshes_path)
		meshes = opmd_h5[full_meshes_path]


		# Create and save datasets
		meshes.create_dataset('rho', data=rho_array[1:,it])
		meshes.create_dataset('pres', data=pres_array[1:,it])
		meshes.create_dataset('temp', data=temp_array[1:,it])
		meshes.create_dataset('vel', data=vel_array[1:,it])

		# Assign SI units
        #              L     M     t     I     T     N     Lum
		meshes['rho'].attrs["unitDimension"] = \
			numpy.array([-3.0,  1.0,  0.0,  0.0,  0.0,  0.0,  0.0], dtype=numpy.float64)
		meshes['pres'].attrs["unitDimension"] = \
			numpy.array([ 1.0, -1.0, -2.0,  0.0,  0.0,  0.0,  0.0], dtype=numpy.float64) #  N m^-2 = kg m s^-2 m^-2 = kg m^-1 s^-2
		meshes['temp'].attrs["unitDimension"] = \
			numpy.array([ 0.0,  0.0,  0.0,  0.0,  1.0,  0.0,  0.0], dtype=numpy.float64) # K
		meshes['vel'].attrs["unitDimension"] = \
			numpy.array([ 1.0,  0.0, -1.0,  0.0,  0.0,  0.0,  0.0], dtype=numpy.float64) # m s^-1

		# All data are already stored in SI units
		meshes['rho'].attrs["unitSI"] = 1.0
		meshes['pres'].attrs["unitSI"] = 1.0
		meshes['temp'].attrs["unitSI"] = 1.0
		meshes['vel'].attrs["unitSI"] = 1.0
		
		# Write the common metadata to pass test
		meshes['rho'].attrs["axisLabels"] = "Zones"
		meshes['pres'].attrs["axisLabels"] = "Zones"
		meshes['temp'].attrs["axisLabels"] = "Zones"
		meshes['vel'].attrs["axisLabels"] = "Zones"
		meshes['rho'].attrs["geometry"] = numpy.string_("NA")
		meshes['rho'].attrs["gridSpacing"] = numpy.string_("NA")
		meshes['rho'].attrs["gridGlobalOffset"] = numpy.string_("NA")
		meshes['rho'].attrs["gridUnitSI"] = numpy.float64(1.0)
		meshes['rho'].attrs["timeOffset"] = 0.
		meshes['pres'].attrs["geometry"] = numpy.string_("NA")
		meshes['pres'].attrs["gridSpacing"] = numpy.string_("NA")
		meshes['pres'].attrs["gridGlobalOffset"] = numpy.string_("NA")
		meshes['pres'].attrs["gridUnitSI"] = numpy.float64(1.0)
		meshes['pres'].attrs["timeOffset"] = 0.
		meshes['temp'].attrs["geometry"] = numpy.string_("NA")
		meshes['temp'].attrs["gridSpacing"] = numpy.string_("NA")
		meshes['temp'].attrs["gridGlobalOffset"] = numpy.string_("NA")
		meshes['temp'].attrs["gridUnitSI"] = numpy.float64(1.0)
		meshes['temp'].attrs["timeOffset"] = 0.
		meshes['vel'].attrs["geometry"] = numpy.string_("NA")
		meshes['vel'].attrs["gridSpacing"] = numpy.string_("NA")
		meshes['vel'].attrs["gridGlobalOffset"] = numpy.string_("NA")
		meshes['vel'].attrs["gridUnitSI"] = numpy.float64(1.0)
		meshes['vel'].attrs["timeOffset"] = 0.
		meshes['rho'].attrs["dataOrder"] = numpy.string_("C")
		meshes['pres'].attrs["dataOrder"] = numpy.string_("C")
		meshes['temp'].attrs["dataOrder"] = numpy.string_("C")
		meshes['vel'].attrs["dataOrder"] = numpy.string_("C")
		
	opmd_h5.close()
