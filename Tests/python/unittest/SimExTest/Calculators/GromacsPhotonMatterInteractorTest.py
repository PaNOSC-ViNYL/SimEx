""" Test module for the GromacsPhotonMatterInteractor.
"""
##########################################################################
#                                                                        #
# Copyright (C) 2020, 2021 Ibrahim Dawod, Juncheng E                     #
# Contact:                                                               #
#       Ibrahim Dawod <ibrahim.dawod@physics.uu.se>                      #
#       Juncheng E <juncheng.e@xfel.eu>                                  #
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
import shutil
import unittest

from SimEx.Parameters.GromacsPhotonMatterInteractorParameters import GromacsPhotonMatterInteractorParameters
from SimEx.Calculators.AbstractPhotonInteractor import AbstractPhotonInteractor
from SimEx.Calculators.AbstractBaseCalculator import AbstractBaseCalculator
from TestUtilities import TestUtilities

# Import the class to test.
from SimEx.Calculators.GromacsPhotonMatterInteractor import GromacsPhotonMatterInteractor


class GromacsPhotonMatterInteractorTest(unittest.TestCase):
    """
    Test class for the GromacsPhotonMatterInteractor class.
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
        self.Gromacs_parameters = GromacsPhotonMatterInteractorParameters(
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
        Gromacs_calculator = GromacsPhotonMatterInteractor(parameters=self.Gromacs_parameters,
                                               input_path=self.input_path,
                                               output_path='Gromacs_out')

        # Check instance and inheritance.
        self.assertIsInstance( Gromacs_calculator, GromacsPhotonMatterInteractor )
        self.assertIsInstance( Gromacs_calculator, AbstractPhotonInteractor )
        self.assertIsInstance( Gromacs_calculator, AbstractBaseCalculator )

    def testConstructionParameters(self):
        """ Testing the input parameter checks pass for a sane parameter dict. """

        # Construct an instance.
        Gromacs_calculator = GromacsPhotonMatterInteractor(
                                                parameters=self.Gromacs_parameters,
                                                input_path=self.input_path,
                                                output_path='Gromacs_out'
                                              )

        # Query the parameters.
        query = Gromacs_calculator.parameters

        # Check query is ok.
        self.assertIsInstance( query, GromacsPhotonMatterInteractorParameters )


    @unittest.skip("Backengine not available.")
    def testBackengine(self):
        """ Check that the backengine can be executed and output is generated. """

        # Setup parameters.
        Gromacs_parameters = self.Gromacs_parameters


        # Construct an instance.
        Gromacs_calculator = GromacsPhotonMatterInteractor( parameters=Gromacs_parameters,
                                                input_path=self.input_path,
                                                output_path='Gromacs_out'
                                              )

        # Call the backengine.
        Gromacs_message = Gromacs_calculator.backengine()

        self.assertEqual(Gromacs_message, "")


    @unittest.skip("Backengine not available.")
    def testSaveH5(self):
        """ Test hdf5 output generation. """

        # Make sure we clean up after ourselves.
        outfile = 'Gromacs_out.h5'
        self.__files_to_remove.append(outfile)

        # Setup parameters.
        Gromacs_parameters = self.Gromacs_parameters

        # Construct an instance.
        Gromacs_calculator = GromacsPhotonMatterInteractor(
                                                parameters=Gromacs_parameters,
                                                input_path=self.input_path,
                                                output_path=outfile,
                                              )

        # Call the backengine.
        Gromacs_calculator.backengine()

        # Save to h5
        Gromacs_calculator.saveH5()

        # Check output was written.
        self.assertTrue( os.path.isfile( Gromacs_calculator.output_path ) )

        # Open file.
        with h5py.File( outfile ) as h5:
            # Check top level group.
            self.assertIn( 'data' , list(h5.keys()) )
            # Check all times are present.
            self.assertEqual( len(list(h5['data'].keys())), int(Gromacs_calculator.parameters.run_time / Gromacs_calculator.parameters.delta_time)+1 ) # run_time/delta_time
            # Check time 0 is present.
            self.assertIn( '0' , list(h5['data'].keys()) )
            # Check  meshes group present.
            self.assertIn( 'meshes' , list(h5['data/0'].keys()) )
            # Check all meshes are present at time 0.
            self.assertIn( 'pos'  , list(h5['data/0/meshes'].keys()) )
            self.assertIn( 'pres' , list(h5['data/0/meshes'].keys()) )
            self.assertIn( 'rho'  , list(h5['data/0/meshes'].keys()) )
            self.assertIn( 'temp' , list(h5['data/0/meshes'].keys()) )
            self.assertIn( 'vel'  , list(h5['data/0/meshes'].keys()) )

            # Check dataset shape
            self.assertEqual( h5['data/0/meshes/vel'].value.shape[0], 2025)


if __name__ == '__main__':
    unittest.main()

