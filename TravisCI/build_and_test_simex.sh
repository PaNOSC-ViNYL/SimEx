#!/bin/bash
set -e # Exit with nonzero exit code if anything fails

# build & install
mkdir build
cd build
cmake -DCMAKE_INSTALL_PREFIX=$VIRTUAL_ENV -DSRW_OPTIMIZED=ON -DUSE_XCSITPhotonDetector=OFF -DDEVELOPER_INSTALL=OFF ..
make -j8
make install

# build & install docs
# make docs install

# Get testdata
# cd $VIRTUAL_ENV
# . $TRAVIS_BUILD_DIR/get_testdata.sh

# unit tests
# cd $VIRTUAL_ENV/Tests/python/unittest/
# python Test.py -v
### DEBUG
#cd $VIRTUAL_ENV/Tests/python/unittest/SimExTest/Calculators
#python SingFELPhotonDiffractorTest.py SingFELPhotonDiffractorTest.testBackengine -v
### END DEBUG


# Test doc.
# cd $VIRTUAL_ENV/Tests/doc
# python Test.py -v
