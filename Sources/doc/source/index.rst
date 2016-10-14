.. simex_platform documentation master file, created by
   sphinx-quickstart on Wed Apr  6 14:14:07 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Users Manual
===========================

Indices and tables
------------------

* :ref:`genindex`
* :ref:`search`


Acknowledgements
----------------

This project has received funding from the European Union’s Horizon 2020 research and innovation programme under grant agreement No 654220


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

Installation
------------

Preliminaries
`````````````

First obtain the source code by either cloning the repository::

    $> git clone https://github.com/eucall-software/simex_platform

or by downloading and extracting the zip_ archive.

.. _zip: https://github.com/eucall-software/simex_platform/archive/master.zip

After downloading (and extracting), switch into the top level directory::

    $> cd simex_platform

Software dependencies
`````````````````````
The build process will fetch and install a number of third party libraries,
such as hdf5, mpich, and boost. Resolving all dependencies for all libraries
certainly goes beyond the scope of this project at the present time and has to
be taken care of by the user. The following lists the minimum required
software needed to build the external simulation tools:

* wget
* boost (version > 1.54) + header files
* armadillo (version >= 4.600) + header files
* hdf (version >= 1.8.4) + header files
* python2.7
* python-numpy
* python-scipy
* python-h5py
* python-cython
* python-setuptools
* python-matplotlib
* build-essential
* bz2 libraries (libbz2-dev)
* GSL (libgsl0-dev)
* FFTW3 (libfftw3-dev) or MKL
* lapack
* cmake
* C/C++ and Fortran compilers, e.g. gcc
* unzip

NOTE 1 (Intel(R) MKL(R)): If you want to link against Intel(R) MKL(R), make sure that the Intel(R) MKL(R) environment variables are set. This is typically done by running one of the
scripts in $INTEL_HOME/bin/, where $INTEL_HOME is the root directory of the Intel(R) MKL(R) installation,
e.g. /opt/intel/2015 for a recent version of MKL(R).

NOTE 2 (BOOST): Sometimes boost_mpi is not built although all libraries (default) where requested as per project.conf in
the boost build directory. Append a "using mpi ;" to that file (without the quotes) to enforce building boost_mpi.

NOTE 3 (BOOST): It has been observed that newer versions of boost (>1.61), if linked against mpich, require libmpich.so.12,
which might not be available on all systems, especially not completely updated clusters. Use boost.1.60 or lower if this problem occurs.
You can find out by running ldd on libboost_mpi.so.

Building
````````

The build process has three stages: configuration, building, and installing.

