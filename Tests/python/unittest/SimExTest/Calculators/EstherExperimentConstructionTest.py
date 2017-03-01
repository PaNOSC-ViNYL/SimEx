##########################################################################
#                                                                        #
# Copyright (C) 2016,2017 Carsten Fortmann-Grote                         #
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

# Include needed directories in sys.path.
import paths
import unittest

#from SimEx.Parameters.AbstractCalculatorParameters import AbstractCalculatorParameters

# Import the class to test.
from SimEx.Calculators.EstherExperimentConstruction import EstherExperimentConstruction
# from SimEx.Parameters.EstherExperimentConstructions import checkAndSetNumberOfLayers
# from SimEx.Parameters.EstherExperimentConstructions import checkAndSetAblator
# from SimEx.Parameters.EstherExperimentConstructions import checkAndSetAblatorThickness
# from SimEx.Parameters.EstherExperimentConstructions import checkAndSetSample
# from SimEx.Parameters.EstherExperimentConstructions import checkAndSetSampleThickness
# from SimEx.Parameters.EstherExperimentConstructions import checkAndSetWindow
# from SimEx.Parameters.EstherExperimentConstructions import checkAndSetWindowThickness
# from SimEx.Parameters.EstherExperimentConstructions import checkAndSetLaserWavelength
# from SimEx.Parameters.EstherExperimentConstructions import checkAndSetLaserPulse
# from SimEx.Parameters.EstherExperimentConstructions import checkAndSetLaserPulseDuration
# from SimEx.Parameters.EstherExperimentConstructions import checkAndSetLaserIntensity

class EstherExperimentConstructionTest(unittest.TestCase):
    """
    Test class for the EstherExperimentConstruction class.
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

    def testDefaultConstruction(self):
        """ Testing the default construction of the class using a dictionary. """

        # Attempt to construct an instance of the class.
        self.assertRaises( RuntimeError, EstherExperimentConstruction )
    
    def testShapedConstruction(self):
        
        #esther_sims_path="/Users/richardbriggs/Simulations/"
        esther_experiment = EstherExperimentConstruction(esther_sims_path="/Users/richardbriggs/Simulations/",sim_name="NickelShock")
        
        # Check instance and inheritance.
        self.assertIsInstance( esther_experiment, EstherExperimentConstruction )

    
if __name__ == '__main__':
    unittest.main()

