#
INCLUDE(ExternalProject)


# Create a new target to with the external project
ExternalProject_Add(
	py_detector_interface
	GIT_REPOSITORY https://github.com/JPBGoe/py_detector_interface.git
	TIMEOUT 10
	CMAKE_ARGS
    "-DXERCESC_ROOT=${XERCESC_ROOT}"
    "-DGEANT4_ROOT=${GEANT4_ROOT}"
    "-DXCSIT_ROOT=${XCSIT_ROOT}"
    "-DBOOST_ROOT=${BOOST_ROOT}"
    "-DCMAKE_INSTALL_PREFIX=${CMAKE_INSTALL_PREFIX}"
    "-DDEBUG=${PY_DETECTOR_INTERFACE_DEBUG}"
	PATCH_COMMAND ""
	INSTALL_COMMAND ""
	)


# get the project binary files
ExternalProject_Get_Property(py_detector_interface BINARY_DIR)
ExternalProject_Get_Property(py_detector_interface SOURCE_DIR)


# Copy the file which initalizes the local variables to the build folder
install(FILES ${BINARY_DIR}/py_detector_interface_env.sh
    DESTINATION ${BINDIR}
)

# Copy the header files
install(DIRECTORY ${SOURCE_DIR}/include/py_detector_interface/
    DESTINATION ${INCLUDEDIR}/py_detector_interface
    USE_SOURCE_PERMISSIONS
    FILES_MATCHING
    PATTERN "*.hh"
)

# Copy the created shared object to the correct location
install(DIRECTORY ${BINARY_DIR}/src/ DESTINATION
${LIBDIR}/python2.7
                                        USE_SOURCE_PERMISSIONS
                                        FILES_MATCHING
                                        PATTERN "*.so"
										PATTERN "CMakeFiles*" EXCLUDE
                                        )


