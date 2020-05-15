""":module DMPhasing: Module that holds the DMPhasing class.  """
##########################################################################
#                                                                        #
# Copyright (C) 2015-2020 Carsten Fortmann-Grote                         #
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

import glob
import h5py
import numpy
import os
import re
import shutil
import subprocess
import tempfile

from SimEx.Calculators.AbstractPhotonAnalyzer import AbstractPhotonAnalyzer
from SimEx.Parameters.DMPhasingParameters import DMPhasingParameters
from SimEx.Utilities.EntityChecks import checkAndSetInstance

class DMPhasing(AbstractPhotonAnalyzer):
    """
    :class DMPhasing: Encapsulates photon diffraction analysis for electron density reconstruction from oriented 3D diffraction patterns.
    """

    def __init__(self, parameters=None, input_path=None, output_path=None):
        """

        :param  parameters: Phasing parameters.
        :type parameters: DMPhasingParameters instance

        :param input_path: Path to input data (file or directory).
        :type input_path: str

        :param output_path: Path to output data (file or directory).
        :type output_path: str
        """

        # Check parameters.
        if isinstance( parameters, dict ):
            parameters = DMPhasingParameters( parameters_dictionary = parameters )

        # Set default parameters is no parameters given.
        if parameters is None:
            parameters = checkAndSetInstance( DMPhasingParameters, parameters, DMPhasingParameters() )
        else:
            parameters = checkAndSetInstance( DMPhasingParameters, parameters, None )

        super(DMPhasing, self).__init__(parameters,input_path,output_path)

        self.__expected_data = ['/data/data',
                                '/data/angle',
                                '/data/center',
                                '/params/info',
                                '/version',]

        self.__provided_data = ['/data/electronDensity',
                                '/params/info',
                                '/history',
                                '/info',
                                '/misc',
                                '/version',
                                ]

    def expectedData(self):
        """ Query for the data expected by the Analyzer.

        :return: A list of strings telling which datasets are expected to be found in the input file.
        """
        return self.__expected_data

    def providedData(self):
        """ Query for the data provided by the Analyzer.

        :return: A list of strings indicating which datasets are produced in the output data."""
        return self.__provided_data

    @property
    def data(self):
        """ Query for the field data.

        :return: The stored 3D electron density map."""
        return self.__data

    def _readH5(self):
        """ """
        """ Private method for reading the hdf5 input and extracting the parameters and data relevant to initialize the object. """
        pass

    def saveH5(self):
        """ """
        """
        Method to save the object to a file.
        """
        pass

    def backengine(self):
        """ Start the actual calculation.

        :return: 0 if the DM run was successful, 1 if not. """

        status = self._run_dm()
        return status


    def _run_dm(self):
        """ """
        """ Run the Difference Map (DM) algorithm.

        :return: 0 if DM returns successfully, 1 if not.
        :note: Copied and adapted from the main routine in s2e_recon/DM/runDM.py
        :private:
        """

        number_of_trials = self.parameters.number_of_trials
        averaging_start = self.parameters.averaging_start
        number_of_iterations = self.parameters.number_of_iterations
        leash = self.parameters.leash
        number_of_shrink_cycles = self.parameters.number_of_shrink_cycles

        # Save current working directory.
        cwd = os.path.abspath(os.curdir)
        try:
            run_instance_dir = tempfile.mkdtemp(prefix='dm_run_')
            out_dir          = tempfile.mkdtemp(prefix='dm_out_')
            support_file     = os.path.join(run_instance_dir, "support.dat")
            input_intensity_file  = self.input_path
            intensity_tmp = os.path.join(run_instance_dir, "object_intensity.dat")
            output_file          = os.path.join(out_dir, "phase_out.h5")

            # Read intensity and translate into ASCII *.dat format
            (qmax, t_intens, intens_len, qPos, qPos_full) = _load_intensities(input_intensity_file)
            input_intens = t_intens
            input_intens.tofile(intensity_tmp, sep=" ")

            # Compute autocorrelation and support
            #print_to_log("Computing autocorrelation...")
            input_intens  = _v_zero_neg(input_intens.ravel()).reshape(input_intens.shape)
            auto        = numpy.fft.fftshift(numpy.abs(numpy.fft.fftn(numpy.fft.ifftshift(input_intens))))
            #print_to_log("Using 2-means clustering to determine significant voxels in autocorrelation...")
            (a_0, a_1)  = _cluster_two_means(auto.ravel())
            #print_to_log("cluster averages: %lf %lf"%(a_0, a_1))
            #print_to_log("Determining support from autocorrelation (will write to support.dat by default)...")
            support     = _support_from_autocorr(auto, qmax, a_0, a_1, support_file)

            #Start phasing
            #Store parameters into phase_out.h5.
            #Link executable from compiled version in srcDir to tmpDir
            cwd = os.path.abspath(os.curdir)
            os.chdir(run_instance_dir)
            input_options = [number_of_trials, number_of_iterations, averaging_start, leash, number_of_shrink_cycles]

            # Link executable
            #if not os.path.isfile("object_recon"):
                #os.symlink(os.path.join(op.srcDir, "object_recon"), "object_recon")
            cmd = ["object_recon"] + [str(o) for o in input_options]

            #print_to_log("Running phasing command: " + cmd)
            process_handle = subprocess.Popen(cmd)
            process_handle.wait()

            #Phasing completed. Write output to single h5
            min_objects     = glob.glob("finish_min_object*.dat")
            logFiles        = glob.glob("object*.log")
            shrinkWrapFile  = "shrinkwrap.log"
            #fin_object      = "finish_object.dat"

            #print_to_log("Done with reconstructions, now saving output from final shrink_cycle to h5 file")
            fp          = h5py.File(output_file, "w")
            g_data      = fp.create_group("data")
            g_params    = fp.create_group("params")
            #g_supp      = fp.create_group("/history/support")
            g_err       = fp.create_group("/history/error")
            g_hist_obj  = fp.create_group("/history/object")
            for n, mo in enumerate(logFiles):
                err = _parse_error_log(mo)
                g_err.create_dataset("%0.4d"%(n+1), data=err, compression="gzip")
                os.remove(mo)

            for n, ob_fn in enumerate(min_objects):
                obj = _extract_object(ob_fn)
                g_hist_obj.create_dataset("%0.4d"%(n+1), data=obj, compression="gzip")
                os.remove(ob_fn)

            finish_object = _extract_object("finish_object.dat")
            g_data.create_dataset("electronDensity", data=finish_object, compression="gzip")
            os.system("cp finish_object.dat start_object.dat")

            g_params.create_dataset("DM_support",           data=support, compression="gzip")
            g_params.create_dataset("DM_numTrials",         data=number_of_trials)
            g_params.create_dataset("DM_numIterPerTrial",   data=number_of_iterations)
            g_params.create_dataset("DM_startAvePerIter",   data=averaging_start)
            g_params.create_dataset("DM_leashParameter",    data=leash)
            g_params.create_dataset("DM_shrinkwrapCycles",  data=number_of_shrink_cycles)

            shrinkWrap = _parse_shrinkwrap_log(shrinkWrapFile)
            fp.create_dataset("/history/shrinkwrap", data=shrinkWrap, compression="gzip")
            fp.create_dataset("version", data=h5py.version.hdf5_version)

            fp.close()

            shutil.copy( output_file, os.path.join( cwd, self.output_path ) )
            os.chdir(cwd)
            return 0

        except:
            os.chdir(cwd)
            return 1

