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
	${echo "\nFetching ${FULL_PROJECT}."}
	cd ${PACKAGES} && \
	<++> && \
	touch $@
	${echo "\nFetched ${PROJECT}."}

${PROJECT_SRC_DIR}/unpack.stamp: ${PACKAGES}/${FULL_PROJECT}_package.stamp
	${echo "\nUnpacking ${PROJECT}."}
	cd ${SRC} && \
	<++> && \
	touch $@
	${echo "\nUnpacked ${PROJECT}."}

${PROJECT_SRC_DIR}/patch.stamp: ${PROJECT_SRC_DIR}/unpack.stamp
	${echo "\nPatching ${PROJECT}."}
	<++> && \
	touch $@
	${echo "\nPatched ${PROJECT}."}

${PROJECT_SRC_DIR}/configure.stamp: ${PROJECT_SRC_DIR}/patch.stamp
	${echo "\nConfiguring ${PROJECT}."}
	cd ${PROJECT_SRC_DIR} && \
	<++> && \
	touch $@
	${echo "\nConfigured ${PROJECT}."}

${PROJECT_SRC_DIR}/build.stamp: ${PROJECT_SRC_DIR}/configure.stamp
	${echo "\nBuilding ${PROJECT}."}
	cd ${PROJECT_SRC_DIR} && \
	<++> && \
	touch $@
	${echo "\nBuilt ${MPICH}."}

${PROJECT_SRC_DIR}/install.stamp: ${PROJECT_SRC_DIR}/build.stamp
	${echo "\nBuilding ${PROJECT}."}
	cd ${PROJECT_SRC_DIR} && \
	<++> && \
	touch $@
	${echo "\nInstalled ${PROJECT}."}



