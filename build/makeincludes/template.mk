MAJOR=<+major version number+>
MINOR=<+minor version number+>
MICRO=<+build number+>

PROJECT=<+target+>
PROJECT_VERSION=${MAJOR}.${MINOR}.${BUILD}
FULL_PROJECT=${PROJECT}-${PROJECT_VERSION}
PROJECT_DIR=${PACKAGES}/${FULL_PROJECT}
PROJECT_SRC_DIR=${SRC}/${FULL_PROJECT}

<+target+>: ${PROJECT_SRC_DIR}/install.stamp

${PACKAGES}/${FULL_PROJECT}_package.stamp:
	${call header2start,"Fetching ${FULL_PROJECT}."}
	cd ${PACKAGES} && \
	<++> && \
	touch $@
	${call header2end,"Fetched ${PROJECT}."}

${PROJECT_SRC_DIR}/unpack.stamp: ${PACKAGES}/${FULL_PROJECT}_package.stamp
	${call header2start,"Unpacking ${PROJECT}."}
	cd ${SRC} && \
	<++> && \
	touch $@
	${call header2end,"Unpacked ${PROJECT}."}

${PROJECT_SRC_DIR}/patch.stamp: ${PROJECT_SRC_DIR}/unpack.stamp
	${call header2start,"Patching ${PROJECT}."}
	<++> && \
	touch $@
	${call header2end,"Patched ${PROJECT}."}

${PROJECT_SRC_DIR}/configure.stamp: ${PROJECT_SRC_DIR}/patch.stamp
	${call header2start,"Configuring ${PROJECT}."}
	cd ${PROJECT_SRC_DIR} && \
	<++> && \
	touch $@
	${call header2end,"Configured ${PROJECT}."}

${PROJECT_SRC_DIR}/build.stamp: ${PROJECT_SRC_DIR}/configure.stamp
	${call header2start,"Building ${PROJECT}."}
	cd ${PROJECT_SRC_DIR} && \
	<++> && \
	touch $@
	${call header2end,"Built ${MPICH}."}

${PROJECT_SRC_DIR}/install.stamp: ${PROJECT_SRC_DIR}/build.stamp
	${call header2start,"Building ${PROJECT}."}
	cd ${PROJECT_SRC_DIR} && \
	<++> && \
	touch $@
	${call header2end,"Installed ${PROJECT}."}



