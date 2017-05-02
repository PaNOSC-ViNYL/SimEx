
import numpy as np
import matplotlib.pyplot as plt

# Parameters to set
filename = "Nickel.txt"
thickness = 5e-4 # Value in microns (5um = 5e-4)

# Setup arrays
energy=[]
mu1=[]
mu2=[]
absorption=[]

# Open filename
f = open(filename)

# Read data
while True:
    temp = f.readline()
    if len(temp) < 5: # End of data reached
        print ("End of data reached.")
        break
    else:
        temp = temp.split()
        if temp[0] == "L1":
            L1_edge = float(temp[1])*1e6
            energy_temp=float(temp[1])
            mu1_temp=float(temp[2])
            mu2_temp=float(temp[3])
            energy.append(energy_temp)
            mu1.append(mu1_temp)
            mu2.append(mu2_temp)
        elif temp[0] == "K":
            K_edge = float(temp[1])*1e6
            energy_temp=float(temp[1])
            mu1_temp=float(temp[2])
            mu2_temp=float(temp[3])
            energy.append(energy_temp)
            mu1.append(mu1_temp)
            mu2.append(mu2_temp)
        else:
            energy_temp=float(temp[0])
            mu1_temp=float(temp[1])
            mu2_temp=float(temp[2])
            energy.append(energy_temp)
            mu1.append(mu1_temp)
            mu2.append(mu2_temp)


for i in range(0,len(mu1)):
    tmp = 1.0*np.exp(-mu1[i]*8.098*thickness)
    absorption.append(tmp)
    energy[i]*=1e6


plt.subplot(2,1,1)
plt.plot(energy, mu1, color='blue', lw=2)
plt.yscale('log')
plt.xscale('log')
plt.xlabel('Energy (eV)')
plt.ylabel('mass absorption coefficient')

plt.subplot(2,1,2)
plt.plot(energy, absorption, color='blue', lw=2)
plt.axis([K_edge-2000.0,K_edge+2000,0.0,1.0])
plt.xlabel('Energy (eV)')
plt.ylabel('Transmission')

plt.show()
