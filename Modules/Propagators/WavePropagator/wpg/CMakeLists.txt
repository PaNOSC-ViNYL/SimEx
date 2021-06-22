# find_package(Python COMPONENTS Interpreter Development)
set(Python_EXECUTABLE "python")

function(find_python_module module ARGV1 HAVE_MODULE)
	string(TOUPPER ${module} module_upper)
	if(NOT PY_${module_upper})
		if(ARGC GREATER 1 AND ARGV1 STREQUAL "REQUIRED")
			set(${module}_FIND_REQUIRED TRUE)
		endif()
		# A module's location is usually a directory, but for binary modules
		# it's a .so file.
		execute_process(COMMAND "${Python_EXECUTABLE}" "-c"
			"import re, ${module}; print(re.compile('/__init__.py.*').sub('',${module}.__file__))"
			RESULT_VARIABLE _${module}_status
			OUTPUT_VARIABLE _${module}_location
			ERROR_QUIET OUTPUT_STRIP_TRAILING_WHITESPACE)
		if(NOT _${module}_status)
			set(PY_${module_upper} ${_${module}_location} CACHE STRING
				"Location of Python module ${module}")
		endif(NOT _${module}_status)
	endif(NOT PY_${module_upper})
	find_package_handle_standard_args(PY_${module} DEFAULT_MSG PY_${module_upper})
	if(PY_${module_upper})
		set(${HAVE_MODULE} TRUE PARENT_SCOPE)
	else ()
		set(${HAVE_MODULE} FALSE PARENT_SCOPE )
	endif(PY_${module_upper})
	#set(foo "${_${module}_location}" PARENT_SCOPE)
endfunction(find_python_module)

find_python_module(wpg REQUIRED HAVE_WPG)
IF (HAVE_WPG)
    MESSAGE (">>> WPG is installed!")
    RETURN()
ELSE ()
    MESSAGE (">>> WPG is not installed!")
ENDIF ()

INCLUDE(ExternalProject)

option (SRW_OPTIMIZED "Use optimized SRW library" TRUE)

ExternalProject_Add(
wpg
# URL  https://github.com/PaNOSC-ViNYL/WPG/archive/develop.zip
URL  https://github.com/samoylv/WPG/archive/develop.zip
PATCH_COMMAND ""
CONFIGURE_COMMAND ""
CMAKE_COMMAND ""
BUILD_IN_SOURCE 1
BUILD_COMMAND OPENMP=omp make all
INSTALL_COMMAND ""
)

ExternalProject_Get_Property(wpg SOURCE_DIR)
install( DIRECTORY ${SOURCE_DIR}/wpg DESTINATION ${PYPATH})
install( DIRECTORY ${SOURCE_DIR}/s2e/prop DESTINATION ${PYPATH})
