SimEx
==================

Software platform for **Sim**ulation of advanced photon **Ex**periments.

[![Build Status master](https://travis-ci.org/PaNOSC-ViNYL/SimEx.svg?branch=master)](https://travis-ci.org/github/panosc-vinyl/simex/branches)
[![Build Status develop](https://travis-ci.org/PaNOSC-ViNYL/SimEx.svg?branch=develop)](https://travis-ci.org/github/panosc-vinyl/simex/branches)


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

# Install
Get source code:
```
git clone --depth 1 -b master https://github.com/PaNOSC-ViNYL/SimEx.git
```

## CENTOS 8
```
yum install -y hdf5 hdf5-devel fftw-devel flex bison
```

### Conda (preferred)
```
wget -c -O /tmp/miniconda.sh https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
sh /tmp/miniconda.sh
```

 * Select a directory XX where to install miniconda, consider 5GB of free disk space.
 * Add the XX/miniconda/bin/ directory to your path

```
./install.sh conda-env
conda init $SHELL
```
restart your shell
```
conda activate simex
./install.sh conda
```
<!--- ## CENTOS non conda --->

## Tutorial notebooks
https://github.com/PaNOSC-ViNYL/SimEx-notebooks

## Development
The size of this Github repository of SimEx is huge due to the historical TestFiles.

This command can clone only the newest develop branch to reduce the dowloading size:
```
git clone --depth 1 -b develop https://github.com/PaNOSC-ViNYL/SimEx.git
```
Now the TestFiles are hosted at [Zenodo](https://zenodo.org/record/3750541#.X2R9DZMzZE5).
The files can be downloaded with [this script](get_testdata.sh).


## Acknowledgements
This project has received funding from the European Union’s Horizon 2020 research
and innovation programme under grant agreement No 654220 and No 823852.
