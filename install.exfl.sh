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
export BOOST_ROOT=$HOME/local
export Boost_NO_SYSTEM_PATHS=ON
export ARMA_DIR=$HOME/local
export HDF5_ROOT=/opt/hdf5/hdf5-1.8.14

# uncomment the next line  if you want to use Intel Fotran compiler (otherwise gfortran will be used). Make sure $MKLROOT is set 
# export FC=ifort

# Uncomment the next line and specify the install dir for a custom user install.
#cmake -DCMAKE_INSTALL_PREFIX=$ROOT_DIR $ROOT_DIR
# Uncomment the next line and specify the install dir for a developer install.
cmake -DDEVELOPER_INSTALL=ON -DCMAKE_INSTALL_PREFIX=$ROOT_DIR $ROOT_DIR

# Build the project.
make

# Install the project.
make install
