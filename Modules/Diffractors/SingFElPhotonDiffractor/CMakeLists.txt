INCLUDE(ExternalProject)

FIND_PACKAGE (HDF5 REQUIRED HL CXX)
MESSAGE("HDF5_INCLUDE_DIRS=${HDF5_INCLUDE_DIRS}")
MESSAGE("HDF5_LIBRARY_DIRS=${HDF5_LIBRARY_DIRS}")
FIND_PACKAGE (MPI REQUIRED)
FIND_PACKAGE (Armadillo REQUIRED)
FIND_PACKAGE(Boost 1.55.0 REQUIRED COMPONENTS python thread date_time system mpi serialization
                                              filesystem unit_test_framework program_options)
FIND_PACKAGE(GSL REQUIRED)
MESSAGE("GSL_INCLUDE_DIRS=${GSL_INCLUDE_DIRS}")
MESSAGE("GSL_LIBRARIES=${GSL_LIBRARIES}")


ExternalProject_Add(
singfel
URL https://github.com/eucall-software/singfel/archive/v0.2.3.zip
PATCH_COMMAND ""
INSTALL_COMMAND ""
)

# cannot find iomp5 unless using intel compiler!

ExternalProject_Get_Property(singfel BINARY_DIR)
ExternalProject_Get_Property(singfel SOURCE_DIR)

install(DIRECTORY ${BINARY_DIR}/bin/ DESTINATION ${BINDIR}
        USE_SOURCE_PERMISSIONS
        )

install(DIRECTORY ${SOURCE_DIR}/libsingfel/ DESTINATION ${INCLUDEDIR}/singfel
                                        USE_SOURCE_PERMISSIONS
                                        FILES_MATCHING
                                        PATTERN "*.h"
#                                        PATTERN "build" EXCLUDE
#                                        PATTERN ".*" EXCLUDE
                                        )

install(DIRECTORY ${SOURCE_DIR}/lib/ DESTINATION ${LIBDIR}
                                        USE_SOURCE_PERMISSIONS
                                        FILES_MATCHING
                                        PATTERN "*.so"
#                                        PATTERN "build" EXCLUDE
#                                        PATTERN ".*" EXCLUDE
                                        )



