INCLUDE(ExternalProject)

ExternalProject_Add(
sdf
GIT_REPOSITORY https://cfsa-pmw.warwick.ac.uk/SDF/SDF.git
GIT_TAG 642be14ccae3bc7db53995f3fa8ea831bbbd3c6a
GIT_SUBMODULES C utilities
CMAKE_ARGS -DCMAKE_INSTALL_PREFIX=${PYPATH}
)