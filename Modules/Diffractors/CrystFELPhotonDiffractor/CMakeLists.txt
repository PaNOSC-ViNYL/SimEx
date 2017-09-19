INCLUDE(ExternalProject)

set (HDF5_USE_STATIC_LIBRARIES OFF)
FIND_PACKAGE (HDF5 REQUIRED COMPONENTS C CXX )
FIND_PACKAGE (GSL REQUIRED )

ExternalProject_Add(
crystfel
GIT_REPOSITORY https://stash.desy.de/scm/crys/crystfel.git
PATCH_COMMAND ./autogen.sh
BUILD_IN_SOURCE 1
CONFIGURE_COMMAND ./configure --with-hdf5=${HDF5_LIBRARY_DIRS}
INSTALL_COMMAND ""
)

ExternalProject_Get_Property(crystfel SOURCE_DIR)

install(PROGRAMS ${SOURCE_DIR}/src/pattern_sim DESTINATION ${BINDIR})
install(PROGRAMS ${SOURCE_DIR}/src/partial_sim DESTINATION ${BINDIR})
