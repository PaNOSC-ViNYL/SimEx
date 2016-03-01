SINGFEL=singfel
SINGFEL_DIR=${PACKAGES}/${SINGFEL}
SINGFEL_SRC_DIR=${SRC}/${SINGFEL}

#export LD_LIBRARY_PATH=/afs/desy.de/products/python/.amd64_rhel60/2.7/lib:${LD_LIBRARY_PATH}
#export INCLUDE_PATH=/afs/desy.de/products/python/.amd64_rhel60/2.7/include/python2.7:${INCLUDE_PATH}


singfel: ${SINGFEL_SRC_DIR}/install.stamp

${PACKAGES}/singfel_package.stamp:
	@echo "\nFetching ${SINGFEL}."
	cd ${PACKAGES} && \
    wget https://www.dropbox.com/s/nnoc78iafor0qrn/singfel.tar.gz?dl=0 -O singfel.tar.gz
	touch $@
	@echo "Fetched ${SINGFEL}.\n"

${SINGFEL_SRC_DIR}/unpack.stamp: ${PACKAGES}/singfel_package.stamp
	@echo "\nUnpacking ${SINGFEL}."
	if [ ! -d ${SINGFEL_SRC_DIR} ]; then \
    	mkdir ${SINGFEL_SRC_DIR}; \
	fi
	cd ${SINGFEL_SRC_DIR} && \
	tar -xvf ${PACKAGES}/singfel.tar.gz --strip-components 1 && \
	touch $@
	@echo "Unpacked ${SINGFEL}.\n"

${SINGFEL_SRC_DIR}/patch.stamp: ${SINGFEL_SRC_DIR}/unpack.stamp
	@echo "\nPatching ${SINGFEL}."
	cd ${SINGFEL_SRC_DIR} && \
	cp -v ${PATCHES}/${SINGFEL}/CMakeLists.txt . && \
	patch CMake/FindArmadillo.cmake ${PATCHES}/${SINGFEL}/FindArmadillo.cmake.patch && \
	touch $@
	@echo "Patched ${SINGFEL}.\n"

${SINGFEL_SRC_DIR}/build.stamp: ${SINGFEL_SRC_DIR}/patch.stamp
	@echo "\nBuilding ${SINGFEL}."
	cd ${SINGFEL_SRC_DIR} && \
	if [ ! -d build ]; then \
		mkdir build; \
    fi
	cd ${SINGFEL_SRC_DIR}/build && \
		cmake .. && \
    make && \
	touch $@
	@echo "Built ${SINGFEL}.\n"

${SINGFEL_SRC_DIR}/install.stamp: ${SINGFEL_SRC_DIR}/build.stamp
	@echo "\nBuilding ${SINGFEL}."
	cd ${SRC} && \
	cp -r singfel/bin/* ${PREFIX_DIR}/bin && \
	if [ ! -d ${PREFIX_DIR}/include/singfel ]; then \
		mkdir -p ${PREFIX_DIR}/include/singfel; \
	fi && \
	cp -r singfel/libsingfel/*.h ${PREFIX_DIR}/include/singfel && \
	cp -r singfel/lib/*.so ${LIBDIR} && \
	touch $@
	@echo "Installed ${SINGFEL}.\n"
