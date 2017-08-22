#! /bin/bash

# Sample installation script. Adjustments might be neccessary.



#INSTALL_PREFIX=/data/netapp/s2e/simex
INSTALL_PREFIX=$PWD
THIRD_PARTY_ROOT=/data/netapp/s2e/simex

# Check for existing build directory, remove if foun.d
if [ -d build ]
then
    echo "Found build/ directory, will remove it now."
    rm -rvf build
fi

# Create new build dir and cd into it.
mkdir -v build
cd build
echo "Changed dir to $PWD."

# Uncomment the next line if you want to use Intel Fotran compiler
# (otherwise gfortran will be used). Make sure $MKLROOT is set. This can be achieved by sourcing
# where $INTEL_HOME is the root of the intel compiler suite (typically /opt/intel), and <arch> is either intel64 or ia32, following need to be load externally
module load intel/2015
module load mpi/mpich-x86_64
. `which compilervars.sh` intel64
export FC=ifort

# Some needed environment variables.
export BOOST_ROOT=${THIRD_PARTY_ROOT}
export Boost_NO_SYSTEM_PATHS=ON
export ARMA_DIR=${THIRD_PARTY_ROOT}


#TODO:
# Please edit the pathes below according to your file system
# If your have another version of xerces_c than 3.1 please edit also the single
# entry in ./src/CMakeLists.txt which starts with ${XERCES} and ends with .so
cmake -DSRW_OPTIMIZED=ON \
      -DDEVELOPER_INSTALL=ON \
      -DCMAKE_INSTALL_PREFIX=$INSTALL_PREFIX \
      -DSingFElPhotonDiffractor=ON \
      -Ds2e=ON \
      -DS2EReconstruction_EMC=ON\
      -DS2EReconstruction_DM=ON\
      -Dwpg=ON\
      -Dprop=ON\
      -Dgenesis=ON\
      -Docelot=ON\
      -DXCSIT_FOLDER=/gpfs/exfel/data/user/burcherj/Development/karaboFramework/karabo/devices/xcsit \
      -DGEANT4_SOURCE=/gpfs/exfel/data/user/burcherj/Development/geant4.10.03.p01/source \
      -DGEANT4_BUILD=/gpfs/exfel/data/user/burcherj/Development/geant4.10.03.p01-build \
      -DGEANT4_SO=/gpfs/exfel/data/user/burcherj/Development/geant4.10.03.p01-install/lib64 \
      -DXERCES=/gpfs/exfel/data/user/burcherj/Development/xerces-c-3.1.4/src \
      ..

# Build the project.
make -j32

# Install the project.
make install
