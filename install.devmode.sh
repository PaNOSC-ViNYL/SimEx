#! /bin/bash

# Sample installation script. Adjustments might be neccessary.

INSTALL_PREFIX=..
THIRD_PARTY_ROOT=/data/netapp/s2e

# Check for existing build directory, remove if found
if [ -d build ]
then
    echo "Found build/ directory, will remove it now."
    rm -rvf build
fi

# Patch CMakeLists to set required python to what's available on maxwell, i.e. python3.4
git apply patch_for_maxwell

# Create new build dir and cd into it.
mkdir -v build
cd build
echo "Changed dir to $PWD."

# Uncomment the next line if you want to use Intel Fotran compiler
# (otherwise gfortran will be used). Make sure $MKLROOT is set. This can be achieved by
# $> source `which compilervars.sh` <arch>
# where <arch> is either intel64 or ia32
export FC=ifort

# Some needed environment variables.
export BOOST_ROOT=${THIRD_PARTY_ROOT}/external_libs
export Boost_NO_SYSTEM_PATHS=ON
export XERCESC_ROOT=${THIRD_PARTY_ROOT}/external_libs
export GEANT4_ROOT=${THIRD_PARTY_ROOT}/external_libs
export Geant4_DIR=${THIRD_PARTY_ROOT}/external_libs/lib64/Geant4-10.4.0
export XCSIT_ROOT=${THIRD_PARTY_ROOT}/external_libs

cmake -DSRW_OPTIMIZED=ON \
      -DDEVELOPER_INSTALL=ON \
      -DCMAKE_INSTALL_PREFIX=$INSTALL_PREFIX \
      -DSingFELPhotonDiffractor=ON \
      -DCrystFELPhotonDiffractor=ON \
      -DGAPDPhotonDiffractor=ON \
      -Ds2e=ON \
      -DS2EReconstruction_EMC=ON \
      -DS2EReconstruction_DM=ON \
      -Dwpg=ON \
      -DGenesisPhotonSource=ON \
      -DXCSITPhotonDetector=ON \
      -DFEFFPhotonInteractor=ON \
      -DXERCESC_ROOT=$XERCESC_ROOT \
      -DGEANT4_ROOT=$GEANT4_ROOT \
      -DXCSIT_ROOT=$XCSIT_ROOT \
      -DBOOST_ROOT=$BOOST_ROOT \
      ..

# Build the project.
make -j32

# Install the project.
make install

cd ..

git checkout -- CMakeLists.txt
