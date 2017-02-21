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
import numpy as np
import sys
import tempfile

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
                 NumLayers,
                 Ablator=None,
                 AblatorThickness=None,
                 Sample=None,
                 SampleThickness=None,
                 Window=None,
                 WindowThickness=None,
                 LaserWavelength=None,
                 LaserPulse=None,
                 LaserPulseLength=None,
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
        self.__NumLayers = checkAndSetNumLayers(NumLayers)
        self.__Ablator = checkAndSetAblator(Ablator)
        self.__AblatorThickness = checkAndSetAblatorThickness(AblatorThickness)
        self.__Sample = checkAndSetSample(Sample)
        self.__SampleThickness = checkAndSetSampleThickness(SampleThickness)
        self.__Window = checkAndSetWindow(Window)
        self.__WindowThickness = checkAndSetWindowThickness(WindowThickness)
        self.__LaserWavelength = checkAndSetLaserWavelength(LaserWavelength)
        #self.__LaserPulse = checkAndSetLaserPulse(LaserPulse)
        #self.__LaserPulseLength = checkAndSetLaserPulseLength(LaserPulseLength)
        #self.__LaserIntensity = checkAndSetLaserIntensity(LaserIntensity)
        
        # Set internal parameters
        """ TO DO PLACEHOLDER -------------------------------------------------------------->
        List of DEMARRAGE (translates as "Start up") parameters
        TRANSFERT_RADIATIF
        USI
        
        "Expert user mode to choose the correct demarrage parameters"
        
        Can also update this so that you can choose which EOS model to run???
        self.__use_eos = BOOL_TO_INT[self.eos == "SESAME"]
        self.__use_eos = BOOL_TO_INT[self.eos == "BLF"]
        """
        self._setDemmargeFlags()
        self._setWindowFlags()
        
        # Set state to not-initialized (e.g. input deck is not written)
        self.__is_initialized = False
    
    def _setDemmargeFlags(self):
    	self.__use_usi = "USI"
    	
    def _setWindowFlags(self):
    	self.__use_window = False       
        
    def _serialize(self):
        """ Write the input deck for the Esther hydrocode. """
        NumberZones = [0] 
        
        # Default variables for feathering 
        n = 250
        NumberZones = n
        FeatherZoneWidth = float(5.0)
        MinZoneWidth = float(1E-4)
        ExterneValue = MinZoneWidth*10000
        NonFeatherZoneWidth = self.AblatorThickness - FeatherZoneWidth
        
        # Determine the correct feathering
        list=[0]*(n+1)
        list[0]=1
        list[-2]=-FeatherZoneWidth/MinZoneWidth
        list[-1]=FeatherZoneWidth/MinZoneWidth-1
        
        f = np.poly1d(list)
        roots = np.roots(f)
        root_found = False
        
        for i in range(n):
            if roots[i].imag == 0 and roots[i].real > 1.000001:
                r = round(roots[i].real,4)
                root_found = True
        
        if root_found == False:
            raise ValueError( "No ratio bigger than 1.000001 was found.")
        
        finalFeatherZoneWidth = round(MinZoneWidth*(r**n),4)
        NonFeatherZones = int(NonFeatherZoneWidth/(MinZoneWidth*(r**n)))
        
        # Materials: [name, EOS shortname, EOS longname, density]
        # material_type = [0]*13
        # material_type[1] = ["Aluminium","Al#","Al#_e_ses",2.7]
        # material_type[2] = ["Diamond","Dia","Dia_e_ses",3.51]
        # material_type[3] = ["CH","CH2", "CH2_e_ses",1.044]
        # material_type[4] = ["Kapton","Kap","Kap_e_ses",1.42]
        # material_type[5] = ["Mo","Mo#","Mo#_e_ses",10.2]
        # material_type[6] = ["Gold","Au#","Au#_e_ses",19.3]
        # material_type[7] = ["Iron","Fe#","Fe#_e_ses",7.85]
        # material_type[8] = ["Copper","Cu#","Cu#_e_ses",8.93]
        # material_type[9] = ["Tin","Sn#","Sn#_e_ses",7.31]
        # material_type[10] = ["LiF","LiF","LiF_e_ses",2.64]
        # material_type[11] = ["Tantalum","Ta#","Ta#_e_ses",16.65]
        # material_type[12] = ["Titanium","Ti#","Ti#_e_ses",4.43]
        
        
        
        # Make a temporary directory
        self._tmp_dir = tempfile.mkdtemp(prefix='esther_')

        # Write the input file
        input_deck_path = os.path.join( self._tmp_dir, 'input.dat')
        print input_deck_path
        with open(input_deck_path, 'w') as input_deck:
            input_deck.write('DEMARRAGE,%s\n' % (self.__use_usi)) # This should be user option
            input_deck.write('\n')
            input_deck.write('MILIEUX_INT_VERS_EXT\n')
            input_deck.write('\n')
            # TO DO PLACEHOLDER -------------------------------------------------------------->
            if self.__use_window == True:
                # Do window write
                input_deck.write('This is the window layer')
            
            # If more than one layer, loop the layer construction here.
            # TO DO PLACEHOLDER -------------------------------------------------------------->
            input_deck.write('- %.1f um %s layer\n' % (self.SampleThickness, self.Sample))
            input_deck.write('NOM_MILIEU=\n')
            input_deck.write('EQUATION_ETAT=EOS_LIST\n')
            if self.__use_window == False:
                input_deck.write('EPAISSEUR_VIDE=100e-6\n')
            input_deck.write('EPAISSEUR_MILIEU=%.1fe-6\n' % (self.SampleThickness))
            input_deck.write('NOMBRE_MAILLES=NUMBER_OF_SAMPLE_ZONES\n')
            input_deck.write('\n')
            
            # Write ablator
            input_deck.write('- %.1f um %s layer\n' % (self.AblatorThickness, self.Ablator))
            input_deck.write('NOM_MILIEU=abl1\n') # 1ST PART OF ABLATOR
            input_deck.write('EQUATION_ETAT=EOS_FROM_LIST\n') # ABLATOR EOS
            # if only simulating ablator layer, then must include empty (VIDE) layer
            if self.NumLayers == 1:
                input_deck.write('EPAISSEUR_VIDE=100e-6\n')               
            input_deck.write('EPAISSEUR_MILIEU=%.1fe-6\n' % (NonFeatherZoneWidth)) # Non-feather thickness
            input_deck.write('NOMBRE_MAILLES=%d\n' % (NonFeatherZones)) # Number of zones
            input_deck.write('\n')
            input_deck.write('NOM_MILIEU=abl2\n') # 1ST PART OF ABLATOR
            input_deck.write('EQUATION_ETAT=EOS_FROM_LIST\n') # ABLATOR EOS
            input_deck.write('EPAISSEUR_MILIEU=%.1fe-6\n' % (FeatherZoneWidth)) # Feather thickness
            input_deck.write('EPAISSEUR_INTERNE=%.3fe-6\n' % (finalFeatherZoneWidth)) # Feather final zone width
            input_deck.write('EPAISSEUR_EXTERNE=%.1fe-10\n' % (ExterneValue)) #Min zone width
            input_deck.write('\n')
            
            # Internal parameters to add to flags
            # TO DO PLACEHOLDER -------------------------------------------------------------->
            input_deck.write('INDICE_REEL_LASER=1.46\n')
            input_deck.write('INDICE_IMAG_LASER=1.0\n')
            input_deck.write('DEPOT_ENERGIE,LASER,DEPOT_HELMHOLTZ\n')
            input_deck.write('LONGUEUR_ONDE_LASER=%.3fe-6\n' % (self.LaserWavelength))
            
    
    @property
    def NumLayers(self):
       	""" Query for the Number of Layers. """
       	return self.__NumLayers
    @NumLayers.setter
    def NumLayers(self, value):
       	""" Set the NumLayers to the value. """
       	self.__NumLayers = checkAndSetNumLayers(value)
    @property
    def Ablator(self):
       	""" Query for the ablator type. """
       	return self.__Ablator
    @Ablator.setter
    def Ablator(self, value):
       	""" Set the ablator to the value. """
       	self.__Ablator = checkAndSetAblator(value)
    @property
    def AblatorThickness(self):
       	""" Query for the ablator type. """
       	return self.__AblatorThickness
    @AblatorThickness.setter
    def AblatorThickness(self, value):
       	""" Set the ablator to the value. """
       	self.__AblatorThickness = checkAndSetAblatorThickness(value)
    @property
    def Sample(self):
       	""" Query for the Sample type. """
       	return self.__Sample
    @Sample.setter
    def Sample(self, value):
       	""" Set the ablator to the value. """
       	self.__Sample = checkAndSetSample(value)
    @property
    def SampleThickness(self):
       	""" Query for the Sample Thickness type. """
       	return self.__SampleThickness
    @SampleThickness.setter
    def SampleThickness(self, value):
       	""" Set the sample thickness to the value. """
       	self.__SampleThickness = checkAndSetSampleThickness(value)
    @property
    def Window(self):
       	""" Query for the Window type. """
       	return self.__Window
    @Window.setter
    def Window(self, value):
       	""" Set the Window to the value. """
       	self.__Window = checkAndSetWindow(value)
    @property
    def WindowThickness(self):
       	""" Query for the Window Thickness type. """
       	return self.__WindowThickness
    @WindowThickness.setter
    def WindowThickness(self, value):
       	""" Set the Window thickness to the value. """
       	self.__WindowThickness = checkAndSetWindowThickness(value)
    @property
    def LaserWavelength(self):
       	""" Query for the Laser wavelength type. """
       	return self.__LaserWavelength
    @LaserWavelength.setter
    def LaserWavelength(self, value):
       	""" Set the laser wavelength to the value. """
       	self.__LaserWavelength = checkAndSetLaserWavelength(value)

