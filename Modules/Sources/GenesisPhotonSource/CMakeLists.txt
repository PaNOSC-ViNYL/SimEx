INCLUDE(ExternalProject)

ExternalProject_Add(
ocelot
#URL https://github.com/eucall-software/ocelot/archive/dev_gen.zip
#URL https://github.com/ocelot-collab/ocelot/archive/dev_gen.zip
URL https://github.com/panosc-vinyl/ocelot/archive/dev_gen.zip
PATCH_COMMAND ""
INSTALL_COMMAND ""
CONFIGURE_COMMAND ""
BUILD_COMMAND ""
)

ExternalProject_Get_Property(ocelot SOURCE_DIR)
install(DIRECTORY ${SOURCE_DIR}/ocelot DESTINATION  ${PYPATH})

set (makestring "make")

ExternalProject_Add(
genesis
URL http://genesis.web.psi.ch/download/source/genesis_source_2.0_120629.tar.gz
PATCH_COMMAND ""
INSTALL_COMMAND ""
CONFIGURE_COMMAND ""
CMAKE_COMMAND ""
BUILD_IN_SOURCE 1
BUILD_COMMAND bash -c "${makestring}"
INSTALL_COMMAND ""
)

ExternalProject_Get_Property(genesis SOURCE_DIR)
install(PROGRAMS ${SOURCE_DIR}/genesis DESTINATION ${BINDIR})

#ExternalProject_Add(
    #pic_test_file
    #DOWNLOAD_COMMAND wget https://docs.xfel.eu/alfresco/d/a/workspace/SpacesStore/4d00d480-34a5-462e-8459-5483a75445c5/simData_8000.h5
    #PATCH_COMMAND ""
    #CONFIGURE_COMMAND ""
    #BUILD_COMMAND ""
    #INSTALL_COMMAND ""
#)

#ExternalProject_Get_Property(pic_test_file DOWNLOAD_DIR)
#install(FILES ${DOWNLOAD_DIR}/simData_8000.h5 DESTINATION ${SIMEX_SOURCE_DIR}/Tests/python/unittest/TestFiles/)
