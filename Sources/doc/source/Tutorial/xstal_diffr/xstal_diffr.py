#! /usr/bin/env python2.7

from SimEx import CrystFELPhotonDiffractor, CrystFELPhotonDiffractorParameters
from SimEx import DiffractionAnalysis
from SimEx import PhotonBeamParameters

beam = PhotonBeamParameters(
        photon_energy = 4972.0,
        beam_diameter_fwhm=1.3e-7,
        pulse_energy=0.45e-3,
        photon_energy_relative_bandwidth=0.003,
        divergence=0.0,
        photon_energy_spectrum_type='tophat',
        )

parameters = CrystFELPhotonDiffractorParameters(sample='5udc.pdb',
        uniform_rotation=True,
        number_of_diffraction_patterns=1,
        powder=None,
        intensities_file=None,
        crystal_size_range=[1e-7,1e-7],
        poissonize=False,
        number_of_background_photons=None,
        suppress_fringes=None,
        beam_parameters=beam,
        geometry='simple.geom',
        )

diffractor = CrystFELPhotonDiffractor(parameters=parameters, input_path=None, output_path="xstal_diffr")

error = False
if not error:
    error = diffractor.backengine()
if not error:
    error = diffractor.saveH5()

if not error:
    print "Completed diffraction calculation, saved patterns to %s." % (diffractor.output_path)
