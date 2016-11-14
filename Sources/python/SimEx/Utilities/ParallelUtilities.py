##########################################################################
#                                                                        #
# Copyright (C) 2016 Carsten Fortmann-Grote                              #
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

""" Module with utilities for parallel job.
    @author SY
    @institution DESY
    @creation 20161111
"""

import os
import subprocess
from distutils.version import StrictVersion


def _getParallelResourceInfoFromEnv():
    resource = {}
    try:
        resource['NCores'] = int(os.environ['SIMEX_NNODES'])
        resource['NNodes'] = int(os.environ['SIMEX_NCORES'])
        if resource['NNodes']<=0 or resource['NCores']<=0:
            raise IOError()
    except:
        raise IOError( "SIMEX_NNODES and SIMEX_NCORES are set incorrectly")

    return resource

def _getParallelResourceInfoFromSlurm():
    resource = {}
    try:
        resource['NNodes'] = int(os.environ['SLURM_NNODES'])
        uniqnodes=os.environ['SLURM_CPUS_PER_NODE'].split(",")
        ncores=0
        for node in uniqnodes:
            ind=node.find("(")
            if ind==-1:
                cores=node
                mul=1
            else:
                cores=node[:ind-1]
                mul=node[ind+1:node.find(")")]
            ncores+=int(cores)*int(mul)

        resource['NCores'] = ncores
        if resource['NNodes']<=0 or resource['NCores']<=0:
            raise IOError()
    except:
        raise IOError( "Cannot use SLURM_NNODES and/or SLURM_CPUS_PER_NODE. Set SIMEX_NNODES and SIMEX_NCORES instead")

    return resource

def _MPICommandName():
    if 'SIMEX_MPICOMMAND' in os.environ:
        mpicmd=os.environ['SIMEX_MPICOMMAND']
    else:
        mpicmd='mpirun'

    return mpicmd

def _getParallelResourceInfoFromMpirun():
    try:
        mpicmd = _MPICommandName()
        process = subprocess.Popen([mpicmd, "hostname"], stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT)
        (output, err) = process.communicate()

        if process.returncode !=0:
            return None

        listnodes=output.strip().split('\n')
        resource = {}
        resource['NNodes']=len(set(listnodes))
        resource['NCores']=len(listnodes)
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


    if 'SLURM_NNODES' in os.environ and 'SLURM_CPUS_PER_NODE' in os.environ:
        return _getParallelResourceInfoFromSlurm()

    resource=_getParallelResourceInfoFromMpirun()

    if resource!=None:
        return resource
    else:
        print("Was unable to determine parallel resources, will run in serial mode")
        return dict([("NCores", 0),("NNodes",1)])



def _getMPIVersionInfo():
    try:
        mpicmd = _MPICommandName()
        process = subprocess.Popen([mpicmd, "--version"], stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT)
        (output, err) = process.communicate()

        version = {}
        if "(Open MPI)" in output:
            version['Vendor']="OpenMPI"
            version['Version']=output.split("(Open MPI)")[1].split('\n')[0].strip()
            return version
        if "HYDRA" in output:
            version['Vendor']="MPICH"
            version['Version']=output.split("Version:")[1].split('\n')[0].strip()
            return version

    except:
        return None


def _getVendorSpecificMPIArguments(version,threadsPerTask):

    if version == None:
        raise IOError( "Could not determine MPI vendor/version. Set SIMEX_MPICOMMAND or "
                       "provide backengine_mpicommand calculator parameter")

    mpicmd=""
    # mapping by node is required to distribute tasks in round-robin mode.
    if version['Vendor'] == "OpenMPI":
        if StrictVersion(version['Version'])>StrictVersion("1.8.0"):
            mpicmd+=" --map-by node"
        else:
            mpicmd+=" --bynode"
        # by default, all cores will be available, no need to set OMP_NUM_THREADS
        if threadsPerTask > 0:
            mpicmd+=" -x OMP_NUM_THREADS="+str(threadsPerTask)
    elif version['Vendor'] == "MPICH":
        mpicmd+=" -map-by node"
        if threadsPerTask > 0:
            mpicmd+=" -env OMP_NUM_THREADS "+str(threadsPerTask)

    return mpicmd


def prepareMPICommandArguments(ntasks, threadsPerTask=0):
    """
    Utility prepares mpi arguments based on mpi version found in the system.

    @return : String with mpi command and arguments
    @rtype  : string

    """

    if ntasks < 0:
        raise IOError("number of tasks should be positive")

    mpicmd = _MPICommandName() + " -np " + str(ntasks)

    version = _getMPIVersionInfo()
    mpicmd+=_getVendorSpecificMPIArguments(version,threadsPerTask)

    if 'SIMEX_EXTRA_MPI_PARAMETERS' in os.environ:
        mpicmd+=" "+os.environ['SIMEX_EXTRA_MPI_PARAMETERS']


    return mpicmd