Configuration via cmake
'''''''''''''''''''''''
This step requires a dedicated build directory. Create one, and change into it::

    $> mkdir build
    $> cd build

Configuration is done by issuing::

    $> cmake ..

Usefull cmake flags are:

i. Installation prefix::

    $> cmake -DCMAKE_INSTALL_PREFIX=/path/to/some/directory ..

ii. Wave propagation with OpenMP::

    $> cmake -DSRW_OPTIMIZED=ON ..

ii. Build the documentation::

    $> cmake -DBUILD_DOC=ON ..

iv. Developer install::

    $> cmake -DCMAKE_INSTALL_PREFIX=.. ..

    This is recommended for simex_platform developers. In this way, you will be able to run the unittests without having to recompile.

v. Create deb packages::

    $> cmake -DPACKAGE_MAKE=ON -DCMAKE_INSTALL_PREFIX=/usr ..
    $> make package

  Probably you will have to call cmake two times because for some unknown reason CMake creates `.tgz` archives in the first time.

  The package can then be installed system-wide along with all necessary dependencies::

    $> dpkg -i <package_name>
    $> apt-get install -f

  on another computer with Debian based OS. Simex will be
  installed in `/usr/...` , Tests are installed in
  `/usr/share/simex/...` and should be system-wide available.
  Calling `dpkg` with `--instdir` option allows to change
  installation dir. In this case `simex_vars.sh` should be
  modified manually to set paths correctly.


Troubleshooting
"""""""""""""""
On some systems cmake fails to find the paths for some of the
third party libraries like boost, armadillo etc. If this should be the case,
consult the corresponding FindXXX.cmake scripts in the CMake directory and
in your system's configuration for how to help cmake find these libraries.
An example for how to specify paths for boost and armadillo are given in
the install.sh script that comes with the sources.

Building the library
''''''''''''''''''''

After successful completion of cmake, just type::

    $> make

On machines with more than 1 CPU, compilation can be sped up with::

    $> make -jN

where N is the number of CPUs to consume.

An example build & installation script is provided (install.sh). It might need manual adjustment as indicated.


Installation
''''''''''''

Finally, after make returns, install the compiled software into the installation directory::

    $> make install

Make sure that the user has write access to the installation directory, or use::

    $> sudo make install

Environment settings
--------------------
simex_platform is a python library, hence python needs to be aware of its location. To this end,
run the command::

    $> source <install_prefix>/bin/simex_vars.sh

after installation.

Testing
-------
Testing the installation.

By default, the installation also creates the unittest suite.
You can switch this option off by appending the flag `-DINSTALL_TESTS=OFF` to the cmake command.

It is advised to run the test suite to check your installation::

    $> cd Tests/python/unittest
    $> python Test.py -v 2>&1 | tee Test.log

This will run the entire test suite and pipe the output to the file `Test.log`.
A final test report is appended.

NOTE 4 (Large Test Files): If you pulled the sources via git and encounter test failures where
the test log mentions something like "hdf file could not be read", make sure you issued a "git lsf pull" command at least once.
This is not a standard git command, you have to install git-lsf (e.g. via https://git-lfs.github.com/).

NOTE 5 (segfault in WavePropagatorTest.py): If you receive a segfault when
running the test module WavePropagatorTest.py, try the following command to fix:
$> ulimit -c unlimited

If this does not fix the problem, please post a bug report on github.


Usage
-----
The intended usage scheme of simex_platform is that of a python module in either an interactive (i)python session or a python script. Hence, the first thing to do is to import the module.

>>> import SimEX

A good starting point for finding examples on how to use simex_platform modules are the tests under `
`Tests/python/unittest/SimExTest/`. Each Calculator is tested, and the test-suite `PhotonExperimentSimulation/PhotonExperimentSimulationTest.py` contains some simex_platform workflow examples for complete start-to-end simulations.

Contribute
----------
- Source Code github.com/eucall-software/simex_platform
- Issue Tracker: github.com/eucall-software/simex_platform/issues

Support
-------
If you are having issues, please let us know at carstendotgroteatxfeldoteu .

License
-------
The project is licensed under the GPL open source license version 3.


Reference Manual
----------------

.. autoclass:: SimEx.Calculators.AbstractBaseCalculator.AbstractBaseCalculator

.. autoclass:: SimEx.Calculators.AbstractPhotonAnalyzer.AbstractPhotonAnalyzer
.. autofunction:: SimEx.Calculators.AbstractPhotonAnalyzer.checkAndSetPhotonAnalyzer

.. autoclass:: SimEx.Calculators.AbstractPhotonDetector.AbstractPhotonDetector
.. autofunction:: SimEx.Calculators.AbstractPhotonDetector.checkAndSetPhotonDetector

.. autoclass:: SimEx.Calculators.AbstractPhotonDiffractor.AbstractPhotonDiffractor
.. autofunction:: SimEx.Calculators.AbstractPhotonDiffractor.checkAndSetPhotonDiffractor

.. autoclass:: SimEx.Calculators.AbstractPhotonInteractor.AbstractPhotonInteractor
.. autofunction:: SimEx.Calculators.AbstractPhotonInteractor.checkAndSetPhotonInteractor

.. autoclass:: SimEx.Calculators.AbstractPhotonPropagator.AbstractPhotonPropagator
.. autofunction:: SimEx.Calculators.AbstractPhotonPropagator.checkAndSetPhotonPropagator

.. autoclass:: SimEx.Calculators.AbstractPhotonSource.AbstractPhotonSource
.. autofunction:: SimEx.Calculators.AbstractPhotonSource.checkAndSetPhotonSource

.. autoclass:: SimEx.Calculators.DMPhasing.DMPhasing
.. autoclass:: SimEx.Parameters.DMPhasingParameters.DMPhasingParameters

.. autoclass:: SimEx.Calculators.EMCOrientation.EMCOrientation
.. autoclass:: SimEx.Parameters.EMCOrientationParameters.EMCOrientationParameters

.. autoclass:: SimEx.Calculators.IdealPhotonDetector.IdealPhotonDetector


.. autoclass:: SimEx.Calculators.FEFFPhotonMatterInteractor.FEFFPhotonMatterInteractor
.. autoclass:: SimEx.Calculators.FEFFPhotonMatterInteractor.FEFFPhotonMatterInteractorParameters

.. autoclass:: SimEx.Calculators.PlasmaXRTSCalculator.PlasmaXRTSCalculator
.. autoclass:: SimEx.Parameters.PlasmaXRTSCalculatorParameters.PlasmaXRTSCalculatorParameters

.. autoclass:: SimEx.Calculators.S2EReconstruction.S2EReconstruction

.. autoclass:: SimEx.Calculators.SingFELPhotonDiffractor.SingFELPhotonDiffractor
.. autoclass:: SimEx.Parameters.SingFELPhotonDiffractorParameters.SingFELPhotonDiffractorParameters

.. autoclass:: SimEx.Calculators.WavePropagator.WavePropagator
.. autoclass:: SimEx.Parameters.WavePropagatorParameters.WavePropagatorParameters

.. autoclass:: SimEx.Calculators.XFELPhotonSource.XFELPhotonSource

.. autoclass:: SimEx.Calculators.XMDYNDemoPhotonMatterInteractor.XMDYNDemoPhotonMatterInteractor

.. .. autoclass:: SimEx.Parameters.AbstractCalculatorParameters.AbstractCalculatorParameters

