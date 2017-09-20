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


try:
    import libpy_detector_interface as lpdi
except ImportError:
    print "\nWARNING: Importing libpy_detector_interface failed. This is most probably due to XCSIT and/or Geant4 not being installed properly on this system. The XCSITPhotonDetector class can still be instantiated, but the backengine() method will throw an exception.\n"
except:
    raise


import h5py
import os
import numpy as np
import sys

from SimEx.Calculators.AbstractPhotonDetector import AbstractPhotonDetector
from SimEx.Calculators.XCSITPhotonDetectorParameters import XCSITPhotonDetectorParameters

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
    __slot__ =  "__expected_data",\
                "__provided_data",\
                "__photon_data",\
                "__ia_data",\
                "__charge_data"

    # Constructor.
    def __init__(self,parameters=None,
                input_path=None,
                output_path=None):
        """
        :param parameters: Parameters of the calulator such as the type of
        detector
        :type parameters: XCSITPhotonDetector

        :param input_path: Path to the hdf5 file holding the input data.
        :type input_path: str

        :param output_path: Path pointing to the path for output
        :type output_path: str
        """

        # Failure if no argument is given
        if any([parameters is None,
                input_path is None]):
            raise AttributeError("parameters and input_path are essential to"+
                " to init an instance of this class")


        # Init base class
        super(XCSITPhotonDetector,self).__init__(parameters,input_path,output_path)

        # Use the setters to check the input and assign it to the attributes
        # the attributes are overwritten in the base class
        self.parameters = parameters
        self.input_path = input_path
        self.output_path = output_path

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



    @AbstractPhotonDetector.input_path.setter
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

        # TODO: loop over multiple files

        # check if absolute path
        # Linux: starts with /
        # Windows: starts with \
        # Modify value accodingly to create an absolute path and normalize it
        if not os.path.isabs(value):
            value = os.path.abspath(value)

        # Check if the parent folder exists since it has to exists in an correct
        # absolute path and check if it is a directory and not a file
        (head,tail) = os.path.split(value)
        if not os.path.isdir(head):
            raise IOError("Parent path is not valid. Please check again: " +
                str(head) +".")

        # Check cases a)-c)
        # Multiple input files are stored in one specifed input folder
        in_pathes = []
        if value.endswith(".h5") and os.path.isfile(value):
            ### syntax??
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


    @AbstractPhotonDetector.output_path.setter
    def output_path(self,value):
        # Check the value type
        ### Default handling: detector_out.h5 -> in case of many input files, put all detector images into one detector.h5, replicate structure of diffr.h5
        if value is None:
            value=os.getcwd()
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
        out_name = "detector_out.h5"
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
            if not os.path.isdir(value):
                os.makedirs(os.path.dirname(value))
        else:
            # a path with non existant folders to the parent folder of a not
            # specified output file

            # Create an outpuf file
            value = os.path.join(value,out_name)
            value = os.path.normpath(value)
            if not os.path.isdir(value):
                os.makedirs(os.path.dirname(value))

        # set the value to the attribute
        self._AbstractBaseCalculator__output_path=value




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
        self.__ia_data = lpdi.InteractionData()

    def __createXCSITChargeMatrix(self):
        self.__charge_data = lpdi.ChargeMatrix()

    # Subengine to calulate the particle simulation: The interaction of the
    # photons with the detector of choice
    def __backengineIA(self):
        """
        Run the particle simulation
        """
        is_successful = True

        # Check containers
        if self.__photon_data is None:
            raise RuntimeError("Photon container has not been initialized yet.")
        if self.__ia_data is None:
            raise RuntimeError("Interaction container has not been initialized yet.")

        # Run the simulation, catch everything that might happen and report
        try:
            param = self.parameters
            ps = lpdi.ParticleSim()
            ps.setInput(self.__photon_data)
            ps.setOutput(self.__ia_data)
            ps.initialization(param.detector_type)
            ps.runSimulation()
        except:
            err = sys.exc_info()
            print("Photon-Detector interaction error:")
            print("Error type: " + str(err[0]))
            print("Error value: " + str(err[1]))
            print("Error traceback: " + str(err[2]))
            is_successful = False


        print("Detected " + str(self.__ia_data.size()) + " interactions from " +
            str(self.__photon_data.size()) + " photons")

        # Results are directly written to the __ia_data instance
        return is_successful


    def __backengineCP(self):
        """
        Run the charge simulation
        """
        is_successful = True

        # Check containers
        if self.__ia_data is None:
            raise RuntimeError("interaction container has not been initialized"+
                " yet.")

        # Run the simulation
        try:
            para = self.parameters
            cs = lpdi.ChargeSim()
            cs.setInput(self.__ia_data)
            cs.setOutput(self.__charge_data)
            cs.setComponents(para.plasma_search_flag,
                            para.point_simulation_method,
                            para.plasma_simulation_flag,
                            para.detector_type
                            )
            cs.runSimulation()

            # Necessary due to the definition of XChargeData.hh
            # self.__charge_data = cs.getOutput()
        except:
            err = sys.exc_info()
            print("Charge propagation error:")
            print("Error type: " + str(err[0]))
            print("Error value: " + str(err[1]))
            print("Error traceback: " + str(err[2]))
            is_successful = False
            return is_successful

        # Count how many pixels have charge
        counter=0
        for x in list(range(self.__charge_data.width())):
            for y in list(range(self.__charge_data.height())):
                entry=self.__charge_data.getEntry(x,y)
                if(entry.getCharge() != 0):
                    counter+=1
        print("Found " + str(counter) + " signals in the detector of size " +
            str(self.__charge_data.height()) + "x" + str(self.__charge_data.width()) +
            " for " + str(self.__ia_data.size()) + " interactions and " +
            str(self.__photon_data.size()) + " photons")

        # Return if everything went well
        return is_successful


    def backengine(self):
        """
        Executes the simulation of the particle and charge simulation.
        """
        print("\nSimulating photon-detector interaction.")
        # Create interaction container
        self.__createXCSITInteractions()

        # Run the particle simulation.
        if not self.__backengineIA():
            raise RuntimeError("Particle simulation caused errors, " +
                "interrupting execution.")
        else:
            print("Interaction simulation of the detector is finished.")

        # Create interaction container
        self.__createXCSITChargeMatrix()

        # Run the charge simulation.
        if not self.__backengineCP():
            raise RuntimeError("Charge simulation caused errors, " +
                "interrupting execution.")
        else:
            print("Charge propagation simulation in the detector is finished.")
        return 0


    def _readH5(self):
        """
        Reads the hdf5 file and create the storage container for the photons
        according to that data
        """
        # The __input_path is a non relative path to an existing file
        if not os.path.exists(self.__input_path[0]):
            raise RuntimeError("Input file " + str(self.__input_path[0]) +
                " does not exists")

        # Raise exception if there is no input file saved
        if len(self.__input_path[0]) == 0 or not os.path.isfile(self.__input_path[0]):
            raise RuntimeError("Input path does not lead to a file. Input path"+
                " is: " + str(self.__input_path[0]))
        infile = self.__input_path[0]

        # Reflect the current handeling of multiple files
        if len(self.__input_path) > 1:
            raise RuntimeError("Currently there should be only one input file.")

        # TODO Accept multiple input pathes as input
        # Open the file to read from
        with h5py.File(infile,"r") as h5_infile:

            keys = h5_infile["/data"].keys()
            matrix = h5_infile["/data/"+ keys[0] + "/diffr"].value
            photons = np.zeros((len(matrix),len(matrix[0])),dtype=np.float_)

            # TODO: Single pattern treatment is not implemented yet
            # Get the array where each pixel contains a number of photons
            # Explaination:
            #       /data/.../data are poissonized patterns
            #       /data/.../diffr are the intensities
            for i in h5_infile["/data"].keys():
                photons += h5_infile["/data/"+i+"/diffr"].value



            # TODO: need to be removed and replaced by a proper transition
            # Rescaling with factor 100000
            photons = photons*100000
            photons = np.floor(photons)
            photons = photons.astype(int)

            x_num = len(photons)        # Assuming an rectangle
            y_num = len(photons[0])
            print("Size of input matrix: " + str(x_num) + "x" + str(y_num))

            # Parameters of the matrix
            x_pixel = h5_infile["/params/geom/pixelWidth"].value
            print("pixel width: " + str(x_pixel))
            y_pixel = h5_infile["/params/geom/pixelHeight"].value
            print("pixel height: " + str(y_pixel))
            center_energy = h5_infile["/params/beam/photonEnergy"].value # missing profile
            print("central beam energy: " + str(center_energy))
            detector_dist = h5_infile["/params/geom/detectorDist"].value
            print("Detector dist: " + str(detector_dist))

            # Create the photon instance
            self.__photon_data = lpdi.PhotonData()

            # Assumptions
            # - All the photon originate from the center
            # - photon energy is everywhere the same in the beam
            print("Creating the photons")
            for i in list(range(x_num)):
                for j in list(range(y_num)):
                    # Transfer from python to cartesian
                    direct = np.zeros((3,),dtype=np.float_)
                    direct[0] = i
                    direct[1] = y_num - 1 - j
                    direct[2] = 0

                    # Center center and correct for center of element
                    direct[0] = direct[0] - 0.5* x_num + 0.5
                    direct[1] = direct[1] - 0.5* y_num + 0.5
                    direct[2] = direct[2]

                    # calculate the length
                    direct[0] = direct[0]*x_pixel
                    direct[1] = direct[1]*y_pixel
                    direct[2] = detector_dist


                    # Calculate the photon flight vector with respect to the matrix
                    # center and the origin of diffraction
                    #direct[0] = x_pixel*(i + 0.5 - 0.5 *x_num) # x-coordinate
                    #direct[1] = y_num*y_pixel - y_pixel*(j + 0.5 -0.5 *y_num)
                    # python goes from left 2 right top 2 to bottom
                    # in conrast to our coordinate space
                    #direct[2] = detector_dist

                    # calculate the normalized direction vector
                    le=np.sqrt(np.sum((direct**2)))
                    normal_direction = np.zeros((3,),dtype=np.float_)
                    if le != 0:
                        normal_direction = direct/le

                    # For each photon detected at (i,j) create an instance
                    # shift into the koordinate system where the detector is in
                    # the origin  direct - (0,0,detector_dist)
                    for ph in list(range(photons[i][j])):
                        entry = self.__photon_data.addEntry()
                        entry.setPositionX(direct[0])
                        entry.setPositionY(direct[1])
                        entry.setPositionZ(0)
                        entry.setDirectionX(np.asscalar(normal_direction[0]))
                        entry.setDirectionY(np.asscalar(normal_direction[1]))
                        entry.setDirectionZ(np.asscalar(normal_direction[2]))
                        entry.setEnergy(center_energy)

            # Close the input file
            h5_infile.close()

        print("XCSITPhotonDetector read " + str(self.__photon_data.size())  + " photons from the input.")

    def saveH5(self):
        """
        Save the results in a file
        """
        print("Save the data")

        # Write the new data into python arrays
        # -------------------------------------

        # Convert the interaction data to a 2D numpy array  (size x 5)
        num_ia = np.zeros((self.__ia_data.size(),5),dtype=np.float_)
        for i in list(range(self.__ia_data.size())):
            entry = self.__ia_data.getEntry(i)
            num_ia[i][0] = entry.getPositionX()
            num_ia[i][1] = entry.getPositionY()
            num_ia[i][2] = entry.getPositionZ()
            num_ia[i][3] = entry.getEnergy()
            num_ia[i][4] = entry.getTime()


        # Convert the ChargeMatrix to a numpy array to be able to store its
        # content
        x_size = self.__charge_data.width()
        y_size = self.__charge_data.height()
        charge_array = np.zeros((x_size,y_size),dtype=np.float_)    # float64
        for x in list(range(x_size)):
            for y in list(range(y_size)):
                entry = self.__charge_data.getEntry(x,y)
                charge_array[x][y] = entry.getCharge()

        # TODO settle this issue:
        # For unknown reasons the interaction entries and the chargematrix is
        # rotated of 180 degree to each other
        charge_array = np.fliplr(charge_array)
        charge_array = np.flipud(charge_array)

        # Identify Nan and Inf in ChargeSim output
        parent =os.path.dirname(self.output_path)
        if not os.path.isdir(parent):
            parent=os.makedirs(parent)
        ofn = os.path.join(parent,"NaNInf.txt")
        with open(ofn,'w') as outfile:
            outfile.write("# All the coordinates are in typical python convention")
            # Search for Nan and Inf
            for x in list(range(x_size)):
                for y in list(range(y_size)):
                    if(np.isnan(charge_array[x][y])):
                        print("Warning: Detected NaN in ChargeMatrix at (" + str(x) +
                            "," + str(y) + ") (python conention: l-r, t-b)")
                        outfile.write(str(x) + "\t" + str(y) + "\tNaN")
                    if(np.isinf(charge_array[x][y])):
                        print("Warning: Detected Inf in ChargeMatrix at (" + str(x) +
                            "," + str(y) + ") (python conention: l-r, t-b)")
                        outfile.write(str(x) + "\t" + str(y) + "\tInf")

        # Create the new datasets
        # ------------------------------------------------------------
        # Open required files
        with h5py.File(self.output_path, "w") as h5_outfile:
            # Create the necessary output groups
            data_gr = h5_outfile.create_group("data")
            info_gr = h5_outfile.create_group("info")
            param_geom_gr= h5_outfile.create_group("params/geom")
            param_beam_gr= h5_outfile.create_group("params/beam")

            # Create the direct data values independent of the input file
            data_gr.create_dataset("data", data=charge_array)
            data_gr.create_dataset("interactions", data=num_ia)
            info_gr.create_dataset("package_version",data="1.0")

            with h5py.File(self.__input_path[0],"r" ) as  h5_infile:

                # Link the data from the input file
                # -------------------------------------------------------------

                # Copy
                dist = h5_infile["/params/geom/detectorDist"]
                param_geom_gr.create_dataset("detectorDist",data=dist[()])
                pw = h5_infile["/params/geom/pixelWidth"]
                param_geom_gr.create_dataset("pixelWidth",data=pw[()])
                ph =  h5_infile["/params/geom/pixelHeight"]
                param_geom_gr.create_dataset("pixelHeight", data=ph[()])
                pe =  h5_infile["/params/beam/photonEnergy"]
                param_beam_gr.create_dataset("photonEnergy",data=pe[()])

                # Close file since it is not possible to link to it via
                # ExternalLink if it is still open
                h5_infile.close()

            # Link in the input file root.
            h5_outfile["/history/parent/"] = h5py.ExternalLink(self.__input_path[0],"/")
            h5_outfile["/data/photons/"] = h5py.ExternalLink(self.__input_path[0],"/data")

            # Close file
            h5_outfile.close()
