""" :module: Test module for the EstherPhotonMatterInteractorParameter class. """
##########################################################################
#                                                                        #
# Copyright (C) 2016,2017 Carsten Fortmann-Grote, Richard Briggs         #
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

import os
import paths
import shutil
import unittest

from SimEx.Parameters.AbstractCalculatorParameters import AbstractCalculatorParameters

# Import the class to test.
from SimEx.Parameters.EstherPhotonMatterInteractorParameters import EstherPhotonMatterInteractorParameters
from SimEx.Parameters.EstherPhotonMatterInteractorParameters import checkAndSetAblator
from SimEx.Parameters.EstherPhotonMatterInteractorParameters import checkAndSetAblatorThickness
from SimEx.Parameters.EstherPhotonMatterInteractorParameters import checkAndSetLaserIntensity
from SimEx.Parameters.EstherPhotonMatterInteractorParameters import checkAndSetLaserPulse
from SimEx.Parameters.EstherPhotonMatterInteractorParameters import checkAndSetLaserPulseDuration
from SimEx.Parameters.EstherPhotonMatterInteractorParameters import checkAndSetLaserWavelength
from SimEx.Parameters.EstherPhotonMatterInteractorParameters import checkAndSetNumberOfLayers
from SimEx.Parameters.EstherPhotonMatterInteractorParameters import checkAndSetSample
from SimEx.Parameters.EstherPhotonMatterInteractorParameters import checkAndSetSampleThickness
from SimEx.Parameters.EstherPhotonMatterInteractorParameters import checkAndSetWindow
from SimEx.Parameters.EstherPhotonMatterInteractorParameters import checkAndSetWindowThickness

