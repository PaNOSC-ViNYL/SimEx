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

    def backengine(self):

        numpy.savetxt( 'beam.dat', self.__input_data)

        command_sequence = 'genesis < beam.dat'

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

        # Check if input is native or openPMD.
        with h5py.File( self.input_path, 'r' ) as h5_handle:

            timestep = h5_handle['data'].keys()[-1]

            h5_positions = '/data/%s/particles/e/position/' % (timestep)
            h5_momenta = '/data/%s/particles/e/momentum/' % (timestep)

            x_data = h5_handle[h5_positions]['x'].value
            x_data_unit = h5_handle[h5_positions]['x'].attrs['unitSI']
            x = x_data*x_data_unit

            y_data = h5_handle[h5_positions]['y'].value
            y_data_unit = h5_handle[h5_positions]['y'].attrs['unitSI']
            y = y_data*y_data_unit

            z_data = h5_handle[h5_positions]['z'].value
            z_data_unit = h5_handle[h5_positions]['z'].attrs['unitSI']
            z = z_data*z_data_unit

            px_data = h5_handle[h5_momenta]['x'].value
            px_data_unit = h5_handle[h5_momenta]['x'].attrs['unitSI']
            px = px_data*px_data_unit

            py_data = h5_handle[h5_momenta]['y'].value
            py_data_unit = h5_handle[h5_momenta]['y'].attrs['unitSI']
            py = py_data*py_data_unit

            pz_data = h5_handle[h5_momenta]['z'].value
            pz_data_unit = h5_handle[h5_momenta]['z'].attrs['unitSI']
            pz = pz_data*pz_data_unit

            psquare = px**2 + py**2 + pz**2
            gamma = numpy.sqrt( 1. + psquare/((m_e*c)**2))

            self.__input_data = numpy.vstack([ x, px, z, pz, y, gamma]).transpose()

            return

        # Reach here only in case the file is a native beam file.
        self.__input_data = numpy.loadtxt( self.__input_path )


    def saveH5(self):
        """ """
        pass
