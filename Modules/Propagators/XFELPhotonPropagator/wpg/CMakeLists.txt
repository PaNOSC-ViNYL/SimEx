INCLUDE(ExternalProject)

ExternalProject_Add(
wpg
URL http://github.com/samoylv/WPG/archive/develop.zip
#PATCH_COMMAND patch wpg/glossary.py ${CMAKE_CURRENT_SOURCE_DIR}/glossary.py.patch
CONFIGURE_COMMAND ""
CMAKE_COMMAND ""
BUILD_IN_SOURCE 1
BUILD_COMMAND make all
INSTALL_COMMAND ""
)

ExternalProject_Get_Property(wpg SOURCE_DIR)
install( DIRECTORY ${SOURCE_DIR}/wpg DESTINATION ${PYPATH}
       )
