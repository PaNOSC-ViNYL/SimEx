""":module GenesisPhotonSource: Module that holds the GenesisPhotonSource class."""
##########################################################################
#                                                                        #
# Copyright (C) 2017-2018 Carsten Fortmann-Grote                         #
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

import numpy
import os
import subprocess
from ocelot.adaptors import genesis

from SimEx.Calculators.AbstractPhotonSource import AbstractPhotonSource
from SimEx.Utilities.IOUtilities import pic2dist

class GenesisPhotonSource(AbstractPhotonSource):
    """
    :class GenesisPhotonSource: Representing a x-ray free electron laser photon source using the Genesis backengine.
    """

    def __init__(self,  parameters=None, input_path=None, output_path=None):
        """

        :param parameters : Photon source parameters.
        :type parameters: dict

        :param input_path: The path to the input data for the photon source.
        :type input_path:  str
        :note input_path: Accepts a native genesis beam file or openPMD conform hdf5.

        :param output_path: The path where to save output data.
        :type output: str, default FELsource_out.h5
        """

        # Initialize base class.
        super(GenesisPhotonSource, self).__init__(parameters, input_path, output_path)

    def _prepareGenesisRun(self):
        """ """
        """ Private method to setup the genesis run. """

        # Setup empty distribution.
        edist = genesis.GenesisElectronDist()

        # Fill in the data. Reverse time axis.
        edist.x  = numpy.flipud(self.__input_data[:,0])
        edist.xp = numpy.flipud(self.__input_data[:,1])
        edist.y  = numpy.flipud(self.__input_data[:,2])
        edist.yp = numpy.flipud(self.__input_data[:,3])
        edist.t  = numpy.flipud(self.__input_data[:,4])
        edist.g  = numpy.flipud(self.__input_data[:,5])
        edist.part_charge = self.__charge / edist.len()

        # Produce a genesis beam
        self.__genesis_beam = genesis.edist2beam(edist, step=self.parameters['time_averaging_window'])

        # Generate genesis input with defaults and guesses from beam peak parameters.
        genesis_input = genesis.generate_input( undulator = self.parameters['undulator_parameters'],
                                                       beam=genesis.get_beam_peak(self.__genesis_beam),
                                                       itdp=self.parameters['is_time_dependent'] )

        # Merge guessed and external input.
        if hasattr(self, '_GenesisPhotonSource__genesis_input') and self.__genesis_input is not None:
            for key,value in list(self.__genesis_input.__dict__.items()):
                if value != 0.0:
                    setattr(genesis_input, key, value)

        genesis_input.exp_dir = genesis_input.run_dir = self.output_path
        # Store merged genesis input.
        self.__genesis_input = genesis_input

        # Set beam to actual beam, not the peak parameters.
        self.__genesis_input.beam = self.__genesis_beam

        # Call "run_genesis" to setup run directories, which also issues the launcher.launch() command, which, naturall, fails here.
        try:
            genesis.run_genesis( self.__genesis_input, launcher=None, debug=0)
        except AttributeError:
            pass
        except:
            raise

    def backengine(self):

        # Setup genesis backengine.
        self._prepareGenesisRun()

        command_sequence = 'genesis < tmp.cmd'

        # Run the backengine command.
        oldpwd = os.getcwd()
        os.chdir(self.output_path)
        proc = subprocess.Popen(command_sequence, shell=True)
        proc.wait()
        os.chdir(oldpwd)

        # FIXME
        self.__data = None


    @property
    def data(self):
        """ Query for the field data. """
        return self.__data

    def _readH5(self):
        """ """
        self.__input_data, self.__charge = pic2dist( self.input_path, 'genesis' )
        return

    def saveH5(self):
        """ """
        pass
