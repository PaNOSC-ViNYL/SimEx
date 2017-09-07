INCLUDE(ExternalProject)

option (SRW_OPTIMIZED "Use optimized SRW library" FALSE)

ExternalProject_Add(
wpg
URL  https://github.com/eucall-software/WPG/archive/feature/openmp.zip
#URL  https://github.com/samoylv/WPG/archive/feature/openmp.zip
PATCH_COMMAND ""
CONFIGURE_COMMAND ""
CMAKE_COMMAND ""
BUILD_IN_SOURCE 1
BUILD_COMMAND make all
INSTALL_COMMAND ""
)

ExternalProject_Get_Property(wpg SOURCE_DIR)
install( DIRECTORY ${SOURCE_DIR}/wpg DESTINATION ${PYPATH})
install( DIRECTORY ${SOURCE_DIR}/s2e/prop DESTINATION ${PYPATH})
