# SIMEX example script for calculation of X-ray Thomson Scattering from a plasma
from SimEx import PlasmaXRTSCalculatorParameters
from SimEx import PlasmaXRTSCalculator

source_input = "prop_out.h5"

parameters = PlasmaXRTSCalculatorParameters(
                 elements=[['Be', 1, -1]],      # Stochiometry and partial charges
                 photon_energy=4970.0,          # [eV]
                 scattering_angle=30.0,         # [deg]
                 electron_temperature=13.0,     # [eV/kB]
                 electron_density=None,       # [1/cm**3]
                 ion_temperature=6.0,           # [eV]
                 ion_charge=2.0,
                 mass_density=1.85,             # [g/cm**3]
                 debye_temperature=None,
                 band_gap=None,
                 energy_range={'min' : -200.0,  # Min. energy/eV to calculate (relative to photon energy)
                               'max' :  200.0,  # Max. energy/eV to calculate (relative to photon energy)
                               'step':    1.0}, # Energy binning/eV.
                 model_Sii='DH',                # Use Debye-Hueckel
                 model_See='RPA',               # Use Born-Mermin
                 model_Sbf='IA',                # Use impulse approximation
                 model_IPL=0.0,                 # No ionization potential lowering.
                 model_Mix=None,                # Use default (advanced mixing).
                 lfc=None,                      # No local field correction.
                 Sbf_norm=None,                 # No normalization of the bound-free spectrum.
                 source_spectrum='PROP',        # Source spectrum will be taken from wavefront input.
                 source_spectrum_fwhm=None,     # Not needed here.
                    )


xrts_calculator = PlasmaXRTSCalculator(parameters=parameters,
                                       input_path=source_input,
                                       output_path='Be_xrts.h5')
xrts_calculator._readH5()
xrts_calculator.backengine()

data = xrts_calculator.data
energies = data[:,0]
See = data[:,1]
Sbf = data[:,2]
Stot = data[:,3]

import pylab
pylab.plot(energies, See, label="free-free")
pylab.plot(energies, Sbf, label="bound-free")
pylab.plot(energies, Stot, label="total")

pylab.xlabel("energy (eV)")
pylab.ylabel(r"$S(k,\omega)$ (1/eV)")

pylab.legend()

pylab.show()
