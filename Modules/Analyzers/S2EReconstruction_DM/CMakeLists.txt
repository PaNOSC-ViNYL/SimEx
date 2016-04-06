INCLUDE(ExternalProject)


FIND_PACKAGE (MKL)

if(MKL_FOUND)
    set (makestring "make mkl")
else()
    set (makestring "make")
    FIND_PACKAGE (FFTW REQUIRED)
endif()

INCLUDE(ExternalProject)
ExternalProject_Add(
recon_dm    
DOWNLOAD_COMMAND wget https://db.tt/8CTthFkw -O recon.tar.gz && tar xf recon.tar.gz && rm -rf recon_dm && mv s2e_recon recon_dm
#URL https://db.tt/8CTthFkw
#DOWNLOAD_NAME recon.tar.gz

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

   
