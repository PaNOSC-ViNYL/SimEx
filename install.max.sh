#! /bin/bash

# Sample installation script. Adjustments might be neccessary.

INSTALL_PREFIX=/data/netapp/s2e/simex
#INSTALL_PREFIX=$PWD

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
# where $INTEL_HOME is the root of the intel compiler suite (typically /opt/intel), and <arch> is either intel64 or ia32
export FC=ifort

# Some needed environment variables.
export BOOST_ROOT=${THIRD_PARTY_ROOT}
export Boost_NO_SYSTEM_PATHS=ON
export ARMA_DIR=${THIRD_PARTY_ROOT}
export XERCESC_ROOT=/home/burcherj/.local
export GEANT4_ROOT=/home/burcherj/.local
export XCSIT_ROOT=/home/burcherj/.local


cmake -DSRW_OPTIMIZED=ON \
      -DDEVELOPER_INSTALL=OFF \
      -DCMAKE_INSTALL_PREFIX=$INSTALL_PREFIX \
      -DSingFElPhotonDiffractor=ON \
      -Ds2e=ON \
      -DS2EReconstruction_EMC=ON\
      -DS2EReconstruction_DM=ON\
      -Dwpg=ON\
      -Dprop=ON\
      -Dgenesis=ON\
      -Docelot=ON\
      -DXCSITPhotonDetector=ON\
      -DXERCESC_ROOT=$XERCESC_ROOT \
      -DGEANT4_ROOT=$GEANT4_ROOT \
      -DXCSIT_ROOT=$XCSIT_ROOT \
      -DBOOST_ROOT=$BOOST_ROOT \
      ..

# Build the project.
make -j32

# Install the project.
make install
