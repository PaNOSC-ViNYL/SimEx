""" Module that holds the CrystFELPhotonDiffractor class.  """
##########################################################################
#                                                                        #
# Copyright (C) 2017 Carsten Fortmann-Grote                              #
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
import inspect
import os
import subprocess,shlex

import prepHDF5
from scipy import constants

from SimEx.Calculators.AbstractPhotonDiffractor import AbstractPhotonDiffractor
from SimEx.Calculators.CrystFELPhotonDiffractorParameters import CrystFELPhotonDiffractorParameters
from SimEx.Utilities import ParallelUtilities
from SimEx.Utilities.EntityChecks import checkAndSetInstance, checkAndSetPositiveInteger

class CrystFELPhotonDiffractor(AbstractPhotonDiffractor):
    """
    Class representing a x-ray free electron laser photon propagator.
    """

    def __init__(self,  parameters=None, input_path=None, output_path=None):
        """

        :param parameters: Parameters of the calculation (not data).
        :type parameters:  CrystFELPhotonDiffractorParameters

        :param input_path: Path to hdf5 file holding the input data.
        :type input_path: str

        :param output_path: Path to hdf5 file for output.
        :type output_path: str
        """

        # Set default parameters if no parameters given.
        if parameters is None:
            raise ValueError( "Parameters must at least specify the sample structure, e.g. in pdb format.")
        else:
            self.__parameters = checkAndSetInstance( CrystFELPhotonDiffractorParameters, parameters, None )


        # Init base class.

        # Dummy input path since none required (we don't read from a beam propgation yet.)
        input_path = os.path.dirname(__file__)

        if output_path is None:
            output_path = os.path.join(os.path.dirname(__file__), "diffr")

        super(CrystFELPhotonDiffractor, self).__init__(parameters,input_path,output_path)

        ### FIXME
        self.__provided_data = [
                                '/data/data',
                                '/data/diffr',
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

    def expectedData(self):
        """ Query for the data expected by the Diffractor. """
        return None

    def providedData(self):
        """ Query for the data provided by the Diffractor. """
        return None


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
        """ This method drives the backengine singFEL."""

        # Setup directory structure as needed.
        if not os.path.isdir( self.output_path ):
            os.makedirs( self.output_path )
        output_file_base = os.path.join( self.output_path, "diffr_out")

        if self.parameters.number_of_diffraction_patterns == 1:
            output_file_base += "_0000001.h5"

        # collect MPI arguments
        if self.parameters.forced_mpi_command=="":
            np=self.computeNTasks()
            mpicommand=ParallelUtilities.prepareMPICommandArguments(np)
        else:
            mpicommand=self.parameters.forced_mpi_command

        # Setup command, minimum set first.
        command_sequence = ['pattern_sim',
                            '-p %s'                 % self.parameters.sample,
                            '--geometry=%s'         % self.parameters.geometry,
                            '--output=%s'           % output_file_base,
                            '--number=%d'           % self.parameters.number_of_diffraction_patterns,
                            ]
        # Handle random rotation is requested.
        if self.parameters.uniform_rotation is True:
            command_sequence.append('--random-orientation')
            command_sequence.append('--really-random')

        if self.parameters.beam_parameters is not None:
            command_sequence.append('--photon-energy=%f' % (self.parameters.beam_parameters.photon_energy))
            command_sequence.append('--beam-bandwidth=%f' % (self.parameters.beam_parameters.photon_energy_relative_bandwidth))
            nphotons = self.parameters.beam_parameters.pulse_energy / constants.e / self.parameters.beam_parameters.photon_energy
            command_sequence.append('--nphotons=%e' % (nphotons))
            command_sequence.append('--beam-radius=%e' % (self.parameters.beam_parameters.beam_diameter_fwhm/2.))
            command_sequence.append('--spectrum=%s' % (self.parameters.beam_parameters.photon_energy_spectrum_type.lower()))

        # put MPI and program arguments together
        args = shlex.split(mpicommand) + command_sequence
        #args =  command_sequence
        command = " ".join(args)

        print command

        if 'SIMEX_VERBOSE' in os.environ:
            if 'MPI' in  os.environ['SIMEX_VERBOSE']:
                print("CrystFELPhotonDiffractor backengine mpicommand: "+mpicommand)

        # Run the backengine command.
        proc = subprocess.Popen(command, shell=True)
        proc.wait()

        # Return the return code from the backengine.
        return proc.returncode

    @property
    def data(self):
        """ Query for the field data. """
        return self.__data

    def _readH5(self):
        """ """
        """ Private method for reading the hdf5 input and extracting the parameters and data relevant to initialize the object. """
        pass

    def saveH5(self):
        """
        Method to save the object to a file. Creates links to h5 files that all contain only one pattern.
        """

        # Path where individual h5 files are located.
        path_to_files = self.output_path

        _rename_files(path_to_files)

        return

        # Setup new file.
        h5_outfile = h5py.File( self.output_path + ".h5" , "w")

        # Files to read from.
        individual_files = [os.path.join( path_to_files, f ) for f in os.listdir( path_to_files ) ]
        individual_files.sort()

        # First rename.
        # Keep track of global parameters being linked.
        global_parameters = False
        # Loop over all individual files and link in the top level groups.
        for ind_file in individual_files:
            # Open file.
            h5_infile = h5py.File( ind_file, 'r')

            # Get file ID.
            file_ID = os.path.split(ind_file)[-1].split(".h5")[0].split("_")[-1]

            # Links must be relative.
            relative_link_target = os.path.relpath(path=ind_file, start=os.path.dirname(os.path.dirname(ind_file)))

            # Link global parameters.
            if not global_parameters:
                global_parameters = True

                h5_outfile["params"] = h5py.ExternalLink(relative_link_target, "params")
                h5_outfile["info"] = h5py.ExternalLink(relative_link_target, "info")
                h5_outfile["misc"] = h5py.ExternalLink(relative_link_target, "misc")
                h5_outfile["version"] = h5py.ExternalLink(relative_link_target, "version")

            for key in h5_infile['data']:

                # Link in the data.
                ds_path = "data/%s" % (key)
                h5_outfile[ds_path] = h5py.ExternalLink(relative_link_target, ds_path)

            # Close input file.
            h5_infile.close()

        # Close file.
        h5_outfile.close()

        # Reset output path.
        self.output_path = self.output_path+".h5"




def _rename_files(path):
    """ Renames all files generated by pattern_sim to simex conform filenames."""

    old_wd = os.getcwd()
    os.chdir( path )
    original_files = os.listdir(".")

    original_files.sort()

    for i,f in enumerate(original_files):
        if not f.split(".")[-1] == "h5":
            continue

        new_filename = "%s_%07d.h5" % ("".join(f.split("-")[:-1]),i+1)
        print "Renaming %s to %s." % (f, new_filename)
        os.rename(f, new_filename)

    os.chdir( old_wd )