def _load_intensities(ref_file):
    """ """
    """ Private function for loading 3D intensity maps from a file.

    :param ref_file: Filename holding the data to load.
    :type ref_file: str
    """

    fp      = h5py.File(ref_file, 'r')
    t_intens = (fp["data/data"][()]).astype("float")
    fp.close()
    intens_len = len(t_intens)
    qmax    = intens_len/2
    (q_low, q_high) = (15, int(0.9*qmax))
    qRange1 = numpy.arange(-q_high, q_high + 1)
    qRange2 = numpy.arange(-qmax, qmax + 1)
    qPos0   = numpy.array([[i,j,0] for i in qRange1 for j in qRange1 if numpy.sqrt(i*i+j*j) > q_low]).astype("float")
    qPos1   = numpy.array([[i,0,j] for i in qRange1 for j in qRange1 if numpy.sqrt(i*i+j*j) > q_low]).astype("float")
    qPos2   = numpy.array([[0,i,j] for i in qRange1 for j in qRange1 if numpy.sqrt(i*i+j*j) > q_low]).astype("float")
    qPos    = numpy.concatenate((qPos0, qPos1, qPos2))
    qPos_full = numpy.array([[i,j,k] for i in qRange2 for j in qRange2 for k in qRange2]).astype("float")
    return (qmax, t_intens, intens_len, qPos, qPos_full)

