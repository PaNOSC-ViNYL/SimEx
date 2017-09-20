INCLUDE(ExternalProject)

# Make sure hdf5 and gsl are available. Want dynamic linking to hdf5.
set (HDF5_USE_STATIC_LIBRARIES OFF)
FIND_PACKAGE (HDF5 REQUIRED COMPONENTS C CXX)
FIND_PACKAGE (GSL REQUIRED)

# Add the project.
ExternalProject_Add( crystfel
    GIT_REPOSITORY https://stash.desy.de/scm/crys/crystfel.git
    PATCH_COMMAND ./autogen.sh
    BUILD_IN_SOURCE 1
    CONFIGURE_COMMAND ./configure --with-hdf5=${HDF5_LIBRARY_DIRS}
    INSTALL_COMMAND ""
)

# Install needed crystfel binaries, scripts and doc material.
ExternalProject_Get_Property(crystfel SOURCE_DIR)

install(PROGRAMS ${SOURCE_DIR}/src/pattern_sim DESTINATION ${BINDIR})
install(PROGRAMS ${SOURCE_DIR}/src/partial_sim DESTINATION ${BINDIR})
install(PROGRAMS ${SOURCE_DIR}/scripts/gen-sfs DESTINATION ${BINDIR})
install(PROGRAMS ${SOURCE_DIR}/scripts/gen-sfs-ano DESTINATION ${BINDIR})
install(PROGRAMS ${SOURCE_DIR}/scripts/gen-sfs-expand DESTINATION ${BINDIR})
install(DIRECTORY ${SOURCE_DIR}/doc/ DESTINATION ${DOCDIR}/crystfel)
