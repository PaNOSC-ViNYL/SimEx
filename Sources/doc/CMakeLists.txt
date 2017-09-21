INCLUDE(ExternalProject)

#soft find package to set needed variable
find_package(Sphinx)

#hard find package during build
add_custom_target(check-sphinx COMMAND ${CMAKE_COMMAND} -P ${SIMEX_CMAKE_DIR}/FindSphinx.cmake)

ExternalProject_Add(
docs
URL ${CMAKE_CURRENT_SOURCE_DIR}
PATCH_COMMAND ""
CONFIGURE_COMMAND ""
CMAKE_COMMAND ""
BUILD_IN_SOURCE 1
BUILD_COMMAND bash -c "source ${CMAKE_INSTALL_PREFIX}/${BINDIR}/simex_vars.sh && make SPHINXBUILD=${SPHINX_EXECUTABLE} html"
INSTALL_COMMAND ""
)

add_custom_target(clean-docs COMMAND ${CMAKE_MAKE_PROGRAM} clean WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR})

set_target_properties(docs PROPERTIES EXCLUDE_FROM_ALL TRUE)
set_target_properties(clean-docs PROPERTIES EXCLUDE_FROM_ALL TRUE)
set_target_properties(check-sphinx PROPERTIES EXCLUDE_FROM_ALL TRUE)


add_dependencies(docs check-sphinx clean-docs)


ExternalProject_Get_Property(docs SOURCE_DIR)
set (DOCS_BUILDDIR ${SOURCE_DIR}/build/html/)

install(DIRECTORY ${DOCS_BUILDDIR}
        DESTINATION ${DOCDIR}/simex
        OPTIONAL
	    PATTERN "*.pyc" EXCLUDE
	    PATTERN ".git*" EXCLUDE
	    PATTERN "CMakeLists.txt" EXCLUDE
)


