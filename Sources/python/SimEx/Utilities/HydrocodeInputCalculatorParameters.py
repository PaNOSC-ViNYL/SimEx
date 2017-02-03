##########################################################################
#                                                                        #
# Copyright (C) 2016 Richard Briggs, Carsten Fortmann-Grote              #
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
import numpy
import sys

#from SimEx.Parameters.AbstractCalculatorParameters import AbstractCalculatorParameters
#from SimEx.Utilities.EntityChecks import checkAndSetInstance
#from SimEx.Utilities.EntityChecks import checkAndSetInteger
#from SimEx.Utilities.EntityChecks import checkAndSetPositiveInteger
#from SimEx.Utilities.EntityChecks import checkAndSetNonNegativeInteger

BOOL_TO_INT = {True : 1, False : 0}

class HydroParameters:
    """
    !!! Need to include the (AbstractCalculatorParameters) !!!
    class representing parameters for the Hydrocode Input Calculator
    """
    def __init__(self,
                 Ablator=None,
                 AblatorThickness=None,
                 Sample=None,
                 SampleThickness=None,
                 Window=None,
                 WindowThickness=None,
                 LaserPulse=None,
                 LaserPulseLength=None,
                 LaserWavelenght=None,
                 LaserIntensity=None,
                 ):

        """
        Constructor for the HydroParameters
        
        @param Ablator The ablating material, Al, CH, or diamond
        </br><b>type</b> String
        
        @param AblatorThickness The ablator thickness (um)
        </br><b>type</b> float
                
        @param Sample The sample material (from limited list of materials)
        </br><b>type</b> String
                
        @param SampleThickness The sample thickness (um)
        </br><b>type</b> String 
        
        @param Window The window material, LiF, SiO2 or diamond
        </br><b>type</b> String 
        
        @param WindowThickness The window thickness, if using window, in (um)
        </br><b>type</b> Float 
        
        @param LaserPulse Pulse type (flat top, ramp pulse, other)
        </br><b>type</b> String
        
        @param LaserPulseLength Pulse length of laser (ns)
        </br><b>type</b> float 
        
        @param LaserWavelength Laser wavelength (nm)
        </br><b>type</b> float
        
        @param LaserIntensity Laser intensity (TW/cm2)
        </br><b>type</b> float
        """
        
        # Check and set all parameters
        self.__Ablator = checkAndSetAblator(Ablator)
        #self.__AblatorThickness = checkAndSetAblatorThickness(AblatorThickness)
        #self.__Sample = checkAndSetSample(Sample)
        #self.__SampleThickness = checkAndSet(SampleThickness)
        #self.__Window = checkAndSet(Window)
        #self.__WindowThickness = checkAndSetWindowThickness(WindowThickness)
        #self.__LaserPulse = checkAndSetLaserPulse(LaserPulse)
        #self.__LaserPulseLength = checkAndSetLaserPulseLength(LaserPulseLength)
        #self.__LaserWavelength = checkAndSetLaserWavelength(LaserWavelength)
        #self.__LaserIntensity = checkAndSetLaserIntensity(LaserIntensity)
        
        # Set internal parameters
        """ PLACE HOLDER
        Can update this so that you can choose which EOS model to run.
        E.g.
        self.__use_eos = BOOL_TO_INT[self.eos == "SESAME"]
        self.__use_eos = BOOL_TO_INT[self.eos == "BLF"]
        """
        
        # Set state to not-initialized (e.g. input deck is not written)
        self.__is_initialized = False
        
        def _serialize(self):
        	""" Write the input deck for the Esther hydrocode. """
        	# Make a temporary directory
        	self._tmp_dir = tempfile.mkdtemp(prefix='esther_')
        	
        	# Write the input file
        	input_deck_path = os.path.join( self._tmp_dir, 'input.dat')
        	with open(input_deck_path, 'w') as input_deck:
        		input_deck.write('--Hydrocode input_file----------\n')
        		input_deck.write('\n')
        		input_deck.write('fini\n')
        
        @property
        def Ablator(self):
        	""" Query for the ablator type. """
        	return self.Ablator
        @Ablator.setter
        def Ablator(self, value):
        	""" Set the ablator to the value. """
        	self.Ablator = checkAndSetAblator(value)                
        

###########################
# Check and set functions #
###########################
def checkAndSetAblator(Ablator):
	"""
	Utility to check if the ablator exists in the EOS database.
	@param Ablator : The ablator material to check
	@return : The ablator choice after being checked
	@raise ValueError if ablator not CH, Al, or diamond     
	"""
	if Ablator is None:
		raise RuntimeError( "Ablator is not defined.")
	
	# ???
	#Ablator = checkAndSetInstance( string, Ablator, None) 
	# ???
	
	# Check if ablator is CH, Al or diamond
	if Ablator is 'CH':
		print ( "Setting CH as ablator.")
	elif Ablator is 'Al':
		print ( "Setting Al as ablator.")
	elif Ablator is 'dia':
		print ( "Setting diamond as ablator.")
	else:
		raise ValueError( "Ablator is not valid. Use CH, Al or dia.")       
	
	return Ablator
        
        
        
                   

