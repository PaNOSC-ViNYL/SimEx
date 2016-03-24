# find needed packages
FIND_PACKAGE (PythonLibs 2.7 REQUIRED)
include(FindPythonModules)
find_python_module(h5py REQUIRED)
find_python_module(matplotlib REQUIRED)
find_python_module(scipy REQUIRED)

FIND_PACKAGE (LAPACK REQUIRED)
#message (STATUS "***** LAPACK_LIBRARIES ${LAPACK_LIBRARIES} ****")


install(DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/python/  DESTINATION ${PYPATH}
		    PATTERN "*.pyc" EXCLUDE
		    PATTERN ".git*" EXCLUDE 
		    PATTERN "CMakeLists.txt" EXCLUDE )	
