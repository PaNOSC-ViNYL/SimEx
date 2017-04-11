INCLUDE(ExternalProject)

option (SRW_OPTIMIZED "Use optimized SRW library" FALSE)

ExternalProject_Add(
wpg
URL  https://github.com/eucall-software/WPG/archive/feature/openmp.zip
#PATCH_COMMAND ${WPG_PATCHCMD}
PATCH_COMMAND ""
CONFIGURE_COMMAND ""
CMAKE_COMMAND ""
BUILD_IN_SOURCE 1
BUILD_COMMAND make all
INSTALL_COMMAND ""
)

ExternalProject_Get_Property(wpg SOURCE_DIR)
set (pyfile ${SOURCE_DIR}/s2e/prop/__init__.py)
add_custom_command (
  OUTPUT ${pyfile}
  COMMAND touch ${pyfile}
  )
add_custom_target(GeneratePyInit ALL DEPENDS ${pyfile})
add_dependencies(GeneratePyInit prop)


install( DIRECTORY ${SOURCE_DIR}/wpg DESTINATION ${PYPATH})
install( DIRECTORY ${SOURCE_DIR}/s2e/prop DESTINATION ${PYPATH})
