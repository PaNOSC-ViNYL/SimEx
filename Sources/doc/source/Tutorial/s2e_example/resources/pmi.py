import sys
from SimEx.Calculators.XMDYNDemoPhotonMatterInteractor import XMDYNDemoPhotonMatterInteractor

# Define the input path (location of propagated pulse data).
prop_path = "prop_out/prop_s2e_example.h5"

# Define the sample as pdb code + ".pdb" extension.
sample="2NIP.pdb"

# Setup propagation parameters.
parameters=None

# Construct the propagator
pmi_calculator = XMDYNDemoPhotonMatterInteractor( parameters=parameters, input_path=prop_path,
        sample_path=sample)

# Read the data.
pmi_calculator._readH5()

# Call the backengine.
status = pmi_calculator.backengine()

if status != 0:
    print "PMI calculation failed, check output."
    sys.exit()

print "PMI calculation succeeded."
