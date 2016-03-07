# Modified slightly for FASTLIB usage; no longer depends on other CMake code
# from the project this came from (http://usg.lofar.org)

# +-----------------------------------------------------------------------------+
# | $Id:: template_FindXX.cmake 1643 2008-06-14 10:19:20Z baehren             $ |
# +-----------------------------------------------------------------------------+
# |   Copyright (C) 2010                                                        |
# |   Lars B"ahren (bahren@astron.nl)                                           |
# |                                                                             |
# |   This program is free software; you can redistribute it and/or modify      |
# |   it under the terms of the GNU General Public License as published by      |
# |   the Free Software Foundation; either version 2 of the License, or         |
# |   (at your option) any later version.                                       |
# |                                                                             |
# |   This program is distributed in the hope that it will be useful,           |
# |   but WITHOUT ANY WA; without even the implied warranty of            |
# |   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the             |
# |   GNU General Public License for more details.                              |
# |                                                                             |
# |   You should have received a copy of the GNU General Public License         |
# |   along with this program; if not, write to the                             |
# |   Free Software Foundation, Inc.,                                           |
# |   59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.                 |
# +-----------------------------------------------------------------------------+

# - Check for the presence of ARMADILLO
#
# The following variables are set when ARMADILLO is found:
#  Armadillo_FOUND       = Set to true, if all components of ARMADILLO have been
#                         found.
#  ARMADILLO_INCLUDES   = Include path for the header files of ARMADILLO
#  ARMADILLO_LIBRARIES  = Link these to use ARMADILLO
#  ARMADILLO_LFLAGS     = Linker flags (optional)

#=============================================================
# _ARMADILLO_GET_VERSION
# Internal function to parse the version number in version.hpp or
# arma_version.hpp (other code should figure out which of these exists).
# This is based on _GTK2_GET_VERSION.
#   _OUT_major = Major version number
#   _OUT_minor = Minor version number
#   _OUT_micro = Micro version number
#   _armaversion_hdr = Header file to parse
#=============================================================
function(_ARMA_GET_VERSION _OUT_major _OUT_minor _OUT_patch _armaversion_hdr)

endfunction()

## -----------------------------------------------------------------------------
## Check for the header files

find_path (ARMADILLO_INCLUDES Mat_meat.hpp
  PATHS 
  $ENV{ARMA_DIR}/include
  /usr/include
  /usr/local/include
  /opt/include
  PATH_SUFFIXES armadillo armadillo_bits
  )

## -----------------------------------------------------------------------------
## Check for the library

find_library (ARMADILLO_LIBRARIES armadillo
  PATHS
  $ENV{ARMA_DIR}/lib
  /usr/lib
  /usr/local/lib
  /opt/lib
  /usr/lib64
  PATH_SUFFIXES
  )



## -----------------------------------------------------------------------------
## Check for correct version of Armadillo

# Newer versions use arma_version.hpp
if (EXISTS "${ARMADILLO_INCLUDES}/arma_version.hpp")
  set(ARMA_VERSION_FILE "${ARMADILLO_INCLUDES}/arma_version.hpp")
elseif (EXISTS "${ARMADILLO_INCLUDES}/armadillo_bits/arma_version.hpp")
  set(ARMA_VERSION_FILE "${ARMADILLO_INCLUDES}/armadillo_bits/arma_version.hpp")
  message (STATUS "FIND_ARMA: YEAH I FOUNZ IT!!!")
else ()
  if (EXISTS "${ARMADILLO_INCLUDES}/version.hpp")
    set(ARMA_VERSION_FILE "${ARMADILLO_INCLUDES}/version.hpp")
  else ()
    # no version file exists... so we have no idea what version we are using
    set(ARMA_MAJOR_VERSION 0)
    set(ARMA_MINOR_VERSION 0)
    set(ARMA_PATCH_VERSION 0)
  endif ()
endif ()

