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
from subprocess import Popen, PIPE


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

def _getParallelResourceInfoFromMpirun():
    try:
        if 'SIMEX_MPICOMMAND' in os.environ:
            mpicmd=os.environ['SIMEX_MPICOMMAND']
        else:
            mpicmd='mpirun'

        process = Popen([mpicmd, "hostname"], stdout=PIPE)
        (output, err) = process.communicate()
        exit_code = process.wait()
        if exit_code!=0:
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


