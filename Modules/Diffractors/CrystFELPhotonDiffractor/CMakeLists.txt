INCLUDE(ExternalProject)

# Make sure hdf5 and gsl are available. Want dynamic linking to hdf5.
set (HDF5_USE_STATIC_LIBRARIES OFF)

FIND_PACKAGE (HDF5 REQUIRED COMPONENTS C CXX)
MESSAGE("HDF5_INCLUDE_DIRS= ${HDF5_INCLUDE_DIRS}")
MESSAGE("HDF5_INCLUDE_DIR= ${HDF5_INCLUDE_DIR}")
MESSAGE("HDF5_DEFINITIONS= ${HDF5_DEFINITIONS}")
MESSAGE("HDF5_C_LIBRARIES= ${HDF5_C_LIBRARIES}")
MESSAGE("HDF5_CXX_LIBRARIES= ${HDF5_CXX_LIBRARIES}")
MESSAGE("HDF5_Fortran_LIBRARIES= ${HDF5_Fortran_LIBRARIES}")
MESSAGE("HDF5_HL_LIBRARIES= ${HDF5_HL_LIBRARIES}")
MESSAGE("HDF5_Fortran_HL_LIBRARIES= ${HDF5_Fortran_HL_LIBRARIES}")
MESSAGE("HDF5_LIBRARIES= ${HDF5_LIBRARIES}")
MESSAGE("HDF5_FOUND= ${HDF5_FOUND}")
MESSAGE("HDF5_VERSION= ${HDF5_VERSION}")
MESSAGE("HDF5_LIBRARY_DIRS= ${HDF5_LIBRARY_DIRS}")

FIND_PACKAGE (GSL REQUIRED)

# This macro invokes the HDF5 compiler wrapper, it parses the output and
# extracts the path where library are stored.
# Usage:
# _get_h5_lib_dir(CXX VARIABLE_STORE_PATH)
# in case of errors the output variable is set to "NOT-FOUND"
# Following, cmake recomendation, local variables/functions not to be 
# used outside of the package have a name that starts with an underscore
# character.
# Usage:
#    _get_h5_lib_dir( LANG OUTLIST)
#    where LANG is the string of the language to be used e.g. CXX and
#    OUTLIST is the output string variable that will contain the *list*
#    of paths to be used
# The intent of this macro is to find the path to be passed to old
# configure style script to parameters like: --with-hdf5.
# Please note that dependening on how HDF5 is instlled on your system the 
# number of elements of OUTLIST could be >1, in such a case client code
# should deal with this.
# In case of erros, OUTLIST will be set to "NOT-FOUND"
# Pre-requisite: find_package(HDF5 REQUIRED)
MACRO(_get_h5_lib_dir language output_value)
    #First check that compiler executable for gien language exists
    if (HDF5_${language}_COMPILER_EXECUTABLE)
        #Call compiler with -show argument and capture output in
        #_cmt_output
        EXEC_PROGRAM( ${HDF5_${language}_COMPILER_EXECUTABLE}
                    ARGS -show
                    OUTPUT_VARIABLE _cmp_output
                    RETURN_VALUE _cmp_ret_val
                    )
        #If return code is zero, we can continue
        IF( ${_cmp_ret_val} EQUAL 0)
            #Use reg-expr to search for the -L flags on the output
            STRING( REGEX MATCHALL "-L([^\" ]+|\"[^\"]|\")"
                    _lib_path_flags
                    "${_cmp_output}")
            #The output is a list of options, now for each one
            #remove -L string and normalize paths
            FOREACH( LPATH ${_lib_path_flags})
                STRING(REGEX REPLACE "^-L" "" LPATH ${LPATH})
                STRING(REPLACE "//" "/" LPATH ${LPATH})
                LIST(APPEND ${output_value} ${LPATH})
            ENDFOREACH()
                # ok
        ELSE()
            MESSAGE(INFO "Unable to determine HDF5 ${language} flags
                    from compiler")

            SET(${output_value} "NOT-FOUND")
        ENDIF()
    ELSE()
        MESSAGE(INFO "Cannot find HDF5 compuiler for language
                ${language}")
        SET(${output_value} "NOT-FOUND")
    ENDIF()
ENDMACRO()


#Retrieve installation path for both C++ and C, do we need both?
_get_h5_lib_dir(CXX MYHDF5_LIBRARY_DIRS)
_get_h5_lib_dir(C MYHDF5_LIBRARY_DIRS)
#Remove duplicates from list
LIST(REMOVE_DUPLICATES MYHDF5_LIBRARY_DIRS)
#Check how many paths have been identified, if more than one
#make a workaround
LIST(LENGTH MYHDF5_LIBRARY_DIRS _listlen)
IF(${_listlen} GREATER 1)
    MESSAGE(WARNING "Retrieved more than one installation path for "
            "HDF5, using only the first one. This may not be correct.")
    FOREACH(_path ${MYHDF5_LIBRARY_DIRS})
            MESSAGE("Candidate path: " ${_path})
    ENDFOREACH()
    #If more than one path is found, extract from the list the first and
    #use that.
    LIST(GET MYHDF5_LIBRARY_DIRS 0 MYHDF5_LIBRARY_DIRS)
ENDIF()
# Add the project.
ExternalProject_Add( crystfel
    URL http://www.desy.de/~twhite/crystfel/crystfel-0.6.3.tar.gz
    BUILD_IN_SOURCE 1
    CONFIGURE_COMMAND ./configure --with-hdf5=${MYHDF5_LIBRARY_DIRS} --disable-gtk --disable-gtk-doc --disable-png --prefix=${CMAKE_INSTALL_PREFIX}
    #CONFIGURE_COMMAND ./configure --with-hdf5=/usr/lib64 --disable-gtk --disable-gtk-doc --disable-png 
)

# Install needed crystfel binaries, scripts and doc material.
ExternalProject_Get_Property(crystfel SOURCE_DIR)
#
install(PROGRAMS ${SOURCE_DIR}/src/pattern_sim DESTINATION ${BINDIR})
install(PROGRAMS ${SOURCE_DIR}/src/partial_sim DESTINATION ${BINDIR})
install(PROGRAMS ${SOURCE_DIR}/scripts/gen-sfs DESTINATION ${BINDIR})
install(PROGRAMS ${SOURCE_DIR}/scripts/gen-sfs-ano DESTINATION ${BINDIR})
install(PROGRAMS ${SOURCE_DIR}/scripts/gen-sfs-expand DESTINATION ${BINDIR})
install(DIRECTORY ${SOURCE_DIR}/doc/ DESTINATION ${DOCDIR}/crystfel)