def _zero_neg(x):
    return 0. if x<=0. else x

_v_zero_neg  = numpy.vectorize(_zero_neg)

def _find_two_means(vals, v0, v1):
    v0_t    = 0.
    v0_t_n  = 0.
    v1_t    = 0.
    v1_t_n  = 0.
    for vv in vals:
        if (numpy.abs(vv-v0) > abs(vv-v1)):
            v1_t    += vv
            v1_t_n  += 1.
        else:
            v0_t    += vv
            v0_t_n  += 1.
    if v0_t_n > 0.:
        v0_t /= v0_t_n
    if v1_t_n > 0.:
        v1_t /= v1_t_n
    return (v0_t, v1_t)

def _cluster_two_means(vals):
    (v0,v1)     = (0.,0.1)
    (v00, v11)  = _find_two_means(vals, v0, v1)
    err = 0.5*(numpy.abs(v00-v0)+numpy.abs(v11-v1))
    while(err > 1.E-5):
        (v00, v11)  = _find_two_means(vals, v0, v1)
        err         = 0.5*(numpy.abs(v00-v0)+numpy.abs(v11-v1))
        (v0, v1)    = (v00, v11)
    return (v0, v1)

def _support_from_autocorr(auto, qmax, thr_0, thr_1, supp_file, kl=1, write=True):
    pos     = numpy.argwhere(numpy.abs(auto-thr_0) > numpy.abs(auto-thr_1))
    pos_set = set()
    pos_list= []
    kerl    = list(range(-kl,kl+1))
    ker     = [[i,j,k] for i in kerl for j in kerl for k in kerl]

    def trun(v):
        return int(numpy.ceil(0.5*v))

    v_trun = numpy.vectorize(trun)

    for (pi, pj, pk) in pos:
        for (ci, cj, ck) in ker:
            pos_set.add((pi+ci, pj+cj, pk+ck))
    for s in pos_set:
        pos_list.append([s[0], s[1], s[2]])

    pos_array = numpy.array(pos_list)
    pos_array -= [a.min() for a in pos_array.transpose()]
    pos_array = numpy.array([v_trun(a) for a in pos_array])

    if write:
        fp  = open(supp_file, "w")
        fp.write("%d %d\n"%(qmax, len(pos_array)))
        for p in pos_array:
            fp.write("%d %d %d\n" % (p[0], p[1], p[2]))
        fp.close()

    return pos_array

def show_support(support):
    #fig = plt.figure()
    #ax = fig.add_subplot(111, projection='3d')
    #(x,y,z) = support.transpose()
    #ax.scatter(x, y, z, c='r', marker='s')
    #plt.show()
    pass

def _parse_shrinkwrap_log(shrinkwrap_fn):
    with open(shrinkwrap_fn, "r") as fp:
        lines = fp.readlines()
        fp.close()
    lst = []
    for ll in lines:
        m = re.match("supp_vox = (\d+)\s", ll)
        if m:
            (supp_size,) = m.groups()
            lst.append(int(supp_size))

    return numpy.array(lst)

def _parse_error_log(err_fn):
    with open(err_fn, "r") as fp:
        lines = fp.readlines()[2:]
        fp.close()
    lst = []
    for ll in lines:
        m = re.match("iter = (\d+)\s+error = (\d+\.\d+)", ll)
        if m:
            (iter, err) = m.groups()
            lst.append(float(err))
    return numpy.array(lst)

def _extract_object(object_fn):
    tmp = numpy.fromfile(object_fn, sep=" ")
    s = tmp.shape[0]
    l = int(round(s**(1./3.)))

    return tmp.reshape(l,l,l)
