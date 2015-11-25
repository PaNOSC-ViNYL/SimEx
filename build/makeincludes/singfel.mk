SINGFEL=singfel
SINGFEL_DIR=${PACKAGES}/${SINGFEL}
SINGFEL_SRC_DIR=${SRC}/${SINGFEL}

singfel: ${MPICH_SRC_DIR}/install.stamp \
	${ARMADILLO_SRC_DIR}/install.stamp \
	${HDF5_SRC_DIR}/install.stamp \
	${BOOST_SRC_DIR}/install.stamp \
	${SINGFEL_SRC_DIR}/install.stamp

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
	patch CMakeLists.txt ${PATCHES}/${SINGFEL}/CMakeLists.txt.patch && \
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
		PATH=${PREFIX_DIR}/bin:${PATH} BOOST_INCLUDEDIR=${PREFIX_DIR}/include/boost BOOST_DIR=${PREFIX_DIR} ARMA_DIR=${PREFIX_DIR} LD_LIBRARY_PATH=${LIBDIR}:${LD_LIBRARY_PATH} HDF5_DIR=${PREFIX_DIR} cmake .. && \
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
