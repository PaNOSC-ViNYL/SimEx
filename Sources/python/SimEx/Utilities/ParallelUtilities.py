""":module ParallelUtilities: Hosts utilities to query HPC runtime parameters."""
##########################################################################
#                                                                        #
# Copyright (C) 2016-2017 Carsten Fortmann-Grote                         #
#               2016-2017 Sergey Yakubov                                 #
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

import os
import subprocess
from distutils.version import StrictVersion
from py3nvml import py3nvml as nvml


def _getParallelResourceInfoFromEnv():
    """ """
    resource = {}
    try:
        resource['NCores'] = int(os.environ['SIMEX_NCORES'])
        resource['NNodes'] = int(os.environ['SIMEX_NNODES'])
        if resource['NNodes'] <= 0 or resource['NCores'] <= 0:
            raise IOError()
    except:
        raise IOError("SIMEX_NNODES and SIMEX_NCORES are set incorrectly")

    return resource


def getThreadsPerCoreFromSlurm():
    process = subprocess.Popen(['slurmd', '-C'],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT)
    (output, err) = process.communicate()
    output = output.decode('utf-8')
    threads_per_core = int(output.partition('ThreadsPerCore=')[2].split()[0])
    return threads_per_core


def _getParallelResourceInfoFromSlurm():
    """ """
    resource = {}
    try:
        threads_per_core = getThreadsPerCoreFromSlurm()
        resource['NNodes'] = int(os.environ['SLURM_JOB_NUM_NODES'])
        uniq_nodes = os.environ['SLURM_JOB_CPUS_PER_NODE'].split(",")
        # SLURM sets this variable to something like 40(x2),20(x1),10(x10). We extract ncores from this
        # print('uniq_nodes =', uniq_nodes)
        ncores = 0
        for node in uniq_nodes:
            ind = node.find("(")
            if ind == -1:
                cores = node
                mul = 1
            else:
                cores=node[:ind]
                mul=node[ind+2:node.find(")")]
            ncores+=int(cores)*int(mul)

        # Use all physical cores
        resource['NCores'] = int(ncores / threads_per_core)
        if resource['NNodes'] <= 0 or resource['NCores'] <= 0:
            raise IOError()
    except:
        print (os.environ['SLURM_JOB_CPUS_PER_NODE'])
        raise IOError( "Cannot use SLURM_JOB_NUM_NODES and/or SLURM_JOB_CPUS_PER_NODE. Set SIMEX_NNODES and SIMEX_NCORES instead")

    return resource


def _MPICommandName():
    """ """
    if 'SIMEX_MPICOMMAND' in os.environ:
        mpicmd = os.environ['SIMEX_MPICOMMAND']
    else:
        mpicmd = 'mpirun'

    return mpicmd


def _getParallelResourceInfoFromMpirun():
    """ """
    # we call mpirun hostname which returns list of nodes where mpi tasks will start. Each node can be
    # listed several times (depending on mpi vendor) that gives us number of cores available for mpirun on this node
    try:
        mpicmd = _MPICommandName()
        process = subprocess.Popen([mpicmd, "hostname"],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT)
        (output, err) = process.communicate()
        # Decode
        output = output.decode('utf-8')

        if process.returncode != 0:
            return None

        nodes = output.strip().split('\n')
        resource = {}
        resource['NNodes'] = len(set(nodes))
        resource['NCores'] = len(nodes)
        return resource
    except:
        return None


def getParallelResourceInfo():
    """
    Utility extract information about available parallel resources.

    @return : The dictionary expected by downstream simex modules.
    @rtype  : resource

    """

    if 'SIMEX_NNODES' in os.environ and 'SIMEX_NCORES' in os.environ:
        return _getParallelResourceInfoFromEnv()

    if 'SLURM_JOB_NUM_NODES' in os.environ and 'SLURM_JOB_CPUS_PER_NODE' in os.environ:
        return _getParallelResourceInfoFromSlurm()

    resource = _getParallelResourceInfoFromMpirun()

    if resource != None:
        return resource
    else:
        print(
            "Was unable to determine parallel resources, will run in serial mode"
        )
        return dict([("NCores", 0), ("NNodes", 1)])


