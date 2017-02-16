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

""" Module that holds the GenesisPhotonSource class.

    @author : CFG
    @institution : XFEL
    @creation 20170215

"""
import h5py
import numpy
import os
import shutil
import subprocess

from scipy.constants import m_e, c

from SimEx.Calculators.AbstractPhotonSource import AbstractPhotonSource

from ScriptCollection.Prototypes.pic2genesis.pic2genesis import pic2genesis

#from ocelot.test.workshop import 5_Genesis_preprocessor as GenPre


class GenesisPhotonSource(AbstractPhotonSource):
    """
    Class representing a x-ray free electron laser photon source using the Genesis backengine.
    """

    def __init__(self,  parameters=None, input_path=None, output_path=None):
        """
        Constructor for the genesis photon source.

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

        # Setup header for distribution file.
        comments = "? "
        size = self.__input_data.shape[0]
        header = "VERSION = 1.0\nSIZE = %d\nCHARGE = %7.6E\nCOLUMNS X XPRIME Y YPRIME T P" % (size, self.__charge)

        numpy.savetxt( fname='beam.dist', X=self.__input_data, header=header, comments=comments)

    def backengine(self):

        self._prepareGenesisRun()

        command_sequence = 'genesis < beam.dist'

        # Run the backengine command.
        proc = subprocess.Popen(command_sequence, shell=True)
        proc.wait()

        # FIXME
        self.__data = None


    @property
    def data(self):
        """ Query for the field data. """
        return self.__data

    def _readH5(self):
        """ """
        self.__input_data, self.__charge = pic2genesis( self.input_path )
        return

        ### TODO: Support beam file/ dist file input.
        #self.__input_data = numpy.loadtxt( self.__input_path )


    def saveH5(self):
        """ """
        pass
