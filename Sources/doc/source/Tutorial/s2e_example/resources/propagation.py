from SimEx.Calculators.XFELPhotonPropagator import XFELPhotonPropagator
from SimEx.Parameters.WavePropagatorParameters import WavePropagatorParameters

#
from prop import exfel_spb_kb_beamline as beamline
import sys

# Setup propagation parameters.
parameters=WavePropagatorParameters(beamline=beamline)

# Path to source files (ADJUST ME).
input_files_path = "source/3fs_5keV_nz35_0000001.h5"

# Construct the propagator
propagator = XFELPhotonPropagator( parameters=parameters,
                             input_path=input_files_path,
                             output_path='prop_out/prop_s2e_example.h5')

# Read the data.
propagator._readH5()

# Call the backengine.
status = propagator.backengine()

if status != 0:
    print "Wave propagation failed, check output."
    sys.exit()

propagator.saveH5()

print "Wave propagation succeeded."
