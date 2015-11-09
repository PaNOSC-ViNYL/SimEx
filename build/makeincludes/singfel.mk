SINGFEL=singfel
SINGFEL_DIR=${PACKAGES}/singfel
SINGFEL_SRC_DIR=${SRC}/singfel

singfel: ${SINGFEL_SRC_DIR}/build.stamp

${PACKAGES}/singfel_package.stamp:
	${call header2start,"Fetching ${SINGFEL}."}
	cd ${PACKAGES} && \
    wget https://www.dropbox.com/s/nnoc78iafor0qrn/singfel.tar.gz?dl=0 -O singfel.tar.gz
	touch $@
	${call header2end,"Fetched ${SINGFEL}."}

${SINGFEL_SRC_DIR}/unpack.stamp: ${PACKAGES}/singfel_package.stamp
	${call header2start,"Unpacking ${SINGFEL}."}
	if [ ! -d ${SINGFEL_SRC_DIR} ]; then \
    	mkdir ${SINGFEL_SRC_DIR}; \
	fi
	cd ${SINGFEL_SRC_DIR} && \
	tar -xvf ${PACKAGES}/singfel.tar.gz --strip-components 1 && \
	touch $@
	${call header2end,"Unpacked ${SINGFEL}."}

${SINGFEL_SRC_DIR}/patch.stamp: ${SINGFEL_SRC_DIR}/unpack.stamp
	${call header2start,"Patching ${SINGFEL}."}
	cd ${SINGFEL_SRC_DIR} && \
	patch CMakeLists.txt ${PATCHES}/${SINGFEL}/CMakeLists.txt.patch
	touch $@
	${call header2end,"Patched ${SINGFEL}."}

${SINGFEL_SRC_DIR}/build.stamp: ${SINGFEL_SRC_DIR}/patch.stamp
	${call header2start,"Building ${SINGFEL}."}
	cd ${SINGFEL_SRC_DIR} && \
	if [ ! -d build ]; then \
		mkdir build; \
    fi
	cd ${SINGFEL_SRC_DIR}/build && \
    cmake .. && \
    make && \
	touch $@
	${call header2end,"Built ${SINGFEL}."}

${SINGFEL_SRC_DIR}/install.stamp: ${SINGFEL_SRC_DIR}/build.stamp
	${call header2start,"Building ${SINGFEL}."}
	cd ${SRC} && \
	cp -r singfel ${LIB} && \
	touch __init__.py && \
	touch $@
	${call header2end,"Installed ${SINGFEL}."}
