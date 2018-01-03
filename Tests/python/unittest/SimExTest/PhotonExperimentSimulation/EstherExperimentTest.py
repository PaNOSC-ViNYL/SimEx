""" :module: Test module for the EstherExperiment class."""
##########################################################################
#                                                                        #
# Copyright (C) 2017 Carsten Fortmann-Grote, Richard Briggs              #
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

import json
import os
from . import paths
import shutil
import unittest

# Import the class to test.
from SimEx.PhotonExperimentSimulation.EstherExperiment import EstherExperiment
from SimEx.Parameters.EstherPhotonMatterInteractorParameters import EstherPhotonMatterInteractorParameters
from SimEx.Utilities.hydro_txt_to_opmd import convertTxtToOPMD
from TestUtilities import TestUtilities

class EstherExperimentTest(unittest.TestCase):
    """
    Test class for the EstherExperiment class.
    """

    @classmethod
    def setUpClass(cls):
        # Make a tmp directory for simulation storage.
        cls._simdir = "tmp/"
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
        self.assertRaises( RuntimeError, EstherExperiment )

    def testComplexWorkflow(self):

        # Create parameters.
        parameters = EstherPhotonMatterInteractorParameters(
                                        number_of_layers=2,
                                         ablator="CH",
                                         ablator_thickness=50.0,
                                         sample="Iron",
                                         sample_thickness=5.0,
                                         layer1=None,
                                         layer1_thickness=None,
                                         window=None,
                                         window_thickness=None,
                                         laser_wavelength=1064.0,
                                         laser_pulse='flat',
                                         laser_pulse_duration=10.0,
                                         laser_intensity=0.33,
                                         run_time=15.0,
                                         delta_time=0.03,
                                         force_passage=True,
                                         )
        # Create experiment.
        sim_name = "CH-test"

        # Make a temporary directory under which experiments will be stored.
        esther_sims_path = "hydroTests"
        os.mkdir(esther_sims_path)

        # Ensure proper cleanup after test.
        self.__dirs_to_remove.append(esther_sims_path)

        # Make directory to store this experiment.
        experiment_root =  os.path.join(esther_sims_path, sim_name)

        # Construct the experiment.
        experiment = EstherExperiment(parameters=parameters,
                                                  esther_sims_path=esther_sims_path,
                                                  sim_name=sim_name)

        # Check presence of expected directories.
        experiment_dir = os.path.join(experiment_root, '1' )
        self.assertTrue( os.path.isdir(experiment_dir) )

        self.assertIn( "CH-test1.txt", os.listdir(experiment_dir) )
        self.assertIn( "CH-test1_intensite_impulsion.txt", os.listdir(experiment_dir) )
        self.assertIn( "parameters.json", os.listdir(experiment_dir) )

        # Create new experiment from previous.
        experiment = EstherExperiment(parameters=parameters,
                                                  esther_sims_path=esther_sims_path,
                                                  sim_name=sim_name)

        # Check presence of expected directories.
        experiment_dir = os.path.join(experiment_root, '2' )
        self.assertTrue( os.path.isdir(experiment_dir) )

        self.assertIn( "CH-test2.txt", os.listdir(experiment_dir) )
        self.assertIn( "CH-test2_intensite_impulsion.txt", os.listdir(experiment_dir) )
        self.assertIn( "parameters.json", os.listdir(experiment_dir) )

        with open(os.path.join(experiment_dir,"parameters.json")) as j:
            dictionary = json.load(j)
            j.close()

        # Check parameter.
        self.assertEqual( dictionary["_EstherPhotonMatterInteractorParameters__sample_thickness"], 5.0 )

        # Create new experiment from previous with update.
        new_parameters = EstherPhotonMatterInteractorParameters(laser_intensity=0.2,
                read_from_file=experiment_dir)

        experiment = EstherExperiment(parameters=new_parameters,
                                                  esther_sims_path=esther_sims_path,
                                                  sim_name=sim_name)

        # Check presence of expected directories.
        new_experiment_dir = os.path.join(experiment_root, '3' )
        self.assertTrue( os.path.isdir(new_experiment_dir) )

        self.assertIn( "CH-test3.txt", os.listdir(new_experiment_dir) )
        self.assertIn( "CH-test3_intensite_impulsion.txt", os.listdir(new_experiment_dir) )
        self.assertIn( "parameters.json", os.listdir(new_experiment_dir) )

        with open(os.path.join(new_experiment_dir,"parameters.json")) as j:
            dictionary = json.load(j)
            j.close()

        # Check update performed.
        self.assertEqual( dictionary["_EstherPhotonMatterInteractorParameters__laser_intensity"], 0.2 )


if __name__ == '__main__':
    unittest.main()
