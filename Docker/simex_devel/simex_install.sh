#!/usr/bin/env bash

set -e

BRANCH=develop
URL=https://github.com/PaNOSC-ViNYL/SimEx/archive/${BRANCH}.zip

cd /opt

wget $URL
unzip ${BRANCH}.zip
rm ${BRANCH}.zip
cd SimEx-${BRANCH}

export PATH=/opt/miniconda/bin:$PATH
#export HDF5_ROOT=/opt/miniconda

echo "###### DONE unzip ${BRANCH}.zip"

conda install -c intel mkl
export MKLROOT=/opt/miniconda

# This is a dirty hack
pushd ${MKLROOT}/lib
ln -s . intel64
popd

echo "##### DONE install mkl"

#ROOT_DIR=/opt/simex_platform
#mkdir -p $ROOT_DIR

# PYPATH is necessary to facilitate the
# install of sdf and s2e; otherwise the
# modules are not installed outside  of 
# the build tree -- dwebster.
PYPATH=/opt/miniconda

CONDA_PREFIX=/opt/miniconda
CONDA_BIN=`which conda`
CONDA_BIN=${CONDA_BIN%/*}
source ${CONDA_BIN%/*}/etc/profile.d/conda.sh
INSTALL_PREFIX=$CONDA_PREFIX
PYVERSION=`python -V | tr  '[:upper:]' '[:lower:]' | tr -d ' '`
PYLIB=${PYVERSION%.*}
DEVELOPER_MODE=ON
export ZLIB_ROOT=$CONDA_PREFIX
export LD_LIBRARY_PATH=$CONDA_PREFIX/lib:$LD_LIBRARY_PATH

# Create new build dir and cd into it.

mkdir -v build
cd build

# Uncomment the next line and specify the install dir for a custom user install.
#cmake -DCMAKE_INSTALL_PREFIX=$ROOT_DIR $ROOT_DIR
# Uncomment the next line and specify the install dir for a developer install.
cmake -DUSE_XCSITPhotonDetector=OFF \
      -DUSE_GAPDPhotonDiffractor=OFF \
      -DUSE_CrystFELPhotonDiffractor=ON \
      -DUSE_SingFELPhotonDiffractor=ON \
      -DINSTALL_TESTS=OFF \
      -DSRW_OPTIMIZED=ON \
      -DDEVELOPER_INSTALL=$DEVELOPER_MODE \
      -DCMAKE_INSTALL_PREFIX=/opt/miniconda \
      -DUSE_sdf=ON \
      -DUSE_s2e=ON \
      -DUSE_S2EReconstruction_EMC=ON \
      -DUSE_S2EReconstruction_DM=ON \
      -DUSE_wpg=ON \
      -DUSE_GenesisPhotonSource=ON \
      -DUSE_FEFFPhotonInteractor=ON \
      -DCMAKE_INSTALL_LOCAL_ONLY=0 \
      .. 


# Build the project.
make -j12

echo "######## done make"

# Install the project.
make install
cd ../..

echo "####### done make install"


cp /opt/SimEx-${BRANCH}/build/simex_vars.sh ${CONDA_PREFIX}/bin
echo "source ${CONDA_PREFIX}/bin/simex_vars.sh" > /etc/profile.d/scripts-simex.sh && \
	chmod 755 /etc/profile.d/scripts-simex.sh

echo "export PYFAI_TESTIMAGES=/tmp" >> /etc/profile.d/scripts-simex.sh

