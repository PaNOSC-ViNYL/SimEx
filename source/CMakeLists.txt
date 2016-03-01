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
set (LIBDIR     ${PREFIX_DIR}/lib)
set (BINDIR     ${PREFIX_DIR}/bin)
set (PYPATH     ${LIBDIR}/python)

add_subdirectory (Framework)

# create build dirs (temporarily)
set (MODULES_SCR ${SIMEX_BINARY_DIR}/modules_src)
set (PACKAGES ${MODULES_SCR})
set (PATCHES ${SIMEX_SOURCE_DIR}/Patches)

file(MAKE_DIRECTORY ${MODULES_SCR})


# find and add modules
set (SIMEX_MODULES_ROOT "${SIMEX_SOURCE_DIR}/Modules")
include (find_modules)
foreach(module ${SIMEX_MODULES})
	message (STATUS "***** Including module : ${module} ****")
    add_subdirectory("${SIMEX_MODULES_ROOT}/${module}")
	message (STATUS "*********************************************************")
endforeach()	

# create simex_vars.sh file
configure_file(simex_vars.sh.in simex_vars.sh)
install(FILES ${CMAKE_BINARY_DIR}/simex_vars.sh
        DESTINATION ${BINDIR})


