INCLUDE(ExternalProject)

find_python_module(numba REQUIRED)
find_python_module(numpy REQUIRED)
find_python_module(scipy REQUIRED)
find_python_module(mpi4py REQUIRED)
find_python_module(h5py REQUIRED)


ExternalProject_Add(
crystfel
GIT_REPOSITORY https://stash.desy.de/scm/crys/crystfel.git
CONFIGURE_COMMAND "./autogen.sh && ./configure"
INSTALL_COMMAND ""
)



ExternalProject_Get_Property(crystfel SOURCE_DIR)

install(PROGRAMS ${SOURCE_DIR}/bin/pattern_sim DESTINATION ${BINDIR})

#install(DIRECTORY ${SOURCE_DIR}/pysingfel DESTINATION  ${PYPATH})

