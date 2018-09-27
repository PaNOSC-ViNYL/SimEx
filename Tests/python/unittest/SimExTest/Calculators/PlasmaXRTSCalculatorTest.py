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
from SimEx.Parameters.PlasmaXRTSCalculatorParameters import PlasmaXRTSCalculatorParameters
from SimEx.Calculators.AbstractPhotonDiffractor import AbstractPhotonDiffractor
from SimEx.Calculators.AbstractBaseCalculator import AbstractBaseCalculator

# Import the class to test.
from SimEx.Calculators.PlasmaXRTSCalculator import PlasmaXRTSCalculator
from SimEx.Calculators.PlasmaXRTSCalculator import _parseStaticData

from TestUtilities import TestUtilities

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
                            energy_range={'min': -50.0, 'max': 50.0, 'step': 0.5},
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
            self.assertTrue( group in list(h5.keys()) )

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
        self.assertAlmostEqual( h5['data/static']['k'].value,           3.555e10,  3)
        self.assertAlmostEqual( h5['data/static']['fk'].value,          1.532,  3)
        self.assertAlmostEqual( h5['data/static']['qk'].value,          0.4427, 4)
        self.assertAlmostEqual( h5['data/static']['Sk_ion'].value,      1.048,  3)
        self.assertAlmostEqual( h5['data/static']['Sk_free'].value,     0.8075, 4)
        self.assertAlmostEqual( h5['data/static']['Sk_core'].value,     0.05999, 4)
        self.assertAlmostEqual( h5['data/static']['Wk'].value,          4.084 ,  2)
        self.assertAlmostEqual( h5['data/static']['Sk_total'].value,    6.002,  3)
        self.assertAlmostEqual( h5['data/static']['ipl'].value,        38.35,  3)
        # IPL has a unit.
        self.assertEqual( h5['data/static']['ipl'].attrs['unit'], 'eV')
        self.assertAlmostEqual( h5['data/static']['lfc'].value,         0.000 , 3)
        self.assertAlmostEqual( h5['data/static']['debye_waller'].value,1.000 , 3)

    def testReadH5(self):
        """ Test the readH5 function to read input from the photon propagator. """
        # Construct parameters.
        xrts_parameters = self.xrts_parameters

        xrts_calculator = PlasmaXRTSCalculator( parameters=xrts_parameters,
                                                input_path=TestUtilities.generateTestFilePath('prop_out_0000001.h5'),
                                                output_path='xrts_out.h5')


        xrts_calculator._readH5()

        self.assertIn( 'source_spectrum', list(xrts_calculator._input_data.keys()) )


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

