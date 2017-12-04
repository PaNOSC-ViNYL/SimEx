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
MACRO(_get_h5_lib_dir language output_value)
    if (HDF5_${language}_COMPILER_EXECUTABLE)
        EXEC_PROGRAM( ${HDF5_${language}_COMPILER_EXECUTABLE}
                    ARGS -show
                    OUTPUT_VARIABLE _cmp_output
                    RETURN_VALUE _cmp_ret_val
                    )
        IF( ${_cmp_ret_val} EQUAL 0)
            STRING( REGEX MATCHALL "-L([^\" ]+|\"[^\"]|\")"
                    _lib_path_flags
                    "${_cmp_output}")
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
    

_get_h5_lib_dir(CXX MYHDF5_LIBRARY_DIRS)
_get_h5_lib_dir(C MYHDF5_LIBRARY_DIRS)
LIST(REMOVE_DUPLICATES MYHDF5_LIBRARY_DIRS)
# Add the project.
ExternalProject_Add( crystfel
    URL http://www.desy.de/~twhite/crystfel/crystfel-0.6.3.tar.gz
    BUILD_IN_SOURCE 1
    CONFIGURE_COMMAND ./configure --with-hdf5=${MYHDF5_LIBRARY_DIRS} --disable-gtk --disable-gtk-doc --disable-png
    INSTALL_COMMAND ""
)

# Install needed crystfel binaries, scripts and doc material.
ExternalProject_Get_Property(crystfel SOURCE_DIR)

install(PROGRAMS ${SOURCE_DIR}/src/pattern_sim DESTINATION ${BINDIR})
install(PROGRAMS ${SOURCE_DIR}/src/partial_sim DESTINATION ${BINDIR})
install(PROGRAMS ${SOURCE_DIR}/scripts/gen-sfs DESTINATION ${BINDIR})
install(PROGRAMS ${SOURCE_DIR}/scripts/gen-sfs-ano DESTINATION ${BINDIR})
install(PROGRAMS ${SOURCE_DIR}/scripts/gen-sfs-expand DESTINATION ${BINDIR})
install(DIRECTORY ${SOURCE_DIR}/doc/ DESTINATION ${DOCDIR}/crystfel)
