from SimEx.Calculators.XCSITPhotonDetector import XCSITPhotonDetector
from SimEx.Calculators.XCSITPhotonDetectorParameters import XCSITPhotonDetectorParameters

import sys
import numpy as np

# Setup propagation parameters.
parameters=XCSITPhotonDetectorParameters(detector_type="AGIPDSPB")

# Path to source files (ADJUST ME).
input_files_path = "diffr/diffr_out_0000001.h5"

# Construct the propagator
detector = XCSITPhotonDetector( parameters=parameters,
                             	input_path=input_files_path,
                             	output_path='detector/detector_out.h5')

# Read the data.
detector._readH5()

# Call the backengine.
status = detector.backengine()

if status != 0:
    print "Detector simulation failed, check output."
    sys.exit()

detector.saveH5()

print("Detector simulation succeeded.")
print(" ")



# -------------------------------------------------------------------------------
#                               Ploting the steps
# -------------------------------------------------------------------------------
print("Plot the data containers")
import matplotlib.pyplot as plt
import h5py

# Read the pixel width
x_pixel = 0
y_pixel = 0
with h5py.File('detector/detector_out.h5','r') as h5:
    x_pixel = h5["/params/geom/pixelWidth"].value
    y_pixel = h5["/params/geom/pixelHeight"].value


# Photons
# =======

# Original data
with h5py.File('diffr/diffr_out_0000001.h5',"r") as h5_infile:
    keys = h5_infile["/data"].keys()
    matrix = h5_infile["/data/"+ keys[0] + "/diffr"].value
    photons = np.zeros((len(matrix),len(matrix[0])),dtype=np.float_)

    # Get the array where each pixel contains a number of photons
    # Explaination:
    #       /data/.../data are poissonized patterns
    #       /data/.../diffr are the intensities
    for i in h5_infile["/data"].keys():
        #    print(h5_infile["/data/"+i+"/diffr"].name)
        photons += h5_infile["/data/"+i+"/diffr"].value

plt.figure()
plt.title('Original Photons from the hdf5 file')
plt.xlabel("detector pixel in x")
plt.ylabel("detector pixel in y")
plt.imshow(photons,cmap='YlOrRd')
plt.colorbar()
plt.savefig("detector/orgphotons.png")


# Histogram of the datacontainer photons
photons=detector.getPhotonData()
x_photons = np.zeros((photons.size(),),dtype=np.float_)
y_photons = np.zeros((photons.size(),),dtype=np.float_)
for i in list(range(photons.size())):
    entry = photons.getEntry(i)
    x_photons[i] = entry.getPositionX()
    y_photons[i] = entry.getPositionY()

plt.figure()
plt.title('Histogram of the photon positions stored in the photon container')
plt.xlabel("x/[m]")
plt.ylabel("y/[m]")
H,xedges,yedges = np.histogram2d(x_photons,y_photons,bins=[512,512],range=[[-512*x_pixel/2,512*x_pixel/2],[-512*y_pixel/2,512*y_pixel/2]])
plt.imshow(H,interpolation='none',extent=[-512*x_pixel/2,512*x_pixel/2,-512*y_pixel/2,512*y_pixel/2],cmap='YlOrRd')
plt.colorbar()
plt.savefig("detector/photons.png")

# Histogram of the interaction container
interacts = detector.getInteractionData()
x_interacts = np.zeros((interacts.size(),),dtype=np.float_)
y_interacts = np.zeros((interacts.size(),),dtype=np.float_)
for i in list(range(interacts.size())):
    entry = interacts.getEntry(i)
    x_interacts[i] = entry.getPositionX()
    y_interacts[i] = entry.getPositionY()

plt.figure()
plt.title('Histogram of the interaction positions stored in the interaction container')
plt.xlabel("x/[m]")
plt.ylabel("y/[m]")
H,xedges,yedges = np.histogram2d(x_interacts,y_interacts,bins=[512,512],range=[[-512*x_pixel/2,512*x_pixel/2],[-512*y_pixel/2,512*y_pixel/2]])
plt.imshow(H,interpolation='none',extent=[-512*x_pixel/2,512*x_pixel/2,-512*y_pixel/2,512*y_pixel/2],cmap='YlOrRd')
plt.colorbar()
plt.savefig("detector/interactions.png")

# Check if the output data are similar
print("Print output from hdf5 file")
with h5py.File('detector/detector_out.h5','r') as h5:
    image=h5["/data/data"].value
    plt.figure()
    plt.title('Charge at each pixel of the detector stored the hdf5 output file')
    plt.xlabel('pixel in x direction')
    plt.ylabel('pixel in y direction')
    plt.imshow(image,cmap='YlOrRd')
    plt.colorbar()
    plt.savefig("detector/charge.png")


# Show the plots
plt.show()
