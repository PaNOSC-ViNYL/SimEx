INCLUDE(ExternalProject)

file(MAKE_DIRECTORY "${LIBDIR}")

FIND_PACKAGE (HDF5 REQUIRED)
FIND_PACKAGE (MPI REQUIRED)
FIND_PACKAGE (Armadillo REQUIRED)
FIND_PACKAGE(Boost 1.55.0 REQUIRED COMPONENTS python thread date_time system mpi serialization filesystem unit_test_framework)

ExternalProject_Add(
    singfel
    DOWNLOAD_COMMAND ""
    SOURCE_DIR ${CMAKE_CURRENT_SOURCE_DIR}
    CONFIGURE_COMMAND ""
    CMAKE_COMMAND ""
    MAKE_COMMAND ""
    BUILD_COMMAND ""
    BUILD_IN_SOURCE 1
    INSTALL_COMMAND LIBDIR=${LIBDIR} PREFIX_DIR=${CMAKE_INSTALL_PREFIX} PACKAGES=${PACKAGES} PATCHES=${PATCHES} SRC=${MODULES_SCR} make -f singfel.mk singfel
    )
    
#BOOST_INCLUDEDIR
#BOOST_DIR
#ARMA_DIR
#HDF5_DIR
#LD_LIBRARY_PATH

# of found mkl- cannot find iomp5 unless using intel compiler! 