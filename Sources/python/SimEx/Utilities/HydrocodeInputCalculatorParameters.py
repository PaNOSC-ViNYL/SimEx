##########################################################################
#                                                                        #
# Copyright (C) 2016-2017 Richard Briggs, Carsten Fortmann-Grote         #
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

BOOL_TO_INT = {True : 1, False : 0}

class HydroParameters(AbstractCalculatorParameters):
    """
    class representing parameters for the Hydrocode Input Calculator
    """
    def __init__(self,
                 number_of_layers,
                 ablator=None,
                 ablator_thickness=None,
                 sample=None,
                 sample_thickness=None,
                 window=None,
                 window_thickness=None,
                 laser_wavelength=None,
                 laser_pulse=None,
                 laser_pulse_duration=None,
                 laser_intensity=None,
                 ):

        """
        Constructor for the HydroParameters

        :param ablator: The ablating material ( "Al" | "CH" | "Diamond" )
        :type ablator: str

        :param ablator_thickness: The ablator thickness (micrometers)
        :type ablator_thickness:

        :param sample: The sample material (from limited list of materials)
        :type sample: str

        :param sample_thickness: The sample thickness (micrometers)
        :type sample_thickness: float

        :param window: The window material (LiF | SiO2 | Diamond)
        :type window: str

        :param window_thickness: The window thickness, if using window (micrometers)
        :type window_thickness: float

        :param laser_pulse: Pulse type ("flat" | "ramp" | "other")
        :type laser_pulse: str

        :param laser_pulse_duration: Pulse duration of the pump laser (ns)
        :type laser_pulse_duration: float

        :param laser_wavelength: Laser wavelength (nm)
        :type laser_wavelength: float

        :param laser_intensity: Laser intensity (TW/cm2)
        :type laser_intensity: float
        """

        # Check and set all parameters
        self.__number_of_layers = checkAndSetNumberOfLayers(number_of_layers)
        self.__ablator = checkAndSetAblator(ablator)
        self.__ablator_thickness = checkAndSetAblatorThickness(ablator_thickness)
        self.__sample = checkAndSetSample(sample)
        self.__sample_thickness = checkAndSetSampleThickness(sample_thickness)
        self.__window = checkAndSetWindow(window)
        self.__window_thickness = checkAndSetWindowThickness(window_thickness)
        self.__laser_wavelength = checkAndSetLaserWavelength(laser_wavelength)

        # Set internal parameters
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
        ### variables names: all_small_with_underscores
        ### methods (except property get/set/delete) camelCase()
        number_of_zones = n
        feather_zone_width = 5.0
        minimum_zone_width = 1.E-4
        externe_value = minimum_zone_width*1.e4
        non_feather_zone_width = self.ablator_thickness - feather_zone_width


        # Determine the correct feathering
        ### More verbose comments.
        # Setup feather zones.
        feather_list=numpy.zeros(n+1)
        feather_list[0]=1
        feather_list[-2]=-feather_zone_width/minimum_zone_width
        feather_list[-1]=-feather_list[-2] - 1

        # Find roots in polynomial over the feathers
        f = numpy.poly1d(list)
        roots = numpy.roots(f)
        root_found = False

        # Get all purely real roots above 1.
        for i in range(n):
            if roots[i].imag == 0 and roots[i].real > 1.000001: # Why not > 1.? This would exclude 1.0f
                r = round(roots[i].real,4)
                root_found = True

        if root_found == False:
            raise RuntimeError( "No ratio bigger than 1.000001 was found.")

        # Set final values for zone widths.
        final_feather_zone_width = round(minimum_zone_width*(r**n),4)
        non_feather_zones = int(non_feather_zone_width/(minimum_zone_width*(r**n)))

        # Dictionary for Esther EOS files
        # TO DO: Add remaining elements from the esther eos folder
        material_dict = {}
        material_dict["Al"] = {"name" : "Aluminum",
                               "shortname" : "Al#",
                               "eos_name" : "Al#_e_ses",
                               "mass_density" : 2.7,
                               },
        material_dict["CH"] = {"name" : "CH",
                               "shortname" : "CH2",
                               "eos_name" : "CH2_e_ses",
                               "mass_density" : 1.044,
                               },
        material_dict["Dia"] = {"name" : "Diamond",
                               "shortname" : "Dia",
                               "eos_name" : "Dia_e_ses",
                               "mass_density" : 3.51,
                               },
        material_dict["Kap"] = {"name" : "Kapton",
                               "shortname" : "Kap",
                               "eos_name" : "Kap_e_ses",
                               "mass_density" : 1.42,
                               },
        material_dict["Mo"] = {"name" : "Mo",
                               "shortname" : "Mo#",
                               "eos_name" : "Mo#_e_ses",
                               "mass_density" : 10.2,
                               },
        material_dict["Au"] = {"name" : "Gold",
                               "shortname" : "Au#",
                               "eos_name" : "Au#_e_ses",
                               "mass_density" : 19.3,
                               },
        material_dict["Fe"] = {"name" : "Iron",
                               "shortname" : "Fe#",
                               "eos_name" : "Fe#_e_ses",
                               "mass_density" : 7.85,
                               },
        material_dict["Cu"] = {"name" : "Copper",
                               "shortname" : "Cu#",
                               "eos_name" : "Cu#_e_ses",
                               "mass_density" : 8.93,
                               },
        material_dict["Sn"] = {"name" : "Tin",
                               "shortname" : "Sn#",
                               "eos_name" : "Sn#_e_ses",
                               "mass_density" : 7.31,
                               },
        material_dict["LiF"] = {"name" : "Lithium Fluoride",
                               "shortname" : "LiF",
                               "eos_name" : "LiF_e_ses",
                               "mass_density" : 2.64,
                               },
        material_dict["Ta"] = {"name" : "Tantalum",
                               "shortname" : "Ta#",
                               "eos_name" : "Ta#_e_ses",
                               "mass_density" : 16.65,
                               },
        material_dict["Ti"] = {"name" : "Titanium",
                               "shortname" : "Ti#",
                               "eos_name" : "Ti#_e_ses",
                               "mass_density" : 4.43,
                               },
        # Determine the mazz of one zone
        mass_of_zone = final_feather_zone_width*material_dict[self.ablator]["mass_density"]

        #al_density = material_dict["Al"]["mass_density"]

        # Make a temporary directory
        self._tmp_dir = tempfile.mkdtemp(prefix='esther_')

        # Write the input file
        input_deck_path = os.path.join( self._tmp_dir, 'input.dat')
        print "Writing input deck to ", input_deck_path, "."

        # Write the file.
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
            # Then change number_of_sample_zones to number_of_zones[i] for i < number of layers
            # TO DO PLACEHOLDER -------------------------------------------------------------->
            input_deck.write('- %.1f um %s layer\n' % (self.sample_thickness, self.sample))
            input_deck.write('NOM_MILIEU=%s\n' % (self.sample)) # DOES material_dict[self.sample]["shortname"] work here?
            input_deck.write('EQUATION_ETAT=EOS_LIST\n') # %s DOES material_dict[self.sample]["eos_name"] work here?
            if self.__use_window == False:
                input_deck.write('EPAISSEUR_VIDE=100e-6\n')
            input_deck.write('EPAISSEUR_MILIEU=%.1fe-6\n' % (self.sample_thickness))
            # Calculate number of zones
            width_of_sample_zone = mass_of_zone/material_type[self.sample]["mass_density"]
            number_of_sample_zones=int(self.samplethickness/width_of_sample_zone)
            input_deck.write('NOMBRE_MAILLES=%d\n' % (number_of_sample_zones))
            input_deck.write('\n')

            #width_of_zone[i] = mass_of_zone/material_type[material_in_zone[i]][3]
            #number_of_zones[i] = int(thickness[i]/width_of_zone[i])

            # Write ablator
            input_deck.write('- %.1f um %s layer\n' % (self.ablator_thickness, self.ablator))
            input_deck.write('NOM_MILIEU=abl1\n') # 1ST PART OF ABLATOR
            input_deck.write('EQUATION_ETAT=EOS_FROM_LIST\n') # ABLATOR EOS
            # if only simulating ablator layer, then must include empty (VIDE) layer
            if self.number_of_layers == 1:
                input_deck.write('EPAISSEUR_VIDE=100e-6\n')
            input_deck.write('EPAISSEUR_MILIEU=%.1fe-6\n' % (non)) # Non-feather thickness
            input_deck.write('NOMBRE_MAILLES=%d\n' % (non_feather_zones)) # Number of zones
            input_deck.write('\n')
            input_deck.write('NOM_MILIEU=abl2\n') # 1ST PART OF ABLATOR
            input_deck.write('EQUATION_ETAT=EOS_FROM_LIST\n') # ABLATOR EOS
            input_deck.write('EPAISSEUR_MILIEU=%.1fe-6\n' % (feather_zone_width)) # Feather thickness
            input_deck.write('EPAISSEUR_INTERNE=%.3fe-6\n' % (final_feather_zone_width)) # Feather final zone width
            input_deck.write('EPAISSEUR_EXTERNE=%.1fe-10\n' % (externe_value)) #Min zone width
            input_deck.write('\n')

            # Internal parameters to add to flags
            # TO DO PLACEHOLDER -------------------------------------------------------------->
            input_deck.write('INDICE_REEL_LASER=1.46\n')
            input_deck.write('INDICE_IMAG_LASER=1.0\n')
            input_deck.write('DEPOT_ENERGIE,LASER,DEPOT_HELMHOLTZ\n')
            input_deck.write('LONGUEUR_ONDE_LASER=%.3fe-6\n' % (self.laser_wavelength))

    @property
    def number_of_layers(self):
       	""" Query for the number of layers. """
       	return self.__number_of_layers
    @number_of_layers.setter
    def number_of_layers(self, value):
       	""" Set the number of layers to the value. """
       	self.__number_of_layers = checkAndSetnumber_of_layers(value)

    @property
    def ablator(self):
       	""" Query for the ablator type. """
       	return self.__ablator
    @ablator.setter
    def ablator(self, value):
       	""" Set the ablator to the value. """
       	self.__ablator = checkAndSetAblator(value)

    @property
    def ablator_thickness(self):
       	""" Query for the ablator thickness. """
       	return self.__ablator_thickness
    @ablator_thickness.setter
    def ablator_thickness(self, value):
       	""" Set the ablator thickness to the value. """
       	self.__ablator_thickness = checkAndSetAblatorThickness(value)

    @property
    def sample(self):
       	""" Query for the sample type. """
       	return self.__sample
    @sample.setter
    def sample(self, value):
       	""" Set the sample type to the value. """
       	self.__sample = checkAndSetSample(value)

    @property
    def sample_thickness(self):
       	""" Query for the sample thickness type. """
       	return self.__sample_thickness
    @sample_thickness.setter
    def sample_thickness(self, value):
       	""" Set the sample thickness to the value. """
       	self.__sample_thickness = checkAndSetSampleThickness(value)

    @property
    def window(self):
       	""" Query for the window type. """
       	return self.__window
    @window.setter
    def window(self, value):
       	""" Set the window to the value. """
       	self.__window = checkAndSetWindow(value)

    @property
    def window_thickness(self):
       	""" Query for the window thickness type. """
       	return self.__window_thickness
    @window_thickness.setter
    def window_thickness(self, value):
       	""" Set the window thickness to the value. """
       	self.__window_thickness = checkAndSetWindowThickness(value)

    @property
    def LaserWavelength(self):
       	""" Query for the laser wavelength type. """
       	return self.__laser_wavelength
    @laser_wavelength.setter
    def laser_wavelength(self, value):
       	""" Set the laser wavelength to the value. """
       	self.__laser_wavelength = checkAndSetLaserWavelength(value)

