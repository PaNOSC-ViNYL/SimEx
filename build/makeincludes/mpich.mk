MPICH_MAJOR=3
MPICH_MINOR=1
MPICH_BUILD=2

MPICH=mpich-${MPICH_MAJOR}.${MPICH_MINOR}.${MPICH_BUILD}
MPICH_DIR=${PACKAGES}/${MPICH}
MPICH_SRC_DIR=${SRC}/${MPICH}

mpich: ${MPICH_SRC_DIR}/install.stamp

${PACKAGES}/mpich_package.stamp:
	@echo "\nFetching ${MPICH}."
	cd ${PACKAGES} && \
    wget http://www.mpich.org/static/downloads/${MPICH_MAJOR}.${MPICH_MINOR}.${MPICH_BUILD}/mpich-${MPICH_MAJOR}.${MPICH_MINOR}.${MPICH_BUILD}.tar.gz && \
	touch $@
	@echo "Fetched ${MPICH}.\n"

${MPICH_SRC_DIR}/unpack.stamp: ${PACKAGES}/mpich_package.stamp
	@echo "\nUnpacking ${MPICH}."
	cd ${SRC} && \
    tar -xvf ${PACKAGES}/mpich-${MPICH_MAJOR}.${MPICH_MINOR}.${MPICH_BUILD}.tar.gz && \
	touch $@
	@echo "Unpacked ${MPICH}.\n"

${MPICH_SRC_DIR}/patch.stamp: ${MPICH_SRC_DIR}/unpack.stamp
	@echo "\nPatching ${MPICH}."
	touch $@
	@echo "Patched ${MPICH}.\n"

${MPICH_SRC_DIR}/configure.stamp: ${MPICH_SRC_DIR}/patch.stamp
	@echo "\nConfiguring ${MPICH}."
	cd ${MPICH_SRC_DIR} && \
    ./configure --disable-fortran --prefix=${PREFIX_DIR} && \
	touch $@
	@echo "Configured ${MPICH}.\n"


${MPICH_SRC_DIR}/build.stamp: ${MPICH_SRC_DIR}/configure.stamp
	@echo "\nBuilding ${MPICH}."
	cd ${MPICH_SRC_DIR} && \
	make && \
	touch $@
	@echo "Built ${MPICH}.\n"

${MPICH_SRC_DIR}/install.stamp: ${MPICH_SRC_DIR}/build.stamp
	@echo "\nBuilding ${MPICH}."
	cd ${MPICH_SRC_DIR} && \
	make install && \
	touch $@
	@echo "Installed ${MPICH}.\n"
