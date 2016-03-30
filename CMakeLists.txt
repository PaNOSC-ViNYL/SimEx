cmake_minimum_required (VERSION 2.8)

project (SIMEX)

include(CMakeDependentOption)

# Disallow in-source build
if ("${SIMEX_SOURCE_DIR}"  STREQUAL "${SIMEX_BINARY_DIR}")
  message(FATAL_ERROR
    "SIMEX requires an out of source Build. "
    "Please create a separate binary directory and run CMake there.")
endif()

# set path for modules
set (SIMEX_CMAKE_DIR "${SIMEX_SOURCE_DIR}/CMake")
set (CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} ${SIMEX_CMAKE_DIR})

option (DEVELOPER_INSTALL "Install modules only, do not install SimEx files" OFF)

CMAKE_DEPENDENT_OPTION(INSTALL_TESTS "Install test files" ON
                       "NOT DEVELOPER_INSTALL" OFF)

set (LIBDIR     lib)
set (INCLUDEDIR include)
set (BINDIR     bin)
set (PYPATH     ${LIBDIR}/python2.7)

option (PACKAGE_MAKE "Use this option to create linux packages" OFF)
if (PACKAGE_MAKE)
 set (TESTSDIR   share/simex/Tests)
else()
 set (TESTSDIR   Tests)
endif()

if (DEVELOPER_INSTALL)
  set (FRAMEWORK_DIR ${SIMEX_SOURCE_DIR}/Sources)
  set (UNITTESTS_DIR ${FRAMEWORK_DIR}/unittest/)
  set (TESTFILES_DIR ${UNITTESTS_DIR}/TestFiles/)
  set (UTILITIES_DIR ${FRAMEWORK_DIR}/python/SimEx/Utilities/)
  set (CALCULATORS_DIR ${FRAMEWORK_DIR}/python/SimEx/Calculators/)
else()
  set (UTILITIES_DIR ${PYPATH}/SimEx/Utilities/)
  set (CALCULATORS_DIR ${PYPATH}/SimEx/Calculators/)
  if (INSTALL_TESTS)
     add_subdirectory (Tests)
  endif()
  add_subdirectory (Sources)
endif()


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
if (DEVELOPER_INSTALL)
  configure_file(simex_vars_dev.sh.in simex_vars.sh)
else()
  configure_file(simex_vars.sh.in simex_vars.sh)
endif()

install(FILES ${CMAKE_BINARY_DIR}/simex_vars.sh
        DESTINATION ${BINDIR})


if (PACKAGE_MAKE)
  add_subdirectory (Packages)
endif()


