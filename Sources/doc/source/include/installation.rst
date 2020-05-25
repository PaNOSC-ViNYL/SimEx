Installation
------------
.. contents::

From sources
____________

To build and install from the source code directly.

Download
````````````````

First obtain the source code by either cloning the repository::

    $> git clone https://github.com/PaNOSC-ViNYL/SimEx

or by downloading and extracting the zip_ archive.

.. _zip: https://github.com/PaNOSC-ViNYL/SimEx/archive/master.zip

After downloading (and extracting), switch into the top level directory::

    $> cd SimEx

Software dependencies
`````````````````````
Python dependencies
..................
The python dependencies are listed in `$SIMEX_ROOT/requirements.txt`, reproduced here:

.. include ../../../../requirements.txt

Note that these these requirements contain all dependencies of all modules. A customized build with only selected Modules may well get away with fewer dependencies installed. The cmake build system will check all dependencies for each individual Module. Cmake will abort the configuration if missing dependencies are detected for a given Module.

The python dependencies can be installed via `pip`::

    $> python -m pip install -r requirements.txt

Except for `xraydb`, all python requirements can also be installed through `conda`.


Non-python dependencies
.......................
The following libraries/executables should be installed on your system:

* cmake 3.12+
* libgsl0-dev
* libfftw3-dev or INTEL-MKL 
* wget
* hdf5 (version >= 1.10.4) + header files
* python3.5+
* libbz2-dev
* unzip
* C/C++ and Fortran compilers, e.g. gcc

Module specific dependencies
............................
* boost (version > 1.54) + header files (only needed for Detector simulations with the XCSITPhotonDetector Module)
* libfftw3-dev or INTEL-MKL (needed to run WPG/SRW wavefront propagation)


NOTE 1 (Intel(R) MKL(R)): If you want to link against Intel(R) MKL(R), make sure that the Intel(R) MKL(R) environment variables are set. This is typically done by running one of the
scripts in $INTEL_HOME/bin/, where $INTEL_HOME is the root directory of the Intel(R) MKL(R) installation,
e.g. /opt/intel/2015.

NOTE 2 (BOOST): Sometimes boost_mpi is not built although all libraries (default) where requested as per project.conf in
the boost build directory. Append a "using mpi ;" to that file (without the quotes) to enforce building boost_mpi.

NOTE 3 (BOOST): It has been observed that newer versions of boost (>1.61), if linked against mpich, require libmpich.so.12,
which might not be available on all systems, especially not completely updated clusters. Use boost.1.60 or lower if this problem occurs.
You can find out by running ldd on libboost_mpi.so.

Installing only the python SimEx library
````````````````````````````````````````
If, for whatever obscure reason, you only need the SimEx python library (the Calculators and Parameters), simply run::

   $> cd Sources/python
   $> python -m pip install [-e] .

The `-e` option is recommended for developers: Changes in `Sources` would be reflected in the imported python module.

Building the backengine modules (aka Modules) and the SimEx python library
``````````````````````````````````````````````````````````````````````````

Install the backengine modules along with the SimEx python API
``````````````````````````````````````````````````````````````

The SimEx python API and backengine modules (aka Modules) can be installed
by following the steps below.

The install process has three stages: configuration, building, and installing.

Configuration via cmake
.......................
This step requires a dedicated build directory. Create one, and change into it::

    $> mkdir build
    $> cd build

Configuration is done by issuing the command `cmake ..`. `cmake` accepts numerous command line arguments. To list them all along with their defaults, run::

    $> cmake -LAH 

To set a flag/argument to a non-default value, it is appended to the `cmake` command. E.g. to set the installation prefix (path under which all SimEx libraries and executables will be installed)::


    $> cmake .. -DCMAKE_INSTALL_PREFIX=/path/to/some/directory

Note the capital "D" before the actual flag.


Module selection
""""""""""""""""
As of version 0.5, no Module is installed by default. To switch to the old behaviour and install all Modules, set the flag `USE_MODULES_DEFAULT`::

   $> cmake .. -DUSE_MODULES_DEFAULT=ON + further flags and arguments]

To keep the new behaviour AND select individual modules, append each selected module with a `-DUSE_` prefix. E.g. to activate the propagation Module based on WPG::

   $> cmake .. -DUSE_wpg=ON

To activate the SingFELPhotonDiffractor::

   $> cmake .. -DUSE_SingFELPhotonDiffractor=ON

As a third alternative, this syntax also allows to deselect individual Modules and install all others::

   $> cmake .. -DUSE_MODULES_DEFAULT=ON -DUSE_wpg=OFF

In this example, all but the wpg module will be installed.


Build the documentation
"""""""""""""""""""""""
   ::
    $> cmake -DBUILD_DOC=ON ..

Developer install
"""""""""""""""""
This is recommended for SimEx developers. In this way, you will be able to run the unittests without having to recompile::

    $> cmake -DCMAKE_INSTALL_PREFIX=.. 


Create deb packages::
"""""""""""""""""""
::

    $> cmake -DPACKAGE_MAKE=ON -DCMAKE_INSTALL_PREFIX=/usr ..
    $> make package

Probably you will have to call cmake two times because for some unknown reason CMake creates ``.tgz`` archives in the first time.

The package can then be installed system-wide along with all necessary dependencies::

    $> dpkg -i <package_name>
    $> apt-get install -f

  on another computer with Debian based OS. Simex will be
  installed in `/usr/...` , Tests are installed in
  `/usr/share/simex/...` and should be system-wide available.
  Calling `dpkg` with `--instdir` option allows to change
  installation dir. In this case `simex_vars.sh` should be
  modified manually to set paths correctly.


Building the library
.................


After successful completion of cmake, just type::

    $> make

On machines with more than 1 CPU, compilation can be sped up with::

    $> make -jN

where N is the number of CPUs to consume.

An example build & installation script is provided (install.sh). It might need manual adjustment as indicated.



Installation
............

Finally, after make returns, install the compiled software into the installation directory::

    $> make install

Make sure that the user has write access to the installation directory, or use::

    $> sudo make install

Troubleshooting
'''''''''''''''

cmake fails to resolve dependency but the library is installed
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
On some systems cmake fails to find the paths for some of the
third party libraries like boost. If this should be the case,
consult the corresponding FindXXX.cmake scripts in the CMake directory and
in your system's configuration for how to help cmake find these libraries.
An example for how to specify paths for boost is given in
the install.sh script that comes with the sources.


gomp/iomp not found / MKL not found
"""""""""""""""""""""""""""""""""""
If compiling with Intel compilers and/or using MKL, run this command before cmake::

    $> source `which compilervars.sh` intel64



