ROOT=${PWD}/..
BUILD=${ROOT}/build
EXTERNALS=${BUILD}/externals
PACKAGES=${EXTERNALS}/packages
SRC=${EXTERNALS}/src
LIB=${ROOT}/lib
MAKE_INCLUDES=${BUILD}/makeincludes
PATCHES=${EXTERNALS}/patches

# Makefile for the SIMEX simulation suite.
# Build external dependencies.
include ${MAKE_INCLUDES}/wpg.mk

clean:
	rm -rf ${LIB}/*
	rm -rf ${SRC}/*
