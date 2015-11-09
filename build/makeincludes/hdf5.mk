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
	${call header2start,"Fetching ${FULL_HDF5}."}
	cd ${PACKAGES} && \
    wget http://www.hdfgroup.org/ftp/HDF5/releases/${FULL_HDF5}/src/${FULL_HDF5}.tar.gz && \
	touch $@
	${call header2end,"Fetched ${HDF5}."}

${HDF5_SRC_DIR}/unpack.stamp: ${PACKAGES}/${FULL_HDF5}_package.stamp
	${call header2start,"Unpacking ${HDF5}."}
	cd ${SRC} && \
    tar -xvf ${HDF5_DIR}.tar.gz && \
	touch $@
	${call header2end,"Unpacked ${HDF5}."}

${HDF5_SRC_DIR}/patch.stamp: ${HDF5_SRC_DIR}/unpack.stamp
	${call header2start,"Patching ${HDF5}."}
	touch $@
	${call header2end,"Patched ${HDF5}."}

${HDF5_SRC_DIR}/configure.stamp: ${HDF5_SRC_DIR}/patch.stamp
	${call header2start,"Configuring ${HDF5}."}
	cd ${HDF5_SRC_DIR} && \
    ./configure --prefix=${PREFIX_DIR} --enable-cxx && \
	touch $@
	${call header2end,"Configured ${HDF5}."}

${HDF5_SRC_DIR}/build.stamp: ${HDF5_SRC_DIR}/configure.stamp
	${call header2start,"Building ${HDF5}."}
	cd ${HDF5_SRC_DIR} && \
	make && \
	touch $@
	${call header2end,"Built ${HDF5}."}

${HDF5_SRC_DIR}/install.stamp: ${HDF5_SRC_DIR}/build.stamp
	${call header2start,"Building ${HDF5}."}
	cd ${HDF5_SRC_DIR} && \
	make install && \
	touch $@
	${call header2end,"Installed ${HDF5}."}

