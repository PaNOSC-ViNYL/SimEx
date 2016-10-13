INCLUDE(ExternalProject)

cmake_minimum_required (VERSION 2.6)
project (feff8.5light)

enable_language (Fortran)

#FIND_PACKAGE (MKL REQUIRED)

ExternalProject_Add(
feff8.5light
URL https://github.com/eucall-software/feff8.5light/archive/master.zip
PATCH_COMMAND ""
)

ExternalProject_Get_Property(feff8.5light BINARY_DIR)
ExternalProject_Get_Property(feff8.5light SOURCE_DIR)

MESSAGE("feff8.5l BINARY_DIR=${BINARY_DIR}")
MESSAGE("feff8.5l SOURCE_DIR=${SOURCE_DIR}")

install(DIRECTORY ${SOURCE_DIR}/bin/ DESTINATION ${BINDIR}
        USE_SOURCE_PERMISSIONS
        )
