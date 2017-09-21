""" Module that holds the PlasmaXRTSCalculatorParameters class.  """
##########################################################################
#                                                                        #
# Copyright (C) 2016-2017 Carsten Fortmann-Grote                         #
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

from scipy.constants import Avogadro
from scipy.constants import physical_constants
import periodictable
import copy
import math
import numpy
import os
import tempfile

from SimEx.Parameters.AbstractCalculatorParameters import AbstractCalculatorParameters
from SimEx.Utilities.Utilities import ALL_ELEMENTS
from SimEx.Utilities.EntityChecks import checkAndSetInstance
from SimEx.Utilities.EntityChecks import checkAndSetInteger
from SimEx.Utilities.EntityChecks import checkAndSetPositiveInteger
from SimEx.Utilities.EntityChecks import checkAndSetNonNegativeInteger

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
                 Sbf_norm=None,
                 source_spectrum=None,
                 source_spectrum_fwhm=None,
                 **kwargs
                 ):

        """

        :param elements: The chemical elements in the scattering target.
        :type elements: list [[element symbol, stochiometric number, charge], ...], default None
        :example elements: [['B', 1, 2], ['N', 1, 2]] for Boron-Nitride with both B and N two fold ionized (ion average).
        :example elements: [['C', 1, 4], ['H', 1, -1]] for Plastic with both four-fold ionized C and ionization of H calculated so that the given average ion charge comes out correct.

        :param photon_energy: The central energy of incoming x-ray photons.
        :type photon_energy: float

        :param scattering_angle: The scattering angle.
        :type scattering_angle: float

        :param electron_temperature: The temperature of the electron subsystems (units of eV).
        :type electron_temperature: float

        :param electron_density: The electron number density (units of 1/cm^3)
        :type electron_density: float

        :param ion_temperature: The temperature of the ion subsystem (units of eV).
        :type ion_temperature: float

        :param ion_charge: The average ion charge (units of elementary charge e).
        :type ion_charge: float

        :param mass_density: The mass density of the target (units of g/cm^3).
        :type mass_density: float

        :param debye_temperature: The Debye temperature (units of eV).
        :type debye_temperature: float

        :param band_gap: The band gap of the target (units of eV).
        :type band_gap: float, default 0

        :param energy_range: The energy range over which to calculate the scattering spectrum.
        :type energy_range: dict, default 0
        :example energy_range: energy_range={'min'  -100.0, 'max'  100, 'step'  0.5} to go from -100 eV to 100 eV in steps of 0.5 eV.

        :param model_Sii: The model to use for the ion-ion structure factor.
        :type model_Sii: str ('DH' || 'OCP' || 'SOCP' || 'SOCPN') || float, default 'DH'
        :example model_Sii: Sii=1.5 to use a fixed value of Sii=1.5

        :param model_See: The model of the dynamic (high frequency) part of the electron-electron structure factor.
        :type model_See: str ('RPA' || 'BMA' || 'BMA+sLFC'), default 'RPA'

        :param model_Sbf: The model for the bound-free structure factor.
        :type model_Sbf: str ('IA' || 'FA'), default 'IA'

        :param model_IPL: Model for ionization potential lowering.
        :type model_IPL: str ('SP' || 'EK') || float, default 'SP'
        :example model_IPL: model_IPL=100.0 # Set the ionization potential difference (lowering) to 100 eV.

        :param model_Mix: The model to use for mixing (of species).
        :type model_Mix: str, default None

        :param lfc:  The local field correction to use.
        :type lfc:  float, default 0.0

        :param Sbf_norm: How to normalize the bound-free structure factor.
        :type Sbf_norm: str || float, default None

        :param source_spectrum: Path to a file holding the x-ray probe energy spectrum.
        :type source_spectrum: str, default None

        :param source_spectrum_fwhm: The x-ray probe energy spectrum fwhm.
        :type source_spectrum_fwhm: float
        """

        # Check and set all parameters.
        self.__elements             = checkAndSetElements(elements)
        self.__photon_energy        = checkAndSetPhotonEnergy(photon_energy)
        self.__scattering_angle     = checkAndSetScatteringAngle(scattering_angle)
        self.__electron_temperature = checkAndSetElectronTemperature(electron_temperature)
        # Set electron density, charge, and mass density depending on which input was given.
        self.__electron_density, self.__ion_charge, self.__mass_density = checkAndSetDensitiesAndCharge(electron_density, ion_charge, mass_density, elements)
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
        self.__source_spectrum    = checkAndSetSourceSpectrum(source_spectrum)
        self.__source_spectrum_fwhm=checkAndSetSourceSpectrumFWHM(source_spectrum_fwhm)

        # Set internal parameters.
        self._setSeeFlags()
        self._setSiiFlags()
        self._setSbfNormFlags()
        self._setDebyeTemperatureFlags()
        self._setBandGapFlags()
        self._setIPLFlags()
        self._setSourceSpectrumFlags()

        # Set state to not-initialized (e.g. input deck is not written).
        self.__is_initialized = False

    def _setDefaults(self):
        """ """
        """ Set the inherited parameters defaults that depend on the special calculator. """
        self._AbstractCalculatorParameters__cpus_per_task_default = 1

    def _setSeeFlags(self):
        """ Set the See parameters as used in the input deck generator. """
        self.__use_rpa         = int(self.model_See == "RPA")
        self.__use_bma         = int(self.model_See == "BMA")
        self.__use_bma_slfc    = int(self.model_See == 'BMA+sLFC')
        self.__write_bma = int(self.model_See == 'BMA+sLFC' or self.model_See == 'BMA')
        self.__use_lindhard    = int(self.model_See == 'Lindhard')
        self.__use_landen      = int(self.model_See == 'Landen')
        self.__use_static_lfc  = int(self.model_See == 'sLFC')
        self.__use_dynamic_lfc = int(self.model_See == 'dLFC')
        self.__use_mff = int(self.model_See == 'MFF')

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
            self.__model_Sii = 'DH'

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

    def _setSourceSpectrumFlags(self):
        """ Set the internal source spectrum flags used in the input deck generation."""
        # Default.
        self.__use_source_spectrum_file = 0
        self.__source_spectrum_identifier = "GAUSSIAN"

        if self.__source_spectrum == "LORENTZ":
            self.__source_spectrum_identifier = "LORENTZIAN"
        elif self.__source_spectrum == "PROP":
            self.__use_source_spectrum_file = 1

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
            input_deck.write('ELECTRON_DENSITY  %4.3e 0\n' % (self.electron_density*1e6) )
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
            input_deck.write('LANDEN                             %d    0\n' % (self.__use_landen) )
            input_deck.write('RPA_TSYTOVICH                       0    0\n')
            input_deck.write('STATIC_LFC                         %d    0\n' % (self.__use_static_lfc) )
            input_deck.write('DYNAMIC_LFC                        %d    0\n' % (self.__use_dynamic_lfc) )
            input_deck.write('MFF                                %d    0\n' % (self.__use_mff) )
            input_deck.write('BMA(+sLFC)                         %d    0\n' % (self.__write_bma))
            input_deck.write('CORE                                1    0\n')
            input_deck.write('TOTAL                               1    0\n')
            input_deck.write('E_MIN                              %8.7f  \n' % (self.energy_range['min']))
            input_deck.write('E_MAX                              %8.7f  \n' % (self.energy_range['max']))
            input_deck.write('E_STEP                             %8.7f  \n' % (self.energy_range['step']))
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
            input_deck.write('USE_FILE %d\n' % (self.__use_source_spectrum_file) )
            input_deck.write('FILE_NAME source_spectrum.txt\n')
            input_deck.write('INST_MODEL %s\n' % (self.__source_spectrum_identifier) )
            input_deck.write('INST_FWHM %4.3f\n' % (self.__source_spectrum_fwhm) )
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
        """ Set the elements to value. """
        self.__elements = checkAndSetElements(value)

    @property
    def photon_energy(self):
        """ Query for the photon energy. """
        return self.__photon_energy
    @photon_energy.setter
    def photon_energy(self, value):
        """ Set the photon energy to value. """
        self.__photon_energy = checkAndSetPhotonEnergy(value)


    @property
    def scattering_angle(self):
        """ Query for the scattering angle. """
        return self.__scattering_angle
    @scattering_angle.setter
    def scattering_angle(self, value):
        """ Set the scattering angle to value. """
        self.__scattering_angle = checkAndSetScatteringAngle(value)

    @property
    def electron_temperature(self):
        """ Query for the electron temperature. """
        return self.__electron_temperature
    @electron_temperature.setter
    def electron_temperature(self, value):
        """ Set the electron temperature to value. """
        self.__electron_temperature = checkAndSetElectronTemperature(value)

    @property
    def electron_density(self):
        """ Query for the electron density. """
        return self.__electron_density
    @electron_density.setter
    def electron_density(self, value):
        """ Set the electron density to value. """
        self.__electron_density = value
        print "WARNING: Electron density might be inconsistent with mass density and charge."
    @property
    def ion_temperature(self):
        """ Query for the ion temperature. """
        return self.__ion_temperature
    @ion_temperature.setter
    def ion_temperature(self, value):
        """ Set the ion temperature to value. """
        self.__ion_temperature = checkAndSetIonTemperature(value)

    @property
    def ion_charge(self):
        """ Query for the ion charge. """
        return self.__ion_charge
    @ion_charge.setter
    def ion_charge(self, value):
        """ Set the ion charge to value. """
        self.__ion_charge = value
        print "WARNING: Ion charge might be inconsistent with electron density and mass density."

    @property
    def mass_density(self):
        """ Query for the mass density. """
        return self.__mass_density
    @mass_density.setter
    def mass_density(self, value):
        """ Set the mass density to value. """
        self.__mass_density = value
        print "WARNING: Mass density might be inconsistent with electron density and charge."

    @property
    def debye_temperature(self):
        """ Query for the Debye temperature. """
        return self.__debye_temperature
    @debye_temperature.setter
    def debye_temperature(self, value):
        """
        @brief Set the Debye temperature to value.

        @param value1 The value to set the Debye temperature to.
        <br/><b>type</b> float
        """
        self.__debye_temperature = checkAndSetDebyeTemperature(value)
        self._setDebyeTemperatureFlags()

    @property
    def band_gap(self):
        """ Query for the band gap. """
        return self.__band_gap
    @band_gap.setter
    def band_gap(self, value):
        """ Set the band gap to value. """
        self.__band_gap = checkAndSetBandGap(value)
        self._setBandGapFlags()

    @property
    def energy_range(self):
        """ Query for the energy range. """
        return self.__energy_range
    @energy_range.setter
    def energy_range(self, value):
        """ Set the energy range to value. """
        self.__energy_range = checkAndSetEnergyRange(value)

    @property
    def model_Sii(self):
        """ Query for the ion-ion structure factor model. """
        return self.__model_Sii
    @model_Sii.setter
    def model_Sii(self, value):
        """ Set the ion-ion structure factor model to value. """
        self.__model_Sii = checkAndSetModelSii(value)
        self._setSiiFlags()

    @property
    def model_See(self):
        """ Query for the electron-electron (high-frequency) structure factor model. """
        return self.__model_See
    @model_See.setter
    def model_See(self, value):
        """ Set the electron-electron (high-frequency) structure factor model to value. """
        self.__model_See = checkAndSetModelSee(value)
        self._setSeeFlags()

    @property
    def model_Sbf(self):
        """ Query for the bound-free structure factor model. """
        return self.__model_Sbf
    @model_Sbf.setter
    def model_Sbf(self, value):
        """ Set the bound-free structure factor model to value. """
        self.__model_Sbf = checkAndSetModelSbf(value)

    @property
    def model_IPL(self):
        """ Query for the ionization potential lowering model. """
        return self.__model_IPL
    @model_IPL.setter
    def model_IPL(self, value):
        """ Set the ionization potential lowering model to value. """
        self.__model_IPL = checkAndSetModelIPL(value)
        self._setIPLFlags()

    @property
    def model_Mix(self):
        """ Query for the mixing model. """
        return self.__model_Mix
    @model_Mix.setter
    def model_Mix(self, value):
        """ Set the mixing model to value. """
        self.__model_Mix = checkAndSetModelMix(value)

    @property
    def lfc(self):
        """ Query for the local field factor. """
        return self.__lfc
    @lfc.setter
    def lfc(self, value):
        """ Set the local field factor to value. """
        self.__lfc = checkAndSetLFC(value)

    @property
    def Sbf_norm(self):
        """ Query for the norm of the bound-free structure factor. """
        return self.__Sbf_norm
    @Sbf_norm.setter
    def Sbf_norm(self, value):
        """ Set the norm of the bound-free structure factor to value. """
        self.__Sbf_norm = checkAndSetSbfNorm(value)
        self._setSbfNormFlags()

    @property
    def source_spectrum(self):
        """ Query for the source spectrum identifier. """
        return self.__source_spectrum
    @source_spectrum.setter
    def source_spectrum(self, value):
        """ Set the source_spectrum to value."""
        self.__source_spectrum = checkAndSetSourceSpectrum(value)
        self._setSourceSpectrumFlags()

    @property
    def source_spectrum_fwhm(self):
        """ Query for the source spectrum fwhm identifier. """
        return self.__source_spectrum
    @source_spectrum_fwhm.setter
    def source_spectrum_fwhm(self, value):
        """ Set the source_spectrum fwhm to value."""
        self.__source_spectrum_fwhm = checkAndSetSourceSpectrumFWHM(value)

    #@property
    #def (self):
        #""" Query for the <++>. """
        #return self.__<++>
    #@<++>.setter
    #def <++>(self, value):
        #""" Set the <++> to value."""
        #self.__<++> = checkAndSet<++>(value)
        #<++>

       #<++>

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

    @param  elements: The elements to check.
    <br/><b>type</b> elements: list
    @return: The checked list of elements.
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
    <br/><b>type</b> : double
    @return : The checked electron temperature.
    """
    if electron_temperature is None:
        raise RuntimeError( "Electron temperature not specified.")
    electron_temperature = checkAndSetInstance( float, electron_temperature, None)
    if electron_temperature <= 0.0:
        raise ValueError( "Electron temperature must be positive.")

    return electron_temperature

def checkAndSetDensitiesAndCharge(electron_density, ion_charge, mass_density, elements):
    """ Utility to check input and return a set of consistent electron density, average ion charge, and mass density, if two are given as input.
    """
    # Find number of Nones in input.
    number_of_nones = (sum(x is None for x in [electron_density, ion_charge, mass_density]))
    # raise if not enough input.
    if number_of_nones > 1:
        raise RuntimeError( "At least two of Electron_density, ion_charge, and mass_density must be given.")

    # Get molar weight needed to convert electron density to mass density.
    element_symbols=[e[0] for e in elements]
    element_abundances = numpy.array([e[1] for e in elements])
    element_charges = numpy.array([e[2] for e in elements])
    element_instances = [getattr(periodictable, es) for es in element_symbols]
    molar_weights = [ei.mass for ei in element_instances]

    molar_weight = sum(element_abundances * molar_weights) / sum( element_abundances )
    if electron_density is None:
        electron_density = mass_density * ion_charge * Avogadro / molar_weight
        print "Setting electron density to %5.4e/cm**3." % (electron_density)
    if ion_charge is None:
        ion_charge = electron_density / (mass_density * Avogadro / molar_weight)
        print "Setting average ion charge to %5.4f." % (ion_charge)
    if mass_density is None:
        mass_density = electron_density / (ion_charge * Avogadro / molar_weight)
        print "Setting mass density to %5.4f g/cm**3." % (mass_density)

    # Adjust
    #negative_charge_element_index = numpy.where(element_charges == -1)
    #positive_charges = element_charges[numpy.where(element_charges >= 0.0)]

    #sum_s_Zini= sum(element_abundances[numpy.where(element_charges >= 0.0)] * positive_charges)
    #sum_s_ni = sum(element_abundances[numpy.where(element_charges >= 0.0)])
    #element_charges[negative_charge_element_index] = sum_s_Zini / ion_charge - sum_s_ni

    if abs( electron_density / (mass_density * ion_charge * Avogadro / molar_weight) - 1. ) > 1e-4:
        raise ValueError( "Electron density, mass_density, and ion charge are not internally consistent: ne = %5.4e/cm**3, rho*Zf*NA/u= %5.4e/cm**3." % (electron_density, mass_density * ion_charge * Avogadro/molar_weight) )

    return electron_density, ion_charge, mass_density

def checkAndSetIonTemperature(ion_temperature, electron_temperature=None):
    """ Utility to check if input is a valid ion temperature.

    @param  ion_temperature : The ion temperature to check.
    <br/><b>type</b> : double
    <br/><b>default</b> : Electron temperature.
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
    <br/><b>type</b> : double
    <br/><b>default</b> : 0.0
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
    <br/><b>type</b> : double
    <br/><b>default</b> 0.0.
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
    <br/><b>type</b> : string
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
    <br/><b>type</b> : double
    @return : The checked lfc.
    """
    lfc = checkAndSetInstance(float, lfc, 0.0)

    return lfc

def checkAndSetSbfNorm(Sbf_norm):
    """ Utility to check if input is a valid norm of the bound-free structure factor.

    @param  Sbf_norm : The norm to check.
    <br/><b>type</b> : string or double.
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
    <br/><b>type</b> dict
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
    <br/><b>type</b> : str
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
    <br/><b>type</b> : str
    @return : The checked model
    @raise ValueError if not a string or not a valid See0 model ('RPA', 'BMA', 'BMA+sLFC', 'BMA+dLFC', 'LFC', 'Landen')
    """

    # Default handling.
    model = checkAndSetInstance( str, model, 'RPA')

    # Valid models.
    valid_models = ['RPA',
                    'Lindhard',
                    'Landen',
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
    <br/><b>type</b> : str
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
    <br/><b>type</b> : str or float
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

def checkAndSetSourceSpectrum( source_spectrum ):
    """
    Utility to check sanity of given input for the source spectrum identifier.

    @param source_spectrum : The source spectrum identifier to check.
    <br/><b>type</b> : str
    @return : The checked identifier.
    @raise : TypeError or ValueError if input is not valid.
    """

    # Check type.
    source_spectrum = checkAndSetInstance( str, source_spectrum, "GAUSS" )

    # Convert to all upper case.
    source_spectrum = source_spectrum.upper()

    # Check input is valid.
    if source_spectrum not in ["GAUSS", "LORENTZ", "PROP"]:
        raise ValueError( "Parameter 'source_spectrum' must be one of 'GAUSS', 'LORENTZ', or 'PROP'.")

    # All checked, return.
    return source_spectrum

def checkAndSetSourceSpectrumFWHM( fwhm ):
    """
    Utility to check sanity of given input for the source spectrum full width at half maximum (fwhm).

    @param source_spectrum : The value to check.
    <br/><b>type</b> : float
    @return : The checked value.
    @raise : TypeError or ValueError if input is not valid.
    """

    # Check type.
    fwhm = checkAndSetInstance( float, fwhm, 5.0 )

    # Check positivity.
    if fwhm <= 0.0:
        raise ValueError( "The parameter 'source_spectrum_fwhm' must be positive.")

    # All checked, return.
    return fwhm
