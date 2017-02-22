##########################################################################
#                                                                        #
# Copyright (C) 2016,2017 Richard Briggs, Carsten Fortmann-Grote         #
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

import numpy as np
import matplotlib.pyplot as plt

#---------------------------------------------------------------------------
# Materials: [name, EOS shortname, EOS longname, density]
material_type = [0]*13
material_type[1] = ["Aluminium","Al#","Al#_e_ses",2.7]
material_type[2] = ["Diamond","Dia","Dia_e_ses",3.51]
material_type[3] = ["CH","CH2", "CH2_e_ses",1.044]
material_type[4] = ["Kapton","Kap","Kap_e_ses",1.42]
material_type[5] = ["Mo","Mo#","Mo#_e_ses",10.2]
material_type[6] = ["Gold","Au#","Au#_e_ses",19.3]
material_type[7] = ["Iron","Fe#","Fe#_e_ses",7.85]
material_type[8] = ["Copper","Cu#","Cu#_e_ses",8.93]
material_type[9] = ["Tin","Sn#","Sn#_e_ses",7.31]
material_type[10] = ["LiF","LiF","LiF_e_ses",2.64]
material_type[11] = ["Tantalum","Ta#","Ta#_e_ses",16.65]
material_type[12] = ["Titanium","Ti#","Ti#_e_ses",4.43]

# Definitions:
#---------------------------------------------------------------------------
# Ask question for raw input
def ask(question, options):
    choice = raw_input(question).lower() # Turn choice to lower case so we only have to check those

    while choice not in options:
        print "You must pick one of the options above"
        choice = raw_input("Try again:").lower()
    return choice

# Ask question for raw input with default values set as int, float or str
def ask_default(question, default):

    ### State default
    choice = raw_input("%s [%s]:" % (question, str(default)))

    if choice == "":
        print default
        return default

    tpe = type(default)
    return tpe(choice)

# Creates the target layers (IMPORTANT: Currently starts from window to ablator)

def write_layer(i, start_zone, start_r):
    ### f not defined.
    f.write("\n- " + str(thickness[i]) + " um " + material_type[material_in_zone[i]][0] + " layer")
    f.write("\nNOM_MILIEU="+ material_type[material_in_zone[i]][1] +"_"+ str(i) + "")
    f.write("\nEQUATION_ETAT="+ material_type[material_in_zone[i]][2] +"")
    if i==2: # CHANGE THIS TO INCLUDE A CHECK FOR MULTI LAYER TARGETS (SELECT LAST LAYER AND ADD THIS)
        f.write("\nEPAISSEUR_VIDE=60e-6") #
    f.write("\nEPAISSEUR_MILIEU="+ str(thickness[i]) + "e-6")
    f.write("\nNOMBRE_MAILLES="+ str(number_of_zones[i]) +"")
    f.write("\nMECANIQUE_RAM")
    f.write("\n")

    return [start_zone + number_of_zones[i],thickness[i]*1E-4 + start_r]

# Definitions for creating the laser pulse information
def flat_top(pulse_length,laser_intensity):
    f.write("\nDUREE_IMPULSION="+ str(pulse_length) +"e-9")
    f.write("\nINTENSITE_IMPUL_MAX="+ str(laser_intensity) +"e16")
    f.write("\nTEMPS_IMPUL_TABULE=0.0e-9,INTENSITE_TABULEE=0.")
    f.write("\nTEMPS_IMPUL_TABULE=0.2e-9,INTENSITE_TABULEE=1")
    f.write("\nTEMPS_IMPUL_TABULE="+ str(pulse_length) +"e-9,INTENSITE_TABULEE=1")
    f.write("\nTEMPS_IMPUL_TABULE="+ str(pulse_length) +"e-9,INTENSITE_TABULEE=0.")
    f.write("\n")

def ramp_t3(pulse_length,laser_intensity,x,y):
    f.write("\nDUREE_IMPULSION="+ str(pulse_length) +"e-9")
    f.write("\nINTENSITE_IMPUL_MAX="+ str(laser_intensity) +"e16")
    for i in range(1,len(x)):
        f.write("\nTEMPS_IMPUL_TABULE="+ str(x[i]) +"e-9,INTENSITE_TABULEE="+ str(y[i]) +"")
    f.write("\n")

# Set declarations
#---------------------------------------------------------------------------
material_in_zone = [0]
thickness = [0]
width_of_zone = [0]
number_of_zones = [0]