###########################
# Check and set functions #
###########################

def checkAndSetNumberOfLayers(number_of_layers):
    """
    Utility to check if the number of layers is reasonable.

    :param number_of_layers: The number of layers to check
    :return: Checked number of layers
    :raise ValueError: not (1 < number_of_layers <=5 )

    """
    if number_of_layers is None:
        raise RuntimeError( "Number of layers is not defined.")

    if number_of_layers <=1 or number_of_layers > 5:
        raise ValueError( "Number of layers must be between 1 and 5 only.")

    return number_of_layers

def checkAndSetAblator(ablator):
	"""
	Utility to check if the ablator exists in the EOS database.

    :param ablator: The ablator material to check.
    :return: The ablator choice after being checked.
    :raise ValueError: ablator not in ["CH", "Al", "Diamond"].

	"""

	if ablator is None:
		raise RuntimeError( "The parameter 'ablator' is not defined.")

    ### Could check if isinstance(ablator, str)
	# Check if ablator is CH, Al or diamond
	if ablator == 'CH':
		print ( "Setting CH as ablator.")
	elif ablator == 'Al':
		print ( "Setting Al as ablator.")
	elif ablator.lower() in ['dia', 'diamond']:
		print ( "Setting diamond as ablator.")
	else:
		raise ValueError( "Ablator is not valid. Use 'CH', 'Al' or 'dia'.")

	return ablator

