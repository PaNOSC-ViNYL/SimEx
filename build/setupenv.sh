#! /bin/sh
export PYTHONPATH=$PWD/../sw/lib/python2.7/site-packages:$PYTHONPATH
export PATH=$PWD/../sw/bin:$PATH
export INCLUDE_PATH=$PWD/../sw/include:$INCLUDE_PATH
export LD_LIBRARY_PATH=$PWD/../sw/lib:$PWD/../sw/lib64:$LD_LIBRARY_PATH

PYTHON27=`which python2.7`
PYTHON27_BIN_PATH=`dirname ${PYTHON27}`
PYTHON27_BASE_PATH=`dirname ${PYTHON27_BIN_PATH}`
export PYTHON27_INCLUDE_PATH=${PYTHON27_BASE_PATH}/include/python2.7
export PYTHON27_LIB=${PYTHON27_BASE_PATH}/lib/libpython2.7.so
