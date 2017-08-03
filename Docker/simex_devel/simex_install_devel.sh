#!/usr/bin/env bash

set -e


BRANCH=develop
URL=https://github.com/eucall-software/simex_platform.git
cd /opt

wget https://github.com/github/git-lfs/releases/download/v1.1.2/git-lfs-linux-amd64-1.1.2.tar.gz
mkdir -p $HOME/bin
tar xvfz git-lfs-linux-amd64-1.1.2.tar.gz
mv git-lfs-1.1.2/git-lfs $HOME/bin/git-lfs
export PATH=$PATH:$HOME/bin/

git clone -b ${BRANCH} $URL
#git clone -b mpi_multifiles $URL
cd simex_platform
git lfs pull

export PATH=/opt/miniconda2/bin:$PATH
export HDF5_ROOT=/opt/miniconda2

ROOT_DIR=/opt/simex_platform

# Create new build dir and cd into it.

mkdir -v build
cd build

# Uncomment the next line and specify the install dir for a custom user install.
#cmake -DCMAKE_INSTALL_PREFIX=$ROOT_DIR $ROOT_DIR
# Uncomment the next line and specify the install dir for a developer install.
cmake -DSRW_OPTIMIZED=ON -DDEVELOPER_INSTALL=ON -DCMAKE_INSTALL_PREFIX=$ROOT_DIR $ROOT_DIR

chmod og+rwX -R $ROOT_DIR

# Build the project.
make


# Install the project.
make install
cd ..

rm -rf build

echo "source /opt/simex_platform/bin/simex_vars.sh" > /etc/profile.d/scripts-simex.sh && \
	chmod 755 /etc/profile.d/scripts-simex.sh
chmod og+rwX -R /opt/simex_platform

echo "export PYFAI_TESTIMAGES=/tmp" >> /etc/profile.d/scripts-simex.sh


