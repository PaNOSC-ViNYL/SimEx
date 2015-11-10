MPICH_MAJOR=3
MPICH_MINOR=1
MPICH_BUILD=2

MPICH=mpich-${MPICH_MAJOR}.${MPICH_MINOR}.${MPICH_BUILD}
MPICH_DIR=${PACKAGES}/${MPICH}
MPICH_SRC_DIR=${SRC}/${MPICH}

mpich: ${MPICH_SRC_DIR}/install.stamp

${PACKAGES}/mpich_package.stamp:
	${call header2start,"Fetching ${MPICH}."}
	cd ${PACKAGES} && \
    wget http://www.mpich.org/static/downloads/${MPICH_MAJOR}.${MPICH_MINOR}.${MPICH_BUILD}/mpich-${MPICH_MAJOR}.${MPICH_MINOR}.${MPICH_BUILD}.tar.gz && \
	touch $@
	${call header2end,"Fetched ${MPICH}."}

${MPICH_SRC_DIR}/unpack.stamp: ${PACKAGES}/mpich_package.stamp
	${call header2start,"Unpacking ${MPICH}."}
	cd ${SRC} && \
    tar -xvf ${PACKAGES}/mpich-${MPICH_MAJOR}.${MPICH_MINOR}.${MPICH_BUILD}.tar.gz && \
	touch $@
	${call header2end,"Unpacked ${MPICH}."}

${MPICH_SRC_DIR}/patch.stamp: ${MPICH_SRC_DIR}/unpack.stamp
	${call header2start,"Patching ${MPICH}."}
	touch $@
	${call header2end,"Patched ${MPICH}."}

${MPICH_SRC_DIR}/configure.stamp: ${MPICH_SRC_DIR}/patch.stamp
	${call header2start,"Configuring ${MPICH}."}
	cd ${MPICH_SRC_DIR} && \
    ./configure --disable-fortran --prefix=${PREFIX_DIR} && \
	touch $@
	${call header2end,"Configured ${MPICH}."}


${MPICH_SRC_DIR}/build.stamp: ${MPICH_SRC_DIR}/configure.stamp
	${call header2start,"Building ${MPICH}."}
	cd ${MPICH_SRC_DIR} && \
	make && \
	touch $@
	${call header2end,"Built ${MPICH}."}

${MPICH_SRC_DIR}/install.stamp: ${MPICH_SRC_DIR}/build.stamp
	${call header2start,"Building ${MPICH}."}
	cd ${MPICH_SRC_DIR} && \
	make install && \
	touch $@
	${call header2end,"Installed ${MPICH}."}
