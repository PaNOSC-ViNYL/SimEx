##########################################################################
#                                                                        #
# Copyright (C) 2015, 2016 Carsten Fortmann-Grote                        #
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

""" Module that holds the WavePropagator class.

    :author: CFG
    :institution: XFEL
    :creation: 20160321

"""
from wpg import Beamline, Wavefront
from wpg.srwlib import srwl
import h5py
import os

from SimEx.Calculators.AbstractPhotonPropagator import AbstractPhotonPropagator
from SimEx.Parameters.WavePropagatorParameters import WavePropagatorParameters
from SimEx.Utilities.EntityChecks import checkAndSetInstance
from SimEx.Utilities import wpg_to_opmd


class WavePropagator(AbstractPhotonPropagator):
    """
    Class representing a photon propagator using wave optics through WPG.
    """

    def __init__(self,  parameters=None, input_path=None, output_path=None):
        """
        Constructor for the xfel photon propagator.

        :param parameters: Parameters steering the propagation of photons.
        :type parameters: WavePropagatorParameters instance

        :param input_path: Location of input data for the photon propagation.
        :type input_path: str

        :param output_path: Location of output data for the photon propagation.
        :type output_path: str
        """

        # DCheck (and set) parameters.
        parameters = checkAndSetInstance(WavePropagatorParameters, parameters, WavePropagatorParameters() )

        # Initialize base class.
        super(WavePropagator, self).__init__(parameters,input_path,output_path)


    def backengine(self):
        """ This method drives the backengine code, in this case the WPG interface to SRW.

        :return: 0 if WPG run was successful, 1 if not.

        """

        # Switch to frequency representation.
        srwl.SetRepresElecField(self.__wavefront._srwl_wf, 'f') # <---- switch to frequency domain

        # Propagate through beamline.
        self.parameters.beamline.propagate(self.__wavefront)

        # Switch back to time representation.
        srwl.SetRepresElecField(self.__wavefront._srwl_wf, 't')

        return 0

    @property
    def data(self):
        """ Query for the field data.

        :return: The WPG wavefront data.

        """
        return self.__data

    def _readH5(self):
        """ """
        """ Private method for reading the hdf5 input and extracting the parameters and data relevant to initialize the object. """
        # Check input.
        try:
            self.__h5 = h5py.File( self.input_path, 'r' )
        except:
            raise IOError( 'The input_path argument (%s) is not a path to a valid hdf5 file.' % (self.input_path) )

        # Construct wpg wavefront based on input data.
        self.__wavefront = Wavefront()
        self.__wavefront.load_hdf5(self.input_path)

    def saveH5(self):
        """
        Method to save the object to a file.

        :param output_path:   The file where to save the wavefront data.
        :type output_path:    str, default 'prop_out.h5'

        """

        # Write data to hdf file using wpg interface function.
        self.__wavefront.store_hdf5(self.output_path)

        # Write openPMD file if requested.
        if self.parameters.use_opmd:
            wpg_to_opmd.convertToOPMD( self.output_path )

