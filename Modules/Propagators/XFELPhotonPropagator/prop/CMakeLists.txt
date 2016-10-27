INCLUDE(ExternalProject)

ExternalProject_Add(
prop
URL  https://github.com/samoylv/prop/archive/b5e918fc8da58a91b2d131a84ff4b6024f7ffc24.zip
CONFIGURE_COMMAND ""
CMAKE_COMMAND ""
PATCH_COMMAND patch propagateSE.py ${CMAKE_CURRENT_SOURCE_DIR}/propagateSE.py.patch &&
              patch diagnostics.py ${CMAKE_CURRENT_SOURCE_DIR}/diagnostics.py.patch
BUILD_COMMAND ""
INSTALL_COMMAND ""
)


ExternalProject_Get_Property(prop SOURCE_DIR)

# creation of __init__.py
set (pyfile ${SOURCE_DIR}/__init__.py)      
add_custom_command (
  OUTPUT ${pyfile}
  COMMAND touch ${pyfile}        
  )
add_custom_target(GeneratePyInit ALL DEPENDS ${pyfile})

add_dependencies(GeneratePyInit prop)

install( DIRECTORY ${SOURCE_DIR} DESTINATION ${PYPATH}
       )   
      

