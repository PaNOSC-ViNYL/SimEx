""" Test module for the EstherPhotonMatterInteractor.
"""
##########################################################################
#                                                                        #
# Copyright (C) 2016, 2017 Carsten Fortmann-Grote                        #
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
import os
import paths
import shutil
import unittest

from SimEx.Parameters.EstherPhotonMatterInteractorParameters import EstherPhotonMatterInteractorParameters
from SimEx.Calculators.AbstractPhotonInteractor import AbstractPhotonInteractor
from SimEx.Calculators.AbstractBaseCalculator import AbstractBaseCalculator
from TestUtilities import TestUtilities

# Import the class to test.
from SimEx.Calculators.EstherPhotonMatterInteractor import EstherPhotonMatterInteractor


class EstherPhotonMatterInteractorTest(unittest.TestCase):
    """
    Test class for the EstherPhotonMatterInteractor class.
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
        self.esther_parameters = EstherPhotonMatterInteractorParameters(
                 number_of_layers=2,
                 ablator="CH",
                 ablator_thickness=10.0,
                 sample="Iron",
                 sample_thickness=20.0,
                 window=None,
                 window_thickness=0.0,
                 laser_wavelength=1064.0,
                 laser_pulse='flat',
                 laser_pulse_duration=6.0,
                 laser_intensity=0.1,
                 run_time=10.,
                 delta_time=.25,
                 read_from_file=None,
                 force_passage=True,
                 without_therm_conduc=False,
                 rad_transfer=False,
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
        """ Testing the default construction of the class. """

        # Attempt to construct an instance of the class.
        esther_calculator = EstherPhotonMatterInteractor(parameters=self.esther_parameters,
                                               input_path=self.input_path,
                                               output_path='esther_out')

        # Check instance and inheritance.
        self.assertIsInstance( esther_calculator, EstherPhotonMatterInteractor )
        self.assertIsInstance( esther_calculator, AbstractPhotonInteractor )
        self.assertIsInstance( esther_calculator, AbstractBaseCalculator )

    def testConstructionParameters(self):
        """ Testing the input parameter checks pass for a sane parameter dict. """

        # Construct an instance.
        esther_calculator = EstherPhotonMatterInteractor(
                                                parameters=self.esther_parameters,
                                                input_path=self.input_path,
                                                output_path='esther_out'
                                              )

        # Query the parameters.
        query = esther_calculator.parameters

        # Check query is ok.
        self.assertIsInstance( query, EstherPhotonMatterInteractorParameters )


    @unittest.skip("Backengine not available.")
    def testBackengine(self):
        """ Check that the backengine can be executed and output is generated. """

        # Setup parameters.
        esther_parameters = self.esther_parameters


        # Construct an instance.
        esther_calculator = EstherPhotonMatterInteractor( parameters=esther_parameters,
                                                input_path=self.input_path,
                                                output_path='esther_out'
                                              )

        # Call the backengine.
        esther_message = esther_calculator.backengine()

        self.assertEqual(esther_message, "")


    @unittest.skip("Backengine not available.")
    def testSaveH5(self):
        """ Test hdf5 output generation. """

        # Make sure we clean up after ourselves.
        outfile = 'esther_out.h5'
        self.__files_to_remove.append(outfile)

        # Setup parameters.
        esther_parameters = self.esther_parameters

        # Construct an instance.
        esther_calculator = EstherPhotonMatterInteractor(
                                                parameters=esther_parameters,
                                                input_path=self.input_path,
                                                output_path=outfile,
                                              )

        # Call the backengine.
        esther_calculator.backengine()

        # Save to h5
        esther_calculator.saveH5()

        # Check output was written.
        self.assertTrue( os.path.isfile( esther_calculator.output_path ) )

        # Open file.
        with h5py.File( outfile ) as h5:
            # Check top level group.
            self.assertIn( 'data' , h5.keys() )
            # Check all times are present.
            self.assertEqual( len(h5['data'].keys()), int(esther_calculator.parameters.run_time / esther_calculator.parameters.delta_time)+1 ) # run_time/delta_time
            # Check time 0 is present.
            self.assertIn( '0' , h5['data'].keys() )
            # Check  meshes group present.
            self.assertIn( 'meshes' , h5['data/0'].keys() )
            # Check all meshes are present at time 0.
            self.assertIn( 'pos'  , h5['data/0/meshes'].keys() )
            self.assertIn( 'pres' , h5['data/0/meshes'].keys() )
            self.assertIn( 'rho'  , h5['data/0/meshes'].keys() )
            self.assertIn( 'temp' , h5['data/0/meshes'].keys() )
            self.assertIn( 'vel'  , h5['data/0/meshes'].keys() )

            # Check dataset shape
            self.assertEqual( h5['data/0/meshes/vel'].value.shape[0], 2025)


if __name__ == '__main__':
    unittest.main()

