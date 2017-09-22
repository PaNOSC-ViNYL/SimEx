#!/bin/bash
set -e # Exit with nonzero exit code if anything fails

printenv

# load git lfs files
git lfs pull

# build & install
mkdir build
cd build
cmake -DCMAKE_INSTALL_PREFIX=$VIRTUAL_ENV -DSRW_OPTIMIZED=ON -DXCSITPhotonDetector=OFF -DDEVELOPER_INSTALL=OFF ..
make -j8
make install

# build & install docs
make docs install

# unit tests
cd $VIRTUAL_ENV/Tests/python/unittest/
python Test.py -v

# Test doc.
cd $VIRTUAL_ENV/Tests/doc
python Test.py -v

# functional tests
#cd $VIRTUAL_ENV/Tests/python/functest/
#python Test.py -v
