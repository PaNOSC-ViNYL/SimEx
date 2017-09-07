""" Module that holds the EMCOrientation class.  """
##########################################################################
#                                                                        #
# Copyright (C) 2015-2017 Carsten Fortmann-Grote                         #
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
import subprocess,shlex
import tempfile
import time

from EMCCaseGenerator import  EMCCaseGenerator, _print_to_log
from SimEx.Calculators.AbstractPhotonAnalyzer import AbstractPhotonAnalyzer
from SimEx.Parameters.EMCOrientationParameters import EMCOrientationParameters
from SimEx.Utilities import IOUtilities
from SimEx.Utilities import ParallelUtilities
from SimEx.Utilities.EntityChecks import checkAndSetInstance

class EMCOrientation(AbstractPhotonAnalyzer):

    """
    Class representing photon data analysis for orientation of 2D diffraction patterns to a 3D diffraction volume. """
    def __init__(self, parameters=None, input_path=None, output_path=None, tmp_files_path=None, run_files_path=None):
        """
        :param  parameters: Parameters for the EMC orientation calculator.
        :type parameters: EMCOrientationParameters instance

        :param input_path: Path to directory holding input data for EMC.
        :type input_path: str

        :param output_path: Path to file where output data will be stored.
        :type output_path: str

        :param tmp_files_path: Path to directory where temporary files will be stored.
        :type tmp_files_path: str

        :param run_files_path: Path to directory where run data will be stored, in particular the sparse photons file 'photons.dat' and 'detector.dat'.
        :type run_files_path: str

        :note: If 'run_files_path' is an existing directory that contains data from a previous EMC run, the current run will append to the
               existing data. A consistency check is performed.

        """

        # Check parameters.
        if isinstance( parameters, dict ):
            parameters = EMCOrientationParameters( parameters_dictionary = parameters )

        # Set default parameters is no parameters given.
        if parameters is None:
            parameters = checkAndSetInstance( EMCOrientationParameters, parameters, EMCOrientationParameters() )
        else:
            parameters = checkAndSetInstance( EMCOrientationParameters, parameters, None )


        # Initialize base class.
        super(EMCOrientation, self).__init__(parameters,input_path,output_path)


        self.__provided_data = ['data/data',
                                'data/angle',
                                'data/center',
                                'params/info',
                                'version',]

        self.__expected_data = ['/data/data',
                                '/data/diffr',
                                '/data/angle',
                                '/params/geom/detectorDist',
                                '/params/geom/pixelWidth',
                                '/params/geom/pixelHeight',
                                '/params/geom/mask',
                                '/params/beam/photonEnergy',
                                '/params/beam/photons',
                                '/params/beam/focusArea',
                                ]

        # Set run and tmp files paths.
        if _checkPaths( run_files_path, tmp_files_path ):
            self.run_files_path = run_files_path
            self.tmp_files_path = tmp_files_path


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

    @property
    def run_files_path(self):
        return self.__run_instance_dir
    @run_files_path.setter
    def run_files_path(self, value):
        """ Set the path to runtime files.

        :param value: The path where runtime generated files shall be saved.
        :type value: str
        """

        if isinstance( value, str ) or value is None:
            self.__run_instance_dir = value
        else:
            raise IOError( "Parameter 'run_files_path' must be a string or None." )

    @property
    def tmp_files_path(self):
        return self.__tmp_out_dir
    @tmp_files_path.setter
    def tmp_files_path(self, value):
        """ Set the path to tmptime files.
        :param value: The path where tmptime generated files shall be saved.
        :type value: str
        """

        if isinstance( value, str ) or value is None:
            self.__tmp_out_dir = value
        else:
            raise IOError( "Parameter 'tmp_files_path' must be a string or None." )

    def _readH5(self):
        """ """
        """ Private method for reading the hdf5 input and extracting the parameters and data relevant to initialize the object. """
        pass # Nothing to be done since IO happens in backengine.

    def saveH5(self):
        """ """
        """
        Private method to save the object to a file.

        :param output_path: The file where to save the object's data.
        :type output_path: string
        """
        pass # No action required since output is written in backengine.

    def _setupPaths(self):
        """ """
        """ Private method do setup all needed directories for temp and persistant output. """
        # If tmp dir is set to None, create a temporary directory and store path on object and return value.
        if self.tmp_files_path is None:
            tmp_out_dir = tempfile.mkdtemp(prefix='emc_out_')
            self.tmp_files_path = tmp_out_dir
        # Else, check if path exists and store on return value.
        else:
            if not os.path.isdir( self.tmp_files_path ):
                os.mkdir( self.tmp_files_path )
            tmp_out_dir = self.tmp_files_path

        # Same for run dir.
        if self.run_files_path is None:
            run_instance_dir = tempfile.mkdtemp(prefix='emc_run_')
            self.__run_instance_dir = run_instance_dir
        else:
            if not os.path.isdir( self.run_files_path ):
                os.mkdir( self.run_files_path )
                # If run dir already existed, this would have been caught earlier.
            run_instance_dir = self.run_files_path

        self._sparsePhotonFile    = os.path.join(tmp_out_dir, "photons.dat")
        self._detectorFile        = os.path.join(tmp_out_dir, "detector.dat")
        self._outputLog           = os.path.join(run_instance_dir, "EMC_extended.log")
        self._avgPatternFile      = os.path.join(tmp_out_dir, "avg_photon.h5")
        self._lockFile            = os.path.join(tmp_out_dir, "write.lock")

        self._run_instance_dir = run_instance_dir
        self._tmp_out_dir = tmp_out_dir

        return run_instance_dir,tmp_out_dir

    def computeNTasks(self):
        resources=ParallelUtilities.getParallelResourceInfo()
        ncores=resources['NCores']
        nnodes=resources['NNodes']

        if self.parameters.cpus_per_task=="MAX":
            np=nnodes
        else:
            np=max(int(ncores/int(self.parameters.cpus_per_task)),1)

        return np

    def backengine(self):
        """ Starts EMC simulations in parallel in a subprocess """

        # Set paths.
        self._setupPaths()

        fname = IOUtilities.getTmpFileName()
        self.dumpToFile(fname)

        # collect MPI arguments
        if self.parameters.forced_mpi_command=="":
            np=self.computeNTasks()
            mpicommand=ParallelUtilities.prepareMPICommandArguments(np)
        else:
            mpicommand=self.parameters.forced_mpi_command
        # collect program arguments
        command_sequence = ['python',
                            __file__,
                            fname,
                            ]
        # put MPI and program arguments together
        args = shlex.split(mpicommand) + command_sequence


        if 'SIMEX_VERBOSE' in os.environ:
            if 'MPI' in  os.environ['SIMEX_VERBOSE']:
                print("EMCOrientation backengine mpicommand: "+mpicommand)

        # Run the backengine command.
        proc = subprocess.Popen(args)
        proc.wait()

        os.remove(fname)


        # Return the return code from the backengine.
        return proc.returncode

    def _need_prepare_photon_files(self,thisProcess):
        ###############################################################
        # A lock file is created if subprocess is converting sparse photons
        #   so that another subprocess does not clobber an ongoing conversion.
        # Make photons.dat and detector.dat if they don't exist.
        # Create time-tagged output subdirectory for intermediate states.
        ###############################################################

        while (os.path.isfile(self._lockFile)):
            # Sleep in 30 s intervals, then check if sparse photon lock has been released.
            sleep_duration = 30
            msg = "Lock file in " + self._tmp_out_dir + ". "
            msg += "Photons.dat likely being written to tmpDir by another programm. "
            msg += "Sleeping this programm for %d s." % sleep_duration
            if thisProcess == 0:
                _print_to_log(msg, log_file=self._outputLog)
            time.sleep(sleep_duration)

        return not (os.path.isfile(self._sparsePhotonFile) and os.path.isfile(self._detectorFile))

    def _join_photon_files(self,numProcesses):

        outf = open(self._sparsePhotonFile, "w")

        for n in range(0,numProcesses):
            fname=self._sparsePhotonFile + "_"+str(n)
            with open(fname) as infile:
                    for line in infile:
                        outf.write(line)
            os.system("rm %s " % fname)
        outf.close()

        outh5 = h5py.File(self._avgPatternFile, 'w')
        for n in range(0,numProcesses):
            fname=self._avgPatternFile + "_"+str(n)
            f = h5py.File(fname, 'r')
            if n == 0:
                mask = f["mask"].value
                avg = f["average"].value
            else:
                avg += f["average"].value
            os.system("rm %s " % fname)

        outh5.create_dataset("average", data=avg, compression="gzip", compression_opts=9)
        outh5.create_dataset("mask", data=mask, compression="gzip", compression_opts=9)
        outh5.close()


    def _prepare_photon_files(self,comm):
        thisProcess = comm.rank
        numProcesses = comm.size

        # Prepare for reading input.
        if os.path.isdir(self.input_path):
            photonFiles         = [ os.path.join(self.input_path, pf) for pf in os.listdir( self.input_path ) ]
            photonFiles.sort()
        elif os.path.isfile(self.input_path):
            photonFiles = [self.input_path]
        else:
            raise IOError( " Input file %s not found." % self.input_path )

        gen = EMCCaseGenerator(self._outputLog)
        gen.readGeomFromPhotonData(photonFiles[0],thisProcess)

        if thisProcess == 0:
            os.system("touch %s" % self._lockFile)
            gen.writeDetectorToFile(filename=self._detectorFile)

        gen.writeSparsePhotonFile(photonFiles, self._sparsePhotonFile+ "_"+str(thisProcess),
                                               self._avgPatternFile + "_"+str(thisProcess),
                                               thisProcess,numProcesses)
        comm.Barrier()

        if thisProcess == 0:
            self._join_photon_files(numProcesses)

        comm.Barrier()

        if thisProcess == 0:
            _print_to_log(msg="Sparse photons file created. Deleting lock file now", log_file=self._outputLog)
            #        _print_to_log(msg="Detector parameters: %d %d %d"%(gen.qmax, len(gen.detector), len(gen.beamstop)), log_file=self._outputLog)
            os.system("rm %s " % self._lockFile)

    def _run(self):

        """ """
        """ Private method to run the Expand-Maximize-Compress (EMC) algorithm.

        :return: 0 if EMC returns successfully, 1 if not.

        :note: Copied and adapted from the main routine in s2e_recon/EMC/runEMC.py
        """
        import mpi4py.rc
        mpi4py.rc.finalize = False

        from mpi4py import MPI
        # MPI info
        comm = MPI.COMM_WORLD
        thisProcess = comm.rank

        if self._need_prepare_photon_files(thisProcess):
            if thisProcess == 0:
                msg = "Photons.dat and detector.dat not found in " + self._tmp_out_dir + ". Will create them now..."
                _print_to_log(msg=msg, log_file=self._outputLog)
            self._prepare_photon_files(comm)
        else:
            if thisProcess == 0:
                msg = "Photons.dat and detector.dat already exists in " + self._tmp_out_dir + "."
                _print_to_log(msg=msg, log_file=self._outputLog)

