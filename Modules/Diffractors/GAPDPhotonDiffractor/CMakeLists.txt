INCLUDE(ExternalProject)


FIND_PACKAGE (MPI REQUIRED)
FIND_PACKAGE (CUDA REQUIRED)


# Add the project.
ExternalProject_Add( gapd
    #URL http://www1.pims.ac.cn/UploadFile/file/GAPD.zip
	URL ${CMAKE_CURRENT_SOURCE_DIR}/GAPD.zip
    CONFIGURE_COMMAND ""
    BUILD_COMMAND ""
    INSTALL_COMMAND ""
)

# Install needed crystfel binaries, scripts and doc material.
ExternalProject_Get_Property(gapd SOURCE_DIR)
#
install(PROGRAMS ${SOURCE_DIR}/GAPD.cuda DESTINATION ${BINDIR})
install(PROGRAMS ${SOURCE_DIR}/GAPD_mem DESTINATION ${BINDIR})
install(FILES ${SOURCE_DIR}/README.pdf DESTINATION ${DOCDIR}/GAPD/README.pdf)
install(FILES ${SOURCE_DIR}/single-cu.cfg DESTINATION ${DOCDIR}/GAPD/single-cu.cfg)
install(FILES ${SOURCE_DIR}/single-cu.custom DESTINATION ${DOCDIR}/GAPD/single-cu.custom)
install(FILES ${SOURCE_DIR}/single-cu.data DESTINATION ${DOCDIR}/GAPD/single-cu.data)
install(FILES ${SOURCE_DIR}/single-cu.s.custom DESTINATION ${DOCDIR}/GAPD/single-cu.s.custom)
install(FILES ${SOURCE_DIR}/sucrose.data DESTINATION ${DOCDIR}/GAPD/sucrose.data)
install(FILES ${SOURCE_DIR}/sucrose.dump DESTINATION ${DOCDIR}/GAPD/sucrose.data)
install(FILES ${SOURCE_DIR}/sucrose.xyz DESTINATION ${DOCDIR}/GAPD/sucrose.xyz)
install(DIRECTORY ${SOURCE_DIR}/spectrum DESTINATION ${DOCDIR}/GAPD/)
