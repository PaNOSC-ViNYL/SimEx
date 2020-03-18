cmake_minimum_required (VERSION 3.12)

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

option (INSTALL_TESTS "Install tests" ON)

# options required for building the py_detector_interface module:
# XCSITPotonDetector
option(PY_DETECTOR_INTERFACE_DEBUG "
    -DPY_DETECTOR_INTERFACE_DEBUG=default: OFF | ON"
)

### PYTHON
FIND_PACKAGE(Python
             3.5
             REQUIRED
             )

set (LIBDIR     lib)
set (INCLUDEDIR include)
set (BINDIR     bin)
set (PYPATH     ${LIBDIR}/python${Python_VERSION_MAJOR}.${Python_VERSION_MINOR})
message( "PYPATH=${PYPATH}" )

set (DOCDIR share/doc)

option (PACKAGE_MAKE "Use this option to create linux packages" OFF)
if (PACKAGE_MAKE)
 set (TESTSDIR   share/simex/Tests)
else()
 set (TESTSDIR   Tests)
endif()

if (DEVELOPER_INSTALL)
  set (FRAMEWORK_DIR ${SIMEX_SOURCE_DIR}/Sources)
  set (UNITTESTS_DIR ${FRAMEWORK_DIR}/unittest/)
  set (UTILITIES_DIR ${FRAMEWORK_DIR}/python/SimEx/Utilities/)
  set (CALCULATORS_DIR ${FRAMEWORK_DIR}/python/SimEx/Calculators/)
else()
  set (UTILITIES_DIR ${PYPATH}/SimEx/Utilities/)
  set (CALCULATORS_DIR ${PYPATH}/SimEx/Calculators/)
  if (INSTALL_TESTS)
    add_subdirectory (Tests)
  endif()
endif()

message (STATUS "************************ checking python dependencies *****************************")
add_subdirectory (Sources)

#By default all modules are included/excluded depending on this flag.
#If a flag: USE_${module_name} is passed, this will overwrite teh default.
#For example:
# [De-]activate all modules:
#      cmake -DUSE_MODULES_DEFAULT=[OFF]ON [...]
# Activate a single module:
#      cmake -DUSE_MODULES_DEFAULT=OFF -DUSE_wpg=ON [...]
# Deactivate a single module:
#      cmake -DUSE_MODULES_DEFAULT=ON -DUSE_wpg=OFF [...]
option(USE_MODULES_DEFAULT "Default to include/exclude a module" ON)
message(STATUS "**************** Including modules (default "
            "${USE_MODULES_DEFAULT}) ****************")
# find and add modules
set (SIMEX_MODULES_ROOT "${SIMEX_SOURCE_DIR}/Modules")
include (find_modules)
foreach(module ${SIMEX_MODULES})
    MESSAGE("CHECKING ${module}")
    get_filename_component(module_name ${module} NAME)
    #If a variable USE_${module_name} is defined, use its value
    #overwrite the default.
    #Since we add the USE_* variable to the cache, we re-use it with
    #multiple cmake calls
    if(DEFINED USE_${module_name})
        #Add a cache variable with some help text. Note the
        #use of FORCE option to be sure the value is updated in the
        #cache
        set(USE_${module_name} ${USE_${module_name}}
                CACHE BOOL "Include mdoule ${module_name}" FORCE)
    endif()
endforeach()

foreach(module ${SIMEX_MODULES})
    get_filename_component(module_name ${module} NAME)
    #If a request specific to this module was done, use it
    if (DEFINED USE_${module_name})
        if(USE_${module_name})
            message (STATUS "***** Including module ${module_name} from: ${module} ****")
            add_subdirectory("${SIMEX_MODULES_ROOT}/${module}")
	        message (STATUS "*********************************************************")
        endif()
    else()
        if(USE_MODULES_DEFAULT)
            message (STATUS "***** Including module ${module_name} from: ${module} ****")
            add_subdirectory("${SIMEX_MODULES_ROOT}/${module}")
	        message (STATUS "*********************************************************")
        endif()
	endif()

endforeach()

# create simex_vars.sh file
if (DEVELOPER_INSTALL)
  configure_file(simex_vars_dev.sh.in simex_vars.sh)
  configure_file(simex_dev.in simex)
else()
  configure_file(simex_vars.sh.in simex_vars.sh)
  configure_file(simex.in simex)
endif()

install(FILES ${CMAKE_BINARY_DIR}/simex_vars.sh
        DESTINATION ${BINDIR})

install(PROGRAMS ${CMAKE_BINARY_DIR}/simex
        DESTINATION ${BINDIR})

# Copy diagnostic scripts to bin dir.
install(PROGRAMS ${SIMEX_SOURCE_DIR}/Sources/python/ScriptCollection/DataAnalysis/propagation/prop_diagnostics.py DESTINATION ${BINDIR})
install(PROGRAMS ${SIMEX_SOURCE_DIR}/Sources/python/ScriptCollection/DataAnalysis/pmi/pmi_diagnostics.py DESTINATION ${BINDIR})
install(PROGRAMS ${SIMEX_SOURCE_DIR}/Sources/python/ScriptCollection/DataAnalysis/scattering/diffr_diagnostics.py DESTINATION ${BINDIR})
install(PROGRAMS ${SIMEX_SOURCE_DIR}/Sources/python/ScriptCollection/DataAnalysis/emc/emc_diagnostics.py DESTINATION ${BINDIR})
install(PROGRAMS ${SIMEX_SOURCE_DIR}/Sources/python/SimEx/Utilities/wpg_to_opmd.py DESTINATION ${BINDIR})

if (PACKAGE_MAKE)
  add_subdirectory (Packages)
endif()

# Add documentation target.
add_subdirectory("Sources/doc")