###########################
# Check and set functions #
###########################

def checkAndSetNumLayers(NumLayers):
    """
    Utility to check if the number of layers is reasonable.
    @param NumLayers : The number of layers to check
    @return : Number of layers
    @raise ValueError if not 1 layer or more than 5
    """
    if NumLayers is None:
        raise RuntimeError( "Number of layers is not defined.")
    
    if NumLayers <=1 or NumLayers > 5:
        raise ValueError( "Number of layers must be between 1 and 5 only.")
    
    return NumLayers

def checkAndSetAblator(Ablator):
	"""
	Utility to check if the ablator exists in the EOS database.
	@param Ablator : The ablator material to check
	@return : The ablator choice after being checked
	@raise ValueError if ablator not CH, Al, or diamond     
	"""
	if Ablator is None:
		raise RuntimeError( "Ablator is not defined.")
	
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


def checkAndSetAblatorThickness(AblatorThickness):
	"""
	Utility to check that the ablator thickness is > 5 um and < 100 um
	"""
	# Set default
	if AblatorThickness is None:
		raise RuntimeError( "Ablator thickness not specified.")
	
	# Check if ablator is between 5 and 100 um
	if AblatorThickness <= 5.0 or AblatorThickness > 100.0:
		raise ValueError( "Ablator must be between 5.0 and 100.0 microns")
	
	print ( "Ablator thickness is %4.1f " % AblatorThickness)
		
	return AblatorThickness


