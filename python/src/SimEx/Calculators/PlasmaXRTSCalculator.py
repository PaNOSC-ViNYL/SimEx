##########################################################################
#                                                                        #
# Copyright (C) 2015 Carsten Fortmann-Grote                              #
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

""" Module that holds the PlasmaXRTSCalculator class.

    @author : CFG
    @institution : XFEL
    @creation 20151104

"""
import os
import numpy
import inspect
import tempfile
import subprocess
from SimEx.Calculators.AbstractPhotonDiffractor import AbstractPhotonDiffractor
from SimEx.Utilities.EntityChecks import checkAndSetInstance, checkAndSetPositiveInteger

from SimEx.Parameters.AbstractCalculatorParameters import AbstractCalculatorParameters
from SimEx.Utilities import prepHDF5

class PlasmaXRTSCalculator(AbstractPhotonDiffractor):
    """
    Class representing a x-ray free electron laser photon propagator.
    """

    def __init__(self,  parameters=None, input_path=None, output_path=None):
        """
        Constructor for the PlasmaXRTSCalculator.

        @param parameters : Parameters for the PlasmaXRTSCalculator.
        @type : dict
        @default : None
        """

        # Check parameters.
        parameters = checkAndSetParameters( parameters )

        # Init base class.
        super( PlasmaXRTSCalculator, self).__init__(parameters, input_path, output_path)

        # Set state to not-initialized (e.g. input deck is not written).
        self.__is_initialized = False

    def expectedData(self):
        """ Query for the data expected by the Diffractor. """
        return self.__expected_data

    def providedData(self):
        """ Query for the data provided by the Diffractor. """
        return self.__provided_data

    def backengine(self):
        """ This method drives the backengine xrts."""

        #if not self.__is_initialized:
            #self._initialize()

        command_sequence = ['xrs']
        process = subprocess.Popen(command_sequence)
        process.wait()

    @property
    def data(self):
        """ Query for the field data. """
        return self.__data

    def _readH5(self):
        """ """
        """ Private method for reading the hdf5 input and extracting the parameters and data relevant to initialize the object. """
        raise( RuntimeError, "Not implemented.")

    def saveH5(self):
        """ """
        """
        Private method to save the object to a file.

        @param output_path : The file where to save the object's data.
        @type : string
        @default : None
        """
        raise( RuntimeError, "Not implemented.")


###########################
# Check and set functions #
###########################
def checkAndSetParameters( parameters ):
    """ Utility to check if the parameters dictionary is ok . """

    if not isinstance( parameters, AbstractCalculatorParameters ):
        raise RuntimeError( "The 'parameters' argument must be of the type PlasmaXRTSCalculatorParameters.")
    return parameters
