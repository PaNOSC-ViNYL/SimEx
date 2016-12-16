INCLUDE(ExternalProject)

ExternalProject_Add(
prop
URL https://github.com/samoylv/WPG/archive/a3c4f3cef591c1c2beca20f2218483248385d2c7.zip
CONFIGURE_COMMAND ""
CMAKE_COMMAND ""
PATCH_COMMAND patch s2e/prop/propagateSE.py ${CMAKE_CURRENT_SOURCE_DIR}/propagateSE.py.patch &&
              patch s2e/prop/diagnostics.py ${CMAKE_CURRENT_SOURCE_DIR}/diagnostics.py.patch
BUILD_COMMAND ""
INSTALL_COMMAND ""
)


ExternalProject_Get_Property(prop SOURCE_DIR)

# creation of __init__.py
set (pyfile ${SOURCE_DIR}/s2e/prop/__init__.py)      
add_custom_command (
  OUTPUT ${pyfile}
  COMMAND touch ${pyfile}        
  )
add_custom_target(GeneratePyInit ALL DEPENDS ${pyfile})

add_dependencies(GeneratePyInit prop)

install( DIRECTORY ${SOURCE_DIR}/s2e/prop DESTINATION ${PYPATH}
       )   
      

