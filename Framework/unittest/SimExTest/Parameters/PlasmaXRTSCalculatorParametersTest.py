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

""" Test module for the PlasmaXRTSCalculatorParameter class.

    @author : CFG
    @institution : XFEL
    @creation 20160219

"""
import paths
import os
import numpy
import shutil
import subprocess

# Include needed directories in sys.path.
import paths
import unittest

from SimEx.Parameters.AbstractCalculatorParameters import AbstractCalculatorParameters

# Import the class to test.
from SimEx.Parameters.PlasmaXRTSCalculatorParameters import PlasmaXRTSCalculatorParameters
from SimEx.Parameters.PlasmaXRTSCalculatorParameters import checkAndSetPhotonEnergy
from SimEx.Parameters.PlasmaXRTSCalculatorParameters import checkAndSetScatteringAngle
from SimEx.Parameters.PlasmaXRTSCalculatorParameters import checkAndSetElements
from SimEx.Parameters.PlasmaXRTSCalculatorParameters import checkAndSetDensitiesAndCharge
from SimEx.Parameters.PlasmaXRTSCalculatorParameters import checkAndSetElectronTemperature
from SimEx.Parameters.PlasmaXRTSCalculatorParameters import checkAndSetIonTemperature
from SimEx.Parameters.PlasmaXRTSCalculatorParameters import checkAndSetDebyeTemperature
from SimEx.Parameters.PlasmaXRTSCalculatorParameters import checkAndSetBandGap
from SimEx.Parameters.PlasmaXRTSCalculatorParameters import checkAndSetModelMix
from SimEx.Parameters.PlasmaXRTSCalculatorParameters import checkAndSetLFC
from SimEx.Parameters.PlasmaXRTSCalculatorParameters import checkAndSetSbfNorm
from SimEx.Parameters.PlasmaXRTSCalculatorParameters import checkAndSetEnergyRange
from SimEx.Parameters.PlasmaXRTSCalculatorParameters import checkAndSetModelSii
from SimEx.Parameters.PlasmaXRTSCalculatorParameters import checkAndSetModelSee
from SimEx.Parameters.PlasmaXRTSCalculatorParameters import checkAndSetModelSbf
from SimEx.Parameters.PlasmaXRTSCalculatorParameters import checkAndSetModelIPL
from SimEx.Parameters.PlasmaXRTSCalculatorParameters import checkAndSetSourceSpectrum
from SimEx.Parameters.PlasmaXRTSCalculatorParameters import checkAndSetSourceSpectrumFWHM

