""":module XFELPhotonPropagator: Module that holds the XFELPhotonPropagator class.  """
##########################################################################
#                                                                        #
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


import os
import subprocess
import shlex

from SimEx.Calculators.AbstractPhotonPropagator import AbstractPhotonPropagator
from SimEx.Parameters.WavePropagatorParameters import WavePropagatorParameters
from SimEx.Utilities import EntityChecks
from SimEx.Utilities import IOUtilities
from SimEx.Utilities import ParallelUtilities
from SimEx.Utilities import wpg_to_opmd
from prop import propagate_s2e

class XFELPhotonPropagator(AbstractPhotonPropagator):
    """
    :class XFELPhotonPropagator: Represents coherent wavefront propagation using the WPG wrapper for SWR.
    """

    def __init__(self, parameters=None, input_path=None, output_path=None):
        """

        :param parameters: Parameters for the photon propagation.
        :type parameters: WavePropagatorParameters instance.

        :param  input_path: Location of input data for photon propagation.
        :type input_path:   str, default 'FELsource/'

        :param output_path: Location of propagation output data.
        :type output_path:  str, default 'prop/'
        """


        # Handle default parameters if None.
        parameters = EntityChecks.checkAndSetInstance( WavePropagatorParameters, parameters, WavePropagatorParameters() )

        # Initialize base class.
        super(XFELPhotonPropagator, self).__init__(parameters,input_path,output_path)


    def computeNTasks(self):
        resources=ParallelUtilities.getParallelResourceInfo()
        nnodes=resources['NNodes']
        ncores=resources['NCores']

        cpusPerTask=self.parameters.cpus_per_task

        if cpusPerTask=="MAX":
            np=nnodes
            ncores=0
        else:
            np=max(1,int(ncores/int(cpusPerTask)))
            ncores=int(cpusPerTask)

        return (np,ncores)


    def backengine(self):
        """ Starts WPG simulations in parallel in a subprocess """

        fname = IOUtilities.getTmpFileName()
        self.dumpToFile(fname)

        forcedMPIcommand=self.parameters.forced_mpi_command

        if forcedMPIcommand=="":
            (np,ncores)=self.computeNTasks()
            mpicommand=ParallelUtilities.prepareMPICommandArguments(np,ncores)
        else:
            mpicommand=forcedMPIcommand

        if 'SIMEX_VERBOSE' in os.environ:
            if 'MPI' in  os.environ['SIMEX_VERBOSE']:
                print(("XFELPhotonPropagator backengine mpicommand: "+mpicommand))
            if 'PYTHON' in os.environ['SIMEX_VERBOSE']:
                import platform
                print("Running python %s." % ( platform.python_version() ) )

        mpicommand+=" python "+__file__+" "+fname


        args = shlex.split(mpicommand)

        proc = subprocess.Popen(args,universal_newlines=True)
        proc.wait()
        os.remove(fname)

        return proc.returncode

    def _run(self):

        """ This method drives the WPG backengine.

        :return: 0 if WPG returns successfully, 1 if not.

        """

        # import should be here, not in header as it calls MPI_Init when imported. We want MPI to be
        # initialized at this stage only.
        from mpi4py import MPI

        # MPI info
        comm = MPI.COMM_WORLD
        thisProcess = comm.rank
        numProcesses = comm.size

        # Check if input path is a directory.
        if os.path.isdir(self.input_path):
            input_files = [ os.path.join( self.input_path, input_file ) for \
                            input_file in os.listdir( self.input_path ) ]
            input_files.sort() # Assuming the filenames have some kind of ordering scheme.
        else:
            if thisProcess == 0: # other MPI processes (if any) have nothing to do
                propagate_s2e.propagate(self.input_path, self.output_path, self.parameters.beamline.get_beamline)
            return 0

        # If we have more than one input file, we should also have more than one output file, i.e.
        # output_path should be a directory.
        if os.path.isfile(self.output_path):
            raise IOError("The given output path is a file but a directory is needed. Cowardly refusing to overwrite.")

        # Check if output dir exists, create if not.
        if not os.path.isdir(self.output_path):
            os.mkdir(self.output_path)

        # Loop over all input files and generate one run per source file.
        for i,input_file in enumerate(input_files):
            ### TODO: Transmit number of cpus.
            # process file on a corresponding process (round-robin)
            if i % numProcesses == thisProcess:
                output_file = os.path.join( self.output_path, 'prop_out_%07d.h5' % (i) )
                propagate_s2e.propagate(input_file, output_file, self.parameters.beamline.get_beamline)

                # Rewrite in openpmd conformant way.
                # wpg_to_opmd.convertToOPMD( output_file )

        return 0


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
        :param output_path: Path to propagation output.
        :type output_path: string
        """
        pass # No action required since output is written in backengine.

if __name__ == '__main__':
    XFELPhotonPropagator.runFromCLI()
