INCLUDE(ExternalProject)

FIND_PACKAGE (HDF5 REQUIRED HL CXX)
MESSAGE("HDF5_INCLUDE_DIRS=${HDF5_INCLUDE_DIRS}")
MESSAGE("HDF5_LIBRARY_DIRS=${HDF5_LIBRARY_DIRS}")
FIND_PACKAGE (MPI REQUIRED)
FIND_PACKAGE (Armadillo REQUIRED)
FIND_PACKAGE(Boost 1.55.0 REQUIRED COMPONENTS python thread date_time system mpi serialization
                                              filesystem unit_test_framework program_options)
FIND_PACKAGE(GSL REQUIRED)

ExternalProject_Add(
singfel
URL https://www.dropbox.com/s/nnoc78iafor0qrn/singfel.tar.gz
PATCH_COMMAND cp ${SIMEX_CMAKE_DIR}/FindArmadillo.cmake CMake/FindArmadillo.cmake &&
	          cp -v ${CMAKE_CURRENT_SOURCE_DIR}/patches/CMakeLists.txt.patch CMakeLists.txt &&
#	          cp ${SIMEX_CMAKE_DIR}/FindMKL.cmake CMake/ARMA_FindMKL.cmake &&
#	          cp ${SIMEX_CMAKE_DIR}/FindPythonLibs.cmake CMake &&
		  rm -rf CMake &&
		  ln -s ${SIMEX_CMAKE_DIR} CMake &&
		  patch	src/radiationDamageMPI.cpp ${CMAKE_CURRENT_SOURCE_DIR}/patches/radiationDamageMPI.cpp.patch
INSTALL_COMMAND ""
)

# cannot find iomp5 unless using intel compiler!

ExternalProject_Get_Property(singfel SOURCE_DIR)

install(DIRECTORY ${SOURCE_DIR}/bin/ DESTINATION ${BINDIR}/
        USE_SOURCE_PERMISSIONS
        )

install(DIRECTORY ${SOURCE_DIR}/libsingfel/ DESTINATION ${INCLUDEDIR}/singfel/
                                        USE_SOURCE_PERMISSIONS
                                        FILES_MATCHING
                                        PATTERN "*.h"
#                                        PATTERN "build" EXCLUDE
#                                        PATTERN ".*" EXCLUDE
                                        )

install(DIRECTORY ${SOURCE_DIR}/lib/ DESTINATION ${LIBDIR}/
                                        USE_SOURCE_PERMISSIONS
                                        FILES_MATCHING
                                        PATTERN "*.so"
#                                        PATTERN "build" EXCLUDE
#                                        PATTERN ".*" EXCLUDE
                                        )



