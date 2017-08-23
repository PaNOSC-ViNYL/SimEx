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
### Should read from DSIM import PhotonEntry ...
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
import sys

from SimEx.Calculators import AbstractPhotonDetector
from SimEx.Calculators import XCSITPhotonDetectorParameters

class XCSITPhotonDetector(AbstractPhotonDetector):
    """
    Class representing an free electorn laser photon detector
    """

    # Define the allowed attributes
    # inherited from AbstractBaseCalculator(object)
    #       __parameters
    #       __input_path            <- here redefined as array of strings
    #       (pathes)
    #       __output_path
    __slot__ = "__expected_data",\
               "__provided_data",\
               "__photon_data",\
               "__ia_data",\
               "__charge_data"


	# Constructor.
	def __init__(self,parameters=None,input_path=None,output_path=None):
		"""
		:param parameters: Parameters of the calulator such as the type of
			detector
		:type parameters: XCSITPhotonDetector

        :param input_path: Path to the hdf5 file holding the input data.
        :type input_path: str

        :param output_path: Path pointing to the path for output
        :type output_path: str
        """

        # Init base class
        super(XCSITPhotonDetector,self).__init__(parameters,input_path,output_path)


        # Use the setters to check the input and assign it to the attributes
        # the attributes are overwritten in the base class
        self.parameters(parameters)
        self.input_path(input_path)
        self.output_path(output_path)

        # Define the input and output structure of the hdf5 file
        self.__expected_data = ['/data/data',       # <- poissonized (int)
                                '/data/diffr',      # <- intensities (float)
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

        self.__provided_data = ['/data/data',       # <- store charge matrix here, in ADU
                                '/data/photons'     # <- store photon/pixel map here, no directions
                                '/data/interactions',
                                '/history/parent/',
                                '/info/package_version',
                                '/params/geom/detectorDist',
                                '/params/geom/pixelWidth',
                                '/params/geom/pixelHeight',
                                '/params/beam/photonEnergy',
                                ]

    

    # Override the setter of AbstractBaseCalculator
    @parameters.setter
    def parameters(self,value):
        # Check the value type
        if value is None:
            raise ValueError("A parameters instance must be given.")
        if not isinstance(value, XCSITPhotonDetectorParameters):
            raise TypeError("As parameters input only instances of "+
                "XCSITPhotonDetectorParameters are allowed.")

        # Check content by calling all the necessary parameters
        # The input
        try:
            self.__parameters.detector_type()
            self.__parameters.plasma_search_flag()
            self.__parameters.plasma_simulation_flag()
            self.__parameters.point_simulation_method()
        except:
            err = sys.exc_info()
            print("Error type: " + str(err[0]))
            print("Error value: " + str(err[1]))
            print("Error traceback: " + str(err[2]))
            
            # end the execution with a new exception
            raise ValueError("Input parameter XCSITPhotonDetectorParameter " +
                "is incomplete.")
    
        # set the value to the attribute
        super(XCSITPhotonDetector,self).parameters(value)

    
    @input_path.setter
    def input_path(self,value):
        # Check the value type
        if value is None:
            raise ValueError("The parameter 'input_path' must be specified.")
        if not isinstance(value,str):
            raise TypeError("As input_path attribute only instances of str " + 
                "are allowed.")
        if not value:
            raise IOError("You must not enter an empty string as output path.") 
        # treat the input path:
        # Cases
        # 1) given is an absolute path
        #       a) ends with <parent path>/<filename>.h5-> complete file path
        #       b) ends with <parent path>/<filename>   -> add .h5
        #       c) ends with <parent path>/<folder>     -> search for an .h5 file in the
        #           parentfolder
        # 2) given is an relative path to the current directory
        #       cases like in 1) a-c just with the cwd added previously

        # check if absolute path
        # Linux: starts with /
        # Windows: starts with \
        # Modify value accodingly to create an absolute path and normalize it
        if not os.path.isabs(value):
            value = os.path.abspath(value)

        # Check if the parent folder exists since it has to exists in an correct
        # absolute path
        (head,tail) = os.path.split(value)
        if not os.path.isdir(head):
            raise IOError("Parent path is not valid. Please check again: " +
                str(head) +".")

        # Check cases a)-c)
        # Multiple input files are stored in one specifed input folder
        in_pathes = []
        if os.endswith(".h5") and os.path.isfile(value):
            # All is fine
            in_pathes.append(value)
        elif os.path.isfile(value + ".h5"):
            # filename without ending
            value += ".h5"
            in_pathes.append(value)
        elif os.path.isdir(value):
            # directory containing many input files

            # directory can contain multiple files and multiple .h5 files
            for i in os.listdir(value):
                if i.endswith(".h5"):
                    in_pathes.append(os.path.join(value,i))         
        else:
            raise IOError("Last path element causes error: " + str(tail) +
                "Please check absolute path again: " + str(value) + ".")

        # Check if the content are all strings
        if not all(isinstance(i,str) for i in in_pathes):
            raise ValueError("One of the pathes is not a python str" +
                str(in_pathes) + ".")

        # Assign to the variable
        self.__input_path = in_pathes


    @output_path.setter
    def output_path(self,value):
        # Check the value type
        if value is None:
            raise ValueError("The parameter 'output_path' has to be specified.")
        if not isinstance(value,str):
            raise TypeError("As output_path attribute only instances of str " + 
                "are allowed.")
        if not value:
            raise IOError("You must not enter an empty string as output path.")

        # Situation: output_path
        # 1) existing path, filename can exist but doesn't need to
        #       i) absolut path:
        #           a) ends with <parent>/<file>.h5
        #           b) ends with <parent>/<file>
        #           c) ends with <parent> -> create a file
        #       ii) a relative path such as 1) i)
        # 2) a partly or non existing path
        #       i) absolute path:
        #           a) create if ends with <file>.h5
        #           b) ends with <parent> -> create path and add another
        #           <file>.h5
        #       ii) relative path:
        #           same as 2) i)

        # check if absolute path
        # Linux: starts with /
        # Windows: starts with \
        # It does not matter if the path exists or not, only the first character
        # is necessary to know
        # Modify value accodingly to create an absolute path and normalize it
        if not os.path.isabs(value):
            value = os.path.abspath(value)

        # Test the cases:
        (head,tail) = os.path.split(value)
        out_name = "XCSITPhotonDetectorOutput.h5"
        if os.path.isdir(value):
            # input is existing path to directory where to put in the output
            # file 1ic) and 1iic)
            
            # Create a file and join
            value = os.path.join(value,out_name)
            value = os.path.normpath(value)
        elif os.path.isdir(head):
            # input is absolute path with file name 1ia 1ib 1iia 1iib
            # isdir checks also for existance
            if value.endswith(".h5"):
                # complete path, create the file there
                pass
            else:
                # last path element is a filename without ending
                value += ".h5"
        elif value.endswith(".h5"):
            # a path including non existant folders but a specified outputfile
            # name -> nothing to do since the hdf5 will create necessary pathes
            pass
        else:
            # a path with non existant folders to the parent folder of a not
            # specified output file

            # Create an outpuf file
            value = os.join(value,out_name)
            value = os.path.normpath(value)
        
        # set the value to the attribute
        super(XCSITPhotonDetector,self).output_path(value)
    



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
        is_successful = True

        # Check containers
        if self.__photon_data == None:
            raise RuntimeError("Photon container has not been initialized yet.")
        if self.__ia_data == None:
            raise RuntimeError("Interaction container has not been initialized yet.")
        
        # Run the simulation, catch everything that might happen and report
        try:
            ps = ParticleSim_ext.ParticleSim()
            ps.initialization(self.__parameters.detector_type())
            ps.runSimulation(self.__photon_data,self.__ia_data)
        except:
            err = sys.exc_info()
            print("Error type: " + str(err[0]))
            print("Error value: " + str(err[1]))
            print("Error traceback: " + str(err[2]))
            is_successfull = False

        # Results are directly written to the __ia_data instance
        return is_successful


    def __backengineCP(self):
        """
        Run the charge simulation
        """
        is_successful = True

        # Check containers
        if self.__ia_data == None:
            raise RuntimeError("interaction container has not been initialized"+
                " yet.")
        if self.__charge_data == None:
            raise RuntimeError("charge matrix has not been initialized yet.")


        # Run the simulation
        try:
            cs = ChargeSim_ext.ChargeSim()
            cs.setInput(self.__ia_data)
            cs.setComponents(self.__charge_data,
                            self.__parameters.plasma_search_flag(),
                            self.__parameters.plasma_simulation_flag(),
                            self.__parameters.point_simulation_method(),
                            self.__parameters.detector_type()
                            )
            cs.runSimulation()
        except:
            err = sys.exc_info()
            print("Error type: " + str(err[0]))
            print("Error value: " + str(err[1]))
            print("Error traceback: " + str(err[2]))
            is_successful = False

        # Return if everything went well
        return is_successful


    def backengine(self):
        """
        Executes the simulation of the particle and charge simulation.
        """
        print("\nSimulating photon-detector interaction.")
        # Create the containers
        self.__ia_data      = self.__createXCSITInteractions(self)
        self.__charge_data  = self.__createXCSITChargeMatrix(self)

        # Run the particle simulation.
        if not self.__backengineIA(self):
            raise RuntimeError("Particle simulation caused errors, " + 
                "interrupting execution.")
        else:
            print("Interaction simulation of the detector is finished.")

        # Run the charge simulation.
        if not self.__backengineCP(self):
            raise RuntimeError("Charge simulation caused errors, " + 
                "interrupting execution.")
        else:
            print("Charge propagation simulation in the detector is finished.")


    def _readH5(self):
        """
        Reads the hdf5 file and create the storage container for the photons
        according to that data
        """
        # The __input_path is a non relative path to an existing file
        if not os.path.exists(self.__input_path):
            raise RuntimeError("Input file " + str(self.__input_path) + 
                " does not exists")

        # Raise exception if there is no input file saved
        if len(self.__input_path) == 0 or os.path.isfile(self.__input_path[0]):
            raise RuntimeError("Input path does not lead to a file.")
        infile = self.__input_path[0]

        # Reflect the current handeling of multiple files
        if len(self.__input_path) > 1:
            raise RuntimeError("Currently there should be only one input file.")

        # TODO Accept multiple input pathes as input
        # Open the file to read from
        with h5py.File(infile,"r") as h5_infile:

            # Get the array where each pixel contains a number of photons
            # TODO use data/data or data/diffr -- also change in writeH5
            photons = h5_infile["data/data"]
            x_num = len(photons)        # Assuming an rectangle
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
                    direct = np.linalg.norm(direct)

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
        charge_array = np.zeros((x_size,y_size),dtype=np.float_)    # float64
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
            param_geom_gr= h5_outfile.create_group("params/geom")
            param_beam_gr= h5_outfile.create_group("params/beam")

            # Create the direct data values independent of the input file
            data_gr.create_dataset("data", data=charge_array)
            data_gr.create_dataset("interactions", data=num_ia)
            info_gr.create_dataset("package_version",data="1.0",dtype=numpy.string_)

            with h5py.File(self.__input_path,"r" ) as  h5_infile:

                # Link the data from the input file
                # -------------------------------------------------------------
               
                # Copy
                data_gr["photons"] = np.asarray(h5_infile["/data/data"]) # make
                    # sure it is an numpy array

                params_geom_gr["detectorDist"] = h5_infile["/params/geom/detectorDist"]
                params_geom_gr["pixelWidth"] = h5_infile["/params/geom/pixelWidth"]
                params_geom_gr["pixelHeight"] = h5_infile["/params/geom/pixelHeight"]
                params_beam_gr["photonEnergy"] = h5_infile["/params/beam/photonEnergy"]

                # Close file since it is not possible to link to it via
                # ExternalLink if it is still open
                h5_infile.close()

            # Link in the input file root.
            h5_outfile["/history/parent/"] = h5py.ExternalLink(self.__input_file,"/")

            # Close file
            h5_outfile.close()




