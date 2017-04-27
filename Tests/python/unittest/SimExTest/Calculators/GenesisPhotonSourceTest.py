""" Test module for the GenesisPhotonSource.  """
##########################################################################
#                                                                        #
# Copyright (C) 2015-2017 Carsten Fortmann-Grote                         #
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

import paths
import unittest

import numpy
import h5py
import os, shutil

# Import the class to test.
from SimEx.Calculators.AbstractPhotonSource import AbstractPhotonSource
from SimEx.Calculators.GenesisPhotonSource import GenesisPhotonSource
from ocelot.adaptors import genesis
from ocelot.rad.undulator_params import UndulatorParameters
from TestUtilities import TestUtilities

from SimEx.Utilities import sase1
from SimEx.Utilities.IOUtilities import wgetData

from ocelot.rad.undulator_params import Ephoton2K

class GenesisPhotonSourceTest(unittest.TestCase):
    """
    Test class for the GenesisPhotonSource class.
    """

    @classmethod
    def setUpClass(cls):
        """ Setting up the test class. """
        # Get pic test data.
        if "simData_8000.h5" in os.listdir("."):
            cls.__simdata = testfile_path
        else:
            try:
                cls.__simdata = wgetData(url = "https://docs.xfel.eu/alfresco/d/a/workspace/SpacesStore/4d00d480-34a5-462e-8459-5483a75445c5/simData_8000.h5")
            except:
                raise RuntimeError("Unable to download simulation input data. Please try again later. If problem persists, contact support.")
                sys.exit()

    @classmethod
    def tearDownClass(cls):
        """ Tearing down the test class. """
        if os.isfile(cls.__simdata):
            os.remove(cls.__simdata)


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

    def testConstructionNativeBeamFile(self):
        """ Testing the construction of the class with a native genesis beam file."""

        # Construct the object.
        xfel_source = GenesisPhotonSource(parameters=None, input_path=TestUtilities.generateTestFilePath('genesis_beam.dat'))

        self.assertIsInstance(xfel_source, AbstractPhotonSource)
        self.assertIsInstance(xfel_source, GenesisPhotonSource)

    def testConstructionPicH5(self):
        """ Testing the construction of the class with a given PIC snapshot. """

        # Construct the object.
        xfel_source = GenesisPhotonSource(parameters=None, input_path=TestUtilities.generateTestFilePath('simData_8000.h5'))

        self.assertIsInstance(xfel_source, AbstractPhotonSource)
        self.assertIsInstance(xfel_source, GenesisPhotonSource)

    def testReadH5(self):
        """ Testing the read function and conversion of openpmd input to native beam file."""

        # Construct the object.
        xfel_source = GenesisPhotonSource(parameters=None, input_path=TestUtilities.generateTestFilePath('simData_8000.h5'), output_path='FELsource_out.h5')

        xfel_source._readH5()
        self.assertTrue( hasattr( xfel_source, '_GenesisPhotonSource__input_data' ) )

    def testPrepareRun(self):
        """ Tests the method that sets up input files and directories for a genesis run. """

        # Ensure proper cleanup.
        self.__dirs_to_remove.append('source')

        # Get SASE1 template undulator object.
        undulator = sase1.und
        photon_energy = 200.0 # eV
        electron_energy = 16.0e-3 # GeV
        undulator.Kx = Ephoton2K(photon_energy, undulator.lperiod, electron_energy)

        # Calculate undulator-radiator parameters.
        undulator_parameters = UndulatorParameters(undulator, electron_energy)


        # Setup parameters.
        parameters_dict = {
                'time_averaging_window': 1e-8,
                'is_time_dependent': False,
                'undulator_parameters': undulator_parameters,
                }

        # Construct the object.
        xfel_source = GenesisPhotonSource(parameters=parameters_dict, input_path=TestUtilities.generateTestFilePath('simData_8000.h5'), output_path='source')

        # Read the input distribution.
        xfel_source._readH5()

        # Prepare the run.
        xfel_source._prepareGenesisRun()

        # Check generated data.
        self.assertIsInstance( xfel_source._GenesisPhotonSource__genesis_input, genesis.GenesisInput )
        self.assertIsInstance( xfel_source._GenesisPhotonSource__genesis_beam, genesis.GenesisBeam )


    def testBackengine(self):
        """ Testing the read function and conversion of openpmd input to native beam file."""

        # Ensure proper cleanup.
        #self.__dirs_to_remove.append('source')

        # Get SASE1 template undulator object.
        undulator = sase1.und
        photon_energy = 200.0 # eV
        electron_energy = 16.0e-3 # GeV
        undulator.Kx = Ephoton2K(photon_energy, undulator.lperiod, electron_energy)

        # Calculate undulator-radiator parameters.
        undulator_parameters = UndulatorParameters(undulator, electron_energy)


        # Setup parameters.
        parameters_dict = {
                'time_averaging_window': 1e-8,
                'is_time_dependent': False,
                'undulator_parameters': undulator_parameters,
                }

        # Construct the object.
        xfel_source = GenesisPhotonSource(parameters=parameters_dict, input_path=TestUtilities.generateTestFilePath('simData_8000.h5'), output_path='source')

        # Read the input distribution.
        xfel_source._readH5()

        # Prepare the run.
        xfel_source._prepareGenesisRun()

        # This should not throw.
        try:
            xfel_source.backengine()
            throws = False
        except:
            throws = True

        self.assertFalse( throws )

 if __name__ == '__main__':
    unittest.main()