# the rest is non-parallel (yet)
        if thisProcess != 0:
            MPI.Finalize()
            return 0

        ###############################################################
        # Instantiate a reconstruction object
        ###############################################################
        # If parameters are given, map them to command line arguments.
        initial_number_of_quaternions = self.parameters.initial_number_of_quaternions
        max_number_of_quaternions = self.parameters.max_number_of_quaternions
        max_number_of_iterations = self.parameters.max_number_of_iterations
        min_error = self.parameters.min_error
        beamstop = self.parameters.beamstop
        detailed_output = self.parameters.detailed_output

        quaternion_dir      = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'CalculatorUtilities', 'quaternions')

        gen = EMCCaseGenerator(self._outputLog)
        gen.readGeomFromDetectorFile(self._detectorFile)
        _print_to_log(msg="Detector parameters: %d %d %d"%(gen.qmax, len(gen.detector),len(gen.beamstop)), log_file=self._outputLog)


        if not (os.path.isfile(os.path.join(self._run_instance_dir,"detector.dat"))):
            os.symlink(os.path.join(self._tmp_out_dir,"detector.dat"), os.path.join(self._run_instance_dir,"detector.dat"))
        if not (os.path.isfile(os.path.join(self._run_instance_dir,"photons.dat"))):
            os.symlink(os.path.join(self._tmp_out_dir,"photons.dat"), os.path.join(self._run_instance_dir,"photons.dat"))

        ###############################################################
        # Create dummy destination h5 for intermediate output from EMC
        ###############################################################
        cwd = os.path.abspath(os.curdir)
        os.chdir(self._run_instance_dir)
        #Output file is kept in tmpOutDir.
        outFile = self.output_path
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
            _print_to_log(msg=msg, log_file=self._outputLog)

        ###############################################################
        # Iterate EMC
        ###############################################################
        intensL = 2*gen.qmax + 1
        iter_num = 1
        currQuat = initial_number_of_quaternions

        try:
            while(currQuat <= max_number_of_quaternions):
                if os.path.isfile(os.path.join(self._run_instance_dir,"quaternion.dat")):
                    os.remove(os.path.join(self._run_instance_dir,"quaternion.dat"))
                os.symlink(os.path.join(quaternion_dir ,"quaternion"+str(currQuat)+".dat"), os.path.join(self._run_instance_dir,"quaternion.dat"))

                diff = 1.
                while (iter_num <= max_number_of_iterations):
                    if (iter_num > 1 and diff < min_error):
                        _print_to_log(msg="Error %0.3e is smaller than threshold %0.3e. Going to next quaternion."%(diff, min_error),
                                log_file=self._outputLog)
                        break
                    _print_to_log("Beginning iteration %d, with quaternion %d %s"%(iter_num+offset_iter, currQuat, "."*20),
                                log_file=self._outputLog)

                    # Here is the actual timed EMC iteration, which calls the EMC.c code.
                    start_time = time.clock()

                    #command_sequence = ['EMC.x', '1']
                    command_sequence = ['EMC', '1']
                    process_handle = subprocess.Popen(command_sequence)
                    process_handle.wait()
                    time_taken = time.clock() - start_time
                    _print_to_log("Took %lf s"%(time_taken),
                                log_file=self._outputLog)

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
                    _print_to_log("rms change in intensities %e"%(diff),
                                log_file=self._outputLog)

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

                    f = open(self._outputLog, "a")
                    f.write("%e\t %lf\n"%(diff, time_taken))
                    f.close()

                    os.system("cp finish_intensity.dat start_intensity.dat")

                    _print_to_log("Iteration number %d completed"%(iter_num),
                                log_file=self._outputLog)
                    iter_num += 1

                currQuat += 1

            _print_to_log("All EMC iterations completed", log_file=self._outputLog)

            os.chdir(cwd)
            MPI.Finalize()
            return 0

        except:
            os.chdir(cwd)
            MPI.Finalize()
            return 1

def _checkPaths(run_files_path, tmp_files_path):
    """ """
    """ Private (hidden) utility to check validity of paths given to constructor. """

    if not all([ (isinstance( path, str ) or path is None) for path in [run_files_path, tmp_files_path] ]):
        raise IOError( "Paths must be strings.")

    if run_files_path is not None:
        if os.path.isdir( run_files_path ):
            raise IOError( "Run files path already exists, cowardly refusing to overwrite.")

    return True

if __name__ == '__main__':
    EMCOrientation.runFromCLI()