def checkAndSetAblatorThickness(ablator_thickness):
	"""
	Utility to check that the ablator thickness is > 5 um and < 100 um
	"""

	# Raise if not set.
	if ablator_thickness is None:
		raise RuntimeError( "Ablator thickness not specified.")

	# Check if ablator is between 5 and 100 um
	if ablator_thickness <= 5.0 or ablator_thickness > 100.0:
		raise ValueError( "Ablator must be between 5.0 and 100.0 microns")

	print ( "Ablator thickness is %4.1f " % ablator_thickness)

	return ablator_thickness

def checkAndSetSample(sample):
	"""
	Utility to check if the sample is in the list of known EOS materials
	"""

    ### Could utilize periodictable module...
	elements = ["Aluminium", "Gold", "Carbon", "CH", "Cobalt", "Copper", "Diamond",
				"Iron", "Molybdenum", "Nickel", "Lead", "Silicon", "Tin", "Tantalum"]

	# Set default
	if sample is None:
		raise RuntimeError( "sample not specified.")

	# Check each element
	if sample in elements:
		pass
	else:
		raise ValueError( "sample is not in list of known EOS materials")

	return sample

def checkAndSetSampleThickness(sample_thickness):
	"""
	Utility to check that the sample thickness is in permissible range (Esther constraint).
	"""

	# Set default
	if sample_thickness is None:
		raise RuntimeError( "sample thickness not specified.")

	# Check if sample thickness is in permissible range.
	if sample_thickness < 1.0 or sample_thickness > 200.0:
		raise ValueError( "Ablator must be between 1.0 and 200.0 microns")

	return sample_thickness

