Introduction
------------

simex_platform provides a software platform for simulation of experiments at advanced laser and x-ray light sources.
All aspects of a typical experiment,
the photon source, light transport through optics elements in the beamline,
interaction with a target or sample,
scattering from the latter,
photon detection, and data analysis can be modelled.
A simulation can contain, one, several, or all of these parts.

As an example, consider a coherent imaging experiment using x-ray free electron laser (XFEL)
radiation:
A molecule, cluster, or nanocrystal is irradiated by highly brilliant,
ultrashort x-ray pulses, these scatter from the sample get detected in an x-ray detector.

The x-ray photons will ionize and destroy the sample after a very short time, typically of the order
of a few tens to a few hundreds of femtoseconds (1 fs = 1x10^-15 s). By using x-ray pulses that
are even shorter, of the order of a few femtoseconds, this radiation damage can, at least partly,
be avoided, i.e. the sample is probed before destruction. The scattered photons are registered in
a area pixel detector and the scattering (diffraction) pattern can be analyzed to infer structural informaton about the sample, i.e. the 3D electron density and the position of atoms within the molecule.

simex_platforms provides scriptable python user interfaces to a number of advanced simulation codes for the various stages of the experiment: Photon Source, Photon Propagation, Photon-Matter Interaction, Photon Diffraction and Scattering, Photon Detection, and Photon Data Analysis. Additionaly, simex_platform defines data interfaces such that the involved simulation codes can "talk" to each other. E.g. output from a photon source calculation can be fed into the photon propagation simulation.

The simex_platform library is open-source, but some of the interfaced simulation codes are not. In such cases, the user has to acquire the simulation code and install on his system.


