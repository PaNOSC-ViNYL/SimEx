""":module S2EReconstruction: Module that holds the S2EReconstruction class.  """
##########################################################################
#                                                                        #
# Copyright (C) 2015-2020 Carsten Fortmann-Grote                         #
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

from SimEx.Calculators.DMPhasing import DMPhasing
from SimEx.Calculators.EMCOrientation import EMCOrientation
from SimEx.Calculators.AbstractPhotonAnalyzer import AbstractPhotonAnalyzer


class S2EReconstruction(AbstractPhotonAnalyzer):
    """
    :class S2EReconstruction: Class representing photon data analysis for electron density reconstruction from 2D diffraction patterns.
    Wraps the EMC orientation module and the DM phasing module.
    """

    def __init__(self,  parameters=None, input_path=None, output_path=None):
        """

        :param parameters: The parameters for the reconstruction.
        :type parameters: dict
        :example parameters: parameters={'EMC_Parameters' : EMCOrientationParameters(), 'DM_Parameters' : DMPhasingParameters()} # Use default parameters for EMC and DM.

        :param input_path: Path for input data.
        :type input_path: str

        :param output_path: Path where to write output to.
        :type output_path: str
        """

        # Initialize base class.
        super(S2EReconstruction, self).__init__(parameters,input_path,output_path)

        self.__provided_data = ['/data/electronDensity',
                                '/params/info',
                                '/history',
                                '/info',
                                '/misc',
                                '/version',
                                ]

        self.__expected_data = [
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

        emc_parameters = None
        dm_parameters = None

        # Construct emc and dm calculators.
        if self.parameters != {}:
            emc_parameters = self.parameters['EMC_Parameters']
            dm_parameters = self.parameters['DM_Parameters']

        if os.path.isdir( self.output_path ):
            intermediate_output_path = os.path.join( self.output_path, 'orient_out.h5' )
        else:
            intermediate_output_path  = 'orient_out.h5'

        self.__emc = EMCOrientation(emc_parameters, self.input_path, intermediate_output_path )
        self.__dm = DMPhasing(dm_parameters, intermediate_output_path, self.output_path)

    def expectedData(self):
        """ Query for the data expected by the Analyzer. """
        return self.__expected_data

    def providedData(self):
        """ Query for the data provided by the Analyzer. """
        return self.__provided_data

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
        Private method to save the object to a file.

        :param output_path: The file where to save the object's data.
        :type output_path: str
        """
        pass # No action required since output is written in backengine.

    def backengine(self):
        """ Run the EMC and DM backengine executables. """

        # Run EMC.
        emc_status = self.__emc.backengine()

        # If EMC was not successful, return with error code.
        if  emc_status!= 0:
            return emc_status

        # Else run DM.
        return self.__dm.backengine()

