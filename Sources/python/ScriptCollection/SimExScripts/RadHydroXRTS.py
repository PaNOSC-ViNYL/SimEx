""" Prototype to generate XRTS spectra from inhomogeneous matter using 1D rad-hydro data. """

import SimEx

# Read hydro data
hydro_data = SimEx.Utilities.checkOpenPMD_h5.open_file( "../../../Tests/python/unittest/TestFiles/hydro.opmd.h5")


# Loop over times
total_spectrum = None

for k in hydro_data["/data"].keys():
    meshes = hydro_data["/data"][k]
    unitSI =
    time_step = meshes.attrs["time_step"]*


# Loop over zones

# Calculate Thomson spectrum at each zone

# Integrate on the fly.

