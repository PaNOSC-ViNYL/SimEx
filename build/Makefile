ROOT=${PWD}/..
BUILD=${ROOT}/build
EXTERNALS=${BUILD}/externals
PACKAGES=${EXTERNALS}/packages
SRC=${EXTERNALS}/src
MAKE_INCLUDES=${BUILD}/makeincludes
PATCHES=${EXTERNALS}/patches
PREFIX_DIR=${ROOT}/sw
LIBDIR=${PREFIX_DIR}/lib
PYPATH=${LIBDIR}/python2.7/site-packages

default: all

all: directories \
	wpg \
	mpich \
	hdf5 \
	boost \
	armadillo \
	singfel

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

allclean: clean \
	rm -rf ${PREFIX_DIR}


# Makefile for the SIMEX simulation suite.
# Build external dependencies.
# WPG
include ${MAKE_INCLUDES}/wpg.mk
include ${MAKE_INCLUDES}/mpich.mk
include ${MAKE_INCLUDES}/hdf5.mk
include ${MAKE_INCLUDES}/boost.mk
include ${MAKE_INCLUDES}/armadillo.mk
include ${MAKE_INCLUDES}/singfel.mk

