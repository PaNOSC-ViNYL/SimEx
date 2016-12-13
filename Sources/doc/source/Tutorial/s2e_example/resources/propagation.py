from SimEx.Calculators.WavePropagator import WavePropagator
from SimEx.Utilities.WPGBeamlines import setup_S2E_SPI_beamline

import sys

# Define a beamline.
beamline = setupSPBDay1Beamline()

# Setup propagation parameters.
parameters=WavePropagatorParameters(beamline=beamline)

# Path to source files (ADJUST ME).
input_files_path = None

while input_files_path is None:
    input_files_path = raw_input("Specify path to source files directory")

# Construct the propagator
propagator = WavePropagator( parameters=parameters, input_path=input_files_path)

# Read the data.
propagator._readH5()

# Call the backengine.
status = propagator.backengine()

if status != 0:
    print "Wave propagation failed, check output."
    sys.exit()

print "Wave propagation succeeded."
