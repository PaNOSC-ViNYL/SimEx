Installation
------------

From sources
____________

Download
````````

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


Binary packages
_____________________
Binary (.deb) packages are provided for Ubuntu (currently supporting version 16.04).
https://github.com/eucall-software/simex_platform/releases/download/v0.2.0/simex-0.2.0-Ubuntu16.04.deb

Simply download and install, e.g. using the command (might require root privileges)::

    $> dpkg --install simex-0.2.0-Ubuntu16.04.deb


Docker
____________

We also provide docker images. Docker is a rather new technology, think of it as a "lightweight virtualbox", i.e. a docker container ships all
software dependencies including hardware abstraction and OS components
along with the executable. To run a docker container, you first need the docker
environment. Get it for your OS from https://www.docker.com/products/overview.
Then, download the simex docker container using the following shell command::

    docker pull yakser/simex

or::

    docker pull yakser/simex:devel

The latter contains all test files.


Getting started
```````````````

The docker command accepts certain parameters on the command line. Of special interest here are::

    -it  -> to have interactive session and pseudo-TTY).
    -v <full_path_to_source_dir/dest_dir> -> to mount data from host (should contain your script and necessary data). Several mounts are possible as well (repeat -v ...). All data that is needed should be mounted, otherwise it will be unavailable inside a Docker container.
    -w -> working directory inside the container. Set it if relative paths are used in your python script.
    -u <UID>:<GID> - user id and group id (not names, because they are not set in the Docker container). Container will run as root if this is omitted and mpirun will complain.



Examples
'''''''''

1. Run unit tests. We do not need to mount any additional folders::

   $> docker run -it -u `id -u`:`id -g` -w /opt/simex_platform/Tests/python/unittest yakser/simex:devel Test.py

Some tests will fail in the moment due to known bugs in the diffraction calculator "singfel".

2. Run some user script script.py in /home/user/somedata_and_script directory::

    $> docker run -it -v /home/user/somedata_and_script:/data -u `id -u`:`id -g` -w /data yakser/simex script.py


Updating docker container
`````````````````````````

To update an existing container, simply do::

    $> docker pull simex

or::

    $> docker pull simex:devel