class EstherPhotonMatterInteractorParametersTest(unittest.TestCase):
    """
    Test class for the EstherPhotonMatterInteractorParameters class.
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

        self.esther_parameters = EstherPhotonMatterInteractorParameters(
                                         number_of_layers=3,
                                         ablator="CH",
                                         ablator_thickness=25.0,
                                         sample="Iron",
                                         sample_thickness=5.0,
                                         window="LiF",
                                         window_thickness=50.0,
                                         layer1="Copper",
                                         layer1_thickness=1.0,
                                         laser_wavelength=1064.0,
                                         laser_pulse='flat',
                                         laser_pulse_duration=6.0,
                                         laser_intensity=0.1,
                                         run_time=10.0,
                                         delta_time=0.05,
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
        esther_parameters = self.esther_parameters
        # Check instance and inheritance.
        self.assertIsInstance( esther_parameters, EstherPhotonMatterInteractorParameters )
        self.assertIsInstance( esther_parameters, AbstractCalculatorParameters )

    def testCheckAndSetNumberOfLayers(self):
        """ Test the check and set method for number of layers. """

        # Type raises.
        self.assertRaises( TypeError, checkAndSetNumberOfLayers, "two")
        self.assertRaises( TypeError, checkAndSetNumberOfLayers, "2")
        self.assertRaises( TypeError, checkAndSetNumberOfLayers, [2,3])
        self.assertRaises( TypeError, checkAndSetNumberOfLayers, 10.5)
        self.assertRaises( TypeError, checkAndSetNumberOfLayers, self.esther_parameters)
        self.assertRaises( TypeError, checkAndSetNumberOfLayers, {"2" : "two"})

        # Value raises.
        self.assertRaises( ValueError, checkAndSetNumberOfLayers, 0)
        self.assertRaises( ValueError, checkAndSetNumberOfLayers, 6)
        self.assertRaises( ValueError, checkAndSetNumberOfLayers, -3)

        # Ok.
        self.assertEqual( checkAndSetNumberOfLayers(3), 3)

    def testCheckAndSetAblator(self):
        """ Test the check and set method for the ablator material. """

        # Type raises.
        self.assertRaises( TypeError, checkAndSetAblator, 1 )
        self.assertRaises( TypeError, checkAndSetAblator, 1.5 )
        self.assertRaises( TypeError, checkAndSetAblator, ["Aluminum", "CH"] )

        # Value raises.
        self.assertRaises( ValueError, checkAndSetAblator, "Boron" )

        # Ok.
        self.assertEqual( checkAndSetAblator("CH"), "CH" )

    def testCheckAndSetAblatorThickness(self):
        """ Test the check and set method for the ablator thickness. """

        self.assertRaises( TypeError, checkAndSetAblatorThickness, "ten microns" )
        self.assertRaises( TypeError, checkAndSetAblatorThickness, [10.0, 10.0] )

        # Value raises.
        self.assertRaises( ValueError, checkAndSetAblatorThickness, -10.0 )
        self.assertRaises( ValueError, checkAndSetAblatorThickness, 0.0 )

        self.assertEqual( checkAndSetAblatorThickness(10.0), 10.0 )
        self.assertEqual( checkAndSetAblatorThickness(6), 6.0 )

    def testCheckAndSetSample(self):
        """ Test the check and set method for the sample material. """

        # Type raises.
        self.assertRaises( TypeError, checkAndSetSample, 1 )
        self.assertRaises( TypeError, checkAndSetSample, 1.5 )
        self.assertRaises( TypeError, checkAndSetSample, ["Aluminum", "CH"] )

        # Value raises.
        self.assertRaises( ValueError, checkAndSetSample, "Boron" )

        # Ok.
        self.assertEqual( checkAndSetSample("CH"), "CH" )

    def testCheckAndSetSampleThickness(self):
        """ Test the check and set method for the sample thickness. """

        self.assertRaises( TypeError, checkAndSetSampleThickness, "ten microns" )
        self.assertRaises( TypeError, checkAndSetSampleThickness, [10.0, 10.0] )

        # Value raises.
        self.assertRaises( ValueError, checkAndSetSampleThickness, -10.0 )
        self.assertRaises( ValueError, checkAndSetSampleThickness, 0.0 )

        self.assertEqual( checkAndSetSampleThickness(10.0), 10.0 )
        self.assertEqual( checkAndSetSampleThickness(10), 10.0 )

    def testCheckAndSetWindow(self):
        """ Test the check and set method for the sample material. """

        # Type raises.
        self.assertRaises( TypeError, checkAndSetWindow, 1 )
        self.assertRaises( TypeError, checkAndSetWindow, 1.5 )
        self.assertRaises( TypeError, checkAndSetWindow, ["Aluminum", "CH"] )

        # Value raises.
        self.assertRaises( ValueError, checkAndSetWindow, "Boron" )

        # Ok.
        self.assertEqual( checkAndSetWindow("SiO2"), "SiO2" )

    def testCheckAndSetWindowThickness(self):
        """ Test the check and set method for the ablator thickness. """

        self.assertRaises( TypeError, checkAndSetWindowThickness, "ten microns" )
        self.assertRaises( TypeError, checkAndSetWindowThickness, [10.0, 10.0] )

        # Value raises.
        self.assertRaises( ValueError, checkAndSetWindowThickness, -10.0 )

        self.assertEqual( checkAndSetWindowThickness(10.0), 10.0 )
        self.assertEqual( checkAndSetWindowThickness(10), 10.0 )

    def testCheckAndSetLaserWavelength(self):
        """ Test the check and set method for the laser wavelength. """

        # Type raises.
        self.assertRaises( TypeError, checkAndSetLaserWavelength, [100.0, 1024.0] )
        self.assertRaises( TypeError, checkAndSetLaserWavelength, "2 omega" )

        # Value raises.
        self.assertRaises( ValueError, checkAndSetLaserWavelength, -1024.0 )

        self.assertEqual( checkAndSetLaserWavelength(800.0), 0.8 )
        self.assertEqual( checkAndSetLaserWavelength(800),   0.8 )

    def testCheckAndSetLaserPulse(self):
        """ Test the check and set method for the laser pulse type. """

        # Type raises.
        self.assertRaises( TypeError, checkAndSetLaserPulse, 1 )
        self.assertRaises( TypeError, checkAndSetLaserPulse, 1.0 )
        self.assertRaises( TypeError, checkAndSetLaserPulse, ["flat", "quasiflat"] )

        # Value raises.
        self.assertRaises( ValueError, checkAndSetLaserPulse, "rectangular" )

        self.assertEqual( checkAndSetLaserPulse("flat"), "flat")
        self.assertEqual( checkAndSetLaserPulse("ramp"), "ramp")
        self.assertEqual( checkAndSetLaserPulse("quasiflat"), "quasiflat")

    def testCheckAndSetLaserPulseDuration(self):
        """ Test the check and set method for the laser pulse duration. """

        # Type raises.
        self.assertRaises( TypeError, checkAndSetLaserPulseDuration, [10.0, 24.0] )
        self.assertRaises( TypeError, checkAndSetLaserPulseDuration, "2 ns" )

        # Value raises.
        self.assertRaises( ValueError, checkAndSetLaserPulseDuration, -10.0 )

        self.assertEqual( checkAndSetLaserPulseDuration( 2.0 ) , 2.0 )
        self.assertEqual( checkAndSetLaserPulseDuration( 10 ) , 10 )

    def testCheckAndSetLaserIntensity(self):
        """ Test the check and set method for the laser intensity. """
        # Type raises.
        self.assertRaises( TypeError, checkAndSetLaserIntensity, [0.1, 0.2] )
        self.assertRaises( TypeError, checkAndSetLaserIntensity, "2 TW/cm2" )

        # Value raises.
        self.assertRaises( ValueError, checkAndSetLaserIntensity, -1.0 )

        self.assertEqual( checkAndSetLaserIntensity( 0.1 ) , 0.1 )
        self.assertEqual( checkAndSetLaserIntensity( 1 ) , 1.0 )

    def testSerialize(self):
        """ Test the serialization of parameters into input deck."""

        # Setup parameters object.
        esther_parameters = self.esther_parameters

        esther_parameters._serialize()

        # Check that the input deck has been generated.
        self.assertTrue( os.path.isdir( esther_parameters._esther_files_path ) )

        self.assertTrue( 'tmp_input.txt' in os.listdir( esther_parameters._esther_files_path ) )
        self.assertTrue( 'parameters.json' in os.listdir( esther_parameters._esther_files_path ) )

    def testExpert(self):
        """ Testing the expert mode parameters pass """

        # Setup parameters object.
        esther_parameters = EstherPhotonMatterInteractorParameters(
                                         number_of_layers=2,
                                         ablator="CH",
                                         ablator_thickness=10.0,
                                         sample="Iron",
                                         sample_thickness=20.0,
                                         window=None,
                                         window_thickness=0.0,
                                         laser_wavelength=800.0,
                                         laser_pulse='flat',
                                         laser_pulse_duration=1.0,
                                         laser_intensity=0.1,
                                         run_time=10.0,
                                         delta_time=0.05,
                                         force_passage=True,
                                         without_therm_conduc=True,
                                         rad_transfer=True)

        esther_parameters._serialize()

        # Assert equal, self.__use_force_passage, "FORCE_PASSAGE" for input.dat?
        self.assertTrue( 'tmp_input.txt' in os.listdir( esther_parameters._esther_files_path ) )
        self.assertTrue( 'parameters.json' in os.listdir( esther_parameters._esther_files_path ) )

    def testReadFromFile(self):
        """ """
        esther_parameters = self.esther_parameters
        esther_parameters._serialize()

        path_to_esther_files = esther_parameters._esther_files_path

        # The function readParametersFromFile needs to set this parameters below from the param.dat file.
        # For now, obtaining the tmp path of esther files is working.
        new_esther_parameters = EstherPhotonMatterInteractorParameters(
                                         read_from_file=path_to_esther_files)

        # Check all members are equal.
        for key,val in esther_parameters.__dict__.items():
            self.assertEqual( val, getattr(new_esther_parameters, key) )

    def testReadFromFileWithUpdate(self):
        """ """
        esther_parameters = self.esther_parameters
        esther_parameters._serialize()

        path_to_esther_files = esther_parameters._esther_files_path

        # The function readParametersFromFile needs to set this parameters below from the param.dat file.
        # For now, obtaining the tmp path of esther files is working.
        new_esther_parameters = EstherPhotonMatterInteractorParameters(
                                         laser_wavelength = 900.0,
                                         read_from_file=path_to_esther_files)

        # Check laser wavelength has been updated.
        self.assertEqual( new_esther_parameters.laser_wavelength, 0.9 )

    def testSetupFeathering(self):
        """ Test the utility responsible for setting up the feathering. """
        # Setup parameters object.
        esther_parameters = self.esther_parameters

        esther_parameters._setupFeathering(number_of_zones=250, feather_zone_width=4.0, minimum_zone_width=4e-4)

        self.assertAlmostEqual( esther_parameters._final_feather_zone_width, 0.0878)
        self.assertAlmostEqual( esther_parameters._mass_of_zone, 0.091662, 5)
        self.assertEqual( esther_parameters._non_feather_zones, 239)


if __name__ == '__main__':
    unittest.main()

