ARMADILLO_MAJOR=6
ARMADILLO_MINOR=200
ARMADILLO_MICRO=2

ARMADILLO=armadillo
ARMADILLO_VERSION=${ARMADILLO_MAJOR}.${ARMADILLO_MINOR}.${ARMADILLO_MICRO}
FULL_ARMADILLO=${ARMADILLO}-${ARMADILLO_VERSION}
ARMADILLO_DIR=${PACKAGES}/${FULL_ARMADILLO}
ARMADILLO_SRC_DIR=${SRC}/${FULL_ARMADILLO}

armadillo: ${ARMADILLO_SRC_DIR}/install.stamp

${PACKAGES}/${FULL_ARMADILLO}_package.stamp:
	${call header2start,"Fetching ${FULL_ARMADILLO}."}
	cd ${PACKAGES} && \
    wget http://sourceforge.net/projects/arma/files/${FULL_ARMADILLO}.tar.gz && \
	touch $@
	${call header2end,"Fetched ${ARMADILLO}."}

${ARMADILLO_SRC_DIR}/unpack.stamp: ${PACKAGES}/${FULL_ARMADILLO}_package.stamp
	${call header2start,"Unpacking ${ARMADILLO}."}
	cd ${SRC} && \
    tar -xvf ${PACKAGES}/${FULL_ARMADILLO}.tar.gz && \
	touch $@
	${call header2end,"Unpacked ${ARMADILLO}."}

${ARMADILLO_SRC_DIR}/patch.stamp: ${ARMADILLO_SRC_DIR}/unpack.stamp
	${call header2start,"Patching ${ARMADILLO}."}
	cd ${ARMADILLO_SRC_DIR} && \
    sed -i -e '12 s/^/ \/\/ /' include/armadillo_bits/config.hpp && \
    sed -i -e '19 s/^/ \/\/ /' include/armadillo_bits/config.hpp && \
	touch $@
	${call header2end,"Patched ${ARMADILLO}."}

${ARMADILLO_SRC_DIR}/configure.stamp: ${ARMADILLO_SRC_DIR}/patch.stamp
	${call header2start,"Configuring ${ARMADILLO}."}
	touch $@
	${call header2end,"Configured ${ARMADILLO}."}

${ARMADILLO_SRC_DIR}/build.stamp: ${ARMADILLO_SRC_DIR}/configure.stamp
	${call header2start,"Building ${ARMADILLO}."}
	cd ${ARMADILLO_SRC_DIR} && \
    cmake . && \
	touch $@
	${call header2end,"Built ${MPICH}."}

${ARMADILLO_SRC_DIR}/install.stamp: ${ARMADILLO_SRC_DIR}/build.stamp
	${call header2start,"Building ${ARMADILLO}."}
	cd ${ARMADILLO_SRC_DIR} && \
    make install DESTDIR=${PREFIX_DIR}
	cp -r ${PREFIX_DIR}/usr/* ${PREFIX_DIR}
	rm -rf ${PREFIX_DIR}/usr
	touch $@
	${call header2end,"Installed ${ARMADILLO}."}
