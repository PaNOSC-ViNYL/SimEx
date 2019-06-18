""":module XCSITPhotonDetector: Hosts the XCSITPhotonDetector class."""
##########################################################################
#                                                                        #
# Copyright (C) 2015-2017 Jan-Philipp Burchert                           #
# Copyright (C) 2015-2018 Carsten Fortmann-Grote                         #
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
    print("\nWARNING: Importing libpy_detector_interface failed. This is most probably due to XCSIT and/or Geant4 not being installed properly on this system. The XCSITPhotonDetector class can still be instantiated, but the backengine() method will throw an exception.\n")
except:
    raise


import h5py
import os
import numpy
import sys

from SimEx.Calculators.AbstractPhotonDetector import AbstractPhotonDetector

class XCSITPhotonDetector(AbstractPhotonDetector):
    """
    :class XCSITPhotonDetector: Wraps detector simulations with XCSIT.
    """

    # Constructor.
    def __init__(self,parameters=None,
                input_path=None,
                output_path=None):
        """
        :param parameters: Parameters of the calulator such as the type of
        detector
        :type parameters: XCSITPhotonDetectorParameters

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

        self.__ia_data = [lpdi.InteractionData() for i in self.parameters.patterns]

    def __createXCSITChargeMatrix(self):
        self.__charge_data = [lpdi.ChargeMatrix() for i in self.parameters.patterns]

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
        for i,pd in enumerate(self.__photon_data):
            # Run the simulation, catch everything that might happen and report
            try:
                param = self.parameters
                ps = lpdi.ParticleSim()
                ps.setInput(pd)
                ps.setOutput(self.__ia_data[i])
                ps.initialization(param.detector_type)
                ps.runSimulation()

            except:
                err = sys.exc_info()
                print("Photon-Detector interaction error:")
                print(("Error type: " + str(err[0])))
                print(("Error value: " + str(err[1])))
                print(("Error traceback: " + str(err[2])))
                is_successful = False

            print("\nSUMMARY:\nDetected {0:d} interactions from {1:d} photons in pattern {2:s}.\n".format(self.__ia_data[i].size(), pd.size(), self.__pattern_ids[i]))

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
        for i, ia in enumerate(self.__ia_data):
            try:
                para = self.parameters
                cs = lpdi.ChargeSim()
                cs.setInput(ia)
                cs.setOutput(self.__charge_data[i])
                cs.setComponents(para.plasma_search_flag,
                                para.point_simulation_method,
                                para.plasma_simulation_flag,
                                para.detector_type
                                )
                cs.runSimulation()

                # Necessary due to the definition of XChargeData.hh
            except:
                err = sys.exc_info()
                print("Charge propagation error:")
                print(("Error type: " + str(err[0])))
                print(("Error value: " + str(err[1])))
                print(("Error traceback: " + str(err[2])))
                is_successful = False
                return is_successful

            # Count how many pixels have charge
            counter=0
            for x in list(range(self.__charge_data[i].width())):
                for y in list(range(self.__charge_data[i].height())):
                    entry=self.__charge_data[i].getEntry(x,y)
                    if(entry.getCharge() != 0):
                        counter+=1
            print(("\nSUMMARY:\nFound " + str(counter) + " signals in the detector of size " +
                str(self.__charge_data[i].height()) + "x" + str(self.__charge_data[i].width()) +
                " for " + str(self.__ia_data[i].size()) + " interactions and " +
                str(self.__photon_data[i].size()) + " photons"))

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

        # Open the file to read from
        with h5py.File(infile,"r") as h5_infile:

            keys = list(h5_infile["/data"].keys())
            keys.sort()

            matrix = h5_infile["/data/"+ keys[0] + "/diffr"].value

            pattern_ids = self.parameters.patterns
            number_of_patterns = len(pattern_ids)

            # Get the array where each pixel contains a number of photons
            # Explaination:
            #       /data/.../data are poissonized patterns
            #       /data/.../diffr are the intensities
            if type(self.parameters.patterns[0]) is int:
                pattern_ids = [keys[i] for i in pattern_ids]

            self.__pattern_ids = pattern_ids
            photons = numpy.empty(shape=(number_of_patterns,
                                         matrix.shape[0],
                                         matrix.shape[1]
                                         )
                                 )
            for i,pid in enumerate(pattern_ids):
                #photons[i,:,:] = h5_infile["/data/{0:s}/diffr".format(pid)].value
                photons[i,:,:] = h5_infile["/data/{0:s}/data".format(pid)].value

            #photons = numpy.floor(photons)
            photons = photons.astype(int)

            x_num, y_num = photons.shape[1:]
            print(("Size of input matrix: " + str(x_num) + "x" + str(y_num)))

            # Parameters of the matrix
            x_pixel = h5_infile["/params/geom/pixelWidth"].value
            print("pixel width = {0:e} m.".format(x_pixel))
            y_pixel = h5_infile["/params/geom/pixelHeight"].value
            print("pixel height= {0:e} m.".format(y_pixel))
            center_energy = h5_infile["/params/beam/photonEnergy"].value # missing profile
            print("central beam energy = {0:e} eV".format(center_energy))
            detector_dist = h5_infile["/params/geom/detectorDist"].value
            print("Detector distance = {0:e} m.".format(detector_dist))

            # Create the photon instance
            self.__photon_data = [lpdi.PhotonData() for i in range(photons.shape[0])]

            # Assumptions
            # - All the photon originate from the center
            # - photon energy is everywhere the same in the beam
            print("Creating the photons")

            for ipd, pd in enumerate(self.__photon_data):
                for i in range(x_num):
                    for j in range(y_num):

                        number_of_photons_in_pixel = photons[ipd,i,j]
                        if number_of_photons_in_pixel < 1:
                            continue


                        # Transfer from python to cartesian
                        direct = numpy.zeros((3,),dtype=numpy.float_)
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
                        # python goes from left 2 right top 2 bottom
                        # in conrast to our coordinate space
                        #direct[2] = detector_dist

                        # calculate the normalized direction vector
                        le=numpy.sqrt(numpy.sum((direct**2)))
                        normal_direction = numpy.zeros((3,),dtype=numpy.float_)
                        if le != 0:
                            normal_direction = direct/le

                        # For each photon detected at (i,j) create an instance
                        # shift into the koordinate system where the detector is in
                        # the origin  direct - (0,0,detector_dist)
                        entries = [ pd.addEntry() for i in range(number_of_photons_in_pixel)]
                        for entry in entries:
                            entry.setPositionX(direct[0])
                            entry.setPositionY(direct[1])
                            entry.setPositionZ(0)
                            entry.setDirectionX(numpy.asscalar(normal_direction[0]))
                            entry.setDirectionY(numpy.asscalar(normal_direction[1]))
                            entry.setDirectionZ(numpy.asscalar(normal_direction[2]))

                            #Photon energies have be set in units of keV.
                            entry.setEnergy(center_energy*1e-3)

            # Close the input file
            h5_infile.close()

        print("XCSITPhotonDetector read {0:d} patterns from the input.".format(len(self.__photon_data)))

    def saveH5(self):
        """
        Save the results in a file
        """
        # Write the new data into python arrays
        # Convert the interaction data to a 2D numpy array  (size x 5)
        #num_ia = numpy.zeros((self.__ia_data.size(),5),dtype=numpy.float_)
        #for i in list(range(self.__ia_data.size())):
            #entry = self.__ia_data.getEntry(i)
            #num_ia[i][0] = entry.getPositionX()
            #num_ia[i][1] = entry.getPositionY()
            #num_ia[i][2] = entry.getPositionZ()
            #num_ia[i][3] = entry.getEnergy()
            #num_ia[i][4] = entry.getTime()

        # Convert the ChargeMatrix to a numpy array to be able to store its
        # content
        x_size = self.__charge_data[0].width()
        y_size = self.__charge_data[0].height()
        charge_array = [numpy.zeros((x_size,y_size),dtype=numpy.float_) for p in self.__pattern_ids]  # float64
        for i,ca in enumerate(charge_array):
            for x in range(x_size):
                for y in range(y_size):
                    entry = self.__charge_data[i].getEntry(x,y)
                    ca[x][y] = entry.getCharge()

            # TODO settle this issue:
            # For unknown reasons the interaction entries and the chargematrix is
            # rotated of 180 degree to each other
            ca = numpy.fliplr(ca)
            ca = numpy.flipud(ca)

            ## Identify Nan and Inf in ChargeSim output
            #parent =os.path.dirname(self.output_path)
            #if not os.path.isdir(parent):
                #parent=os.makedirs(parent)
            #ofn = os.path.join(parent,"NaNInf.txt")
            #with open(ofn,'w') as outfile:
                #outfile.write("# All the coordinates are in typical python convention")
                ## Search for Nan and Inf
                #for x in list(range(x_size)):
                    #for y in list(range(y_size)):
                        #if(numpy.isnan(ca[x][y])):
                            #print(("Warning: Detected NaN in ChargeMatrix at (" + str(x) +
                                #"," + str(y) + ") (python conention: l-r, t-b)"))
                            #outfile.write(str(x) + "\t" + str(y) + "\tNaN")
                        #if(numpy.isinf(ca[x][y])):
                            #print(("Warning: Detected Inf in ChargeMatrix at (" + str(x) +
                                #"," + str(y) + ") (python conention: l-r, t-b)"))
                            #outfile.write(str(x) + "\t" + str(y) + "\tInf")

        # Create the new datasets
        # ------------------------------------------------------------
        # Open required files
        with h5py.File(self.output_path, "w") as h5_outfile:
            # Create the necessary output groups
            data_gr = h5_outfile.create_group("data")
            info_gr = h5_outfile.create_group("info")
            param_geom_gr= h5_outfile.create_group("params/geom")
            param_beam_gr= h5_outfile.create_group("params/beam")

            for i, pid in enumerate(self.__pattern_ids):
                # Create the direct data values independent of the input file
                data_gr.create_dataset("{0:s}/data".format(pid), data=charge_array[i])
                #data_gr.create_dataset("{0:s}/interactions".format(pid), data=num_ia[i])
            info_gr.create_dataset("package_version".format(pid),data="1.0")

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

            # Close file
            h5_outfile.close()