# CHOOSE TARGET TYPE
#---------------------------------------------------------------------------
# Next version: have options for default targets (diamond window, plastic with / without windows etc.)
#
# EG. Take ablator parameters from an input file and run script quicker (go straight to laser properties)
#
# Set the total number of layers
number_of_layers = int(raw_input("\nNumber of layers in target (including ablator): "))

# Create arrays for each layer
for i in range(number_of_layers):
    material_in_zone = material_in_zone + [0]
    thickness = thickness + [0]
    width_of_zone = width_of_zone + [0]
    number_of_zones = number_of_zones + [0]

# ABLATOR (THICKNESS AND ZONE FEATHERING)
#---------------------------------------------------------------------------
# Provide list of materials for ablator
# CHANGE THIS SO THAT IT ONLY SHOWS PLASTIC, DIAMOND ETC.
print "\nAblating material:"
for i,mtp in enumerate(material_type):
    print "\n\t", i, "\b.", mtp[0],

material_in_zone[1] = ask_default("\n\nChoice", 3)
thick = ask_default("Enter ablator thickness in um", 20.0)
n = ask_default("Enter number of mesh points in feathered zone", 250)
number_of_zones[0] = n
S = ask_default("Enter width of feathered region in um", 5.0)
a = ask_default("Enter minimum zone width allowed in um", 1E-4)

width = thick-S

# Determine the correct feathering
### code duplication with relevant Parameters class.
list = [0]*(n+1)
list[0]=1
list[-2]=-S/a
list[-1]=S/a-1

f = np.poly1d(list)
#print "\nSolving:\n\n", f
roots = np.roots(f)
root_found = False

for i in range(n):
    if roots[i].imag == 0 and roots[i].real > 1.000001:
        #print "Setting ratio to be: ", round(roots[i].real,4)
        r = round(roots[i].real,4)
        root_found = True

if root_found == False:
    print "No ratio bigger than 1.000001 found...exiting"
    exit()

# Determine final feathered zone width (used in Esther)
final_feathered_zone_width = a*(r**n)
final_feather_zone_width=round(final_feathered_zone_width,4)

# Determine number of remaining zones for ablator
N = int(width/(a*(r**n)))
number_of_zones[1] = N

mass_of_zone = a*(r**n)*material_type[material_in_zone[1]][3]

# SAMPLE + WINDOW (REMAINING LAYER CHOICES)
#---------------------------------------------------------------------------
# FIX SO THAT THE LAYERS CAN BE WRITTEN IN THE NORMAL WAY OF ABLATOR TO WINDOW
# FOR NOW THIS MUST BE RUN FROM THE WINDOW TO THE SAMPLE
for i in range(2,number_of_layers+1):
    print "\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
    print "\nREMINDER: START FROM WINDOW AS 2ND LAYER, THEN ADD NEXT LAYERS TOWARDS ABLATOR AS 3, 4 ETC."
    print "What material is layer",i,":\n"
    for j in range(1,len(material_type)):
        print "\t", j, ". ", material_type[j][0]
    material_in_zone[i] = int(ask("\n\nChoice: ", ["1","2","3","4","5","6","7","8","9","10","11","12"]))
    thickness[i] = float(raw_input("Thickness of layer " + str(i) + " (in um)? "))

    width_of_zone[i] = mass_of_zone/material_type[material_in_zone[i]][3]
    number_of_zones[i] = int(thickness[i]/width_of_zone[i])


# PRINT USEFUL OUTPUTS FOR USER:
print "-----------------------------------------------------------"
print "Ablator configuration:"
print "Number of zones required in non-feathered region: ", N
print "Final feathered zone width : %.4f" % final_feathered_zone_width, "um"
print "Zone information:"
print "Number of zones in each region: ", number_of_zones
print "Total number of zones: ", sum(number_of_zones)
print "-----------------------------------------------------------"
print_to_file = ask("Print input file? (y/n): ",["y","n"])

