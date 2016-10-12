#! /bin/bash

# Sample installation script. Adjust lines 5,15,16,17 according to system
# and personal taste.

ROOT_DIR=$PWD

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


# Some needed environment variables.
export BOOST_ROOT=/usr/local
export Boost_NO_SYSTEM_PATHS=ON
export ARMA_DIR=/usr
cmake -DSRW_OPTIMIZED=ON \
      -DDEVELOPER_INSTALL=ON \
      -DCMAKE_INSTALL_PREFIX=$ROOT_DIR \
      -DSingFElPhotonDiffractor=OFF \
      -Ds2e=OFF \
      -DS2EReconstruction_EMC=OFF\
      -DS2EReconstruction_DM=OFF\
      -Dwpg=OFF\
      -Dprop=OFF\
      -DFEFFPhotonInteractor=ON\
      $ROOT_DIR

# Build the project.
make -j8

# Install the project.
make install
