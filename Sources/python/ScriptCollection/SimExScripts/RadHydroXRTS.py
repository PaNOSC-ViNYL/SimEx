""" Prototype to generate XRTS spectra from inhomogeneous matter using 1D rad-hydro data. """
import numpy
import os
import h5py

from SimEx.Calculators.PlasmaXRTSCalculator import PlasmaXRTSCalculator
from SimEx.Parameters.PlasmaXRTSCalculatorParameters import PlasmaXRTSCalculatorParameters

# Read hydro data
path_to_data = os.path.abspath( os.path.join(r"..",r"..",r"..",r"..",r"Tests",r"python",r"unittest",r"TestFiles",r"hydro1D_out_0000001.opmd.h5") )
print path_to_data
hydro_data = h5py.File( path_to_data, 'r' )

Kelvin_to_eV = 1./11806.

# Loop over times
total_spectrum = None

plasma_parameters = PlasmaXRTSCalculatorParameters(
        elements = [["Be", 1, -1]],
        photon_energy=8500.0,
        scattering_angle=40.0,
        electron_temperature=10.0,
        electron_density=1.0e29,
        ion_temperature=None,
        ion_charge=2.0,
        mass_density=1.85,
        debye_temperature=None,
        band_gap=None,
        energy_range={"min" : 8200., "max" : 8500., "step" : 1.0},
        model_Sii="SOCP",
        model_See="RPA",
        model_Sbf="IA",
        model_IPL="EK",
        model_Mix=None,
        lfc=None,
        Sbf_norm=None,
        source_spectrum="GAUSS",
        source_spectrum_fwhm=10.0
        )

ks = ['100']
for k in ks:
    time_entry = hydro_data["/data"][k]
    time_unitSI = time_entry.attrs["timeUnitSI"]
    time_step = time_entry.attrs["dt"] * time_unitSI

    # Get data for this time.
    meshes = hydro_data["/data"][k]['meshes']
    pos = meshes["pos"]
    rho = meshes["pres"]
    temp = meshes["temp"]
    vel = meshes["vel"] ### Use for applying Doppler shift (?)

    # Get number of zones.
    number_of_zones = pos.shape[0]

    # Get information from last zone.
    zone_index = number_of_zones - 1

    # Update plasma parameters.
    plasma_parameters.electron_temperature = temp[zone_index] * Kelvin_to_eV
    plasma_parameters.ion_temperature = temp[zone_index] * Kelvin_to_eV
    plasma_parameters.mass_density = rho[zone_index] * 1e-3

    # Set up the calculator.
    xrts_calculator = PlasmaXRTSCalculator(parameters=plasma_parameters,
        input_path=None,
        output_path=None,
        )

    # Run the calculation.
    print "Processing zone 0 of %d" % (number_of_zones)
    xrts_calculator.backengine()

    # Get the total spectrum.
    total_spectrum = xrts_calculator.data[:,3] * abs(pos[zone_index - 1])

    # Loop over all but last zones.
    for zone in range(number_of_zones - 1):

        print "Processing zone %d of %d" % (zone, number_of_zones)

        # Decrement zone index.
        zone_index -= 1

        # Update plasma parameters.
        plasma_parameters.electron_temperature = temp[zone_index] * Kelvin_to_eV
        plasma_parameters.ion_temperature = temp[zone_index] * Kelvin_to_eV
        plasma_parameters.mass_density = rho[zone_index] * 1e-3

        # Get a new calculator.
        xrts_calculator = PlasmaXRTSCalculatorParameters(parameters=plasma_parameters,
            input_path=None,
            output_path=None,
            )

        # Run calculation.
        xrts_calculator.backengine()

        # Update spectrum.
        total_spectrum += xrts_calculator.data[:,3] * abs(pos[zone_index - 1])
hydro_data.close()
    #import ipdb; ipdb.set_trace()