def checkAndSetWindow(window):
    """
    Utility to check that the window thickness is > 1 um and < 200 um
    """
    # Change this to be just window materials (LiF, Quartz etc.)
    ### TODO PLACEHOLDER ------------------------------------------------------------------------------>
    elements = ["Aluminium", "Gold", "Carbon", "CH", "Cobalt", "Copper", "Diamond",
                "Iron", "Molybdenum", "Nickel", "Lead", "Silicon", "Tin", "Tantalum"]

    if window is None:
        print ( "Running simulation without window material")
    else:
        # Check each element
        if window in elements:
            pass
        else:
            raise ValueError( "window is not in list of known EOS materials")

    return window

def checkAndSetWindowThickness(window_thickness):
    """
    Utility to check that the window thickness is > 1 um and < 500 um
    """
    # FIND THE BEST WAY TO IGNORE THIS IF THERE IS NO WINDOW.
    # TO DO PLACE HOLDER--------------------------------------------------------------------------------->
    ### One solution could be to call this function from within checkAndSetWindow if window is not None.
    # Set default
    if window_thickness is None:
        raise RuntimeError( "Window thickness not specified.")

    # Check if ablator is between 1 and 100 um
    if window_thickness == 0.0:
        pass
    elif window_thickness < 1.0 or window_thickness > 500.0:
        raise ValueError( "Window must be between 1.0 and 500.0 microns")

    return window_thickness

def checkAndSetLaserWavelength(laser_wavelength):
    """
    Utility to check that the laser wavelength is correct.
    """

    print (laser_wavelength)

    if laser_wavelength is None:
        raise RuntimeError( "Laser wavelength is not defined")

    # Convert to microns.
    laser_wavelength = laser_wavelength*1e-3
    print ("Laser wavelength = %.3fe-6" % (laser_wavelength))

    return laser_wavelength
