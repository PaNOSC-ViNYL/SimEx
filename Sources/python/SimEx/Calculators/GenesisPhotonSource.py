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
            
            # Convert to xprime, yprime.
            xprime = numpy.arctan(px/py)
            zprime = numpy.arctan(pz/py)            
            
            # Calculate particle charge.
            charge_group = h5_handle['/data/%d/particles/e/charge/' %(timestep)]
    
            charge_value = charge_group.attrs['value']
            charge_unit = charge_group.attrs['unitSI']
            charge = charge_value * charge_unit # 1e in As
            
            # Get number of particles and total charge.
            particle_patches = h5_handle['/data/%d/particles/e/particlePatches/numParticles' %(timestep)].value
            total_number_of_electrons = numpy.sum( particle_patches )
            total_charge = total_number_of_electrons * charge
    
            # Calculate momentum
            psquare = px**2 + py**2 + pz**2
            #gamma = numpy.sqrt( 1. + psquare/((m_e*c)**2))
            P = numpy.sqrt(psquare/((m_e*c)**2))
            
            # Store on object.
            self.__input_data = numpy.vstack([ x, xprime, z, zprime, y/c, P]).transpose()
            self.__charge = total_charge

            return

        ### TODO: Support beam file/ dist file input.
        #self.__input_data = numpy.loadtxt( self.__input_path )


    def saveH5(self):
        """ """
        pass
