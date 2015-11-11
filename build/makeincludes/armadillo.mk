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
	@echo "\nFetching ${FULL_ARMADILLO}."
	cd ${PACKAGES} && \
    wget http://sourceforge.net/projects/arma/files/${FULL_ARMADILLO}.tar.gz && \
	touch $@
	@echo "Fetched ${ARMADILLO}.\n"

${ARMADILLO_SRC_DIR}/unpack.stamp: ${PACKAGES}/${FULL_ARMADILLO}_package.stamp
	@echo "\nUnpacking ${ARMADILLO}."
	cd ${SRC} && \
    tar -xvf ${PACKAGES}/${FULL_ARMADILLO}.tar.gz && \
	touch $@
	@echo "Unpacked ${ARMADILLO}.\n"

${ARMADILLO_SRC_DIR}/patch.stamp: ${ARMADILLO_SRC_DIR}/unpack.stamp
	@echo "\nPatching ${ARMADILLO}."
	cd ${ARMADILLO_SRC_DIR} && \
    sed -i -e '12 s/^/ \/\/ /' include/armadillo_bits/config.hpp && \
    sed -i -e '19 s/^/ \/\/ /' include/armadillo_bits/config.hpp && \
	touch $@
	@echo "Patched ${ARMADILLO}.\n"

${ARMADILLO_SRC_DIR}/configure.stamp: ${ARMADILLO_SRC_DIR}/patch.stamp
	@echo "\nConfiguring ${ARMADILLO}."
	touch $@
	@echo "Configured ${ARMADILLO}.\n"

${ARMADILLO_SRC_DIR}/build.stamp: ${ARMADILLO_SRC_DIR}/configure.stamp
	@echo "\nBuilding ${ARMADILLO}."
	cd ${ARMADILLO_SRC_DIR} && \
    cmake . && \
	touch $@
	@echo "Built ${MPICH}.\n"

${ARMADILLO_SRC_DIR}/install.stamp: ${ARMADILLO_SRC_DIR}/build.stamp
	@echo "\nBuilding ${ARMADILLO}."
	cd ${ARMADILLO_SRC_DIR} && \
    make install DESTDIR=${PREFIX_DIR}
	cp -r ${PREFIX_DIR}/usr/* ${PREFIX_DIR}
	rm -rf ${PREFIX_DIR}/usr
	touch $@
	@echo "Installed ${ARMADILLO}.\n"
