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

execute_process(COMMAND python setup.py build WORKING_DIRECTORY ${SOURCE_DIR}/python)
install(DIRECTORY ${SOURCE_DIR}/python/build/lib.linux-x86_64-2.7/xraydb DESTINATION  ${PYPATH})
