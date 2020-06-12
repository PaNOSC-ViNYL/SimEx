Installation
------------

From sources
____________

Download
````````

First obtain the source code by either cloning the repository::

    $> git clone https://github.com/PaNOSC-ViNYL/SimEx

or by downloading and extracting the zip_ archive.

.. _zip: https://github.com/PaNOSC-ViNYL/SimEx/archive/master.zip

After downloading (and extracting), switch into the top level directory::

    $> cd SimEx

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
* hdf5 (version >= 1.8.4) + header files
* python2.7
* python-numpy
* python-scipy
* python-h5py
* python-cython
* python-setuptools
* python-matplotlib
* python-dill
* build-essential
* bz2 libraries (libbz2-dev)
* GSL (libgsl0-dev)
* FFTW3 (libfftw3-dev) or MKL
* lapack
* cmake
* C/C++ and Fortran compilers, e.g. gcc
* unzip

See also requirements.txt in the simex_platform root directory.

For conda, we provide an environment.yml file to create a simex environment::


    $> conda env create --file environment.yml

See below for how to install the dependencies and backengines into the same environment.

NOTE 1 (Intel(R) MKL(R)): If you want to link against Intel(R) MKL(R), make sure that the Intel(R) MKL(R) environment variables are set. This is typically done by running one of the
scripts in $INTEL_HOME/bin/, where $INTEL_HOME is the root directory of the Intel(R) MKL(R) installation,
e.g. /opt/intel/2015.

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


By setting the installation prefix to $CONDA_PREFIX, one can install the backengines and the simex library into the same environment.

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

vi. Disable/activate modules::

    $> #Disable all modules
    $> cmake -DUSE_MODULES_DEFAULT=OFF [...]
    $> #Enable all modules (this is the default)
    $> cmake -DUSE_MODULES_DEFAULT=ON [...]
    $> #Disable all moules except the one named wpg
    $> cmak -DUSE_MODULES_DEFAULT=OFF -DUSE_wpg=ON [...]

vii. Install the SimEx python module::

    $> cd Sources/python
    $> python -m pip [--user] install .

The --user flag is needed if installing in a system wide python installation.

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