class PlasmaXRTSCalculatorParametersTest(unittest.TestCase):
    """
    Test class for the PlasmaXRTSCalculatorParameters class.
    """

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        """ Tearing down the test class. """
        pass

    def setUp(self):
        """ Setting up a test. """
        self.__files_to_remove = []
        self.__dirs_to_remove = []

        self.xrts_parameters = PlasmaXRTSCalculatorParameters(
                                                         elements=[['Be', 1, -1]],
                                                         photon_energy=4.96e3,
                                                         scattering_angle=90.0,
                                                         electron_temperature=10.0,
                                                         electron_density=3.0e29,
                                                         ion_charge=2.3,
                                                         mass_density=1.85
                                                         )

    def tearDown(self):
        """ Tearing down a test. """
        for f in self.__files_to_remove:
            if os.path.isfile(f):
                os.remove(f)
        for d in self.__dirs_to_remove:
            if os.path.isdir(d):
                shutil.rmtree(d)

    def testConstruction(self):
        """ Testing the default construction of the class using a dictionary. """

        # Attempt to construct an instance of the class.
        xrts_parameters = PlasmaXRTSCalculatorParameters(elements=[['Be', 1, -1]],
                                                         photon_energy=4.96e3,
                                                         scattering_angle=90.0,
                                                         electron_temperature=10.0,
                                                         electron_density=1.0e23,
                                                         ion_charge=2.3,
                                                         mass_density=1.85,
                                                         )


        # Check instance and inheritance.
        self.assertIsInstance( xrts_parameters, PlasmaXRTSCalculatorParameters )
        self.assertIsInstance( xrts_parameters, AbstractCalculatorParameters )

    def testCheckAndSetScatteringAngle(self):
        """ Test the scattering angle set/check function. """
        # Check default.
        self.assertRaises( RuntimeError, checkAndSetScatteringAngle, None )

        # Check out of range.
        self.assertRaises( ValueError, checkAndSetScatteringAngle, 190. )

        # Check negative
        self.assertRaises( ValueError, checkAndSetScatteringAngle, -90. )

        # Check zero.
        self.assertRaises( ValueError, checkAndSetScatteringAngle, 0.0 )

        # Check return.
        self.assertEqual( checkAndSetScatteringAngle( 10.3156734 ), 10.3156734, 7 )

    def testCheckAndSetPhotonEnergy(self):
        """ Test the photon energy  set/check function. """
        # Check default.
        self.assertRaises( RuntimeError, checkAndSetPhotonEnergy, None )

        # Check negative
        self.assertRaises( ValueError, checkAndSetPhotonEnergy, -90. )

        # Check zero.
        self.assertRaises( ValueError, checkAndSetPhotonEnergy, 0.0 )

        # Check return.
        self.assertEqual( checkAndSetPhotonEnergy( 1600. ), 1600. )

    def testCheckAndSetElements(self):
        """ Test the elements set/check function."""
        # Check default.
        self.assertRaises( RuntimeError, checkAndSetElements, None)

        # Check not a valid elements list.
        self.assertRaises( TypeError, checkAndSetElements, 'Beryllium')

        # Check not a valid elements list.
        # Only symbol.
        self.assertRaises( TypeError, checkAndSetElements, ['Be'])
        # Not a list of lists.
        self.assertRaises( TypeError, checkAndSetElements, ['Be', 1, -1])
        # Element name instead of symbol.
        self.assertRaises( TypeError, checkAndSetElements, ['Beryllium', 1, -1])
        # Not a valid symbol.
        self.assertRaises( ValueError, checkAndSetElements, [['Hx', 1, -1]])
        # Floating stoch.
        self.assertRaises( TypeError, checkAndSetElements, [['Be', 0.0, -1]])
        # Zero stoch.
        self.assertRaises( TypeError, checkAndSetElements, [['Be', 0, -1]])
        # Charge not valid.
        self.assertRaises( ValueError, checkAndSetElements, [['Be', 1, -2]])
        # One element in list is faulty.
        self.assertRaises( ValueError, checkAndSetElements,[['Be', 1, -1], ['Hx', 1, -1]])

        # Check return from well behaved input.
        sane_return = checkAndSetElements([['B',1, -1], ['N', 1, 2]])
        self.assertEqual(sane_return[0][0], 'B')
        self.assertEqual(sane_return[0][1], 1)
        self.assertEqual(sane_return[0][2], -1)
        self.assertEqual(sane_return[1][0], 'N')
        self.assertEqual(sane_return[1][1], 1)
        self.assertEqual(sane_return[1][2], 2)

    def testCheckAndSetElectronTemperature(self):
        """ Check the electron temperature set/check function. """

        # Check default.
        self.assertRaises( RuntimeError, checkAndSetElectronTemperature, None)

        # Check incorrect type.
        self.assertRaises( TypeError, checkAndSetElectronTemperature, "1.0")
        # Zero.
        self.assertRaises( ValueError, checkAndSetElectronTemperature, 0.0)
        # Negative.
        self.assertRaises( ValueError, checkAndSetElectronTemperature, -10.0)

    def testCheckAndSetDensitiesAndCharge(self):
        """ Check the utility for setting the charge, number and mass densities works correctly. """

        # Case 1: No input -> raise
        self.assertRaises( RuntimeError, checkAndSetDensitiesAndCharge, None, None, None )

        # Case 2: Not enough input.
        self.assertRaises( RuntimeError, checkAndSetDensitiesAndCharge, 1e19, None, None )
        self.assertRaises( RuntimeError, checkAndSetDensitiesAndCharge, None, 2.3, None )
        self.assertRaises( RuntimeError, checkAndSetDensitiesAndCharge, None, None, 1.5 )

        ed, Zf, rho = 3e29, 2.3, 1.85

        self.assertAlmostEqual( (ed, Zf, rho) , checkAndSetDensitiesAndCharge( ed, Zf, rho ) )

    def testCheckAndSetIonTemperature(self):
        """ Test the ion temperature check'n'set function. """

        # Default
        Te = 10.0
        Ti = None
        self.assertEqual( checkAndSetIonTemperature( Ti, Te), Te)

        # Check incorrect type.
        self.assertRaises( TypeError, checkAndSetIonTemperature, "1.0")
        # Zero.
        self.assertRaises( ValueError, checkAndSetIonTemperature, 0.0)
        # Negative.
        self.assertRaises( ValueError, checkAndSetIonTemperature, -10.0)

    def testCheckAndSetDebyeTemperature(self):
        """ Test the Debye temperature check'n'set function. """

        # Default
        self.assertEqual( checkAndSetDebyeTemperature( None), None )

        # Check incorrect type.
        self.assertRaises( TypeError, checkAndSetDebyeTemperature, "1.0")
        # Negative.
        self.assertRaises( ValueError, checkAndSetDebyeTemperature, -10.0)

    def testCheckAndSetBandGap(self):
        """ Test the bandgap check'n'set function."""
        # Default
        self.assertEqual( checkAndSetBandGap( None), None )

        # Check incorrect type.
        self.assertRaises( TypeError, checkAndSetBandGap, "1.0")
        # Negative.
        self.assertRaises( ValueError, checkAndSetBandGap, -10.0)

    def testCheckAndSetModelMix(self):
        """ Test the mixing model check'n'set function."""
        # Default
        self.assertEqual( checkAndSetModelMix( None ), 0)

        # Check malformed input.
        self.assertRaises( ValueError, checkAndSetModelMix, "halleluja")
        self.assertRaises( TypeError, checkAndSetModelMix, 1.0)

        # Check ok return.
        self.assertEqual( checkAndSetModelMix( 'aDV' ), 1)

    def testCheckAndSetLFC(self):
        """ Test the lfc check'n'set function."""
        # Default.
        self.assertEqual( checkAndSetLFC( None ), 0.0 )

        # Check exception.
        # Wrong type.
        self.assertRaises( TypeError, checkAndSetLFC, "1.0")

        # Ok return.
        self.assertEqual( checkAndSetLFC( 1.234 ), 1.234 )

    def testCheckAndSetSbfNorm(self):
        """ Test the Sbf norm check'n'set function."""
        # Default.
        self.assertEqual( checkAndSetSbfNorm( None ), 'FK' )

        # Wrong value.
        self.assertRaises( ValueError, checkAndSetSbfNorm, 'Skw')

        # Ok return.
        self.assertEqual( checkAndSetSbfNorm( "FK" ), "FK" )
        self.assertEqual( checkAndSetSbfNorm( "NO" ), "NO" )
        self.assertEqual( checkAndSetSbfNorm( 1.0 ), 1.0 )

    def testCheckAndSetEnergyRange(self):
        """ Test the energy range check'n'set function."""
        # Default.
        electron_density = 1.0e28
        energy_range = checkAndSetEnergyRange(energy_range=None,electron_density=electron_density)
        self.assertAlmostEqual( energy_range['min'], -37.13276417 )
        self.assertAlmostEqual( energy_range['max'],  37.13276417 )
        self.assertAlmostEqual( energy_range['step'],  0.37132764 )


        # Check exception.
        # Wrong type.
        self.assertRaises( TypeError, checkAndSetEnergyRange, [1,0, 2,0] )
        # Wrong keys.
        self.assertRaises( ValueError, checkAndSetEnergyRange, {'minimum': -10.0, 'max' : 10.0, 'step': 1.0})
        self.assertRaises( ValueError, checkAndSetEnergyRange, {'min': -10.0, 'maximum' : 10.0, 'step': 1.0})
        self.assertRaises( ValueError, checkAndSetEnergyRange, {'min': -10.0, 'max' : 10.0, 'd': 1.0})
        # Wrong values.
        self.assertRaises( TypeError, checkAndSetEnergyRange, {'min': "-10.0", 'max' : 10.0, 'step': 1.0})
        self.assertRaises( TypeError, checkAndSetEnergyRange, {'min': -10.0, 'max' : "10.0", 'step': 1.0})
        self.assertRaises( TypeError, checkAndSetEnergyRange, {'min': -10.0, 'max' : 10.0, 'step': "1.0"})
        # min > max.
        self.assertRaises( ValueError, checkAndSetEnergyRange, {'min': 10.0, 'max' : 9.0, 'step': 1.0})
        # min = max.
        self.assertRaises( ValueError, checkAndSetEnergyRange, {'min': 10.0, 'max' : 10.1, 'step': 1.0})

        # Ok return.
        energy_range = {'min': -10.0, 'max' : 10.0, 'step': 1.0}
        self.assertEqual( checkAndSetEnergyRange( energy_range, None ), energy_range )

    def testCheckAndSetModelSii(self):
        """ Test the Sii model check'n'set function."""
        # Default.
        self.assertEqual( checkAndSetModelSii( None ), "SOCP" )

        # Wrong type.
        self.assertRaises( TypeError, checkAndSetModelSii, [1,0, 2.0] )

        # Wrong specifier.
        self.assertRaises( ValueError, checkAndSetModelSii, "Magic" )

        # Return from ok input.
        self.assertEqual( checkAndSetModelSii( "DH" ), "DH" )
        self.assertAlmostEqual( checkAndSetModelSii( numpy.pi ), 3.1416, 4 )

    def testCheckAndSetModelSee(self):
        """ Test the See model check'n'set function."""
        # Default.
        self.assertEqual( checkAndSetModelSee( None ), "RPA" )

        # Wrong type.
        self.assertRaises( TypeError, checkAndSetModelSee, [1,0, 2.0] )
        self.assertRaises( TypeError, checkAndSetModelSee, 1.0 )

        # Wrong specifier.
        self.assertRaises( ValueError, checkAndSetModelSee, "Magic" )

        # Return from ok input.
        self.assertEqual( checkAndSetModelSee( "RPA" ), "RPA" )
        self.assertEqual( checkAndSetModelSee( "BMA" ), "BMA" )
        self.assertEqual( checkAndSetModelSee( "BMA+sLFC" ), "BMA+sLFC" )

    def testCheckAndSetModelSbf(self):
        """ Test the Sbf model check'n'set function."""
        # Default.
        self.assertEqual( checkAndSetModelSbf( None ), "IA" )

        # Wrong type.
        self.assertRaises( TypeError, checkAndSetModelSbf, [1,0, 2.0] )
        self.assertRaises( TypeError, checkAndSetModelSbf, 1.0 )

        # Wrong specifier.
        self.assertRaises( ValueError, checkAndSetModelSbf, "Magic" )

        # Return from ok input.
        self.assertEqual( checkAndSetModelSbf( "FFA" ), "FFA" )
        self.assertEqual( checkAndSetModelSbf( "IA" ), "IA" )
        self.assertEqual( checkAndSetModelSbf( "IBA" ), "IBA" )

    def testCheckAndSetModelIPL(self):
        """ Test the IPL model check'n'set function."""
        # Default.
        self.assertEqual( checkAndSetModelIPL( None ), "SP" )

        # Wrong type.
        self.assertRaises( TypeError, checkAndSetModelIPL, [1,0, 2.0] )

        # Wrong specifier.
        self.assertRaises( ValueError, checkAndSetModelIPL, "Magic" )

        # Return from ok input.
        self.assertEqual( checkAndSetModelIPL( "SP" ), "SP" )
        self.assertEqual( checkAndSetModelIPL( "EK" ), "EK" )
        self.assertEqual( checkAndSetModelIPL( -10.0 ), -10.0 )

    def testCheckAndSetSourceSpectrum(self):
        """ Test the source spectrum check'n'set function. """
        # Default.
        self.assertEqual( checkAndSetSourceSpectrum( None ), "GAUSS" )

        # Return from sane input.
        self.assertEqual( checkAndSetSourceSpectrum( "Gauss" ), "GAUSS" )
        self.assertEqual( checkAndSetSourceSpectrum( "Lorentz" ), "LORENTZ" )
        self.assertEqual( checkAndSetSourceSpectrum( "prop" ), "PROP" )

        # Wrong type.
        self.assertRaises( TypeError, checkAndSetSourceSpectrum, ["GAUSS", 1.0] )

        # Wrong value.
        self.assertRaises( ValueError, checkAndSetSourceSpectrum, "VOIGT" )

    def testCheckAndSetSourceSpectrumFWHM(self):
        """ Test the source spectrum fwhm check'n'set function. """
        # Default.
        self.assertEqual( checkAndSetSourceSpectrumFWHM( None ), 5.0 )

        # Return from sane input.
        self.assertEqual( checkAndSetSourceSpectrumFWHM( 5.9 ), 5.9 )

        # Wrong type.
        self.assertRaises( TypeError, checkAndSetSourceSpectrumFWHM, ["GAUSS", 1.0] )

        # Wrong value.
        self.assertRaises( ValueError, checkAndSetSourceSpectrumFWHM, 0.0 )
        self.assertRaises( ValueError, checkAndSetSourceSpectrumFWHM, -10.0 )

    def testSetSourceSpectrumFlags(self):
        """ Test the setter for the internal source spectrum flags. """

        # Check default.
        xrts_parameters = self.xrts_parameters
        self.assertEqual( xrts_parameters._PlasmaXRTSCalculatorParameters__use_source_spectrum_file, 0 )
        self.assertEqual( xrts_parameters._PlasmaXRTSCalculatorParameters__source_spectrum_identifier, 'GAUSSIAN' )
        self.assertEqual( xrts_parameters._PlasmaXRTSCalculatorParameters__source_spectrum_fwhm, 5.0 )

        # Check Gauss
        xrts_parameters.source_spectrum = 'Gauss'
        self.assertEqual( xrts_parameters._PlasmaXRTSCalculatorParameters__use_source_spectrum_file, 0 )
        self.assertEqual( xrts_parameters._PlasmaXRTSCalculatorParameters__source_spectrum_identifier, 'GAUSSIAN' )
        self.assertEqual( xrts_parameters._PlasmaXRTSCalculatorParameters__source_spectrum_fwhm, 5.0 )

        # Check Lorentz
        xrts_parameters.source_spectrum = 'Lorentz'
        self.assertEqual( xrts_parameters._PlasmaXRTSCalculatorParameters__use_source_spectrum_file, 0 )
        self.assertEqual( xrts_parameters._PlasmaXRTSCalculatorParameters__source_spectrum_identifier, 'LORENTZIAN' )
        self.assertEqual( xrts_parameters._PlasmaXRTSCalculatorParameters__source_spectrum_fwhm, 5.0 )

        # Check prop.
        xrts_parameters.source_spectrum = 'prop'
        self.assertEqual( xrts_parameters._PlasmaXRTSCalculatorParameters__use_source_spectrum_file, 1 )
        self.assertEqual( xrts_parameters._PlasmaXRTSCalculatorParameters__source_spectrum_identifier, 'GAUSSIAN' )
        self.assertEqual( xrts_parameters._PlasmaXRTSCalculatorParameters__source_spectrum_fwhm, 5.0 )

    def testSetSeeFlagsRPA(self):
        """ Test the internal conversion of the See model into use_* flags. """

        # Check default.
        xrts_parameters = self.xrts_parameters

        self.assertEqual( xrts_parameters._PlasmaXRTSCalculatorParameters__use_rpa,         1 )
        self.assertEqual( xrts_parameters._PlasmaXRTSCalculatorParameters__use_bma,         0 )
        self.assertEqual( xrts_parameters._PlasmaXRTSCalculatorParameters__use_bma_slfc,    0 )
        self.assertEqual( xrts_parameters._PlasmaXRTSCalculatorParameters__write_bma,       0 )
        self.assertEqual( xrts_parameters._PlasmaXRTSCalculatorParameters__use_lindhard,    0 )
        self.assertEqual( xrts_parameters._PlasmaXRTSCalculatorParameters__use_dynamic_lfc, 0 )
        self.assertEqual( xrts_parameters._PlasmaXRTSCalculatorParameters__use_static_lfc,  0 )
        self.assertEqual( xrts_parameters._PlasmaXRTSCalculatorParameters__use_mff,         0 )

        # Check RPA.
        xrts_parameters.model_See = 'RPA'

        self.assertEqual( xrts_parameters._PlasmaXRTSCalculatorParameters__use_rpa,         1 )
        self.assertEqual( xrts_parameters._PlasmaXRTSCalculatorParameters__use_bma,         0 )
        self.assertEqual( xrts_parameters._PlasmaXRTSCalculatorParameters__use_bma_slfc,    0 )
        self.assertEqual( xrts_parameters._PlasmaXRTSCalculatorParameters__write_bma,       0 )
        self.assertEqual( xrts_parameters._PlasmaXRTSCalculatorParameters__use_lindhard,    0 )
        self.assertEqual( xrts_parameters._PlasmaXRTSCalculatorParameters__use_dynamic_lfc, 0 )
        self.assertEqual( xrts_parameters._PlasmaXRTSCalculatorParameters__use_static_lfc,  0 )
        self.assertEqual( xrts_parameters._PlasmaXRTSCalculatorParameters__use_mff,         0 )

        # Check RPA.
        xrts_parameters.model_See = None

        self.assertEqual( xrts_parameters._PlasmaXRTSCalculatorParameters__use_rpa,         1 )
        self.assertEqual( xrts_parameters._PlasmaXRTSCalculatorParameters__use_bma,         0 )
        self.assertEqual( xrts_parameters._PlasmaXRTSCalculatorParameters__use_bma_slfc,    0 )
        self.assertEqual( xrts_parameters._PlasmaXRTSCalculatorParameters__write_bma,       0 )
        self.assertEqual( xrts_parameters._PlasmaXRTSCalculatorParameters__use_lindhard,    0 )
        self.assertEqual( xrts_parameters._PlasmaXRTSCalculatorParameters__use_dynamic_lfc, 0 )
        self.assertEqual( xrts_parameters._PlasmaXRTSCalculatorParameters__use_static_lfc,  0 )
        self.assertEqual( xrts_parameters._PlasmaXRTSCalculatorParameters__use_mff,         0 )

    def testSetSeeFlagsBMA(self):
        """ Test the internal conversion of the See model into use_* flags. """

        # Check BMA.
        xrts_parameters = self.xrts_parameters
        xrts_parameters.model_See = 'BMA'

        self.assertEqual( xrts_parameters._PlasmaXRTSCalculatorParameters__use_rpa,         0 )
        self.assertEqual( xrts_parameters._PlasmaXRTSCalculatorParameters__use_bma,         1 )
        self.assertEqual( xrts_parameters._PlasmaXRTSCalculatorParameters__use_bma_slfc,    0 )
        self.assertEqual( xrts_parameters._PlasmaXRTSCalculatorParameters__write_bma,       1 )
        self.assertEqual( xrts_parameters._PlasmaXRTSCalculatorParameters__use_lindhard,    0 )
        self.assertEqual( xrts_parameters._PlasmaXRTSCalculatorParameters__use_dynamic_lfc, 0 )
        self.assertEqual( xrts_parameters._PlasmaXRTSCalculatorParameters__use_static_lfc,  0 )
        self.assertEqual( xrts_parameters._PlasmaXRTSCalculatorParameters__use_mff,         0 )

        # Check BMA+sLFC.
        xrts_parameters.model_See = 'BMA+sLFC'
        self.assertEqual( xrts_parameters._PlasmaXRTSCalculatorParameters__use_rpa,         0 )
        self.assertEqual( xrts_parameters._PlasmaXRTSCalculatorParameters__use_bma,         0 )
        self.assertEqual( xrts_parameters._PlasmaXRTSCalculatorParameters__use_bma_slfc,    1 )
        self.assertEqual( xrts_parameters._PlasmaXRTSCalculatorParameters__write_bma,       1 )
        self.assertEqual( xrts_parameters._PlasmaXRTSCalculatorParameters__use_lindhard,    0 )
        self.assertEqual( xrts_parameters._PlasmaXRTSCalculatorParameters__use_dynamic_lfc, 0 )
        self.assertEqual( xrts_parameters._PlasmaXRTSCalculatorParameters__use_static_lfc,  0 )
        self.assertEqual( xrts_parameters._PlasmaXRTSCalculatorParameters__use_mff,         0 )

    def testSetSiiFlags(self):
        """ Test setting the internal Sii usage flags. """
        # Setup parameters object.
        xrts_parameters = self.xrts_parameters

        self.assertEqual( xrts_parameters._PlasmaXRTSCalculatorParameters__Sii_value, 0.0 )
        self.assertEqual( xrts_parameters._PlasmaXRTSCalculatorParameters__use_Sii_value, 0 )

        xrts_parameters.model_Sii = 'DH'
        self.assertEqual( xrts_parameters._PlasmaXRTSCalculatorParameters__Sii_value, 0.0 )
        self.assertEqual( xrts_parameters._PlasmaXRTSCalculatorParameters__use_Sii_value, 0 )

        xrts_parameters.model_Sii = 'OCP'
        self.assertEqual( xrts_parameters._PlasmaXRTSCalculatorParameters__Sii_value, 0.0 )
        self.assertEqual( xrts_parameters._PlasmaXRTSCalculatorParameters__use_Sii_value, 0 )

        xrts_parameters.model_Sii = 'SOCP'
        self.assertEqual( xrts_parameters._PlasmaXRTSCalculatorParameters__Sii_value, 0.0 )
        self.assertEqual( xrts_parameters._PlasmaXRTSCalculatorParameters__use_Sii_value, 0 )

        xrts_parameters.model_Sii = 'SOCPN'
        self.assertEqual( xrts_parameters._PlasmaXRTSCalculatorParameters__Sii_value, 0.0 )
        self.assertEqual( xrts_parameters._PlasmaXRTSCalculatorParameters__use_Sii_value, 0 )

        xrts_parameters.model_Sii = 1.5
        self.assertEqual( xrts_parameters._PlasmaXRTSCalculatorParameters__Sii_value, 1.5 )
        self.assertEqual( xrts_parameters._PlasmaXRTSCalculatorParameters__use_Sii_value, 1 )
        self.assertEqual( xrts_parameters.model_Sii, 'USR' )

    def testSetSbfNormFlags(self):
        """ Test setting the internal Sbf norm flags. """
        # Get default parameters.
        xrts_parameters = self.xrts_parameters

        # Check.
        self.assertEqual( xrts_parameters._PlasmaXRTSCalculatorParameters__Sbf_norm, 'FK' )
        self.assertEqual( xrts_parameters._PlasmaXRTSCalculatorParameters__Sbf_norm_value, 0.0 )

        xrts_parameters.Sbf_norm = 'FK'
        # Check.
        self.assertEqual( xrts_parameters._PlasmaXRTSCalculatorParameters__Sbf_norm, 'FK' )
        self.assertEqual( xrts_parameters._PlasmaXRTSCalculatorParameters__Sbf_norm_value, 0.0 )

        xrts_parameters.Sbf_norm = 'NO'
        # Check.
        self.assertEqual( xrts_parameters._PlasmaXRTSCalculatorParameters__Sbf_norm, 'NO' )
        self.assertEqual( xrts_parameters._PlasmaXRTSCalculatorParameters__Sbf_norm_value, 0.0 )

        xrts_parameters.Sbf_norm = .1435
        # Check.
        self.assertEqual( xrts_parameters._PlasmaXRTSCalculatorParameters__Sbf_norm, 'USR' )
        self.assertEqual( xrts_parameters._PlasmaXRTSCalculatorParameters__Sbf_norm_value, 0.1435 )

    def testSetDebyeTemperatureFlags(self):
        """ Check setting the internal Debye temperature flags. """
        # Get default parameters.
        xrts_parameters = self.xrts_parameters
        # Check.
        self.assertEqual( xrts_parameters.debye_temperature, None )
        self.assertEqual( xrts_parameters._PlasmaXRTSCalculatorParameters__debye_temperature_value, 0.0 )
        self.assertEqual( xrts_parameters._PlasmaXRTSCalculatorParameters__use_debye_temperature, 0 )

        xrts_parameters.debye_temperature = 1.0
        # Check.
        self.assertEqual( xrts_parameters.debye_temperature, 1.0 )
        self.assertEqual( xrts_parameters._PlasmaXRTSCalculatorParameters__debye_temperature_value, 1.0 )
        self.assertEqual( xrts_parameters._PlasmaXRTSCalculatorParameters__use_debye_temperature, 1 )

    def testSetBandGapFlags(self):
        """ Check setting the internal bandgap flags. """
        # Get default parameters.
        xrts_parameters = self.xrts_parameters
        # Check.
        self.assertEqual( xrts_parameters.band_gap, None )
        self.assertEqual( xrts_parameters._PlasmaXRTSCalculatorParameters__band_gap_value, 0.0 )
        self.assertEqual( xrts_parameters._PlasmaXRTSCalculatorParameters__use_band_gap, 0 )

        xrts_parameters.band_gap = 1.234
        # Check.
        self.assertEqual( xrts_parameters.band_gap, 1.234 )
        self.assertEqual( xrts_parameters._PlasmaXRTSCalculatorParameters__band_gap_value, 1.234 )
        self.assertEqual( xrts_parameters._PlasmaXRTSCalculatorParameters__use_band_gap, 1 )

    def testSetIPLFlags(self):
        """ Check setting the internal IPL flags. """
        # Get default parameters.
        xrts_parameters = self.xrts_parameters
        # Check.
        self.assertEqual( xrts_parameters.model_IPL, 'SP' )
        self.assertEqual( xrts_parameters._PlasmaXRTSCalculatorParameters__ipl_value, 0.0 )

        xrts_parameters.model_IPL = 1.234
        # Check.
        self.assertEqual( xrts_parameters.model_IPL, 'USR' )
        self.assertEqual( xrts_parameters._PlasmaXRTSCalculatorParameters__ipl_value, 1.234 )

    def testSerialize(self):
        """ Test the serialization of parameters into input deck."""

        # Setup parameters object.
        xrts_parameters = self.xrts_parameters

        xrts_parameters._serialize()

        # Check that the input deck has been generated.
        self.assertTrue( os.path.isdir( xrts_parameters._tmp_dir ) )

        self.assertTrue( 'input.dat' in os.listdir( xrts_parameters._tmp_dir ) )

if __name__ == '__main__':
    unittest.main()

