import h5py
import numpy as np
import os
import sys

def convertTxtToOPMD(input):
	""" Converts the .txt files that are output by Esther simulation program
		@param simulation_name: The folder of simulations files to be converted
		@type : string
		@example: simulation_name = "test"
	"""
	
	# Open in and out files
	f_rho = open(str(input)+"/densite_massique.txt")

	
	#f_pres = open(str(input)+"/pression_hydrostatique.txt")
	#f_temp = open(str(input)+"/temperature_du_milieu.txt")
	#f_vel = open(str(input)+"/vitesse_moyenne.txt")
	h5 = h5py.File(str(input)+".h5", 'w')
	
	tmp = f_rho.readline() # Save header line as temp
	tmp = tmp.split() # Split header line to obtain timesteps and zones
	number_of_timesteps = int(tmp[0])
	number_of_zones = int(tmp[1])	
	f_rho.close()

	rho_array = np.loadtxt(str(input)+"/densite_massique.txt",skiprows=3,unpack=True)
	#print (rho_array.shape)		
	pres_array = np.loadtxt(str(input)+"/pression_hydrostatique.txt",skiprows=3,unpack=True)
	temp_array = np.loadtxt(str(input)+"/temperature_du_milieu.txt",skiprows=3,unpack=True)
	vel_array = np.loadtxt(str(input)+"/vitesse_moyenne.txt",skiprows=3,unpack=True)
	
	time_array = rho_array[0]
	# Unit Conversions
	time_array = time_array * 1e9 	# Convert time into nanoseconds
	timestep = time_array[1] - time_array[0] # time step in ns
	
	#
	# Need to convert rho, pressure, temp, and vel to SI ready for OMPD
	#
	
	datagroup = h5.create_group('data')
	
	for row in range(number_of_timesteps):
		# Create and save datasets
		datagroup.create_dataset(str(row)+'/rho', data=rho_array[1:,row])
		datagroup.create_dataset(str(row)+'/pres', data=pres_array[1:,row])
		datagroup.create_dataset(str(row)+'/temp', data=temp_array[1:,row])
		datagroup.create_dataset(str(row)+'/vel', data=vel_array[1:,row])
	
		# Save time attribute
		datagroup[str(row)].attrs["time"] = rho_array[0,row]
	
	h5.close()
		

simulation_name = "test" # Simulation folder
convertTxtToOPMD(simulation_name)