if(ARMA_VERSION_FILE)
    file(READ ${ARMA_VERSION_FILE} _contents)
    if(_contents)
        if (EXISTS "${ARMADILLO_INCLUDES}/arma_version.hpp")
          string(REGEX REPLACE ".*#define ARMA_VERSION_MAJOR \([0-9]+\).*" "\\1" ARMA_MAJOR_VERSION "${_contents}")
          string(REGEX REPLACE ".*#define ARMA_VERSION_MINOR \([0-9]+\).*" "\\1" ARMA_MINOR_VERSION "${_contents}")
          string(REGEX REPLACE ".*#define ARMA_VERSION_PATCH \([0-9]+\).*" "\\1" ARMA_PATCH_VERSION "${_contents}")
        elseif (EXISTS "${ARMADILLO_INCLUDES}/armadillo_bits/arma_version.hpp")
          string(REGEX REPLACE ".*#define ARMA_VERSION_MAJOR \([0-9]+\).*" "\\1" ARMA_MAJOR_VERSION "${_contents}")
          string(REGEX REPLACE ".*#define ARMA_VERSION_MINOR \([0-9]+\).*" "\\1" ARMA_MINOR_VERSION "${_contents}")
          string(REGEX REPLACE ".*#define ARMA_VERSION_PATCH \([0-9]+\).*" "\\1" ARMA_PATCH_VERSION "${_contents}")
        else()
          string(REGEX REPLACE ".*static const unsigned int major = \([0-9]+\).*" "\\1" ARMA_MAJOR_VERSION "${_contents}")
          string(REGEX REPLACE ".*static const unsigned int minor = \([0-9]+\).*" "\\1" ARMA_MINOR_VERSION "${_contents}")
          string(REGEX REPLACE ".*static const unsigned int patch = \([0-9]+\).*" "\\1" ARMA_PATCH_VERSION "${_contents}")
        endif()

	if(NOT "${ARMA_MAJOR_VERSION}" MATCHES "^[0-9]+$")
	  # For some reason Debian puts version.hpp where arma_version.hpp is
	  # supposed to be and this messes up our regexes (0.9.52), so try
	  # again.
          string(REGEX REPLACE ".*static const unsigned int major = \([0-9]+\).*" "\\1" ARMA_MAJOR_VERSION "${_contents}")
          string(REGEX REPLACE ".*static const unsigned int minor = \([0-9]+\).*" "\\1" ARMA_MINOR_VERSION "${_contents}")
          string(REGEX REPLACE ".*static const unsigned int patch = \([0-9]+\).*" "\\1" ARMA_PATCH_VERSION "${_contents}")
        endif()  

        if(NOT "${ARMA_MAJOR_VERSION}" MATCHES "^[0-9]+$")
            message(FATAL_ERROR "Version parsing failed for ARMA_VERSION_MAJOR!")
        endif()
        if(NOT "${ARMA_MINOR_VERSION}" MATCHES "^[0-9]+$")
            message(FATAL_ERROR "Version parsing failed for ARMA_VERSION_MINOR!")
        endif()
        if(NOT "${ARMA_PATCH_VERSION}" MATCHES "^[0-9]+$")
            message(FATAL_ERROR "Version parsing failed for ARMA_VERSION_PATCH!")
        endif()
    else()
        # This should not be possible, but just in case...
        message(FATAL_ERROR "Include file ${ARMA_VERSION_FILE} does not exist")
    endif()
endif()

# Assemble version number
set(ARMA_FOUND_VERSION
  ${ARMA_MAJOR_VERSION}.${ARMA_MINOR_VERSION}.${ARMA_PATCH_VERSION})

if(Armadillo_FIND_VERSION)
  if(ARMA_FOUND_VERSION VERSION_EQUAL "0.0.0")
    message (FATAL_ERROR "Could not figure out which version of Armadillo is installed!")
    return()
  endif()

  set(ARMADILLO_FAILED_VERSION_CHECK true)

#  message(STATUS "Found version ${ARMA_FOUND_VERSION} and find version ${Armadillo_FIND_VERSION}")
  if(Armadillo_FIND_VERSION_EXACT)
    if(ARMA_FOUND_VERSION VERSION_EQUAL Armadillo_FIND_VERSION)
      set(ARMADILLO_FAILED_VERSION_CHECK false)
    endif()
  else() # not exact version requirement
    if(ARMA_FOUND_VERSION VERSION_EQUAL   Armadillo_FIND_VERSION OR
       ARMA_FOUND_VERSION VERSION_GREATER Armadillo_FIND_VERSION)
      set(ARMADILLO_FAILED_VERSION_CHECK false)
    endif()
  endif()

  if(ARMADILLO_FAILED_VERSION_CHECK)
    if(Armadillo_FIND_VERSION_EXACT)
      message (FATAL_ERROR "Found Armadillo version ${ARMA_FOUND_VERSION}; version ${Armadillo_FIND_VERSION} exactly is required.")
    else()
      message (FATAL_ERROR "Found Armadillo version ${ARMA_FOUND_VERSION}; version ${Armadillo_FIND_VERSION} or newer is required.")
    endif()
    return()
  endif()
endif()

# The header files will be in armadillo_bits/ but we also want to include the
# parent of that directory, which will include the armadillo header itself.
string(REGEX REPLACE "/armadillo_bits" "" ARMADILLO_EXTRA_INCLUDE ${ARMADILLO_INCLUDES})
set (ARMADILLO_INCLUDES ${ARMADILLO_INCLUDES} ${ARMADILLO_EXTRA_INCLUDE})

include (FindPackageHandleStandardArgs)
find_package_handle_standard_args (Armadillo DEFAULT_MSG ARMADILLO_LIBRARIES ARMADILLO_INCLUDES)


include (GetPrerequisites)
  
foreach (lib ${ARMADILLO_LIBRARIES})
    get_prerequisites(${lib} DEPENDENCIES 0 1 "" "")
    foreach(DEPENDENCY_FILE ${DEPENDENCIES})
       gp_resolve_item("${lib}" "${DEPENDENCY_FILE}" "" "" 
                       resolved_file)
    if(NOT EXISTS ${resolved_file})
        message (FATAL_ERROR "Cannot resolve armadillo's library dependency. ${resolved_file} not found. Set LD_LIBRARY_PATH")
    endif()                       
    endforeach()    
ENDFOREACH(lib)

## -----------------------------------------------------------------------------
## Actions taken when all components have been found


## -----------------------------------------------------------------------------
## Mark advanced variables

mark_as_advanced (
  ARMADILLO_INCLUDES
  ARMADILLO_LIBRARIES
  )


