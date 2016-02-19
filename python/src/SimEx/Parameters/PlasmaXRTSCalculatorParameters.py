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

""" Module that holds the PlasmaXRTSCalculatorParameters class.

    @author : CFG
    @institution : XFEL
    @creation 20151104

"""
import os
import numpy
import inspect
import tempfile
import subprocess
from SimEx.CalculatorParameterss.AbstractPhotonDiffractor import AbstractPhotonDiffractor
from SimEx.Utilities.EntityChecks import checkAndSetInstance, checkAndSetPositiveInteger


from SimEx.Utilities import prepHDF5

class PlasmaXRTSCalculatorParameters(AbstractPhotonDiffractor):
    """
    Class representing a x-ray free electron laser photon propagator.
    """

    def __init__(self,  parameters=None, input_path=None, output_path=None):
        """
        Constructor for the PlasmaXRTSCalculatorParameters.

        @param parameters : Parameters for the PlasmaXRTSCalculatorParameters.
        @type : dict
        @default : None
        """

        # Check parameters.
        parameters = checkAndSetParameters( parameters )

        # Init base class.
        super( PlasmaXRTSCalculatorParameters, self).__init__(parameters, input_path, output_path)

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

    def _initialize(self):
        """ Initialize all parameters and io slots needed by the backengine. """

        # Make a temporary directory.
        self.__tmp_dir = tempfile.mkdtemp(prefix='xrs_')

        # Write the input file.
        input_deck_path = os.path.join( self.__tmp_dir, 'input.dat' )
        with open(input_deck_path, 'w') as input_deck:
            input_deck.write('--XRTS---input_file-----------------------------------\n')
            input_deck.write('--\n')
            input_deck.write('--fit_parameters------------------------------flag----\n')
            input_deck.write('DO_FIT 				0\n')
            input_deck.write('PHOTON_ENERGY %4.3f\n' % (self._input_data['photon_energy']))
            input_deck.write('SCATTERING_ANGLE 	%4.3f\n' % (self.parameters['scattering_angle']))
            input_deck.write('ELECTRON_TEMP 	%4.3f 0\n' % (self._input_data['electron_temperature']) )
            input_deck.write('ELECTRON_DENSITY 	%4.3e 0\n' % (self._input_data['electron_density']))
            input_deck.write('AMPLITUDE 		1.0 		0\n')
            input_deck.write('BASELINE 			0.0 		0\n')
            input_deck.write('Z_FREE 			%4.3f		0\n' % (self._input_data['average_ion_charge']) )
            input_deck.write('OUT(1=XSEC,2=PWR)	2\n')
            input_deck.write('--model_for_total_spec---------use-flag--------------\n')
            input_deck.write('USE_RPA %d\n' % (self._input_data['use_rpa']))
            input_deck.write('USE_LINDHARD %d\n' % (self._input_data['use_lindhard']))
            input_deck.write('USE_TSYTOVICH %d\n' % (self._input_data['use_tsytovich']))
            input_deck.write('USE_STATIC_LFC %d\n' % (self._input_data['use_static_lfc']))
            input_deck.write('USE_DYNAMIC_LFC %d\n' % (self._input_data['use_dynamic_lfc']))
            input_deck.write('USE_MFF %d\n' % (self._input_data['use_mff']))
            input_deck.write('USE_BMA %d\n' % (self._input_data['use_bma']))
            input_deck.write('USE_BMA+sLFC \n' % (self._input_data['use_bma_slfc']))
            input_deck.write('USE_CORE 1\n')
            input_deck.write('--gradients------------------------------------------\n')
            input_deck.write('GRAD 0\n')
            input_deck.write('L_GRADIENT			0.0e-0		\n')
            input_deck.write('T_GRADIENT			0.0\n')
            input_deck.write('DSTEP				0.0	\n')
            input_deck.write('--ion_parameters----------------------------use_flag-\n')
            input_deck.write('ION_TEMP %d 1\n' % (self._input_data['ion_temperature']))
            input_deck.write('S_ION_FEATURE %4.3f %d\n' % (self._input_data['ion_feature'], self._input_data['use_ion_feature']))
            input_deck.write('DEBYE_TEMP %4.3f %d\n' % (self._input_data['debye_temperature'], self._input_data['use_debye_temperature']))
            input_deck.write('BAND_GAP %4.3f %d\n' % (self._input_data['band_gap'], self._input_data['use_band_gap']))

            input_deck.write('--integration----------------------------------------\n')
            input_deck.write('N_DAWSON 32\n')
            input_deck.write('N_DISTRIBUTION 32\n')
            input_deck.write('N_PVI 32\n')
            input_deck.write('N_LANDEN 512\n')
            input_deck.write('N_RELAXATION 1024\n')
            input_deck.write('N_FFT 4096\n')
            input_deck.write('EPS 1.0E-4\n')
            input_deck.write('--See(k,w)------------------------------use/norm-----\n')
            input_deck.write('STATIC_MODEL(DH,OCP,SOCP,SOCPN) %s\n' % (self.parameters['model_Sii']))
            input_deck.write('USE_ADV_MIX %d\n' % (self._input_data['use_adv_mix']))
            input_deck.write('USE_IRS_MODEL 					0\n')
            input_deck.write('HARD_SPHERE_DIAM 				1E-10 0\n')
            input_deck.write('POLARIZABILITY 					0.0 0.0\n')
            input_deck.write('BOUND-FREE_MODEL(IA,IBA,FFA) 	FFA\n')
            input_deck.write('BOUND-FREE_NORM(FK,NO,USR) 		NO 	0\n')
            input_deck.write('BOUND-FREE_MEFF					1.0\n')
            input_deck.write('USE_BOUND-FREE_DOPPLER          0\n')
            input_deck.write('CONT-LOWR_MODEL(SP,EK,USR) 		SP 1\n')
            input_deck.write('GK 								1.5 0\n')
            input_deck.write('RPA 							0 0\n')
            input_deck.write('LINDHARD 						0 0\n')
            input_deck.write('SALPETER 						0 0\n')
            input_deck.write('LANDEN 							0 0\n')
            input_deck.write('RPA_TSYTOVICH 					0 0\n')
            input_deck.write('STATIC_LFC 						0 0\n')
            input_deck.write('DYNAMIC_LFC 					0 0\n')
            input_deck.write('MFF 							0 0\n')
            input_deck.write('BMA(+sLFC) 						0 0\n')
            input_deck.write('CORE 							1 0\n')
            input_deck.write('TOTAL 							0 0\n')
            input_deck.write('E_MIN 							-100\n')
            input_deck.write('E_MAX 							100\n')
            input_deck.write('E_STEP 							0.10\n')
            input_deck.write('--target_spec--------------------------chem----Zfree--\n')
            input_deck.write('NUMBER_OF_SPECIES 1\n')
            input_deck.write('TARGET_1 H 1 -1\n')
            input_deck.write('MASS_DENSITY 0.8\n')
            input_deck.write('NE_ZF_LOCK 0\n')
            input_deck.write('DATA_FILE 35082_s2_h.txt\n')
            input_deck.write('NUMBER_POINTS 320\n')
            input_deck.write('OPACITY_FILE nofile 0\n')
            input_deck.write('--instrument_function---------------------------------\n')
            input_deck.write('USE_FILE 0\n')
            input_deck.write('FILE_NAME newsource_68632.dat\n')
            input_deck.write('INST_MODEL GAUSSIAN\n')
            input_deck.write('INST_FWHM 5.0\n')
            input_deck.write('BIN_PER_PIXEL 1.0\n')
            input_deck.write('INST_INDEX 2.0\n')
            input_deck.write('--additional_parameters-------------------------------\n')
            input_deck.write('MAX_ITERATIONS 0\n')
            input_deck.write('LEVENBERG_MARQUARDT 0\n')
            input_deck.write('SIGMA_LM 1.0\n')
            input_deck.write('SAVE_FILE out3.txt\n')


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
