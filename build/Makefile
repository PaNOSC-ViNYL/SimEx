ROOT=${PWD}/..
BUILD=${ROOT}/build
EXTERNALS=${BUILD}/externals
PACKAGES=${EXTERNALS}/packages
SRC=${EXTERNALS}/src
MAKE_INCLUDES=${BUILD}/makeincludes
PATCHES=${EXTERNALS}/patches
PREFIX_DIR=${ROOT}/sw
LIBDIR=${PREFIX_DIR}/lib
PYTHON_LIBDIR=${LIBDIR}/python2.7/site-packages

# Makefile for the SIMEX simulation suite.
# Build external dependencies.
# WPG
include ${MAKE_INCLUDES}/wpg.mk

# mpich
include ${MAKE_INCLUDES}/mpich.mk

# hdf5
include ${MAKE_INCLUDES}/hdf5.mk

# boost
include ${MAKE_INCLUDES}/boost.mk

## armadillo
include ${MAKE_INCLUDES}/armadillo.mk

## singFEL
include ${MAKE_INCLUDES}/singfel.mk

directories:
	if [ ! -d ${PREFIX_DIR} ]; then \
		mkdir -p ${PREFIX_DIR}; \
	fi
	if [ ! -d ${PREFIX_DIR}/lib/python2.7/site-packages ]; then \
		mkdir -p ${PREFIX_DIR}/lib/python2.7/site-packages; \
	fi




clean:
	rm -rf ${LIBDIR}/*
	rm -rf ${SRC}/*