def _getMPIVersionInfo():
    """ """
    try:
        mpi_cmd = _MPICommandName()

        process = subprocess.Popen([mpi_cmd, "--version"],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT)
        (output, err) = process.communicate()
        output = output.decode('utf-8')

        version = {}
        if "(Open MPI)" in output:
            version['Vendor'] = "OpenMPI"
            version['Version'] = output.split("(Open MPI)")[1].split(
                '\n')[0].strip()
            return version
        if "HYDRA" in output:
            version['Vendor'] = "MPICH"
            version['Version'] = output.split("Version:")[1].split(
                '\n')[0].strip()
            return version

    except Exception:
        return None


def _getVendorSpecificMPIArguments(version, threads_per_task):
    """ """

    mpi_cmd = ""

    # If version is empty
    if version is None:
        msg = ('Warning: Could not determine MPI vendor/version.'
               'Please set your own MPI arguments if needed.')
        print(msg)
    else:
        # Mapping by node is required to distribute tasks in round-robin mode.
        if version['Vendor'] == "OpenMPI":
            if StrictVersion(version['Version']) > StrictVersion("1.8.0"):
                mpi_cmd += " --map-by node --bind-to none"
            else:
                mpi_cmd += " --bynode"
            # by default, all cores will be available, no need to set OMP_NUM_THREADS
            if threads_per_task > 0:
                mpi_cmd += " -x OMP_NUM_THREADS=" + str(threads_per_task)
            mpi_cmd += " -x OMPI_MCA_mpi_warn_on_fork=0 -x OMPI_MCA_btl_base_warn_component_unused=0"
            mpi_cmd += ' --mca mpi_cuda_support 0'+' --mca btl_openib_warn_no_device_params_found 0'
        elif version['Vendor'] == "MPICH":
            mpi_cmd += " -map-by node"
            if threads_per_task > 0:
                mpi_cmd += " -env OMP_NUM_THREADS " + str(threads_per_task)

    return mpi_cmd


def prepareMPICommandArguments(ntasks, threads_per_task=0):
    """
    Utility prepares mpi arguments based on mpi version found in the system.

    :param ntasks: Number of MPI tasks
    :type ntasks: int

    :param threads_per_task: Number of threads per task
    :type threads_per_task: int

    @return : String with mpi command and arguments
    @rtype  : string

    """

    if ntasks < 0:
        raise IOError("number of tasks should be positive")

    mpi_cmd = _MPICommandName() + " -np " + str(ntasks)

    version = _getMPIVersionInfo()
    MPIArguments = _getVendorSpecificMPIArguments(version, threads_per_task)
    mpi_cmd += MPIArguments

    if 'SIMEX_EXTRA_MPI_PARAMETERS' in os.environ:
        mpi_cmd += " " + os.environ['SIMEX_EXTRA_MPI_PARAMETERS']

    if mpi_cmd.split(' ')[0] != "mpirun":
        raise IOError(
            "MPI command: '" + mpi_cmd + "' is not starting with 'mpirun' " +
            "Please check your SIMEX_MPICOMMAND environment variable setting.")

    return mpi_cmd


def getCUDAEnvironment():
    """ Get the CUDA runtime environment parameters (number of cards etc.). """

    rdict = dict()
    rdict['first_available_device_index'] = None
    rdict['device_count'] = 0

    try:
        nvml.nvmlInit()
        rdict['device_count'] = nvml.nvmlDeviceGetCount()

    except Exception:
        print(
            'WARNING: At least one of (py3nvml.nvml, CUDA) is not available. Will continue without GPU.'
        )
        return rdict

    for i in range(rdict['device_count']):
        memory_info = nvml.nvmlDeviceGetMemoryInfo(
            nvml.nvmlDeviceGetHandleByIndex(i))
        memory_usage_percentage = memory_info.used / memory_info.total

        if memory_usage_percentage <= 0.1:
            rdict['first_available_device_index'] = i
            break

    nvml.nvmlShutdown()

    return rdict
