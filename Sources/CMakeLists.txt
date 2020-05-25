# find needed packages
include(FindPythonModules)
find_python_module(Bio REQUIRED)
find_python_module(Cython REQUIRED)
find_python_module(dill REQUIRED)
find_python_module(h5py REQUIRED)
find_python_module(matplotlib REQUIRED)
find_python_module(mpi4py REQUIRED)
find_python_module(openpmd_api REQUIRED)
find_python_module(numpy REQUIRED)
find_python_module(periodictable REQUIRED)
find_python_module(pint REQUIRED)
find_python_module(pyFAI REQUIRED)
find_python_module(scipy REQUIRED)
find_python_module(setuptools REQUIRED)
find_python_module(xraydb REQUIRED)

if (NOT DEVELOPER_INSTALL)
	install(DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/python/  DESTINATION ${PYPATH}
		    PATTERN "*.pyc" EXCLUDE
		    PATTERN ".git*" EXCLUDE
		    PATTERN "CMakeLists.txt" EXCLUDE )
endif()
