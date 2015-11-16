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
	armadillo \
	boost \
	hdf5 \
	singfel

directories:
	@echo "Making directories."
	if [ ! -d ${PREFIX_DIR} ]; then \
		mkdir -p ${PREFIX_DIR}; \
	fi
	if [ ! -d ${SRC} ]; then \
		mkdir -p ${SRC}; \
	fi
	if [ ! -d ${PACKAGES} ]; then \
		mkdir -p ${PACKAGES}; \
	fi
	if [ ! -d ${PYPATH} ]; then \
		mkdir -p ${PYPATH}; \
	fi
	touch ${PYPATH}/__init__.py
	@echo "Made directories.\n"

clean:
	@echo "\nCleaning."
	rm -rf ${LIBDIR}/* && \
	rm -rf ${SRC}
	@echo "Done cleaning.\n"

allclean: clean
	@echo "\nCleaning all."
	rm -rf ${PREFIX_DIR}
	@echo "Done cleaning all.\n"

# Makefile for the SIMEX simulation suite.
# Build external dependencies.
# WPG
include ${MAKE_INCLUDES}/wpg.mk
include ${MAKE_INCLUDES}/mpich.mk
include ${MAKE_INCLUDES}/hdf5.mk
include ${MAKE_INCLUDES}/boost.mk
include ${MAKE_INCLUDES}/armadillo.mk
include ${MAKE_INCLUDES}/singfel.mk

