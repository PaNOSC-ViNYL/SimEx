import sys
from SimEx.Calculators.SingFELPhotonDiffractor import SingFELPhotonDiffractor
from SimEx.Parameters.SingFELPhotonDiffractorParameters import SingFELPhotonDiffractorParameters

# Define the input path (location of pmi trajectories.)
pmi_path = "pmi/"

# Give path of beam and geom files.
beam = "s2e.beam" # e.g. s2e.beam
geom = "s2e.geom" # e.g. s2e.geom

parameters= SingFELPhotonDiffractorParameters(uniform_rotation=True,                  # Uniform sampling of rotation space.
             calculate_Compton = False,               # Do not calculate Compton scattering
             slice_interval = 100,                    # Take interval of 100 pmi snapshots
             number_of_slices = 2,                    # Take two snapshots from this interval
             pmi_start_ID = 1,                        # Start with this pmi file ID.
             pmi_stop_ID  = 1,                        # Stop after this pmi file ID.
             number_of_diffraction_patterns = 100,   # Calculate 100 patterns from each trajectory.
             beam_parameter_file = beam,              # Beam file.
             beam_geometry_file = geom,               # Geometry file (detector).
             cpus_per_task =  1,                      # Use one CPU per MPI process. Number of processes is guessed from machine parameters.
             )

# Construct the object.
diffractor = SingFELPhotonDiffractor(parameters=parameters, input_path=pmi_path, output_path='diffr')

# Call backengine.
status = diffractor.backengine()

if status != 0:
    print "Diffraction calculation failed, check output."
    sys.exit()

print "Diffraction calculation succeeded."
