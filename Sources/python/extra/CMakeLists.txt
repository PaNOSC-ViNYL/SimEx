INCLUDE(ExternalProject)

ExternalProject_Add(
xraydb
URL  https://github.com/scikit-beam/XrayDB/archive/master.zip
CONFIGURE_COMMAND ""
CMAKE_COMMAND ""
BUILD_COMMAND ""
INSTALL_COMMAND ""
)

ExternalProject_Get_Property(xraydb SOURCE_DIR)

install(DIRECTORY ${SOURCE_DIR}/python/xraydb DESTINATION  ${PYPATH})
install(FILES ${SOURCE_DIR}/xraydb.sqlite DESTINATION  ${PYPATH}/xraydb)
