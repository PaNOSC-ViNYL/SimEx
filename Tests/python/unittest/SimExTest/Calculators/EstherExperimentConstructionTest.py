##########################################################################
#                                                                        #
# Copyright (C) 2017 Carsten Fortmann-Grot, Richard Briggs               #
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

""" Test module for the EstherExperimentConstruction class.

    @author : CFG
    @institution : XFEL
    @creation 20160219

"""
import paths
import os
import numpy
import shutil
import subprocess
import json

# Include needed directories in sys.path.
import paths
import unittest


# Import the class to test.
from SimEx.Calculators.EstherExperimentConstruction import EstherExperimentConstruction
from SimEx.Parameters.EstherPhotonMatterInteractorParameters import EstherPhotonMatterInteractorParameters

class EstherExperimentConstructionTest(unittest.TestCase):
    """
    Test class for the EstherExperimentConstruction class.
    """

    @classmethod
    def setUpClass(cls):
        # Make a directory for simulation storage.
        cls._simdir = os.path.join(os.getcwd(), "Simulations")
        os.mkdir(cls._simdir)

    @classmethod
    def tearDownClass(cls):
        """ Tearing down the test class. """
        shutil.rmtree(cls._simdir)

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

    def testDefaultConstruction(self):
        """ Testing the default construction of the class using a dictionary. """

        # Attempt to construct an instance of the class.
        self.assertRaises( RuntimeError, EstherExperimentConstruction )

    def testConstruction1(self):

        esther_sims_path=self._simdir
        sim_name = "NickelShock"
        esther_experiment = EstherExperimentConstruction(esther_sims_path=esther_sims_path, sim_name=sim_name)

        # Check presence of expected directories.
        self.assertIn( sim_name, os.listdir( esther_sims_path ) )
        self.assertIn( "1",  os.listdir(os.path.join(esther_sims_path, sim_name) ) )

        # Check instance and inheritance.
        self.assertIsInstance( esther_experiment, EstherExperimentConstruction )

    def testConstruction2(self):

        esther_sims_path=self._simdir
        sim_name = "NickelShock"
        esther_experiment = EstherExperimentConstruction(esther_sims_path=esther_sims_path, sim_name=sim_name)

        # Check presence of expected directories.
        self.assertIn( sim_name, os.listdir( esther_sims_path ) )
        self.assertIn( "1", os.listdir( os.path.join(esther_sims_path, sim_name) ) )
        self.assertIn( "2", os.listdir( os.path.join(esther_sims_path, sim_name) ) )

        # Check instance and inheritance.
        self.assertIsInstance( esther_experiment, EstherExperimentConstruction )

    def testComplexWorkflow(self):

        # Create parameters.
        parameters = EstherPhotonMatterInteractorParameters(
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
                                         delta_time=0.05
                                         )
        # Create experiment.
        experiment = EstherExperimentConstruction(parameters=parameters,
                                                  esther_sims_path=self._simdir,
                                                  sim_name=parameters.sample)

        # Check presence of expected directories.
        expected_dir = "Simulations/Iron/1"
        self.assertTrue( os.path.isdir(expected_dir) )

        self.assertIn( "Iron1.dat", os.listdir(expected_dir) )
        self.assertIn( "Iron1_intensite_impulsion.dat", os.listdir(expected_dir) )
        self.assertIn( "parameters.json", os.listdir(expected_dir) )

        # Create new experiment from previous.
        experiment = EstherExperimentConstruction(parameters=parameters,
                                                  esther_sims_path=self._simdir,
                                                  sim_name=parameters.sample)

        # Check presence of expected directories.
        expected_dir = "Simulations/Iron/2"
        self.assertTrue( os.path.isdir(expected_dir) )

        self.assertIn( "Iron2.dat", os.listdir(expected_dir) )
        self.assertIn( "Iron2_intensite_impulsion.dat", os.listdir(expected_dir) )
        self.assertIn( "parameters.json", os.listdir(expected_dir) )

        with open(os.path.join(expected_dir,"parameters.json")) as j:
            dictionary = json.load(j)
            j.close()

        # Check parameter.
        self.assertEqual( dictionary["_EstherPhotonMatterInteractorParameters__sample_thickness"], 20.0 )


        # Create new experiment from previous with update.
        new_parameters = EstherPhotonMatterInteractorParameters(sample_thickness=15.0,
                read_from_file="Simulations/Iron/2")

        experiment = EstherExperimentConstruction(parameters=new_parameters,
                                                  esther_sims_path=self._simdir,
                                                  sim_name=parameters.sample)

        # Check presence of expected directories.
        expected_dir = "Simulations/Iron/3"
        self.assertTrue( os.path.isdir(expected_dir) )

        self.assertIn( "Iron3.dat", os.listdir(expected_dir) )
        self.assertIn( "Iron3_intensite_impulsion.dat", os.listdir(expected_dir) )
        self.assertIn( "parameters.json", os.listdir(expected_dir) )

        with open(os.path.join(expected_dir,"parameters.json")) as j:
            dictionary = json.load(j)
            j.close()

        # Check update performed.
        self.assertEqual( dictionary["_EstherPhotonMatterInteractorParameters__sample_thickness"], 15.0 )



        ## Serialize.
        ## New experiment based on first experiment.
        #esther_sims_path=self._simdir
        #sim_name = "NickelShock"
        #esther_experiment = EstherExperimentConstruction(esther_sims_path=esther_sims_path, sim_name=sim_name)

        ## Check presence of expected directories.
        #self.assertIn( sim_name, os.listdir( esther_sims_path ) )
        #self.assertIn( "1", os.listdir( os.path.join(esther_sims_path, sim_name) ) )
        #self.assertIn( "2", os.listdir( os.path.join(esther_sims_path, sim_name) ) )

        ## Check instance and inheritance.
        #self.assertIsInstance( esther_experiment, EstherExperimentConstruction )




if __name__ == '__main__':
    unittest.main()

