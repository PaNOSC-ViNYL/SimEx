BOOST_MAJOR=1
BOOST_MINOR=57
BOOST_MICRO=0

BOOST=boost
BOOST_DOTTED_VERSION=${BOOST_MAJOR}.${BOOST_MINOR}.${BOOST_MICRO}
BOOST_UNDERSCORED_VERSION=${BOOST_MAJOR}_${BOOST_MINOR}_${BOOST_MICRO}
FULL_BOOST=${BOOST}_${BOOST_UNDERSCORED_VERSION}
BOOST_DIR=${PACKAGES}/${FULL_BOOST}
BOOST_SRC_DIR=${SRC}/${FULL_BOOST}

boost: ${BOOST_SRC_DIR}/build.stamp \
	${BOOST_SRC_DIR}/install.stamp

${PACKAGES}/${FULL_BOOST}_package.stamp:
	${call header2start,"Fetching ${FULL_BOOST}."}
	cd ${PACKAGES} && \
    wget http://sourceforge.net/projects/boost/files/boost/${BOOST_DOTTED_VERSION}/${FULL_BOOST}.tar.gz && \
	touch $@
	${call header2end,"Fetched ${BOOST}."}

${BOOST_SRC_DIR}/unpack.stamp: ${BOOST_DIR}_package.stamp
	${call header2start,"Unpacking ${BOOST}."}
	cd ${SRC} && \
    tar -xvf ${BOOST_DIR}.tar.gz && \
	touch $@
	${call header2end,"Unpacked ${BOOST}."}

${BOOST_SRC_DIR}/configure.stamp: ${BOOST_SRC_DIR}/unpack.stamp
	${call header2start,"Configuring ${BOOST}."}
	cd ${BOOST_SRC_DIR} && \
    LD_LIBRARY_PATH=${LIBDIR} PATH=${PREFIX_DIR}/bin:${PATH} ./bootstrap.sh --prefix=${PREFIX_DIR} --with-python=/usr/bin/python && \
	touch $@
	${call header2end,"Configured ${BOOST}."}

${BOOST_SRC_DIR}/patch.stamp: ${BOOST_SRC_DIR}/configure.stamp
	${call header2start,"Patching ${BOOST}."}
	cd ${BOOST_SRC_DIR} && \
	echo "using mpi : ${PREFIX_DIR}/bin/mpicxx ;" >> project-config.jam && \
    echo "using mpi : ${PREFIX_DIR}/bin/mpicxx ;" >> user-config.jam && \
	touch $@
	${call header2end,"Patched ${BOOST}."}

${BOOST_SRC_DIR}/build.stamp: ${BOOST_SRC_DIR}/patch.stamp
	${call header2start,"Building ${BOOST}."}
	cd ${BOOST_SRC_DIR} && \
    LD_LIBRARY_PATH=${LIBDIR} PATH=${PREFIX_DIR}/bin:${PATH} ./b2 --with-mpi --debug-configuration --debug-building 2>&1 | tee b2.log && \
	touch $@
	${call header2end,"Built ${BOOST}."}

${BOOST_SRC_DIR}/install.stamp:
	${call header2start,"Building ${BOOST}."}
	cd ${BOOST_SRC_DIR} && \
    ./b2 --prefix=${PREFIX_DIR} install && \
	touch $@
	${call header2end,"Installed ${BOOST}."}

