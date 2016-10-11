find_package(Sphinx REQUIRED)

if(NOT DEFINED SPHINX_THEME)
    set(SPHINX_THEME default)
endif()

if(NOT DEFINED SPHINX_THEME_DIR)
    set(SPHINX_THEME_DIR)
endif()

# configured documentation tools and intermediate build results
set(BINARY_BUILD_DIR "${CMAKE_CURRENT_BINARY_DIR}/source")
# HTML output directory
set(SPHINX_HTML_DIR "${CMAKE_CURRENT_BINARY_DIR}/build/html")
set(SPHINX_PDF_DIR "${CMAKE_CURRENT_BINARY_DIR}/build/latex")

configure_file(
    "${CMAKE_CURRENT_SOURCE_DIR}/source/conf.py"
    "${BINARY_BUILD_DIR}/conf.py"
    @ONLY)

configure_file(
    "${CMAKE_CURRENT_SOURCE_DIR}/source/index.rst"
    "${BINARY_BUILD_DIR}/index.rst"
    @ONLY)


add_custom_target(simex_doc_html ALL
    ${SPHINX_EXECUTABLE}
        -q -b html
        -c "${BINARY_BUILD_DIR}"
        "${CMAKE_CURRENT_SOURCE_DIR}/source"
        "${SPHINX_HTML_DIR}"
    COMMENT "Building HTML documentation with Sphinx.")

#add_custom_target(simex_doc_pdf ALL
    #${SPHINX_EXECUTABLE}
        #-q -b latex
        #-c "${BINARY_BUILD_DIR}"
        #"${CMAKE_CURRENT_SOURCE_DIR}/source"
        #"${SPHINX_PDF_DIR}"
        #COMMENT "Building PDF documentation with Sphinx.")
