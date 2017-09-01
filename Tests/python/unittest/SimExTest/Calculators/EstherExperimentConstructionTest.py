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
from SimEx.Utilities.hydro_txt_to_opmd import convertTxtToOPMD

class EstherExperimentConstructionTest(unittest.TestCase):
    """
    Test class for the EstherExperimentConstruction class.
    """

    @classmethod
    def setUpClass(cls):
        # Make a tmp directory for simulation storage.
        cls._simdir = "/Users/richardbriggs/Desktop/tmp/"
        os.mkdir(cls._simdir)
        # The os.mkdir is to create the files for temporary use only, obviously this isn't used for main code.

    @classmethod
    def tearDownClass(cls):
        """ Tearing down the test class. """
        shutil.rmtree(cls._simdir) # Comment out if you want to keep the files, but then also comment setUpClass mkdir.

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

    def notestDefaultConstruction(self):
        """ Testing the default construction of the class using a dictionary. """

        # Attempt to construct an instance of the class.
        self.assertRaises( RuntimeError, EstherExperimentConstruction )

    def testComplexWorkflow(self):

        # Create parameters.
        parameters = EstherPhotonMatterInteractorParameters(
                                        number_of_layers=2,
                                         ablator="CH",
                                         ablator_thickness=50.0,
                                         sample="Iron",
                                         sample_thickness=5.0,
                                         window=None,
                                         window_thickness=0.0,
                                         laser_wavelength=1064.0,
                                         laser_pulse='flat',
                                         laser_pulse_duration=6.0,
                                         laser_intensity=0.33,
                                         run_time=12.0,
                                         delta_time=0.05
                                         )
        # Create experiment.
        simName = "test"
        experiment = EstherExperimentConstruction(parameters=parameters,
                                                  esther_sims_path=self._simdir,
                                                  sim_name=simName)

        # Check presence of expected directories.
        expected_dir = "/Users/richardbriggs/Desktop/tmp/test/1/"
        self.assertTrue( os.path.isdir(expected_dir) )

        self.assertIn( "test1.txt", os.listdir(expected_dir) )
        self.assertIn( "test1_intensite_impulsion.txt", os.listdir(expected_dir) )
        self.assertIn( "parameters.json", os.listdir(expected_dir) )

        # Create new experiment from previous.
        experiment = EstherExperimentConstruction(parameters=parameters,
                                                  esther_sims_path=self._simdir,
                                                  sim_name=simName)

        # Check presence of expected directories.
        expected_dir = "/Users/richardbriggs/Desktop/tmp/test/2/"
        self.assertTrue( os.path.isdir(expected_dir) )

        self.assertIn( "test2.txt", os.listdir(expected_dir) )
        self.assertIn( "test2_intensite_impulsion.txt", os.listdir(expected_dir) )
        self.assertIn( "parameters.json", os.listdir(expected_dir) )

        with open(os.path.join(expected_dir,"parameters.json")) as j:
            dictionary = json.load(j)
            j.close()

        # Check parameter.
        self.assertEqual( dictionary["_EstherPhotonMatterInteractorParameters__sample_thickness"], 5.0 )
        
        # Create new experiment from previous with update.
        new_parameters = EstherPhotonMatterInteractorParameters(sample_thickness=4.0,
                read_from_file="/Users/richardbriggs/Desktop/tmp/test/2/")

        experiment = EstherExperimentConstruction(parameters=new_parameters,
                                                  esther_sims_path=self._simdir,
                                                  sim_name=simName)

        # Check presence of expected directories.
        expected_dir = "/Users/richardbriggs/Desktop/tmp/test/3/"
        self.assertTrue( os.path.isdir(expected_dir) )

        self.assertIn( "test3.txt", os.listdir(expected_dir) )
        self.assertIn( "test3_intensite_impulsion.txt", os.listdir(expected_dir) )
        self.assertIn( "parameters.json", os.listdir(expected_dir) )

        with open(os.path.join(expected_dir,"parameters.json")) as j:
            dictionary = json.load(j)
            j.close()

        # Check update performed.
        self.assertEqual( dictionary["_EstherPhotonMatterInteractorParameters__sample_thickness"], 4.0 )

    def testConversion(self):
        # Existing files and output data need to be saved

        # Create experiment.
        dirName = "/Users/richardbriggs/OneDrive/Data/Hydrocode/tmp/Fe-Example/1"
        
        convertTxtToOPMD(dirName)

        # Check presence of expected directories.
        expected_dir = "/Users/richardbriggs/OneDrive/Data/Hydrocode/tmp/Fe-Example/1/"
        self.assertTrue( os.path.isdir(expected_dir) )
        
        # Check the output file is created in opmd.h5 format
        self.assertIn( "output.opmd.h5", os.listdir(expected_dir) )
     
        

if __name__ == '__main__':
    unittest.main()

