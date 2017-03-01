##########################################################################
#                                                                        #
# Copyright (C) 2016, 2017 Richard Briggs, Carsten Fortmann-Grote        #
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

import numpy
import os
import sys
import tempfile

class EstherExperimentConstruction():
    """
    TO DO: Description here.
    """
    def __init__(self,
                 parameters=None,
                 input_path=None,
                 output_path=None,
                 tmp_files_path=None,
                 esther_sims_path=None,
                 sim_name=None,
                 ):
        
        """
        Check if run files pathway exists and then look for existing directories.
        Directory setup should be incremental numbers
        """
        # TO DO: CHECK IF PARAMETERS HAVE BEEN INCLUDED
        
        # Check if the simulation root path has been set
        if esther_sims_path is None:
            raise RuntimeError( "Esther simulation folder path is not set!")
        
        # Check if the simulation root path exists
        if os.path.isdir(esther_sims_path) is not True:
            raise ValueError( "Esther simulation folder path does not exist!")
        
        # Check if the simulation name has been set
        if sim_name is None:
            raise RuntimeError ("Simulation name is not specified")
        else:
            # Define simulation path to the simulation name's folder
            sim_path=esther_sims_path+sim_name+"/"
            if os.path.isdir(sim_path) is True:
                # List all iterations within the simulation name's folder
                print ("These are the current simulations within %s" % sim_name)
                for sims in os.listdir(sim_path):
                    if not sims.startswith('.'):
                        print sims
                # Create new folder with new iteration numbers
                # TO DO: Generate updated parameters from SimName
                output_sim = int(sims)+1
                print ("New simulation iteration is %d" % output_sim)
                output_path=(sim_path+"%s/" % (output_sim))
                print ("Output path is set to %s" % (output_path))
            else:
                # Create new simulation folder called Sim_name and start first iteration /1/
                print ("No simulation exists. Creating new simulation if asked to do so")
                output_path = sim_path+"1/"
                print ("Output path is set to %s" % (output_path))
                # TO DO: Generate new parameters for new simulations from parameterss