if print_to_file == "y":
    file_number = raw_input("Filenumber: ")
    is_number = False
    while is_number == False:
        try:
            file_number = int(file_number)
            is_number = True
        except:
            is_number = False
            print "Please enter a number."
            file_number = raw_input("Filenumber: ")

    f = open(str(file_number) + ".txt", 'w')
    transfert_radiatif = ask("Include transfert_radiatif? (y/n): ", ["y","n"])
    f.write("DEMARRAGE,USI\n")
    if transfert_radiatif == "y":
    	f.write("TRANSFERT_RADIATIF\n")
    f.write("\n")
    f.write("MILIEUX_INT_VERS_EXT\n")

    start_zone = N+n
    start_r = S*1E-4+width*1E-4

    for i in range(2,number_of_layers+1):
        start_values = write_layer(i,start_zone,start_r)
        start_zone = start_values[0]
        start_r = start_values[1]

    #   Laser interaction zones will always be the first 2 in the material array [0] and [1]
    f.write("\n")
    f.write("\nNOM_MILIEU="+ material_type[material_in_zone[1]][1] +"_abl1")
    f.write("\nEQUATION_ETAT="+ material_type[material_in_zone[1]][2] +"")
    f.write("\nEPAISSEUR_MILIEU="+ str(width) + "e-6")
    f.write("\nNOMBRE_MAILLES="+ str(number_of_zones[1]) +"")
    f.write("\nMECANIQUE_RAM")

    f.write("\n")
    f.write("\nNOM_MILIEU="+ material_type[material_in_zone[1]][1] + "_abl2")
    f.write("\nEQUATION_ETAT="+ material_type[material_in_zone[1]][2] +"")
    f.write("\nEPAISSEUR_MILIEU="+ str(S) + "e-6")
    f.write("\nEPAISSEUR_INTERNE="+ str(round(final_feathered_zone_width,3)) + "e-6")
    f.write("\nEPAISSEUR_EXTERNE="+ str(a*10000) +"e-10")
    f.write("\nMECANIQUE_RAM")
    f.write("\n")
    f.write("\nINDICE_REEL_LASER=1.46") # Refractive index of material (add to material_in_zone[] later)
    f.write("\nINDICE_IMAG_LASER=1.0")
    f.write("\n")
    f.write("\nDEPOT_ENERGIE,LASER,DEPOT_HELMHOLTZ")
    f.write("\nLONGUEUR_ONDE_LASER=1.06e-6")

    # Choose laser pulse type
    #---------------------------------------------------------------------------

    pulse_type = [0]*4
    pulse_type[1] = ["Flat top", 1]
    pulse_type[2] = ["Ramp - t**3", 2]
    pulse_type[3] = ["Ramp - linear",3]

    print "\nLaser pulse shape"
    for i in range(1,len(pulse_type)):
        print "\t", i, "\b.", pulse_type[i][0]

    pulse_choice = raw_input("\nChoose laser pulse 1, 2 or 3: ")
    pulse_length = raw_input("Pulse Length (ns): ")
    pulse_length = float(pulse_length)
    laser_intensity = raw_input("Laser Intensity (TW/cm**2), e.g. 1.0 : ")

    if pulse_choice == "1":
        #print "Flat top"
        x = [0,0.2,pulse_length-0.2,pulse_length]
        y = [0, 1.0, 1.0, 0]
        flat_top(pulse_length,laser_intensity) # write laser pulse to file
    elif pulse_choice == "2":
        #print "Ramp with t**3"
        x = np.arange(0.,pulse_length+1,1)
        y = x**3
        y = y/np.amax(y)
        ramp_t3(pulse_length,laser_intensity,x,y) # write laser pulse to file
    elif pulse_choice == "3":
        #print "Ramp (linear)"
        x = [0,pulse_length]
        y = [0,1.0]
        # ADD LINEAR DEFINITION TO START FOR WRITING TO MAIN FILE
    else:
        print "Problem selecting laser pulse"
    #quit

    f.write("\nSORTIES_GRAPHIQUES")
    f.write("\nDECOUPAGE_TEMPS")
    f.write("\nBORNE_TEMPS=16e-9") # NEED TO BE ABLE TO ADJUST THIS
    f.write("\nINCREMENT_TEMPS=0.05e-9") # NEED TO BE ABLE TO ADJUST THIS
    f.write("\n")
    f.write("\nARRET")
    f.write("\nTEMPS_ARRET=16e-9") # NEED TO BE ABLE TO ADJUST THIS
    f.write("\n")
    f.write("\nFIN_DES_INSTRUCTIONS")

    f.close()

    plt.xlabel('Time (ns)')
    plt.ylabel('Intensity (TW/cm**2)')
    plt.title('Laser pulse')
    plt.grid(True)
    plt.plot(x, y*float(laser_intensity), 'ro-')

    plt.show()

#foo = pulse_length-0.2
#    f = open(str(file_number) + "_intensite_impulsion.txt", 'w')
#    f.write("4\n")
#    f.write("temps (s ou u.a.) intensite (W/m2 ou u.a.)\n")
#    f.write("0.\t0\n")
#    f.write("0.2e-9\t" + str(laser_intensity) + "\n")
#    f.write("" + str(foo) + "e-9\t" + str(laser_intensity) + "\n")
#    f.write("" + str(pulse_length) + "e-9\t0.\n")
#    f.write("fin_de_fichier")
