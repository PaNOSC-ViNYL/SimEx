# find needed packages
FIND_PACKAGE(PythonInterp 2.7 REQUIRED)
FIND_PACKAGE (PythonLibs 2.7 REQUIRED)
include(FindPythonModules)
find_python_module(h5py REQUIRED)
find_python_module(matplotlib REQUIRED)
find_python_module(scipy REQUIRED)
find_python_module(mpi4py REQUIRED)
find_python_module(periodictable REQUIRED)
find_python_module(dill REQUIRED)
find_python_module(Bio REQUIRED)
find_python_module(argparse REQUIRED)
find_python_module(Cython REQUIRED)
find_python_module(datetime REQUIRED)
find_python_module(numpy REQUIRED)
find_python_module(setuptools REQUIRED)
find_python_module(breathe REQUIRED)
find_python_module(sqlalchemy REQUIRED)
find_python_module(pyfftw REQUIRED)
find_python_module(pyFAI REQUIRED)
find_python_module(numba REQUIRED)
find_python_module(PyQt4 REQUIRED)

#FIND_PACKAGE (LAPACK REQUIRED)
##message (STATUS "***** LAPACK_LIBRARIES ${LAPACK_LIBRARIES} ****")

if (NOT DEVELOPER_INSTALL)
	install(DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/python/  DESTINATION ${PYPATH}
		    PATTERN "*.pyc" EXCLUDE
		    PATTERN ".git*" EXCLUDE
		    PATTERN "CMakeLists.txt" EXCLUDE )
endif()


