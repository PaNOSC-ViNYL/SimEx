INCLUDE(ExternalProject)

find_python_module(numba REQUIRED)
find_python_module(numpy REQUIRED)
find_python_module(scipy REQUIRED)
find_python_module(mpi4py REQUIRED)
find_python_module(h5py REQUIRED)


ExternalProject_Add(
singfel
URL https://github.com/eucall-software/pysingfel/archive/master.zip
CONFIGURE_COMMAND ""
CMAKE_COMMAND ""
PATCH_COMMAND ""
BUILD_COMMAND ""
INSTALL_COMMAND ""
)



ExternalProject_Get_Property(singfel SOURCE_DIR)

install(PROGRAMS ${SOURCE_DIR}/bin/ DESTINATION ${BINDIR})

install(DIRECTORY ${SOURCE_DIR}/pysingfel DESTINATION  ${PYPATH})

