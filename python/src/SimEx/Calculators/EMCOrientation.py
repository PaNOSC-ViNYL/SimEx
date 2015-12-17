""" Module that holds the EMCOrientation class.

    @author : CFG
    @institution : XFEL
    @creation 20151104

"""
import os
import subprocess
import tempfile
import numpy
import h5py
import time

from SimEx.Calculators.AbstractPhotonAnalyzer import AbstractPhotonAnalyzer

from EMCCaseGenerator import  EMCCaseGenerator, print_to_log

class EMCOrientation(AbstractPhotonAnalyzer):
    """
    Class representing photon data analysis for orientation of 2D diffraction patterns to a 3D diffraction volume. """

    def __init__(self,  parameters=None, input_path=None, output_path=None):
        """
        Constructor for the reconstruction analyser.

        @param  parameters : Dictionary of reconstruction parameters.
        @type : dict
        @example : parameters={'initial_number_of_quaternions' : 1,
                               'max_number_of_quaternions'     : 9,
                               'max_number_of_iterations'      : 100,
                               'min_error'                     : 1.0e-8,
                               'beamstop'                      : 1.0e-5,
                               'detailed_output'               : False
                               }
        """

        # Initialize base class.
        super(EMCOrientation, self).__init__(parameters,input_path,output_path)


        self.__provided_data = ['data/data',
                                'data/angle',
                                'data/center',
                                'params/info',
                                'version',]

        self.__expected_data = ['/-input_dir'
                                '/-output_dir'
                                '/-config_file'
                                '/-b',
                                '/-g',
                                '/-uniformRotation',
                                '/-calculateCompton',
                                '/-sliceInterval',
                                '/-numSlices',
                                '/-pmiStartID',
                                '/-pmiEndID',
                                '/-dpID',
                                '/-numDP',
                                '/-USE_GPU',
                                '/version']


    def expectedData(self):
        """ Query for the data expected by the Analyzer. """
        return self.__expected_data

    def providedData(self):
        """ Query for the data provided by the Analyzer. """
        return self.__provided_data

    @property
    def data(self):
        """ Query for the field data. """
        return self.__data

    def _readH5(self):
        """ """
        """ Private method for reading the hdf5 input and extracting the parameters and data relevant to initialize the object. """
        pass # Nothing to be done since IO happens in backengine.

    def saveH5(self):
        """ """
        """
        Private method to save the object to a file.

        @param output_path : The file where to save the object's data.
        @type : string
        @default : None
        """
        pass # No action required since output is written in backengine.


    def backengine(self):

        status = self.run_emc()

        return status

    def run_emc(self):
        """ Run the Expand-Maximize-Compress (EMC) algorithm.

        @return : 0 if EMC returns successfully, 1 if not.
        @note : Copied and adapted from the main routine in
        s2e_recon/EMC/runEMC.py
        """
        ###############################################################
        # Instantiate a reconstruction object
        ###############################################################
        # If parameters are given, map them to command line arguments.
        if 'initial_number_of_quaternions' in self.parameters.keys():
            initial_number_of_quaternions = self.parameters['initial_number_of_quaternions']
        else:
            initial_number_of_quaternions = 1

        if 'max_number_of_quaternions' in self.parameters.keys():
            max_number_of_quaternions = self.parameters['max_number_of_quaternions']
        else:
            max_number_of_quaternions = 1

        if 'max_number_of_iterations' in self.parameters.keys():
            max_number_of_iterations = self.parameters['max_number_of_iterations']
        else:
            max_number_of_iterations = 1

        if 'min_error' in self.parameters.keys():
            min_error = self.parameters['min_error']
        else:
            min_error = 1e-5 # This is very optimistic.

        if 'beamstop' in self.parameters.keys():
            beamstop = self.parameters['beamstop']
        else:
            beamstop = 1e-5 # This is very optimistic.

        if 'detailed_output' in self.parameters.keys():
            detailed_output = self.parameters['detailed_output']
        else:
            detailed_output = False


        ###############################################################
        # Check that subdirectories for intermediate output exist
        ###############################################################
        #tmp_log_dir = tempfile.mkdtemp(prefix='emc_log')
        tmp_out_dir = tempfile.mkdtemp(prefix='emc_out_')
        #out_dir = self.output_path
        run_instance_dir = tempfile.mkdtemp(prefix='emc_run_')
        src_installation_dir = os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)),'..', '..','..','..','sw','bin'))

        ###############################################
        import ipdb
        ipdb.set_trace()
        ###############################################

        outputLog           = os.path.join(run_instance_dir, "EMC_extended.log")
        #run_log_file        = os.path.join(run_instance_dir, "orient.log")
        if os.path.isdir(self.input_path):
            photonFiles         = [ os.path.join(self.input_path, pf) for pf in os.listdir( self.input_path ) ]
            photonFiles.sort()
        elif os.path.isfile(self.input_path):
            photonFiles = [self.input_path]
        else:
            raise IOError( " Input file %s not found." % self.input_path )

        sparsePhotonFile    = os.path.join(tmp_out_dir, "photons.dat")
        avgPatternFile      = os.path.join(tmp_out_dir, "avg_photon.h5")
        detectorFile        = os.path.join(tmp_out_dir, "detector.dat")
        lockFile            = os.path.join(tmp_out_dir, "write.lock")
        quaternion_dir      = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'CalculatorUtilities', 'quaternions')

        gen = EMCCaseGenerator(outputLog)
        ###############################################################
        # A lock file is created if subprocess is converting sparse photons
        #   so that another subprocess does not clobber an ongoing conversion.
        # Make photons.dat and detector.dat if they don't exist.
        # Create time-tagged output subdirectory for intermediate states.
        ###############################################################
        while (os.path.isfile(lockFile)):
            # Sleep in 30 s intervals, then check if sparse photon lock has been released.
            sleep_duration = 30
            msg = "Lock file in " + tmp_out_dir + ". "
            msg += "Photons.dat likely being written to tmpDir by another process. "
            msg += "Sleeping this process for %d s." % sleep_duration
            print_to_log(msg)
            time.sleep(sleep_duration)

        if not (os.path.isfile(sparsePhotonFile) and os.path.isfile(detectorFile)):
            msg = "Photons.dat and detector.dat not found in " + tmp_out_dir + ". Will create them now..."
            print_to_log(msg=msg, log_file=outputLog)
            os.system("touch %s" % lockFile)
            gen.readGeomFromPhotonData(photonFiles[0])
            #gen.readGeomFromPhotonData(photonFiles)
            gen.writeDetectorToFile(filename=detectorFile)
            gen.writeSparsePhotonFile(photonFiles, sparsePhotonFile, avgPatternFile)
            print_to_log(msg="Sparse photons file created. Deleting lock file now", log_file=outputLog)
            os.system("rm %s " % lockFile)
        else:
            msg = "Photons.dat and detector.dat already exists in " + tmp_out_dir + "."
            print_to_log(msg=msg, log_file=outputLog)
            gen.readGeomFromDetectorFile(detectorFile)
            print_to_log(msg="Detector parameters: %d %d %d"%(gen.qmax, len(gen.detector), len(gen.beamstop)),
                    log_file=outputLog)


        #msg = time.asctime() + ":: " +"Creating symbolic link to crucial files in output subdirectory, " + run_instance_dir
        #print_to_log(msg, log_file=runLogFile)
        if not (os.path.isfile(os.path.join(run_instance_dir,"detector.dat"))):
            os.symlink(os.path.join(tmp_out_dir,"detector.dat"), os.path.join(run_instance_dir,"detector.dat"))
        if not (os.path.isfile(os.path.join(run_instance_dir,"photons.dat"))):
            os.symlink(os.path.join(tmp_out_dir,"photons.dat"), os.path.join(run_instance_dir,"photons.dat"))
        if not (os.path.isfile(os.path.join(run_instance_dir,"EMC"))):
            os.symlink(os.path.join(src_installation_dir,"EMC"), os.path.join(run_instance_dir,"EMC"))
        if not (os.path.isfile(os.path.join(run_instance_dir,"object_recon"))):
            os.symlink(os.path.join(src_installation_dir,"object_recon"), os.path.join(run_instance_dir,"object_recon"))
        #if not (os.path.isdir(os.path.join(runInstanceDir,"supp_py_modules"))):
            #os.symlink(os.path.join(op.srcDir,"supp_py_modules"), os.path.join(runInstanceDir,"supp_py_modules"))
        #if not (os.path.isfile(os.path.join(op.tmpOutDir, "make_diagnostic_figures.py"))):
            #os.symlink(os.path.join(op.srcDir,"make_diagnostic_figures.py"), os.path.join(op.tmpOutDir, "make_diagnostic_figures.py"))

        ###############################################################
        # Create dummy destination h5 for intermediate output from EMC
        ###############################################################
        cwd = os.path.abspath(os.curdir)
        os.chdir(run_instance_dir)
        #Output file is kept in tmpOutDir,
        #a hard-linked version of this is kept in outDir
        outFile = self.output_path
        #outFileHardLink = os.path.join(output_path, "orient_out_" + op.timeStamp +".h5")
        offset_iter = 0
        if not (os.path.isfile(outFile)):
            f = h5py.File(outFile, "w")
            f.create_group("data")
            f.create_group("misc")
            f.create_group("info")
            f.create_group("params")

            f.create_group("history")
            gg = f["history"]
            gg.create_group("intensities")
            gg.create_group("error")
            gg.create_group("angle")
            gg.create_group("mutual_info")
            gg.create_group("quaternion")
            gg.create_group("time")
            c = numpy.array([gen.qmax, gen.qmax, gen.qmax])
            f.create_dataset("data/center", data=c)
            f.create_dataset("misc/qmax", data=gen.qmax)
            f.create_dataset("misc/detector", data=gen.detector)
            f.create_dataset("misc/beamstop", data=gen.beamstop)

            f.create_dataset("version", data=h5py.version.hdf5_version)
            f.close()
        else:
            f = h5py.File(outFile, 'r')
            offset_iter = len(f["/history/intensities"].keys())
            f.close()
            msg = "Output will be appended to the results of %d iterations before this."%offset_iter
            print_to_log(msg=msg, log_file=outputLog)

        #if not (os.path.isfile(outFileHardLink)):
            #os.link(outFile, outFileHardLink)
        #else:
            #msg = "Hard link to %s already exists and will not be re-created.."%(outFileHardLink)
            #print_to_log(msg)

        ###############################################################
        # Iterate EMC
        ###############################################################
        intensL = 2*gen.qmax + 1
        iter_num = 1
        currQuat = initial_number_of_quaternions

        try:
            while(currQuat <= max_number_of_quaternions):
                if os.path.isfile(os.path.join(run_instance_dir,"quaternion.dat")):
                    os.remove(os.path.join(run_instance_dir,"quaternion.dat"))
                os.symlink(os.path.join(quaternion_dir ,"quaternion"+str(currQuat)+".dat"), os.path.join(run_instance_dir,"quaternion.dat"))

                diff = 1.
                while (iter_num <= max_number_of_iterations):
                    if (iter_num > 1 and diff < min_error):
                        print_to_log(msg="Error %0.3e is smaller than threshold %0.3e. Going to next quaternion."%(diff, min_error),
                                log_file=outputLog)
                        break
                    print_to_log("Beginning iteration %d, with quaternion %d %s"%(iter_num+offset_iter, currQuat, "."*20),
                                log_file=outputLog)

                    # Here is the actual timed EMC iteration, which calls the EMC.c code.
                    start_time = time.clock()

                    command_sequence = ['./EMC', '1']
                    process_handle = subprocess.Popen(command_sequence)
                    process_handle.wait()
                    time_taken = time.clock() - start_time
                    print_to_log("Took %lf s"%(time_taken),
                                log_file=outputLog)

                    # Read intermediate output of EMC.c and stuff them into a h5 file
                    # Delete these EMC.c-generated intermediate files afterwards,
                    # except finish_intensity.dat --> start_intensity.dat for next iteration.
                    gen.intensities = (numpy.fromfile("finish_intensity.dat", sep=" ")).reshape(intensL, intensL, intensL)

                    data_info = numpy.fromfile("mutual_info.dat", sep=" ")
                    most_likely_orientations = numpy.fromfile("most_likely_orientations.dat", sep=" ")

                    if(os.path.isfile("start_intensity.dat")):
                        intens1 = numpy.fromfile("start_intensity.dat", sep=" ")
                        diff = numpy.sqrt(numpy.mean(numpy.abs(gen.intensities.flatten()-intens1)**2))
                    else:
                        diff = 2.*min_error

                    f = h5py.File(outFile, "a")
                    gg = f["history/intensities"]
                    if detailed_output:
                        gg.create_dataset("%04d"%(iter_num + offset_iter), data=gen.intensities, compression="gzip", compression_opts=9)
                    try:
                        f.create_dataset("data/data", data=gen.intensities, compression="gzip", compression_opts=9)
                    except:
                        temp = f["data/data"]
                        temp[...] = gen.intensities

                    gg = f["history/error"]
                    gg.create_dataset("%04d"%(iter_num + offset_iter), data=diff)
                    print_to_log("rms change in intensities %e"%(diff),
                                log_file=outputLog)

                    gg = f["history/angle"]
                    gg.create_dataset("%04d"%(iter_num + offset_iter), data=most_likely_orientations, compression="gzip", compression_opts=9)
                    try:
                        f.create_dataset("data/angle", data=most_likely_orientations, compression="gzip", compression_opts=9)
                    except:
                        temp = f["data/angle"]
                        temp[...] = most_likely_orientations

                    gg = f["history/mutual_info"]
                    gg.create_dataset("%04d"%(iter_num + offset_iter), data=data_info)

                    gg = f["history/quaternion"]
                    gg.create_dataset("%04d"%(iter_num + offset_iter), data=currQuat)

                    gg = f["history/time"]
                    gg.create_dataset("%04d"%(iter_num + offset_iter), data=time_taken)

                    f.close()

                    f = open(outputLog, "a")
                    f.write("%e\t %lf\n"%(diff, time_taken))
                    f.close()

                    os.system("cp finish_intensity.dat start_intensity.dat")

                    print_to_log("Iteration number %d completed"%(iter_num),
                                log_file=outputLog)
                    iter_num += 1

                currQuat += 1

            print_to_log("All EMC iterations completed", log_file=outputLog)

            os.chdir(cwd)
            return 0

        except:
            os.chdir(cwd)
            #raise
            return 1

