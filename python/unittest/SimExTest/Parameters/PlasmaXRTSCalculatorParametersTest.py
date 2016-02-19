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

""" Test module for the PlasmaXRTSCalculatorParameter class.

    @author : CFG
    @institution : XFEL
    @creation 20160219

"""

import os
import numpy
import shutil
import subprocess

# Include needed directories in sys.path.
import paths
import unittest

from SimEx.Calculators.AbstractPhotonDiffractor import AbstractPhotonDiffractor
from SimEx.Calculators.AbstractBaseCalculator import AbstractBaseCalculator

# Import the class to test.
from SimEx.Calculators.PlasmaXRTSCalculator import PlasmaXRTSCalculator
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

    def tearDown(self):
        """ Tearing down a test. """
        for f in self.__files_to_remove:
            if os.path.isfile(f):
                os.remove(f)
        for d in self.__dirs_to_remove:
            if os.path.isdir(d):
                shutil.rmtree(d)

    def testConstructionDict(self):
        """ Testing the default construction of the class using a dictionary. """

        # Attempt to construct an instance of the class.
        parameters_dict =
        xrts_parameters = PlasmaXRTSCalculatorParameters(
                elements=['Be'],
                average_charge=2.0,
                scattering_angle=90.0,


        # Check instance and inheritance.
        self.assertIsInstance( xrts_calculator, PlasmaXRTSCalculator )
        self.assertIsInstance( xrts_calculator, AbstractPhotonDiffractor )
        self.assertIsInstance( xrts_calculator, AbstractBaseCalculator )

    def testCheckSaneParameters(self):
        """ Testing the input parameter checks pass for a sane parameter dict. """

        # Setup parameters.
        xrts_parameters = {'scattering_angle' : 90,
                           'photon_energy_range' : numpy.arange(-100., 100., 1.0),
                           'model_See0'          : 'RPA',
                           'model_Sii'           : 'DH',
                           'model_Sbf'           : 'IA',
                           }


        # Construct an instance.
        xrts_calculator = PlasmaXRTSCalculator( parameters=xrts_parameters,
                                                input_path=self.input_path,
                                                output_path='xrts_out'
                                              )

        # Query the parameters.
        query = xrts_calculator.parameters

        # Check query is ok.
        for key, value in xrts_parameters.items():
            print "Checking %s" % (key)
            if isinstance( value, str ):
                self.assertEqual( query[key], value )
            if isinstance( value, numpy.ndarray ):
                for i,v in enumerate(value):
                    self.assertAlmostEqual( query[key][i], v )

    def testCheckInsaneParameters(self):
        """ Testing the input parameter checks bark for insane parameter dict. """

        # Setup parameters.
        insane_parameters = {'scattering_angle' : 270,
                             'photon_energy_range' : 1.0,
                             'model_See0'          : 'NambuJonaLassino',
                             'model_Sii'           : 'KobayashiMaskawa',
                             'model_Sbf'           : 'FermiDirac',
                            }


        # Attempt construction, check should bark.
        self.assertRaises( ValueError,  PlasmaXRTSCalculator, insane_parameters, self.input_path, 'xrts_out' )

        # Cure angle.
        insane_parameters['scattering_angle'] = 91.32
        # Attempt construction, check should bark.
        self.assertRaises( TypeError,  PlasmaXRTSCalculator, parameters=insane_parameters, input_path=self.input_path, output_path='xrts_out' )

        # Cure energy range.
        insane_parameters['photon_energy_range'] = numpy.arange( -10., 10., 0.1 )
        # Attempt construction, check should bark.
        self.assertRaises( ValueError,  PlasmaXRTSCalculator, parameters=insane_parameters, input_path=self.input_path, output_path='xrts_out' )

        # Cure Sii model.
        insane_parameters['model_Sii'] = 'DH'
        # Attempt construction, check should bark.
        self.assertRaises( ValueError,  PlasmaXRTSCalculator, parameters=insane_parameters, input_path=self.input_path, output_path='xrts_out' )

        # Cure See0 model.
        insane_parameters['model_See0'] = 'BMA'
        # Attempt construction, check should bark.
        self.assertRaises( ValueError,  PlasmaXRTSCalculator, insane_parameters, self.input_path, 'xrts_out' )

        # Cure Sbf model.
        insane_parameters['model_Sbf'] = 'IA'
        # Attempt construction, check should pass.
        xrts_calculator = PlasmaXRTSCalculator( insane_parameters,
                                                self.input_path,
                                                'xrts_out')

        self.assertIsInstance( xrts_calculator, PlasmaXRTSCalculator )

    def testBackengine(self):
        """ Check that the backengine can be executed. """

        # Setup parameters.
        xrts_parameters = {'scattering_angle' : 90,
                           'photon_energy_range' : numpy.arange(-100., 100., 1.0),
                           'model_See0'          : 'RPA',
                           'model_Sii'           : 'DH',
                           'model_Sbf'           : 'IA',
                           }


        # Construct an instance.
        xrts_calculator = PlasmaXRTSCalculator( parameters=xrts_parameters,
                                                input_path=self.input_path,
                                                output_path='xrts_out'
                                              )

        # Call the backengine.
        xrts_calculator.backengine()

if __name__ == '__main__':
    unittest.main()

