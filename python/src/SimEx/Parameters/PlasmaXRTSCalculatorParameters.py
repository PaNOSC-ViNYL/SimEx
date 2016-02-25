##########################################################################
#                                                                        #
# Copyright (C) 2016 Carsten Fortmann-Grote                              #
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
    @creation 20160219

"""
import os
import copy
import numpy
import math
import tempfile
from scipy.constants import physical_constants
from scipy.constants import Avogadro

from SimEx.Parameters.AbstractCalculatorParameters import AbstractCalculatorParameters
from SimEx.Utilities.Utilities import ALL_ELEMENTS
from SimEx.Utilities.EntityChecks import checkAndSetInstance
from SimEx.Utilities.EntityChecks import checkAndSetInteger
from SimEx.Utilities.EntityChecks import checkAndSetPositiveInteger
from SimEx.Utilities.EntityChecks import checkAndSetNonNegativeInteger


BOOL_TO_INT = {True : 1, False : 0}

class PlasmaXRTSCalculatorParameters(AbstractCalculatorParameters):
    """
    Class representing parameters for the plasma x-ray Thomson scattering calculator.
    """

    def __init__(self,
                 elements=None,
                 photon_energy=None,
                 scattering_angle=None,
                 electron_temperature=None,
                 electron_density=None,
                 ion_temperature=None,
                 ion_charge=None,
                 mass_density=None,
                 debye_temperature=None,
                 band_gap=None,
                 energy_range=None,
                 model_Sii=None,
                 model_See=None,
                 model_Sbf=None,
                 model_IPL=None,
                 model_Mix=None,
                 lfc=None,
                 Sbf_norm=None
                 ):

        """
        Constructor for the PlasmaXRTSCalculatorParameters.

        @params elements: The chemical elements in the scattering target.
        @type: List of [[element symbol, stochiometric number, charge], ...]
        @default: None
        @example: [['B', 1, 2], ['N', 1, 2]] for Boron-Nitride with both B and N two fold ionized (ion average).
        @example: [['C', 1, 4], ['H', 1, -1]] for Plastic with both four-fold ionized C and ionization of H calculated so that the given average ion charge comes out correct.

        @param photon_energy : The central energy of incoming x-ray photons.
        @type : float
        @default : None

        @params scattering_angle: The scattering angle.
        @type: double
        @default: None

        @params electron_temperature: The temperature of the electron subsystems (units of eV).
        @type: double
        @default: None

        @params electron_density: The electron number density (units of 1/m^3)
        @type: double
        @default: None

        @params ion_temperature: The temperature of the ion subsystem (units of eV).
        @type: double
        @default: None

        @params ion_charge: The average ion charge (units of elementary charge e).
        @type: double
        @default: None

        @params mass_density: The mass density of the target (units of g/cm^3).
        @type: double
        @default: None

        @params debye_temperature: The Debye temperature (units of eV).
        @type: double
        @default: 0.0

        @params band_gap: The band gap of the target (units of eV).
        @type: double
        @default: 0.0

        @params energy_range: The energy range over which to calculate the scattering spectrum.
        @type: dict
        @default: [-10*wpl, 10*wpl, 0.1*wpl], wpl = electron plasma frequency.
        @example: {'min' : -100.0, 'max' : 100, 'step' : 0.5}



        @params model_Sii: The model to use for the ion-ion structure factor.
        @type: string or double
        @default: SOCP
        @example: model_Sii='DH' for the Debye-Hueckel structure factor.
        @example: model_Sii=1.5 to use a fixed value of Sii=1.5
        @note: Supported models are 'DH' (Debye-Hueckel), 'OCP' (one component plasma), 'SOCP' (screened one component plasma), 'SOCPN' (SOCP with negative screening Fourier component). Values >=0.0 are also allowed.


        @params model_See: The model of the dynamic (high frequency) part of the electron-electron structure factor.
        @type: string
        @default: RPA
        @note: Supported models are: 'RPA' (random phase approximation), 'BMA' (Mermin approximation with Born collision frequency), 'BMA+sLFC' (BMA with static local field correction).

        @params model_Sbf: The model for the
        @type: string
        @default: 'IA' (impulse approximation).
        @note: Supported are 'IA' (impulse approximation), 'FA' (form factor approximation).

        @params model_IPL: Model for ionization potential lowering.
        @type: string or double
        @default: SP (Stewart-Pyatt)
        @note: Supported are 'SP' (Stewart-Pyatt) and 'EK' (Eckard-Kroll). If a numeric value is given, this is interpreted as the ionization potential difference (lowering) in eV.

        @params model_Mix: The model to use for mixing (of species).
        @type: string
        @default: None

        @params lfc:  The local field correction to use.
        @type: double
        @default: 0.0 (calculate).

        @params Sbf_norm: How to normalize the bound-free structure factor.
        @type: string or double
        @default: None
        """

        # Check and set all parameters.
        self.__elements             = checkAndSetElements(elements)
        self.__photon_energy        = checkAndSetPhotonEnergy(photon_energy)
        self.__scattering_angle     = checkAndSetScatteringAngle(scattering_angle)
        self.__electron_temperature = checkAndSetElectronTemperature(electron_temperature)
        # Set electron density, charge, and mass density depending on which input was given.
        self.__electron_density, self.__ion_charge, self.__mass_density = checkAndSetDensitiesAndCharge(electron_density, ion_charge, mass_density)
        self.__ion_temperature   = checkAndSetIonTemperature(ion_temperature, self.electron_temperature)
        self.__debye_temperature = checkAndSetDebyeTemperature(debye_temperature)
        self.__band_gap          = checkAndSetBandGap(band_gap)
        self.__energy_range      = checkAndSetEnergyRange(energy_range, self.electron_density)
        self.__model_Sii         = checkAndSetModelSii(model_Sii)
        self.__model_See         = checkAndSetModelSee(model_See)
        self.__model_Sbf         = checkAndSetModelSbf(model_Sbf)
        self.__model_IPL         = checkAndSetModelIPL(model_IPL)
        self.__model_Mix         = checkAndSetModelMix(model_Mix)
        self.__lfc               = checkAndSetLFC(lfc)
        self.__Sbf_norm          = checkAndSetSbfNorm(Sbf_norm)

        # Set internal parameters.
        self._setSeeFlags()
        self._setSiiFlags()
        self._setSbfNormFlags()
        self._setDebyeTemperatureFlags()
        self._setBandGapFlags()
        self._setIPLFlags()

        # Set state to not-initialized (e.g. input deck is not written).
        self.__is_initialized = False

    def _setSeeFlags(self):
        """ Set the See parameters as used in the input deck generator. """
        self.__use_rpa         = BOOL_TO_INT[self.model_See == "RPA"]
        self.__use_bma         = BOOL_TO_INT[self.model_See == "BMA"]
        self.__use_bma_slfc    = BOOL_TO_INT[self.model_See == 'BMA+sLFC']
        self.__write_bma = BOOL_TO_INT[self.model_See == 'BMA+sLFC' or self.model_See == 'BMA']
        self.__use_lindhard    = BOOL_TO_INT[self.model_See == 'Lindhard']
        self.__use_static_lfc  = BOOL_TO_INT[self.model_See == 'sLFC']
        self.__use_dynamic_lfc = BOOL_TO_INT[self.model_See == 'dLFC']
        self.__use_mff = BOOL_TO_INT[self.model_See == 'MFF']

    def _setSiiFlags(self):
        """ Set the internal Sii parameters as used in the input deck generator."""
        # By default, switch off usage of user given Sii value.
        self.__Sii_value = 0.0
        self.__use_Sii_value = 0

        # Only if Sii model input parameter is float, use it as Sii(k).
        if isinstance( self.__model_Sii, float):
            self.__use_Sii_value = 1
            # Copy value.
            self.__Sii_value = copy.deepcopy(self.__model_Sii)
            # Reset model parameter but short-cutting the setter.
            self.__model_Sii = 'USR'

    def _setSbfNormFlags(self):
        """ Set the internal Sbf norm flags used in the input deck generator. """

        # By default, switch off usage of user given SbfNorm value.
        self.__Sbf_norm_value = 0.0

        # Only if SbfNorm model input parameter is float, use it as SbfNorm(k).
        if isinstance( self.Sbf_norm, float):
            # Copy value.
            self.__Sbf_norm_value = copy.deepcopy(self.Sbf_norm)
            # Reset model parameter.
            self.__Sbf_norm = 'USR'

    def _setDebyeTemperatureFlags(self):
        """ Set the internal Debye temperature flags used in the input deck generator. """

        # By default, switch off usage of user given Debye temperature.
        self.__use_debye_temperature = 0
        self.__debye_temperature_value = 0.0

        # Only if Debye Temperature is non-zero use it.
        if self.debye_temperature is not None:
            self.__debye_temperature_value = self.__debye_temperature
            self.__use_debye_temperature = 1

    def _setBandGapFlags(self):
        """ Set the internal bandgap flags used in the input deck generator. """

        # By default, switch off usage of band gap.
        self.__use_band_gap = 0
        self.__band_gap_value = 0.0

        # Only if bandgap is non-zero use it.
        if self.band_gap is not None:
            self.__use_band_gap = 1
            self.__band_gap_value = self.__band_gap

    def _setIPLFlags(self):
        """ Set the internal ionization potential lowering flags used in the input deck generator. """

        # By default, switch off usage of band gap.
        self.__ipl_value = 0.0

        # Only if ipl is non-zero use it.
        if isinstance( self.__model_IPL, float ):
            self.__ipl_value = copy.deepcopy(self.__model_IPL)
            self.__model_IPL = 'USR'

    def _serialize(self):
        """ Write the input deck for the xrts backengine. """
        # Make a temporary directory.
        self._tmp_dir = tempfile.mkdtemp(prefix='xrs_')

        # Write the input file.
        input_deck_path = os.path.join( self._tmp_dir, 'input.dat' )
        with open(input_deck_path, 'w') as input_deck:
            input_deck.write('--XRTS---input_file-----------------------------------\n')
            input_deck.write('--\n')
            input_deck.write('--fit_parameters------------------------------flag----\n')
            input_deck.write('DO_FIT                0\n')
            input_deck.write('PHOTON_ENERGY     %4.3f\n' % (self.photon_energy))
            input_deck.write('SCATTERING_ANGLE  %4.3f\n' % (self.scattering_angle) )
            input_deck.write('ELECTRON_TEMP     %4.3f 0\n' % (self.electron_temperature) )
            input_deck.write('ELECTRON_DENSITY  %4.3e 0\n' % (self.electron_density) )
            input_deck.write('AMPLITUDE         1.0   0\n')
            input_deck.write('BASELINE          0.0   0\n')
            input_deck.write('Z_FREE            %4.3f 0\n' % (self.ion_charge) )
            input_deck.write('OUT(1=XSEC,2=PWR)       1\n')
            input_deck.write('--model_for_total_spec---------use-flag--------------\n')
            input_deck.write('USE_RPA %d\n' % (self.__use_rpa) )
            input_deck.write('USE_LINDHARD    %d\n' % (self.__use_lindhard) )
            input_deck.write('USE_TSYTOVICH    0\n' )
            input_deck.write('USE_STATIC_LFC  %d\n' % (self.__use_static_lfc) )
            input_deck.write('USE_DYNAMIC_LFC %d\n' % (self.__use_dynamic_lfc) )
            input_deck.write('USE_MFF         %d\n' % (self.__use_mff) )
            input_deck.write('USE_BMA         %d\n' % (self.__use_bma) )
            input_deck.write('USE_BMA+sLFC    %d\n' % (self.__use_bma_slfc) )
            input_deck.write('USE_CORE         1\n')
            input_deck.write('--gradients------------------------------------------\n')
            input_deck.write('GRAD 0\n')
            input_deck.write('L_GRADIENT            0.0e-0 \n')
            input_deck.write('T_GRADIENT            0.0    \n')
            input_deck.write('DSTEP                 0.0    \n')
            input_deck.write('--ion_parameters----------------------------use_flag-\n')
            input_deck.write('ION_TEMP %d 1\n' % (self.ion_temperature) )
            input_deck.write('S_ION_FEATURE %4.3f %d\n' % (self.__Sii_value, self.__use_Sii_value) )
            input_deck.write('DEBYE_TEMP    %4.3f %d\n' % (self.__debye_temperature_value, self.__use_debye_temperature) )
            input_deck.write('BAND_GAP      %4.3f %d\n' % (self.__band_gap_value, self.__use_band_gap) )

            input_deck.write('--integration----------------------------------------\n')
            input_deck.write('N_DAWSON       32\n')
            input_deck.write('N_DISTRIBUTION 32\n')
            input_deck.write('N_PVI          32\n')
            input_deck.write('N_LANDEN      512\n')
            input_deck.write('N_RELAXATION 1024\n')
            input_deck.write('N_FFT        4096\n')
            input_deck.write('EPS        1.0E-4\n')
            input_deck.write('--See(k,w)------------------------------use/norm-----\n')
            input_deck.write('STATIC_MODEL(DH,OCP,SOCP,SOCPN) %s\n' % (self.model_Sii) )
            input_deck.write('USE_ADV_Mix %d\n' % (self.model_Mix) )
            input_deck.write('USE_IRS_MODEL                            0\n')
            input_deck.write('HARD_SPHERE_DIAM                 1E-10   0\n')
            input_deck.write('POLARIZABILITY                     0.0 0.0\n')
            input_deck.write('BOUND-FREE_MODEL(IA,IBA,FFA)            %s\n' % (self.model_Sbf) )
            input_deck.write('BOUND-FREE_NORM(FK,NO,USR)        %s %4.3f\n' % (self.Sbf_norm, self.__Sbf_norm_value) )
            input_deck.write('BOUND-FREE_MEFF                        1.0\n')
            input_deck.write('USE_BOUND-FREE_DOPPLER                   0\n')
            input_deck.write('CONT-LOWR_MODEL(SP,EK,USR)         %s    %4.3f\n' % (self.model_IPL, self.__ipl_value) )
            input_deck.write('GK                                 %4.3f 0\n' % self.__lfc)
            input_deck.write('RPA                                %d    0\n' % (self.__use_rpa) )
            input_deck.write('LINDHARD                           %d    0\n' % (self.__use_lindhard) )
            input_deck.write('SALPETER                            0    0\n')
            input_deck.write('LANDEN                              0    0\n')
            input_deck.write('RPA_TSYTOVICH                       0    0\n')
            input_deck.write('STATIC_LFC                         %d    0\n' % (self.__use_static_lfc) )
            input_deck.write('DYNAMIC_LFC                        %d    0\n' % (self.__use_dynamic_lfc) )
            input_deck.write('MFF                                %d    0\n' % (self.__use_mff) )
            input_deck.write('BMA(+sLFC)                         %d    0\n' % (self.__write_bma))
            input_deck.write('CORE                                1    0\n')
            input_deck.write('TOTAL                               1    0\n')
            input_deck.write('E_MIN                              %4.3f  \n' % (self.energy_range['min']))
            input_deck.write('E_MAX                              %4.3f  \n' % (self.energy_range['max']))
            input_deck.write('E_STEP                             %4.3f  \n' % (self.energy_range['step']))
            input_deck.write('--target_spec--------------------------chem----Zfree--\n')
            input_deck.write('NUMBER_OF_SPECIES %d\n' % (len(self.elements)) )
            for i,element in enumerate(self.elements):
                input_deck.write('TARGET_%d %s %d %d\n' % (i+1, element[0], element[1], element[2] ) )
            input_deck.write('MASS_DENSITY %4.3f\n' % (self.mass_density))
            input_deck.write('NE_ZF_LOCK 1\n')
            input_deck.write('DATA_FILE data.txt\n')
            input_deck.write('NUMBER_POINTS 1024\n')
            input_deck.write('OPACITY_FILE nofile 0\n')
            input_deck.write('--instrument_function---------------------------------\n')
            input_deck.write('USE_FILE 0\n')
            input_deck.write('FILE_NAME nofile.dat\n')
            input_deck.write('INST_MODEL GAUSSIAN\n')
            input_deck.write('INST_FWHM 100.0\n')
            input_deck.write('BIN_PER_PIXEL 1.0\n')
            input_deck.write('INST_INDEX 2.0\n')
            input_deck.write('--additional_parameters-------------------------------\n')
            input_deck.write('MAX_ITERATIONS 0\n')
            input_deck.write('LEVENBERG_MARQUARDT 0\n')
            input_deck.write('SIGMA_LM 1.0\n')
            input_deck.write('SAVE_FILE xrts_out.txt\n')


    @property
    def elements(self):
        """ Query for the field data. """
        return self.__elements
    @elements.setter
    def elements(self, value):
        """ Set the elements to <value> """
        self.__elements = checkAndSetElements(value)

    @property
    def photon_energy(self):
        """ Query for the photon energy. """
        return self.__photon_energy
    @photon_energy.setter
    def photon_energy(self, value):
        """ Set the photon energy to <value>. """
        self.__photon_energy = checkAndSetPhotonEnergy(value)


    @property
    def scattering_angle(self):
        """ Query for the scattering angle. """
        return self.__scattering_angle
    @scattering_angle.setter
    def scattering_angle(self, value):
        """ Set the scattering angle to <value>. """
        self.__scattering_angle = checkAndSetScatteringAngle(value)

    @property
    def electron_temperature(self):
        """ Query for the electron temperature. """
        return self.__electron_temperature
    @electron_temperature.setter
    def electron_temperature(self, value):
        """ Set the electron temperature to <value>. """
        self.__electron_temperature = checkAndSetElectronTemperature(value)

    @property
    def electron_density(self):
        """ Query for the electron density. """
        return self.__electron_density
    @electron_density.setter
    def electron_density(self, value):
        """ Set the electron density to <value>. """
        self.__electron_density = value
        print "WARNING: Electron density might be inconsistent with mass density and charge."
    @property
    def ion_temperature(self):
        """ Query for the ion temperature. """
        return self.__ion_temperature
    @ion_temperature.setter
    def ion_temperature(self, value):
        """ Set the ion temperature to <value>. """
        self.__ion_temperature = checkAndSetIonTemperature(value)

    @property
    def ion_charge(self):
        """ Query for the ion charge. """
        return self.__ion_charge
    @ion_charge.setter
    def ion_charge(self, value):
        """ Set the ion charge to <value>. """
        self.__ion_charge = value
        print "WARNING: Ion charge might be inconsistent with electron density and mass density."

    @property
    def mass_density(self):
        """ Query for the mass density. """
        return self.__mass_density
    @mass_density.setter
    def mass_density(self, value):
        """ Set the mass density to <value>. """
        self.__mass_density = value
        print "WARNING: Mass density might be inconsistent with electron density and charge."

    @property
    def debye_temperature(self):
        """ Query for the Debye temperature. """
        return self.__debye_temperature
    @debye_temperature.setter
    def debye_temperature(self, value):
        """ Set the Debye temperature to <value>. """
        self.__debye_temperature = checkAndSetDebyeTemperature(value)
        self._setDebyeTemperatureFlags()

    @property
    def band_gap(self):
        """ Query for the band gap. """
        return self.__band_gap
    @band_gap.setter
    def band_gap(self, value):
        """ Set the band gap to <value>. """
        self.__band_gap = checkAndSetBandGap(value)
        self._setBandGapFlags()

    @property
    def energy_range(self):
        """ Query for the energy range. """
        return self.__energy_range
    @energy_range.setter
    def energy_range(self, value):
        """ Set the energy range to <value>. """
        self.__energy_range = checkAndSetEnergyRange(value)

    @property
    def model_Sii(self):
        """ Query for the ion-ion structure factor model. """
        return self.__model_Sii
    @model_Sii.setter
    def model_Sii(self, value):
        """ Set the ion-ion structure factor model to <value>. """
        self.__model_Sii = checkAndSetModelSii(value)
        self._setSiiFlags()

    @property
    def model_See(self):
        """ Query for the electron-electron (high-frequency) structure factor model. """
        return self.__model_See
    @model_See.setter
    def model_See(self, value):
        """ Set the electron-electron (high-frequency) structure factor model to <value>. """
        self.__model_See = checkAndSetModelSee(value)
        self._setSeeFlags()

    @property
    def model_Sbf(self):
        """ Query for the bound-free structure factor model. """
        return self.__model_Sbf
    @model_Sbf.setter
    def model_Sbf(self, value):
        """ Set the bound-free structure factor model to <value>. """
        self.__model_Sbf = checkAndSetModelSbf(value)

    @property
    def model_IPL(self):
        """ Query for the ionization potential lowering model. """
        return self.__model_IPL
    @model_IPL.setter
    def model_IPL(self, value):
        """ Set the ionization potential lowering model to <value>. """
        self.__model_IPL = checkAndSetModelIPL(value)
        self._setIPLFlags()

    @property
    def model_Mix(self):
        """ Query for the mixing model. """
        return self.__model_Mix
    @model_Mix.setter
    def model_Mix(self, value):
        """ Set the mixing model to <value>. """
        self.__model_Mix = checkAndSetModelMix(value)

    @property
    def lfc(self):
        """ Query for the local field factor. """
        return self.__lfc
    @lfc.setter
    def lfc(self, value):
        """ Set the local field factor to <value>. """
        self.__lfc = checkAndSetLFC(value)

    @property
    def Sbf_norm(self):
        """ Query for the norm of the bound-free structure factor. """
        return self.__Sbf_norm
    @Sbf_norm.setter
    def Sbf_norm(self, value):
        """ Set the norm of the bound-free structure factor to <value>. """
        self.__Sbf_norm = checkAndSetSbfNorm(value)
        self._setSbfNormFlags()

    #@property
    #def (self):
        #""" Query for the <++>. """
        #return self.__<++>

    #@property
    #def <++>(self):
        #""" Query for the <++>. """
        #return self.__<++>

    #@property
    #def <++>(self):
        #""" Query for the <++>. """
        #return self.__<++>

    #@property
    #def <++>(self):
        #""" Query for the <++>. """
        #return self.__<++>

    #@property
    #def <++>(self):
        #""" Query for the <++>. """
        #return self.__<++>

    #@property
    #def <++>(self):
        #""" Query for the <++>. """
        #return self.__<++>
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
        raise RuntimeError( "Scattering angle not specified.")

    angle = checkAndSetInstance( float, angle, None)
    # Check if in range.
    if angle <= 0.0 or angle > 180.0:
        raise( ValueError, "Scattering angle must be between 0 and 180 [degrees].")

    # Return.
    return angle

def checkAndSetPhotonEnergy(energy):
    """
    Utility to check if the photon energy is correct.
    @param energy : The energy to check.
    @return The checked energy.
    """

    # Set default.
    if energy is None:
        raise RuntimeError( "Photon energy not specified.")

    energy = checkAndSetInstance( float, energy, None)

    # Check if in range.
    if energy <= 0.0:
        raise( ValueError, "Photon energy must be positive.")

    # Return.
    return energy

def checkAndSetElements(elements):
    """ Utility to check if input is a valid list of elements.

    @param  elements : The elements to check.
    @type : list
    @return : The checked list of elements.
    """

    if elements is None:
        raise RuntimeError( "No element(s) specified. Give at least one chemical element.")
    elements = checkAndSetInstance( list, elements, None )

    # Check each element.
    for element in elements:
        symbol, stoch, chrg = checkAndSetInstance( list, element, None )
        if symbol not in ALL_ELEMENTS:
            raise ValueError( '%s is not a valid chemical element symbol.' % (symbol) )
        stoch = checkAndSetPositiveInteger(stoch)
        chrg = checkAndSetInteger(chrg)
        if chrg < -1:
            raise ValueError( "Charge must be >= -1.")

        element = [symbol, stoch, chrg]
    return elements

def checkAndSetElectronTemperature(electron_temperature):
    """ Utility to check if input is a valid electron temperature.

    @param  electron_temperature : The electron temperature to check.
    @type : double
    @return : The checked electron temperature.
    """
    if electron_temperature is None:
        raise RuntimeError( "Electron temperature not specified.")
    electron_temperature = checkAndSetInstance( float, electron_temperature, None)
    if electron_temperature <= 0.0:
        raise ValueError( "Electron temperature must be positive.")

    return electron_temperature

def checkAndSetDensitiesAndCharge(electron_density, ion_charge, mass_density):
    """ Utility to check input and return a set of consistent electron density, average ion charge, and mass density, if two are given as input.
    """
    # Find number of Nones in input.
    number_of_nones = (sum(x is None for x in [electron_density, ion_charge, mass_density]))
    # raise if not enough input.
    if number_of_nones > 0:
        raise RuntimeError( "Electron_density, ion_charge, and mass_density must be given.")

    #if electron_density is None:
        #electron_density = mass_density * ion_charge * Avogadro
    #if ion_charge is None:
        #ion_charge = electron_density / (mass_density * Avogadro)
    #if mass_density is None:
        #mass_density = electron_density / (ion_charge * Avogadro)

    #if abs( electron_density / (mass_density * ion_charge * Avogadro) - 1 ) > 1e-4:
        #raise ValueError( "Electron density, mass_density, and ion charge are not internally consistent: ne = %5.4e/m**3, rho*Zf*NA = %5.4e/m**3." % (electron_density, mass_density * ion_charge * Avogadro) )

    return electron_density, ion_charge, mass_density

def checkAndSetIonTemperature(ion_temperature, electron_temperature=None):
    """ Utility to check if input is a valid ion temperature.

    @param  ion_temperature : The ion temperature to check.
    @type : double
    @default : Electron temperature.
    @return : The checked ion temperature.
    """
    if electron_temperature is None:
        if ion_temperature is None:
            raise RuntimeError(" Could not fix ion temperature because electron temperature not given.")
    ion_temperature = checkAndSetInstance( float, ion_temperature, electron_temperature)
    if ion_temperature <= 0.0:
        raise ValueError( "Ion temperature must be positive.")

    return ion_temperature

def checkAndSetDebyeTemperature(debye_temperature):
    """ Utility to check if input is a valid Debye temperature.

    @param  debye_temperature : The Debye temperature to check.
    @type : double
    @default : 0.0
    @return : The checked Debye temperature.
    """
    if debye_temperature is None:
        return None

    debye_temperature = checkAndSetInstance( float, debye_temperature, 0.0)
    if debye_temperature < 0.0:
        raise ValueError( "Debye temperature must be non-negative.")

    return debye_temperature

def checkAndSetBandGap(band_gap):
    """ Utility to check if input is a valid bandgap.

    @param  band_gap: The bandgap to check.
    @type : double
    @default 0.0.
    @return : The checked bandgap.
    """
    if band_gap is None:
        return None

    band_gap = checkAndSetInstance( float, band_gap, 0.0)
    if band_gap < 0.0:
        raise ValueError( "Debye temperature must be positive.")

    return band_gap

def checkAndSetModelMix(model_Mix):
    """ Utility to check if input is a valid mixing model.

    @param  model_Mix : The mixing model to check.
    @type : string
    @return : The checked mixing model.
    """
    if model_Mix is None:
        return 0
    if not isinstance( model_Mix, str):
        raise TypeError('The mixing model must be a string or None.')
    model_Mix = model_Mix.lower()
    if not model_Mix == 'adv':
        raise ValueError('The mixing model has to be "ADV" (advanced) or None.')

    return {'adv' : 1, None: 0}[model_Mix]

def checkAndSetLFC(lfc):
    """ Utility to check if input is a valid local field correction factor.

    @param  lfc : The lfc to check.
    @type : double
    @return : The checked lfc.
    """
    lfc = checkAndSetInstance(float, lfc, 0.0)

    return lfc

def checkAndSetSbfNorm(Sbf_norm):
    """ Utility to check if input is a valid norm of the bound-free structure factor.

    @param  Sbf_norm : The norm to check.
    @type : string or double.
    @return : The checked norm.
    """
    if Sbf_norm not in ['FK', 'NO', None] and not isinstance( Sbf_norm, float ):
        raise ValueError('The bound-free norm parameter has to be "FK", "NO", None, or a numerical value.')
    if Sbf_norm is None:
        Sbf_norm = 'FK'
    return Sbf_norm

def checkAndSetEnergyRange(energy_range, electron_density=None):
    """
    Utility to check if the photon energy range is ok.
    @param energy_range : The range to check.
    @type dict
    @return The checked photon energy range.
    @raise ValueError if not of correct shape.
    """
    # Raise if both arguments None.
    if energy_range is None and electron_density is None:
        raise RuntimeError( "At least one argument (electron_density or energy_range) must be given.")
    # Some constants.
    bohr_radius_m = physical_constants['Bohr radius'][0]
    rydberg_energy_eV = physical_constants['Rydberg constant times hc in eV'][0]

    energy_range_default = None
    if electron_density is not None:
        # Get plasma frequency.
        plasma_frequency_eV = 4. * math.sqrt( electron_density * (bohr_radius_m)**3 * math.pi) * rydberg_energy_eV

        # Set to +/- 10*wpl if no range given.
        energy_range_default = {'min' : -10.0*plasma_frequency_eV,
                                'max' :  10.0*plasma_frequency_eV,
                                'step':   0.1*plasma_frequency_eV}
    energy_range = checkAndSetInstance( dict, energy_range, energy_range_default)

    # Check keys.
    if 'min' not in energy_range.keys():
        raise ValueError( "'min' missing in energy range (keys).")
    if 'max' not in energy_range.keys():
        raise ValueError( "'max' missing in energy range (keys).")
    if 'step' not in energy_range.keys():
        raise ValueError( "'step' missing in energy range (keys).")

    # Check values.
    for key in energy_range.keys():
        if not isinstance( energy_range[key], float):
            raise TypeError( "All values in energy_range must be floats.")
    if energy_range['min'] > energy_range['max']:
            raise ValueError( "energy_range['min'] must be smaller than energy_range['max'].")
    if energy_range['max'] - energy_range['min'] < energy_range['step']:
            raise ValueError( "energy_range['max'] - energy_range['min'] must be larger than the stepsize energy_range['step'].")

    # Return
    return energy_range

def checkAndSetModelSii( model ):
    """
    Utility to check if the model is a valid model for the Rayleigh (quasistatic) scattering feature.

    @param model : The model to check.
    @type : str
    @return : The checked model
    @raise ValueError if not a string or not a valid Sii model ('RPA', 'DH',
    """

    if model is None:
        model = 'SOCP'

    valid_models = [ 'DH', 'OCP', 'SOCP', 'SOCPN' ]
    if not (isinstance( model, str) or isinstance( model, float )):
        raise TypeError( "The Sii model must be a valid model specifier (string) or a float giving the value of Sii(k).")
    if not (model in valid_models or isinstance( model, float )):
        raise ValueError( "The Sii model must be a valid Sii model or a numerical value. Valid Sii models are %s." % (str(valid_models)) )

    return model


def checkAndSetModelSee( model ):
    """
    Utility to check if the model is a valid model for the high frequency (dynamic) feature.

    @param model : The model to check.
    @type : str
    @return : The checked model
    @raise ValueError if not a string or not a valid See0 model ('RPA', 'BMA', 'BMA+sLFC', 'BMA+dLFC', 'LFC', 'Landen')
    """

    # Default handling.
    model = checkAndSetInstance( str, model, 'RPA')

    # Valid models.
    valid_models = ['RPA',
                    'Lindhard',
                    'static LFC',
                    'dynamic LFC',
                    'BMA',
                    'BMA+sLFC',
                    'BMA+dLFC',
                    ]

    if model not in valid_models:
        raise ValueError( "The See model must be a valid See0 model. Valid See0 models are %s." % (str(valid_models)) )

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

    # Handle default.
    model = checkAndSetInstance( str, model, 'IA')

    valid_models = ['IA',
                    'IBA',
                    'FFA'
                    ]

    if model not in valid_models:
        raise ValueError( "The Sbf model must be a valid Sbf model. Valid Sbf models are %s." % (str(valid_models)) )

    # Return
    return model

def checkAndSetModelIPL( model ):
    """
    Utility to check if the model is a valid model for ionization potential lowering.

    @param model : The model to check.
    @type : str or float
    @return : The checked model
    @raise ValueError if not a valid IPL model.
    """

    # Handle default.
    if model is None:
        model = 'SP'

    valid_models = ['SP',
                    'EK',
                    ]
    if not ( isinstance( model, str ) or isinstance( model, float ) ):
            raise TypeError("The IPL model must be a string or a float.")
    if not (model in valid_models or isinstance( model, float )):
        raise ValueError( "The Sbf model must be a valid Sbf model or a numerical value. Valid Sbf models are %s." % (str(valid_models)) )

    # Return
    return model
