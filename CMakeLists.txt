cmake_minimum_required (VERSION 2.8)
project (SIMEX)

# Disallow in-source build
if ("${SIMEX_SOURCE_DIR}"  STREQUAL "${SIMEX_BINARY_DIR}")
  message(FATAL_ERROR
    "SIMEX requires an out of source Build. "
    "Please create a separate binary directory and run CMake there.")
endif()

# set path for modules
set (SIMEX_CMAKE_DIR "${SIMEX_SOURCE_DIR}/CMake")
set (CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} ${SIMEX_CMAKE_DIR})

# set install paths
set (PREFIX_DIR ${CMAKE_INSTALL_PREFIX})
set (FRAMEWORK_DIR ${CMAKE_INSTALL_PREFIX}/Framework)
set (UNITTESTS_DIR ${FRAMEWORK_DIR}/unittest/)
set (TESTFILES_DIR ${UNITTESTS_DIR}/TestFiles/)
set (UTILITIES_DIR ${FRAMEWORK_DIR}/src/SimEx/Utilities/)
set (CALCULATORS_DIR ${FRAMEWORK_DIR}/src/SimEx/Calculators/)
set (LIBDIR     ${PREFIX_DIR}/lib)
set (INCLUDEDIR     ${PREFIX_DIR}/include)
set (BINDIR     ${PREFIX_DIR}/bin)
set (PYPATH     ${LIBDIR}/python)



# add Framework source
add_subdirectory (Framework)

# find and add modules
set (SIMEX_MODULES_ROOT "${SIMEX_SOURCE_DIR}/Modules")
include (find_modules)
foreach(module ${SIMEX_MODULES})
    get_filename_component(module_name ${module} NAME)
    option(${module_name} "include ${module_name} module" ON)
endforeach()

foreach(module ${SIMEX_MODULES})
    get_filename_component(module_name ${module} NAME)
    if (${module_name})
	    message (STATUS "***** Including module : ${module} ****")
        add_subdirectory("${SIMEX_MODULES_ROOT}/${module}")
	    message (STATUS "*********************************************************")
	endif()
endforeach()	

# create simex_vars.sh file
configure_file(simex_vars.sh.in simex_vars.sh)
install(FILES ${CMAKE_BINARY_DIR}/simex_vars.sh
        DESTINATION ${BINDIR})


