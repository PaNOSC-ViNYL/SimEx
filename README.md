SIMEX PLATFORM
==================

Software platform for simulation of advanced photon experiments.

[![Build Status master](https://img.shields.io/travis/eucall-software/simex_platform/master.svg?label=master)](https://travis-ci.org/eucall-software/simex_platform/branches)
[![Build Status develop](https://img.shields.io/travis/eucall-software/simex_platform/develop.svg?label=develop)](https://travis-ci.org/eucall-software/simex_platform/branches)


Contents
==============

1.) Purpose of the software

2.) Installation

3.) Getting started


## 1.) Purpose of simex_platform

The present code is meant to facilitate setup, execution, and analysis of
simulations of experiments at advanced laser light sources.
As an example, consider a molecule radiated by highly brilliant,
ultrashort x-ray pulses such as delivered by an X-Ray Free Electron Laser (X-FEL).
The simulation platform allows to combine tools and codes for the
simulation of each step of the experiment: Generation of radiation in the
photon source, propagation through optics and waveguides to the interaction
point, photon-matter interaction, scattering of the radiation into the far
field and detection of the latter. The platform provides slots and
interfaces for the various simulation steps.


## 2.) Installation
### 2.1.) Preliminaries

First obtain the source code either via cloning the repository or via
downloading and extracting the zip file. Change into the top level directory
simex_platform/. The python/ directory contains code for the simulation
framework itself, but it does not contain any actual simulation tools.
A selection of simulation tools tailored for simulation of coherent
diffractive single particel imaging can be built using the Makefile in build/.

### 2.2) Software dependencies

The build process will fetch and install a number of third party libraries,
such as hdf5, mpich, and boost. Resolving all dependencies for all libraries
certainly goes beyond the scope of this project at the present time and has to
be taken care of by the user. The following lists the minimum required
software needed to build the external simulation tools:
 - wget
 - boost (version > 1.54) + header files
 - armadillo (version >= 4.600) + header files
 - hdf (version >= 1.8.4) + header files
 - python2.7
 - python-numpy
 - python-scipy
 - python-h5py
 - python-cython
 - python-setuptools
 - python-matplotlib
 - build-essential
 - bz2 libraries (libbz2-dev)
 - GSL (libgsl0-dev)
 - FFTW3 (libfftw3-dev) or MKL
 - lapack
 - cmake
 - C/C++ and Fortran compilers, e.g. gcc
 - unzip

A note on MKL: Make sure that the Intel(R) MKL(R) environment variables are set. This is typically done by running one of the scripts in $INTEL_HOME/bin/, where $INTEL_HOME is the root directory of the Intel(R) MKL(R) installation, e.g. /opt/intel/2015 for a recent version of MKL(R).

## 2.3)

The build process takes place in three steps:

### 2.3.1 Configuration via cmake:

This step requires a dedicated build directory. Create one, e.g. mkdir build, and switch to it (cd build).
In principle, configuration is done by issuing the command
```bash
$> cmake ..
```
An installation prefix can be given via
```bash
$> cmake -DCMAKE_INSTALL_PREFIX=/path/to/some/directory ..
```

On some systems, however, cmake fails to find the paths for some of the
third party libraries like boost, armadillo etc. If this should be the case,
consult the corresponding FindXXX.cmake scripts in the CMake directory and
in your system's configuration for how to help cmake find these libraries.
An example for how to specify paths for boost and armadillo are given in
the install.sh script that comes with the sources.

### 2.3.2 Building the library

After successful completion of cmake, just type
```bash
$> make
```
on the command line. This will download, extract, and build the platform
and a minimal set of simulation modules.
An example build & installation script is provided (install.sh). It might need manual adjustment as indicated.
**Build external tools**
Change into the `build/` directory and type
```bash
$> make
```

### 2.3.3 Installation
Finally, after make returns, typing
```bash
$> make install
```
will install all executables and libraries under the prefix directory given through the DCMAKE_INSTALL_PREFIX directive in step 2.3.1. Make sure that the user has write access to that directory or use
```bash
$> sudo make install
```

**NOTE TO DEVELOPERS:**
a) For simex_platform developers, it is recommended to install the platform
directly into the source tree, e.g. give the top level directory to the DCMAKE_INSTALL_PREFIX directive, e.g.
```bash
$> cmake -DCMAKE_INSTALL_PREFIX=.. ..
```
supposing the build directory is located in the top level source directory.

In this way, you will be able to run the unittests without having to recompile.

b) There is an option to create debian package which can then be installed along with all necessary dependencies via

```bash
$> dpkg -i <package_name>
$> apt-get install -f 
```

on another computer with Debian based OS. In this case Simex will be installed in `/usr/...` , Tests are installed in `/usr/share/simex/...` and should be system-wide available.
Calling `dpkg` with `--instdir` option allows to change installation dir. In this case `simex_vars.sh` should be modified manually to set paths correctly.

To create the package call

```bash
$> cmake -DPACKAGE_MAKE=ON -DCMAKE_INSTALL_PREFIX=/usr <PATH TO SOURCE>
$> make package
```

(probably you will have to call cmake two times because for some unknown reason CMake creates `.tgz` archives in the first time).


## 3.)

Getting started

### 3.1) Testing the installation.

The project comes with a unittest suite that should be run immediately
after installation. You can also switch this option off by setting `-DINSTALL_TESTS=OFF` when running CMake. Besides many small tests, the suite also contains a
minimal workflow using the external simulation tools. `cd` to `<install_prefix>/Tests/python/unittest` and type
```bash
$> python Test.py -v 2>&1 | tee Test.log
```
This will run the entire test suite and pipe the output to the file `Test.log`.
A final test report is appended.

### 3.2) Minimal workflow.

The test module
  `<install_prefix>/Tests/python/unittest/SimExTest/PhotonExperimentSimulation/PhotonExperimentSimulation.py`
contains the test `testMininalWorkflow`. It illustrates how to use the platform to execute photon experiment simulations.

