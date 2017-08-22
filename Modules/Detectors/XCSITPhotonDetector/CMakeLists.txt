#
INCLUDE(ExternalProject)


# Create a new target to with the external project
ExternalProject_Add(
	dsim
	GIT_REPOSITORY https://github.com/JPBGoe/py_detector_interface.git
	TIMEOUT 10
	CMAKE_ARGS "-DXCSIT_FOLDER=${XCSIT_FOLDER}"
	"-DGEANT4_SOURCE=${GEANT4_SOURCE}"
	"-DGEANT4_BUILD=${GEANT4_BUILD}"
	"-DGEANT4_SO=${GEANT4_SO}"
	"-DXERCES=${XERCES}"
	PATCH_COMMAND ""
	INSTALL_COMMAND ""
	)


# get the project binary files
ExternalProject_Get_Property(dsim BINARY_DIR)

# Copy the created shared object to the correct location
install(DIRECTORY ${BINARY_DIR}/src/ DESTINATION ${LIBDIR}
                                        USE_SOURCE_PERMISSIONS
                                        FILES_MATCHING
                                        PATTERN "*.so"
										PATTERN "CMakeFiles*" EXCLUDE
                                        )

# Copz the file which initalizes the local variables to the build folder
install(FILES ${BINARY_DIR}/env.sh  DESTINATION ${BINDIR} 
	RENAME "py_detector_interface_env.sh"
)
