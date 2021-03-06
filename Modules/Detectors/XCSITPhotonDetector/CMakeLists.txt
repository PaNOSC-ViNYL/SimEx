#
INCLUDE(ExternalProject)

#Check for dependencies
#I think Geant4 is required w/ gdml support
#To specify directory of Geant4 use standard cmake argument:
# -DGeant4_DIR=<g4install>/lib[64]/Geant4-<version>
find_package(Geant4 REQUIRED gdml)
#Given we required gdml above, there is no more need of this here
#find_package(XercesC REQUIRED)

#Are we really sure about the minimal version needed?
find_package(Boost 1.54 REQUIRED)

option(XCSIT_ROOT "-DXCSIT_ROOT=<abs path> absolute path to the xcist
    installation directory that includes\n
    ./include/xcsit/
    ./lib/
    ./lib/xcsit/
    ./bin/"
)

# Create a new target to with the external project
ExternalProject_Add(
	py_detector_interface
	GIT_REPOSITORY https://github.com/eucall-software/py_detector_interface.git
    GIT_TAG python3
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
${PYPATH}
                                        USE_SOURCE_PERMISSIONS
                                        FILES_MATCHING
                                        PATTERN "*.so"
										PATTERN "CMakeFiles*" EXCLUDE
                                        )


