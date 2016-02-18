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
import subprocess
from SimEx.Calculators.AbstractPhotonDiffractor import AbstractPhotonDiffractor
from SimEx.Utilities.EntityChecks import checkAndSetInstance, checkAndSetPositiveInteger


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

    def expectedData(self):
        """ Query for the data expected by the Diffractor. """
        return self.__expected_data

    def providedData(self):
        """ Query for the data provided by the Diffractor. """
        return self.__provided_data

    def backengine(self):
        """ This method drives the backengine singFEL."""
        raise( RuntimeError, "Not implemented.")

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
def checkAndSetScatteringAngle(angle):
    """
    Utility to check if the scattering angle is in the correct range.
    @param angle : The angle to check.
    @return The checked angle.
    @raise ValueError if not 0 <= angle <= 180
    """

    # Set default.
    if angle is None:
        angle = 0.0

    # Check if in range.
    if angle < 0.0 or angle > 180.0:
        raise( ValueError, "Scattering angle must be between 0 and 180 [degrees].")

    # Return.
    return angle

def checkAndSetPhotonEnergyRange(photon_energy_range):
    """
    Utility to check if the photon energy range is ok.
    @param photon_energy_range : The range to check.
    @type numpy.ndarray or list of doubles.
    @return The checked photon energy range.
    @raise ValueError if not of correct shape.
    """

    if photon_energy_range is None:
        photon_energy_range = numpy.arange( -100. ,100., 1.0 )
    if not ( isinstance( photon_energy_range, numpy.ndarray) or isinstance( photon_energy_range, list) ):
        raise TypeError( "The photon energy range must be a numpy array or list of doubles specifying the range of photon energy shifts (in units of eV) with respect to the probe photon energy to calculate.")

    # Return
    return photon_energy_range

def checkAndSetModelSii( model ):
    """
    Utility to check if the model is a valid model for the Rayleigh (quasistatic) scattering feature.

    @param model : The model to check.
    @type : str
    @return : The checked model
    @raise ValueError if not a string or not a valid Sii model ('RPA', 'DH',
    """

    if model is None:
        model = 'DH'

    ###TODO: Complete
    valid_models = ['RPA',
                    'DH',
                    ]
    if not isinstance( model, str ):
        raise TypeError( "The Sii model must be a string.")

    if model not in valid_models:
        raise ValueError( "The Sii model must be a valid Sii model. Valid Sii models are %s." % (str(valid_models)) )

    # Return
    return model


def checkAndSetModelSee0( model ):
    """
    Utility to check if the model is a valid model for the high frequency (dynamic) feature.

    @param model : The model to check.
    @type : str
    @return : The checked model
    @raise ValueError if not a string or not a valid See0 model ('RPA', 'BMA', 'BMA+sLFC', 'BMA+dLFC', 'LFC', 'Landen')
    """

    if model is None:
        model = 'RPA'

    ###TODO: Complete
    valid_models = ['RPA',
                    'BMA',
                    'BMA+sLFC',
                    'BMA+dLFC',
                    'LFC',
                    'Landen',
                    ]
    if not isinstance( model, str ):
        raise TypeError( "The See0 model must be a string.")

    if model not in valid_models:
        raise ValueError( "The See0 model must be a valid See0 model. Valid See0 models are %s." % (str(valid_models)) )

    # Return
    return model

def checkAndSetModelSbf( model ):
    """
    Utility to check if the model is a valid model for the bound-free (Compton) scattering feature.

    @param model : The model to check.
    @type : str
    @return : The checked model
    @raise ValueError if not a string or not a valid Sbf model ('IA', 'HWF')
    """

    if model is None:
        model = 'IA'

    ###TODO: Complete
    valid_models = ['IA',
                    'HWF',
                    ]
    if not isinstance( model, str ):
        raise TypeError( "The Sbf model must be a string.")

    if model not in valid_models:
        raise ValueError( "The Sbf model must be a valid Sbf model. Valid Sbf models are %s." % (str(valid_models)) )

    # Return
    return model

def checkAndSetParameters( parameters ):
    """ Utility to check if the parameters dictionary is ok . """

    if parameters is None:
        parameters = {}
    # Get keys from the dict.
    present_keys = parameters.keys()

    # The list of keys that will be needed.
    expected_keys = ['scattering_angle',
                     'photon_energy_range',
                     'model_Sii',
                     'model_See0',
                     'model_Sbf',
                     ]

    # Check for missing keys and set value to None if not present.
    for expected_key in expected_keys:
        if expected_key not in present_keys:
            parameters[expected_key] = None

    # Now check individual parameters.
    parameters['scattering_angle']    = checkAndSetScatteringAngle( parameters['scattering_angle'] )
    parameters['photon_energy_range'] = checkAndSetPhotonEnergyRange( parameters['photon_energy_range'] )
    parameters['model_Sii']           = checkAndSetModelSii(  parameters['model_Sii'] )
    parameters['model_See0']          = checkAndSetModelSee0( parameters['model_See0'] )
    parameters['model_Sbf']           = checkAndSetModelSbf(  parameters['model_Sbf'] )

    return parameters
