SimEx
==================

Software platform for **Sim**ulation of advanced photon **Ex**periments.

[![Build Status](https://travis-ci.org/PaNOSC-ViNYL/SimEx.svg?branch=master)](https://travis-ci.org/PaNOSC-ViNYL/SimEx)
[![Build Status](https://travis-ci.org/PaNOSC-ViNYL/SimEx.svg?branch=develop)](https://travis-ci.org/PaNOSC-ViNYL/SimEx)


## Purpose of SimEx

SimEx is a python library to facilitate setup, execution, and analysis of
simulations of experiments at advanced laser light sources.
As an example, consider a molecule radiated by highly brilliant,
ultrashort x-ray pulses such as delivered by an X-Ray Free Electron Laser (X-FEL).
The simulation platform allows to combine tools and codes for the
simulation of each step of the experiment: Generation of radiation in the
photon source, propagation through optics and waveguides to the interaction
point, photon-matter interaction, scattering of the radiation into the far
field and detection of the latter. The platform provides slots and
interfaces for the various simulation steps.

For more details (User Manual, installation instructions, examples, etc.),
please visit the project's homepage at https://panosc-vinyl.github.io/SimEx/

## Development

The size of this Github repository of SimEx is huge due to the historical TestFiles.

This command can clone only the newest develop branch to reduce the dowloading size:
`git clone --depth 1 -b develop git@github.com:PaNOSC-ViNYL/SimEx.git`

Now the TestFiles are hosted at [Zenodo](https://zenodo.org/record/3750541#.X2R9DZMzZE5).
The files can be downloaded with [this script](get_testdata.sh).

## Acknowledgements
This project has received funding from the European Union’s Horizon 2020 research
and innovation programme under grant agreement No 654220 and No 823852.
