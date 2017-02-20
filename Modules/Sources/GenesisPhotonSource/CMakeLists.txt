INCLUDE(ExternalProject)

ExternalProject_Add(
ocelot
URL https://github.com/eucall-software/ocelot/archive/disable_pyfftw.zip
PATCH_COMMAND ""
INSTALL_COMMAND ""
CONFIGURE_COMMAND ""
BUILD_COMMAND ""
)

ExternalProject_Get_Property(ocelot SOURCE_DIR)
install(DIRECTORY ${SOURCE_DIR} DESTINATION  ${PYPATH})

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
