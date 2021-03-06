""":module XFELPhotonSource: Module that holds the XFELPhotonSource class.  """
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
import shutil

from SimEx.Calculators.AbstractPhotonSource import AbstractPhotonSource

class XFELPhotonSource(AbstractPhotonSource):
    """
    :class XFELPhotonSource: Class representing a x-ray free electron laser photon source.
    """

    def __init__(self, parameters=None, input_path=None, output_path=None):
        """

        :param parameters : Photon source parameters.
        :type parameters: dict

        :param input_path: The path to the input data for the photon source.
        :type input_path:  str, default FELsource_in.h5

        :param output_path: The path where to save output data.
        :type output: str, default FELsource_out.h5
        """

        # Initialize base class.
        super(XFELPhotonSource, self).__init__(parameters, input_path, output_path)

    def backengine(self):
        # Copy input to output.
        # Check if input_path is a directory.
        if os.path.isdir(self.input_path):
            # Make directory target if not existing already.
            if not os.path.isdir(self.output_path):
                os.mkdir( self.output_path )
            # Copy files.
            files_to_copy = [os.path.join(self.input_path, ff) for ff in os.listdir(self.input_path) if 'FELsource_out' in ff and ff.split('.')[-1] == 'h5']
            for f in files_to_copy:
                shutil.copy( f, self.output_path )

        # If input is a single file, just copy it to output.
        else:
            shutil.copy( self.input_path, self.output_path )

    @property
    def data(self):
        """ Query for the field data. """
        return self.__data

    def _readH5(self):
        """ """
        pass

    def saveH5(self):
        """ """
        pass
