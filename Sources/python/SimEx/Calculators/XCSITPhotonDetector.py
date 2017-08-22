##########################################################################
#                                                                        #
# Copyright (C) 2015-2017 Jan-Philipp Burchert, Carsten Fortmann-Grote   #
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

# IO class imports
import PhotonEntry_ext
import PhotonData_ext
import InteractionEntry_ext
import InteractionData_ext
import ChargeEntry_ext
import ChargeMatrix_ext

# Simulation imports
import ParticleSim_ext
import ChargeSim_ext

import os
import numpy as np

from SimEx.Calculators import AbstractPhotonDetector
from SimEx.Calculators import XCSITPhotonDetectorParameters

class XCSITPhotonDetector(AbstractPhotonDetector):
	"""
	Class representing an free electorn laser photon detector
	"""

	# Define the allowed attributes
	__slot__ = "__parameters",\
               "__expected_data",\
               "__provided_data",\
               "__input_path",\
               "__output_path",\
               "__photon_data",\
               "__ia_data",\
               "__charge_data"


	# Definition of the init
	__init__(self,parameters=None,input_path=None,output_path=None):
		"""
		:param parameters: Parameters of the calulator such as the type of
			detector
		:type parameters: XCSITPhotonDetector

		:param input_path: Path to the hdf5 file holding the input data.
		:type input_path: str

		:param output_path: Path pointing to the path for output
		:type output_path: str
		"""

        ### COMMENT: Consider moving these checks and sets to propery setters. What if a parameter is set via
        ### COMMENT: setter method? then, no check would happen.

		# Handle parameters
		if parameters == None:
			raise ValueError("A parameters instance must be given.")
		if not isinstance(parameters, XCSITPhotonDetectorParameters):
			raise TypeError("Only XCSITPhotonDetectorParameters instances  are allowed as input.")

		# Checking of in and output path are given and assign them for storage
		# to internals
		if input_path is None)
			raise ValueError("The parameter 'input_path' must be specified.")

		if output_path is None)
			raise ValueError("The parameter 'output_path' has to be specified.")

		# input and output path can either be dirctionaries or files but must be
		# relative pathes
		# Cases:
		# 1) ends with .h5     -> it is a file: no action
		# 2) ends without .h5
		# 		a) Such a dictionary exists  -> invent a new file to put in or
		# 		look up existing
		#		b) Such a dictionary does not exist -> filename without .h5
		#		specified, but parent folder has to exist

		# Join the current working directory with the relative path given
        ### COMMENT: What if an absolute path is given?
		abs_inpath = os.path.normpath(os.path.join(os.getcwd(), input_path))
		if abs_inpath.endswith(".h5"):
			# a specified file
			if not os.path.exists(abs_inpath):
				raise IOError("File " + str(abs_inpath) + " does not exist.")
		else:
			# Check for existing input file
			if os.path.isdir(abs_inpath):
				count = 1
				found = ""
				for candidate in os.listdir(abs_inpath)
					# the candidates file
					if candidate.endswith(".h5"):
						found = candidate
						count -= 1

					# there should be only one candidate file
					# TODO: loop over all files
					if count < 0:
						raise IOError("Multiple files ending with .h5 in "+
							str(abs_inpath))

				if count == 1:
					raise IOError("There is no such input file.")
				abs_inpath = os.path.join(abs_inpath, found)

			# last argument is file name
			else:
				# Check if parent is not an existing directory
				path, test = os.path.split(abs_inpath)
				if not os.path.isdir(path):
					raise IOError("Please specify the input file and path
						directly.")
				else:
					abs_inpath += ".h5"

		# Join the current working directory with the relative path given
		abs_outpath = os.path.normpath(os.path.join(os.getcwd(), output_path))
		if abs_outpath.endswith(".h5"):
			# a specified file
			if not os.path.exists(abs_outpath):
				raise IOError("File " + str(abs_outpath) + " does not exists")
		else:
			# Check for existing directory
			if os.path.isdir(abs_outpath):
				abs_outpath = os.path.join(abs_out_path,"XCSITDetectorOutput.h5")

			# last argument is file name
			else:
				# Check if parent is not an existing directory
				path, test = os.path.split(abs_outpath)
				if not os.path.isdir(path):
					raise IOError("Please specify the input file and path
						directly")
				else:
					abs_outpath += ".h5"


		# Save the input in attributes
		self.__parameters = parameters
		self.__input_path = abs_inpath
		self.__output_path= abs_outpath

		# Init base class
		super(XCSITPhotonDetector,self).__init__(parameters,input_path,output_path)

		# Define the input and output structure of the hdf5 file
		self.__expected_data = ['/data/data', # <- poissonized (int)
                                '/data/diffr',# <- intensities (float)
                                '/data/angle',
                                '/history/parent/detail',
                                '/history/parent/parent',
                                '/info/package_version',
                                '/info/contact',
                                '/info/data_description',
                                '/info/method_description',
                                '/params/geom/detectorDist',
                                '/params/geom/pixelWidth',
                                '/params/geom/pixelHeight',
                                '/params/geom/mask',
                                '/params/beam/photonEnergy',
                                '/params/beam/photons',
                                '/params/beam/focusArea',
                                '/params/info',
                                ]

		self.__provided_data = ['/data/data', # <- store charge matrix here, in ADU
								'/data/photons' # <- store photon/pixel map here, no directions
								'/data/interactions',
                                '/history/parent/',
                                '/info/package_version',
                                '/params/geom/detectorDist',
                                '/params/geom/pixelWidth',
                                '/params/geom/pixelHeight',
                                '/params/beam/photonEnergy',
                                ]





	def expectedData(self):
		return self.__expectedData

	def providedData(self):
		return self.__providedData

	def getChargeData(self):
		return self.__charge_data

	def getInteractionData(self):
		return self.__ia_data

	def getPhotonData(self):
		return self.__photon_data

	def __createXCSITInteractions(self):
		self.__ia_data = InteractionData_ext.InteractionData()

	def __createXCSITChargeMatrix(self):
		self.__charge_data = ChargeMatrix_ext.ChargeMatrix()
		# Size will be addapted by ParticleSim.cc implementation


	# Subengine to calulate the particle simulation: The interaction of the
	# photons with the detector of choice
	def __backenginIA(self):
		"""
		Run the particle simulation
		"""
		# Check containers
		if self.__photon_data == None:
			raise RuntimeError("Photon container has not been initialized yet.")
		if self.__ia_data == None:
			raise RuntimeError("Interaction container has not been initialized yet.")
		# Run the simulation
		ps = ParticleSim_ext.ParticleSim()
		ps.initialization(self.__parameters["detector_type"])
		ps.runSimulation(self.__photon_data,self.__ia_data)
		# Results are directly written to the __ia_data instance


	def __backengineCP(self):
		"""
		Run the charge simulation
		"""
		# Check containers
		if self.__ia_data == None:
			raise RuntimeError("interaction container has not been initialized
yet")
		if self.__charge_data == None:
			raise RuntimeError("charge matrix has not been initialized yet")


		# Run the simulation
		cs = ChargeSim_ext.ChargeSim()
		cs.setInput(self.__ia_data)
		cs.setComponents(self.__charge_data,
						self.__parameters["plasma_search_flag"],
						self.__parameters["plasma_simulation_flag"],
						self.__parameters["point_simulation_method"],
						self.__parameters["detector_type"]
						)
		cs.runSimulation()


	def backengine(self):
		"""
		Executes the simulation of the particle and charge simulation.
		"""
		print("\nSimulating photon-detector interaction.")
		# Create the containers
		self.__ia_data 		= self.__createXCSITInteractions(self)
		self.__charge_data	= self.__createXCSITChargeMatrix(self)

		# Run the particle simulation.
        ### Check status of backengine.
		self.__backengineIA(self)
		print("Interaction simulation of the detector is finished.")

		# Run the charge simulation.
        ### Check status of backengine.
		self.__backengineCP(self)
		print("Charge propagation simulation in the detector is finished.")

	def __normalize(vector):
        ### What's this? can we use numpy.linalg.norm?
		su = 0
		length = len(vector)
		out = np.zero((length,1))
		i = 0
		for j in vector:
			su += j
			out[i] = j
			i++
		if su == 0:
			return out
		for i in list(range(length)):
			out[i] = out[i]/su;
		return out

	def _readH5(self):
		"""
		Reads the hdf5 file and create the storage container for the photons
		according to that data
		"""
		# The __input_path is a non relative path to an existing file
		if not os.path.exists(self.__input_path):
			raise RuntimeError("Input file " + str(self.__input_path) + " does
				not exists")

		# Open the input file
		infile = self.__input_path
        with h5py.File(infile,"r") as h5_infile:

            # Get the array where each pixel contains a number of photons
            photons = h5_infile["data/data"]
            x_num = len(photons)		# Assuming an rectangle
            y_num = len(photons[0])

            # Parameters of the matrix
            detector_dist = h5_infile["params/geom/detectorWidth"]
            x_pixel = h5_infile["params/geom/pixelWidth"]
            y_pixel = h5_infile["params/geom/pixelHeight"]
            center_energy = h5_infile["params/beam/photonEnergy"] # missing profile

            # Define base vectors
            base_x = np.zeros((3,1))
            base_x[0] = x_pixel
            base_y = np.zeros((3,1))
            base_y[1] = y_pixel
            base_z = np.zeros((3,1))
            base_z[2] = detector_dist

            # Create the photon instance
            self.__photon_data = PhotonData_ext.PhotonData()

            # Assumptions
            # - All the photon originate from the center
            # - photon energy is everywhere the same in the beam
            #
            for i in list(range(x_num)):
                for j in list(range(y_num)):
                    # Calculate the photon flight vector with respect to the matrix
                    # center
                    direct = base_x *(i-x_num/2) + base_y *(j-y_num/2) + base_z

                    # Normalize since only the direction is necessary
                    direct = normalize(direct)

                    # For each photon detected at (i,j) create an instance
                    for ph in list(range(photons[i,j])):
                        entry = self.__photon_data.addEntry()
                        entry.setPositionX(x_pixel*(i-x_num/2))
                        entry.setPositionY(y_pixel*(j-y_num/2))
                        entry.setPositionZ(detector_dist)
                        entry.setDirectionX(detect[0])
                        entry.setDirectionY(detect[1])
                        entry.setDirectionZ(detect[2])
                        entry.setEnergy(center_energy)

            # Close the input file
            h5_infile.close()

		print("Photons read from photon matrix and transfered to XCSIT input form.")

	def saveH5(self):
		"""
		Save the results in a file
		"""
		# Write the new data into python arrays
		# -------------------------------------

		# Convert the photon data to a 2D numpy array   (size x 7)
		num_photon = np.zeros((self.__photon_data.size(),7),dtype=np.float_)
        ### Try this:
        ### num_photon[:,0] = entry.getPositionX()
		for i in list(range(self.__photon_data.size())):
			entry = self.__photon_data.getEntry(i)
			num_photon[i,0] = entry.getPositionX()
			num_photon[i,1] = entry.getPositionY()
			num_photon[i,2] = entry.getPositionZ()
			num_photon[i,3] = entry.getDirectionX()
			num_photon[i,4] = entry.getDirectionY()
			num_photon[i,5] = entry.getDirectionZ()
			num_photon[i,6] = entry.getEnergy()


		# Convert the interaction data to a 2D numpy array  (size x 5)
		num_ia = np.zeros((self.__ia_data.size(),5),dtype=np.float_)
			entry = self.__ia_data.getEntry(i)
			num_ia[i,0] = entry.getPositionX()
			num_ia[i,1] = entry.getPositionY()
			num_ia[i,2] = entry.getPositionZ()
			num_ia[i,3] = entry.getEnergy()
			num_ia[i,4] = entry.getTime()


		# Convert the ChargeMatrix to a numpy array to be able to store its
		# content
		x_size = self.__charge_data.width()
		y_size = self.__charge_data.height()
		charge_array = np.zeros((x_size,y_size),dtype=np.float_)	# float64
		for x in list(range(x_size)):
			for y in list(range(y_size)):
				entry = self.__charge_data.getEntry(x,y)
				charge_array[x,y] = entry.getCharge()

		# Create the new datasets
		# ------------------------------------------------------------

		# Open required files
        with h5py.File(self.__output_path, "w") as h5_outfile:
            # Create the necessary output groups
            data_gr = h5_outfile.create_group("data")
            info_gr = h5_outfile.create_group("info")
            param_gr= h5_outfile.create_group("params/geom")

            # Create the direct data values independent of the input file
            data_gr.create_dataset("data", data=charge_array)
            data_gr.create_dataset("photons", data=num_photon)
            data_gr.create_dataset("interactions", data=num_ia)
            info_gr.create_dataset("package_version",data="1.0",dtype=numpy.string_)

            ### Does the link targe have to be open to make a link?
            with h5py.File(self.__input_path,"r" ) as  h5_infile:

                # Link the data from the input file
                # -------------------------------------------------------------
                params_group["detectorDist"] = h5_infile["/params/geom/detectorDist"]
                params_group["pixelWidth"] = h5_infile["/params/geom/pixelWidth"]
                params_group["pixelHeight"] = h5_infile["/params/geom/pixelHeight"]
                params_group["photonEnergy"] = h5_infile["/params/geom/photonEnergy"]

                # Link in the input file root.
                h5_outfile["/history/parent/"] = h5py.ExternalLink(self.__input_file,"/")

                # Close files
                h5_infile.close()
            h5_outfile.close()