def checkAndSetSample(Sample):
	"""
	Utility to check if the sample is in the list of known EOS materials
	"""
	
	elements = ["Aluminium", "Gold", "Carbon", "CH", "Cobalt", "Copper", "Diamond",
				"Iron", "Molybdenum", "Nickel", "Lead", "Silicon", "Tin", "Tantalum"]
		
	# Set default
	if Sample is None:
		raise RuntimeError( "Sample not specified.")
	
	# Check each element
	if Sample in elements:
		pass
	else:
		raise ValueError( "Sample is not in list of known EOS materials")
		
	return Sample

def checkAndSetSampleThickness(SampleThickness):
	"""
	Utility to check that the sample thickness is > 1 um and < 200 um
	"""
	
	# Set default
	if SampleThickness is None:
		raise RuntimeError( "Sample thickness not specified.")
	
	# Check if ablator is between 1 and 100 um
	if SampleThickness < 1.0 or SampleThickness > 200.0:
		raise ValueError( "Ablator must be between 1.0 and 200.0 microns")
	
	return SampleThickness

def checkAndSetWindow(Window):
    """
	Utility to check that the sample thickness is > 1 um and < 200 um
	"""    
    # Change this to be just window materials (LiF, Quartz etc.)
    # TO DO PLACEHOLDER ------------------------------------------------------------------------------>
    elements = ["Aluminium", "Gold", "Carbon", "CH", "Cobalt", "Copper", "Diamond",
				"Iron", "Molybdenum", "Nickel", "Lead", "Silicon", "Tin", "Tantalum"]
    
    if Window is None:
		print ( "Running simulation without window material")
    else:
        # Check each element
        if Window in elements:
            pass
        else:
            raise ValueError( "Window is not in list of known EOS materials")
		
	return Window
	

        self.__WindowThickness = checkAndSetWindowThickness(WindowThickness)
        self.__LaserPulse = checkAndSetLaserPulse(LaserPulse)
        self.__LaserPulseLength = checkAndSetLaserPulseLength(LaserPulseLength)
        self.__LaserWavelength = checkAndSetLaserWavelength(LaserWavelength)
        self.__LaserIntensity = checkAndSetLaserIntensity(LaserIntensity)
	

	
def checkAndSetWindowThickness(WindowThickness):
    """
	Utility to check that the sample thickness is > 1 um and < 500 um
	"""
    # FIND THE BEST WAY TO IGNORE THIS IF THERE IS NO WINDOW.
    # TO DO PLACE HOLDER--------------------------------------------------------------------------------->
    # Set default
    if WindowThickness is None:
      	raise RuntimeError( "Window thickness not specified.")
    
    # Check if ablator is between 1 and 100 um
    if WindowThickness == 0.0:
        pass
    elif WindowThickness < 1.0 or WindowThickness > 500.0:
        raise ValueError( "Window must be between 1.0 and 500.0 microns")
        
    return WindowThickness

def checkAndSetSampleThickness(SampleThickness):
    """
    Utility to check that the sample thickness is > 1 um and < 200 um
    """
    
    # Set default
    if SampleThickness is None:
        raise RuntimeError( "Sample thickness not specified.")
    
    # Check if ablator is between 1 and 100 um
    if SampleThickness < 1.0 or SampleThickness > 200.0:
        raise ValueError( "Ablator must be between 1.0 and 200.0 microns")
    
    return SampleThickness

def checkAndSetLaserWavelength(LaserWavelength):
    """
    Utility to check that the laser wavelength is correct.
    """
    
    print (LaserWavelength)
    
    if LaserWavelength is None:
        raise RuntimeError( "Laser wavelength is not defined")
    
    LaserWavelength = float(LaserWavelength)/1000
    print ("Laser wavelength = %.3fe-6" % (LaserWavelength))
    
    return LaserWavelength
