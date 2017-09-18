""" Test module for the PlasmaXRTSCalculator.  """
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

import h5py
import numpy
import os
import shutil
import unittest

# Include needed directories in sys.path.
import paths

from SimEx.Parameters.PlasmaXRTSCalculatorParameters import PlasmaXRTSCalculatorParameters
from SimEx.Calculators.AbstractPhotonDiffractor import AbstractPhotonDiffractor
from SimEx.Calculators.AbstractBaseCalculator import AbstractBaseCalculator
from TestUtilities import TestUtilities

# Import the class to test.
from SimEx.Calculators.PlasmaXRTSCalculator import PlasmaXRTSCalculator
from SimEx.Calculators.PlasmaXRTSCalculator import _parseStaticData


class PlasmaXRTSCalculatorTest(unittest.TestCase):
    """
    Test class for the PlasmaXRTSCalculator class.
    """

    @classmethod
    def setUpClass(cls):
        """ Setting up the test class. """
        cls.input_path = TestUtilities.generateTestFilePath('')

    @classmethod
    def tearDownClass(cls):
        """ Tearing down the test class. """
        del cls.input_path

    def setUp(self):
        """ Setting up a test. """
        self.__files_to_remove = []
        self.__dirs_to_remove = []

        # Setup parameters.
        self.xrts_parameters = PlasmaXRTSCalculatorParameters(
                            elements=[['Be', 1, -1]],
                            photon_energy=4.96e3,
                            electron_density=3.0e23,
                            electron_temperature=10.0,
                            ion_charge=2.3,
                            scattering_angle=90.,
                            )

    def tearDown(self):
        """ Tearing down a test. """
        for f in self.__files_to_remove:
            if os.path.isfile(f):
                os.remove(f)
        for d in self.__dirs_to_remove:
            if os.path.isdir(d):
                shutil.rmtree(d)
        del self.xrts_parameters

    def testConstruction(self):
        """ Testing the default construction of the class. """

        # Attempt to construct an instance of the class.
        xrts_calculator = PlasmaXRTSCalculator(parameters=self.xrts_parameters,
                                               input_path=self.input_path,
                                               output_path='xrts_out')

        # Check instance and inheritance.
        self.assertIsInstance( xrts_calculator, PlasmaXRTSCalculator )
        self.assertIsInstance( xrts_calculator, AbstractPhotonDiffractor )
        self.assertIsInstance( xrts_calculator, AbstractBaseCalculator )

        # Check attributes are initialized.
        self.assertEqual( xrts_calculator._input_data, {} )

    def testConstructionParameters(self):
        """ Testing the input parameter checks pass for a sane parameter dict. """

        # Construct an instance.
        xrts_calculator = PlasmaXRTSCalculator( parameters=self.xrts_parameters,
                                                input_path=self.input_path,
                                                output_path='xrts_out'
                                              )

        # Query the parameters.
        query = xrts_calculator.parameters

        # Check query is ok.
        self.assertIsInstance( query, PlasmaXRTSCalculatorParameters )

        # Check attributes are initialized.
        self.assertEqual( xrts_calculator._input_data, {})

    def testBackengine(self):
        """ Check that the backengine can be executed and output is generated. """

        # Setup parameters.
        xrts_parameters = self.xrts_parameters

        # Construct an instance.
        xrts_calculator = PlasmaXRTSCalculator( parameters=xrts_parameters,
                                                input_path=self.input_path,
                                                output_path='xrts_out'
                                              )

        # Call the backengine.
        xrts_calculator.backengine()

        # Check for output.
        self.assertTrue( os.path.isdir( xrts_calculator.parameters._tmp_dir ) )
        self.assertTrue( 'xrts_out.txt' in os.listdir( xrts_calculator.parameters._tmp_dir ) )
        self.assertTrue( 'xrts.log' in os.listdir( xrts_calculator.parameters._tmp_dir ) )

        # Check log content.
        self.assertIn( "SUMMARY TABLE", xrts_calculator._PlasmaXRTSCalculator__run_log )
        # Check data shape.
        self.assertEqual( xrts_calculator._PlasmaXRTSCalculator__run_data.shape, (201, 4 ) )

    def testSaveH5(self):
        """ Test hdf5 output generation. """
        # Make sure we clean up after ourselves.
        outfile = 'xrts_out.h5'
        self.__files_to_remove.append(outfile)

        # Setup parameters.
        xrts_parameters = self.xrts_parameters


        # Construct an instance.
        xrts_calculator = PlasmaXRTSCalculator( parameters=xrts_parameters,
                                                input_path=self.input_path,
                                                output_path=outfile
                                              )

        # Call the backengine.
        xrts_calculator.backengine()

        # Save to h5
        xrts_calculator.saveH5()

        # Check output was written.
        self.assertTrue( os.path.isfile( xrts_calculator.output_path ) )

        # Open the file for reading.
        h5 = h5py.File( xrts_calculator.output_path, 'r' )

        # Check that the all data to be provided is present.
        for key in xrts_calculator.providedData():
            group = key.split('/')[1]
            self.assertTrue( group in h5.keys() )

        # Check dynamic datasets shapes and units.
        self.assertEqual( numpy.array( h5['data/dynamic/']['energy_shifts']).shape, (201,) )
        self.assertEqual( str( h5['data/dynamic/']['energy_shifts'].attrs['unit']), 'eV')

        self.assertEqual( numpy.array( h5['data/dynamic/']['Skw_free']).shape,      (201,) )
        self.assertEqual( str( h5['data/dynamic/']['Skw_free'].attrs['unit']), 'eV**-1')

        self.assertEqual( numpy.array( h5['data/dynamic/']['Skw_bound']).shape,     (201,) )
        self.assertEqual( str( h5['data/dynamic/']['Skw_bound'].attrs['unit']), 'eV**-1')

        self.assertEqual( numpy.array( h5['data/dynamic/']['Skw_total']).shape,     (201,) )
        self.assertEqual( str( h5['data/dynamic/']['Skw_total'].attrs['unit']), 'eV**-1')

        # Check static data.
        self.assertAlmostEqual( h5['data/static']['fk'].value,          1.532,  3)
        self.assertAlmostEqual( h5['data/static']['qk'].value,          0.4427, 4)
        self.assertAlmostEqual( h5['data/static']['Sk_ion'].value,      1.048,  3)
        self.assertAlmostEqual( h5['data/static']['Sk_free'].value,     0.8075, 4)
        self.assertAlmostEqual( h5['data/static']['Sk_core'].value,     0.0601, 4)
        self.assertAlmostEqual( h5['data/static']['Wk'].value,          4.084 ,  2)
        self.assertAlmostEqual( h5['data/static']['Sk_total'].value,    6.002,  3)
        self.assertAlmostEqual( h5['data/static']['ipl'].value,        38.353,  3)
        # IPL has a unit.
        self.assertEqual( h5['data/static']['ipl'].attrs['unit'], 'eV')
        self.assertAlmostEqual( h5['data/static']['lfc'].value,         0.000 , 3)
        self.assertAlmostEqual( h5['data/static']['debye_waller'].value,1.000 , 3)


    def testParseStaticDebyeWaller1(self):
        """ Test the parser to extract static dat from the log Debye-Waller factor = 1. """
        # Setup a log.
        log_text = """ ----------------------------------------
Reading parameters from input file ......done.
Initializing ...... done.
Reading input data file ...... done.
Initializing element properties ...... done.
Calculating average state of the system ...
Electron Density - Zfree lock is enabled.
... done
Initializing instrument function ...... done.
Init bound states ... ... done.
NSPEC=2
Initializing static structure factors ...... done.
Lineshape construction:

Init vectors ...... done.
Writing spectrum to file ...... done.
Free memory ...... done.

SUMMARY TABLE

Target             = Be1
SPECIE 1           = Be (Zf = 2.3, Zb = 1.7)
Mass den.   [g/cc] = 1.85
Wavelength    [nm] = 0.25 (4960.0 eV)
Theta        [deg] = 90.00
k(w=0)      [m^-1] = 3.555E+10
Te            [eV] =  10 (1.16E+05 K)
ne         [cm^-3] = 2.843E+23
Zfree/ion average  = 2.3
Zbound/ion average = 1.7
Zhopping           = 0.9695
L_kx           [m] =   0
T_wx           [s] =   0
Amplitude          =   1
Baseline           =   0
Ion At. Num. av.   = 9.012
Tion          [eV] =  10
Zfree/molecule     = 2.3
Tf non rel    [eV] = 15.77
Tf            [eV] = 15.77
Tquantum      [eV] = 14.5
Tclas         [eV] = 17.61
Compton shift [eV] = 47.68
l_compton      [m] = 3.482E-11
l_debye        [m] = 4.409E-11
dis            [m] = 9.434E-11
Alpha              = 0.481
rs                 = 1.783
Gamma_ee_0         = 1.526
Gamma_ee_fermi     = 0.968
Gamma_ee           = 0.867
Gamma_ii           = 6.117
wpe         [s^-1] = 3.008E+16 (19.8 eV)
k vt        [s^-1] = 6.256E+16 (41.18 eV)
k vF        [s^-1] = 8.372E+16 (55.1 eV)
k dis              = 3.354
k l_debye          = 1.567
l_compton/dis      = 0.369
G(k)               = 0.000
IP depression [eV] = 37.683
Free_inelastic(k)  = 1.868
Elastic(k)         = 4.07
Core_inelastic(k)  = 0.0591
S_total(k)         = 5.997
Peak ratio         = 0.459
f(k)               = 1.513
q(k)               = 0.4319
1-f(k)^2/Zb        = -0.3469
S_ee^0(k)          = 0.8122
S_ii(k)            = 1.076
Static correction  = 0.1622
Debye-Waller       =   1
Charge calculated without IRS model
data for curve fitting saved on file: xrts_out.txt

User time: 12.4 seconds
Real time: 12.0 seconds
"""
        static_dict = _parseStaticData( log_text )

        # Check keys.
        static_data_keys = static_dict.keys()
        self.assertIn( 'fk',            static_data_keys )
        self.assertIn( 'qk',            static_data_keys )
        self.assertIn( 'Sk_ion',        static_data_keys )
        self.assertIn( 'Sk_free',       static_data_keys )
        self.assertIn( 'Sk_core',       static_data_keys )
        self.assertIn( 'Wk',            static_data_keys )
        self.assertIn( 'Sk_total',      static_data_keys )
        self.assertIn( 'ipl',           static_data_keys )
        self.assertIn( 'lfc',           static_data_keys )
        self.assertIn( 'debye_waller',  static_data_keys )

    def testParseStaticDebyeWallerFloat(self):
        """ Test the parser to extract static dat from the log Debye-Waller factor = some float. """
        # Setup a log.
        log_text = """ ----------------------------------------
Reading parameters from input file ......done.
Initializing ...... done.
Reading input data file ...... done.
Initializing element properties ...... done.
Calculating average state of the system ...
Electron Density - Zfree lock is enabled.
... done
Initializing instrument function ...... done.
Init bound states ... ... done.
NSPEC=2
Initializing static structure factors ...... done.
Lineshape construction:

Init vectors ...... done.
Writing spectrum to file ...... done.
Free memory ...... done.

SUMMARY TABLE

Target             = Be1
SPECIE 1           = Be (Zf = 2.3, Zb = 1.7)
Mass den.   [g/cc] = 1.85
Wavelength    [nm] = 0.25 (4960.0 eV)
Theta        [deg] = 90.00
k(w=0)      [m^-1] = 3.555E+10
Te            [eV] =  10 (1.16E+05 K)
ne         [cm^-3] = 2.843E+23
Zfree/ion average  = 2.3
Zbound/ion average = 1.7
Zhopping           = 0.9695
L_kx           [m] =   0
T_wx           [s] =   0
Amplitude          =   1
Baseline           =   0
Ion At. Num. av.   = 9.012
Tion          [eV] =  10
Zfree/molecule     = 2.3
Tf non rel    [eV] = 15.77
Tf            [eV] = 15.77
Tquantum      [eV] = 14.5
Tclas         [eV] = 17.61
Compton shift [eV] = 47.68
l_compton      [m] = 3.482E-11
l_debye        [m] = 4.409E-11
dis            [m] = 9.434E-11
Alpha              = 0.481
rs                 = 1.783
Gamma_ee_0         = 1.526
Gamma_ee_fermi     = 0.968
Gamma_ee           = 0.867
Gamma_ii           = 6.117
wpe         [s^-1] = 3.008E+16 (19.8 eV)
k vt        [s^-1] = 6.256E+16 (41.18 eV)
k vF        [s^-1] = 8.372E+16 (55.1 eV)
k dis              = 3.354
k l_debye          = 1.567
l_compton/dis      = 0.369
G(k)               = 0.000
IP depression [eV] = 37.683
Free_inelastic(k)  = 1.868
Elastic(k)         = 4.07
Core_inelastic(k)  = 0.0591
S_total(k)         = 5.997
Peak ratio         = 0.459
f(k)               = 1.513
q(k)               = 0.4319
1-f(k)^2/Zb        = -0.3469
S_ee^0(k)          = 0.8122
S_ii(k)            = 1.076
Static correction  = 0.1622
Debye-Waller       = 1.2345
Charge calculated without IRS model
data for curve fitting saved on file: xrts_out.txt

User time: 12.4 seconds
Real time: 12.0 seconds
"""
        static_dict = _parseStaticData( log_text )

        # Check keys.
        static_data_keys = static_dict.keys()
        self.assertIn( 'fk',            static_data_keys )
        self.assertIn( 'qk',            static_data_keys )
        self.assertIn( 'Sk_ion',        static_data_keys )
        self.assertIn( 'Sk_free',       static_data_keys )
        self.assertIn( 'Sk_core',       static_data_keys )
        self.assertIn( 'Wk',            static_data_keys )
        self.assertIn( 'Sk_total',      static_data_keys )
        self.assertIn( 'ipl',           static_data_keys )
        self.assertIn( 'lfc',           static_data_keys )
        self.assertIn( 'debye_waller',  static_data_keys )

    def testReadH5(self):
        """ Test the readH5 function to read input from the photon propagator. """
        # Construct parameters.
        xrts_parameters = self.xrts_parameters

        xrts_calculator = PlasmaXRTSCalculator( parameters=xrts_parameters,
                                                input_path=TestUtilities.generateTestFilePath('prop_out_0000001.h5'),
                                                output_path='xrts_out.h5')


        xrts_calculator._readH5()

        self.assertIn( 'source_spectrum', xrts_calculator._input_data.keys() )


        e = xrts_calculator._input_data['source_spectrum'][:,0]
        s = xrts_calculator._input_data['source_spectrum'][:,1]

        ### For local testing only.
        #import pylab
        #pylab.plot(e, s)
        #pylab.show()

    def testSerializeSourceSpectrum(self):
        """ Test saving the source spectrum to file in the correct location. """
        # Construct parameters.
        xrts_parameters = self.xrts_parameters

        xrts_calculator = PlasmaXRTSCalculator( parameters=xrts_parameters,
                                                input_path=TestUtilities.generateTestFilePath('prop_out_0000001.h5'),
                                                output_path='xrts_out.h5')


        xrts_calculator._readH5()

        xrts_parameters.source_spectrum = 'prop'

        xrts_parameters._serialize()

        xrts_calculator._serializeSourceSpectrum()

        self.assertTrue( 'source_spectrum.txt' in os.listdir( xrts_parameters._tmp_dir ) )

    def testBackengineWithSpectrum(self):
        """ Test saving the source spectrum to file in the correct location. """
        # Construct parameters.
        xrts_parameters = self.xrts_parameters

        xrts_calculator = PlasmaXRTSCalculator( parameters=xrts_parameters,
                                                input_path=TestUtilities.generateTestFilePath('prop_out_0000001.h5'),
                                                output_path='xrts_out.h5')

        # Read in the data.
        xrts_calculator._readH5()

        # Specify that we want to use the measured source spectrum.
        xrts_parameters.source_spectrum = 'prop'
        xrts_parameters.energy_range = {'min' :-300.0,
                                        'max' :300.0,
                                        'step':3.,
                                       }


        # Run the backengine.
        xrts_calculator.backengine()


    def notestBackengineWithWPGOut(self):
        """ Test that extracting the spectrum from a wpg output works. """
        """ notested because requires file not in TestFiles. """
        # Construct parameters.
        xrts_parameters = self.xrts_parameters

        xrts_calculator = PlasmaXRTSCalculator( parameters=xrts_parameters,
                                                input_path='prop_out.h5',
                                                output_path='xrts_out.h5')

        # Read in the data.
        xrts_calculator._readH5()

        # Specify that we want to use the measured source spectrum.
        xrts_parameters.source_spectrum = 'prop'
        xrts_parameters.energy_range = {'min' :-300.0,
                                        'max' :300.0,
                                        'step':3.,
                                       }


        # Run the backengine.
        xrts_calculator.backengine()

        self.assertTrue( 'source_spectrum.txt' in os.listdir( xrts_parameters._tmp_dir ) )


    def testPhotonEnergyConsistency(self):
        """ Test that an exception is thrown if the given photon energy is not equal to the source photon energy. """
        # Construct parameters.
        xrts_parameters = self.xrts_parameters

        xrts_calculator = PlasmaXRTSCalculator( parameters=xrts_parameters,
                                                input_path=TestUtilities.generateTestFilePath('prop_out_0000001.h5'),
                                                output_path='xrts_out.h5')
        # Should print a warning.
        xrts_calculator.parameters.photon_energy = 5.0e3




    def testBackengineWithGauss(self):
        """ Test saving the source spectrum to file in the correct location. """
        # Construct parameters.
        xrts_parameters = self.xrts_parameters

        xrts_calculator = PlasmaXRTSCalculator( parameters=xrts_parameters,
                                                input_path=TestUtilities.generateTestFilePath('prop_out_0000001.h5'),
                                                output_path='xrts_out.h5')

        # Read in the data.
        xrts_calculator._readH5()

        # Specify that we want to use the measured source spectrum.
        xrts_parameters.source_spectrum_fwhm=1.0
        xrts_parameters.energy_range = {'min' :-200.0,
                                        'max' :200.0,
                                        'step':2.,
                                          }


        # Run the backengine.
        xrts_calculator.backengine()


if __name__ == '__main__':
    unittest.main()

