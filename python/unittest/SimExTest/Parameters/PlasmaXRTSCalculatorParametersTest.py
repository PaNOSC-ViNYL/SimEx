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
import paths
import os
import numpy
import shutil
import subprocess

# Include needed directories in sys.path.
import paths
import unittest


# Import the class to test.
from SimEx.Parameters.PlasmaXRTSCalculatorParameters import PlasmaXRTSCalculatorParameters
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
                                                         electron_temperature=10.0,
                                                         electron_density=1.0e23,
                                                         ion_charge=2.3)


        # Check instance and inheritance.
        self.assertIsInstance( xrts_parameters, PlasmaXRTSCalculatorParameters )

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

        # Case 3: Inconsistent input.
        self.assertRaises( ValueError, checkAndSetDensitiesAndCharge, 1e19, 2.3, 5.0 )

        # Case 4: Get correct number density based on charge and mass density.
        ed, Z, rho = checkAndSetDensitiesAndCharge( None, 2.3, 5.0 )
        self.assertAlmostEqual( ed/1.e30, 6.92546, 4 )
        ed, Z, rho = checkAndSetDensitiesAndCharge( ed, None, 5.0 )
        self.assertAlmostEqual( Z, 2.3, 4 )
        ed, Z, rho = checkAndSetDensitiesAndCharge( ed, 2.3, None )
        self.assertAlmostEqual( rho, 5.0, 4 )


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
        self.assertEqual( checkAndSetDebyeTemperature( None), 0.0 )

        # Check incorrect type.
        self.assertRaises( TypeError, checkAndSetDebyeTemperature, "1.0")
        # Zero.
        self.assertRaises( ValueError, checkAndSetDebyeTemperature, 0.0)
        # Negative.
        self.assertRaises( ValueError, checkAndSetDebyeTemperature, -10.0)

    def testCheckAndSetBandGap(self):
        """ Test the bandgap check'n'set function."""
        # Default
        self.assertEqual( checkAndSetBandGap( None), 0.0 )

        # Check incorrect type.
        self.assertRaises( TypeError, checkAndSetBandGap, "1.0")
        # Negative.
        self.assertRaises( ValueError, checkAndSetBandGap, -10.0)


    def testCheckAndSetModelMix(self):
        """ Test the mixing model check'n'set function."""
        # Default
        self.assertEqual( checkAndSetModelMix( None ), 0)

        # Check malformed input.
        self.assertRaises( TypeError, checkAndSetModelMix, "halleluja")
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
        self.assertTrue(False)

    def testCheckAndSetEnergyRan(self):
        """ Test the <++> check'n'set function."""
        self.assertTrue(False)

    def testCheckAndSetModelSii(self):
        """ Test the <++> check'n'set function."""
        self.assertTrue(False)

    def testCheckAndSetModelSee(self):
        """ Test the <++> check'n'set function."""
        self.assertTrue(False)

    def testCheckAndSetModelSbf(self):
        """ Test the <++> check'n'set function."""
        self.assertTrue(False)

    def testCheckAndSetModelIPL(self):
        """ Test the <++> check'n'set function."""
        self.assertTrue(False)



if __name__ == '__main__':
    unittest.main()

