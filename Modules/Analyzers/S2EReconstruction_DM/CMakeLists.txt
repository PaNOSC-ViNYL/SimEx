INCLUDE(ExternalProject)


FIND_PACKAGE (MKL)

if(MKL_FOUND)
    set (makestring "make mkl")
else()
    FIND_PACKAGE (FFTW REQUIRED)
    MESSAGE("FFTW_INCLUDES=${FFTW_INCLUDES}")
    get_filename_component(FFTW_LIBRARY_DIR ${FFTW_LIBRARIES} DIRECTORY)
    MESSAGE("FFTW_LIBRARY_DIR=${FFTW_LIBRARY_DIR}")
    set (makestring "CPATH=${FFTW_INCLUDES} LIBRARY_PATH=${FFTW_LIBRARY_DIR} make")
endif()

INCLUDE(ExternalProject)
ExternalProject_Add(
recon_dm
URL https://github.com/eucall-software/emc_and_dm/archive/master.zip
PATCH_COMMAND cp ${CMAKE_CURRENT_SOURCE_DIR}/makefile_DM DM_Src/Makefile
CONFIGURE_COMMAND ""
CMAKE_COMMAND ""
BUILD_IN_SOURCE 1
BUILD_COMMAND bash -c "cd DM_Src && ${makestring}"
INSTALL_COMMAND ""
)

ExternalProject_Get_Property(recon_dm SOURCE_DIR)
set (DM_SOURCE_DIR ${SOURCE_DIR}/DM_Src)


install(PROGRAMS ${DM_SOURCE_DIR}/object_recon DESTINATION ${BINDIR})

install(FILES ${DM_SOURCE_DIR}/runDM.py DESTINATION  ${PYPATH})


