INCLUDE(ExternalProject)

option (SRW_OPTIMIZED "Use optimized SRW library" FALSE)
if (SRW_OPTIMIZED)
	set (WPG_PATCHCMD patch build/Makefile ${CMAKE_CURRENT_SOURCE_DIR}/Makefile.patch)
else()
	set (WPG_PATCHCMD "")
endif()

ExternalProject_Add(
wpg
URL https://github.com/samoylv/WPG/archive/a3c4f3cef591c1c2beca20f2218483248385d2c7.zip
PATCH_COMMAND ${WPG_PATCHCMD}
CONFIGURE_COMMAND ""
CMAKE_COMMAND ""
BUILD_IN_SOURCE 1
BUILD_COMMAND make all
INSTALL_COMMAND ""
)

ExternalProject_Get_Property(wpg SOURCE_DIR)
install( DIRECTORY ${SOURCE_DIR}/wpg DESTINATION ${PYPATH}
       )
