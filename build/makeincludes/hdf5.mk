HDF5_MAJOR=1
HDF5_MINOR=8
HDF5_MICRO=15

HDF5=hdf5
HDF5_VERSION=${HDF5_MAJOR}.${HDF5_MINOR}.${HDF5_MICRO}
FULL_HDF5=${HDF5}-${HDF5_VERSION}
HDF5_DIR=${PACKAGES}/${FULL_HDF5}
HDF5_SRC_DIR=${SRC}/${FULL_HDF5}

hdf5: ${HDF5_SRC_DIR}/install.stamp

${PACKAGES}/${FULL_HDF5}_package.stamp:
	@echo "\nFetching ${FULL_HDF5}."
	cd ${PACKAGES} && \
    wget http://www.hdfgroup.org/ftp/HDF5/releases/${FULL_HDF5}/src/${FULL_HDF5}.tar.gz && \
	touch $@
	@echo "Fetched ${HDF5}.\n"

${HDF5_SRC_DIR}/unpack.stamp: ${PACKAGES}/${FULL_HDF5}_package.stamp
	@echo "\nUnpacking ${HDF5}."
	cd ${SRC} && \
    tar -xvf ${HDF5_DIR}.tar.gz && \
	touch $@
	@echo "Unpacked ${HDF5}.\n"

${HDF5_SRC_DIR}/patch.stamp: ${HDF5_SRC_DIR}/unpack.stamp
	@echo "\nPatching ${HDF5}."
	touch $@
	@echo "Patched ${HDF5}.\n"

${HDF5_SRC_DIR}/configure.stamp: ${HDF5_SRC_DIR}/patch.stamp
	@echo "\nConfiguring ${HDF5}."
	cd ${HDF5_SRC_DIR} && \
    ./configure --prefix=${PREFIX_DIR} --enable-cxx && \
	touch $@
	@echo "Configured ${HDF5}.\n"

${HDF5_SRC_DIR}/build.stamp: ${HDF5_SRC_DIR}/configure.stamp
	@echo "\nBuilding ${HDF5}."
	cd ${HDF5_SRC_DIR} && \
	make && \
	touch $@
	@echo "Built ${HDF5}.\n"

${HDF5_SRC_DIR}/install.stamp: ${HDF5_SRC_DIR}/build.stamp
	@echo "\nBuilding ${HDF5}."
	cd ${HDF5_SRC_DIR} && \
	make install && \
	touch $@
	@echo "Installed ${HDF5}.\n"

