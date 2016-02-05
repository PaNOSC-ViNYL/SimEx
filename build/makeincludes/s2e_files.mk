SIMS2E=simS2E
SIMS2E_DIR=${PACKAGES}/${SIMS2E}
SIMS2E_SRC_DIR=${SRC}/${SIMS2E}

s2e_files: ${SIMS2E_SRC_DIR}/install.stamp

${PACKAGES}/s2e_files_package.stamp:
	@echo "Fetching ${SIMS2E}."
	cd ${PACKAGES} && \
	wget https://github.com/chuckie82/simS2E/archive/master.zip && \
	mv master.zip ${SIMS2E}.zip && \
	touch $@
	@echo "Fetched ${SIMS2E}.\n"

${SIMS2E_SRC_DIR}/unpack.stamp: ${PACKAGES}/s2e_files_package.stamp
	@echo "Unpacking ${SIMS2E}."
	unzip -d ${SRC} ${PACKAGES}/${SIMS2E}.zip
	mv ${SRC}/${SIMS2E}-master ${SIMS2E_SRC_DIR}
	touch $@
	@echo "Unpacked ${SIMS2E}.\n"

${SIMS2E_SRC_DIR}/patch.stamp: ${SIMS2E_SRC_DIR}/unpack.stamp
	@echo "Installing ${SIMS2E}."
	cp ${PATCHES}/simS2E/pmi_demo.py ${SIMS2E_SRC_DIR}/packages/pmi/pmi_demo.py
	touch $@

${SIMS2E_SRC_DIR}/install.stamp: ${SIMS2E_SRC_DIR}/patch.stamp
	@echo "Installing ${SIMS2E}."
	cd ${SIMS2E_SRC_DIR} && \
	cp -av data/sim_example/diffr/s2e.beam ${SIMEX}/unittest/TestFiles/. && \
	cp -av data/sim_example/diffr/s2e.geom ${SIMEX}/unittest/TestFiles/. && \
	cp -av modules/diffr/prepHDF5.py       ${SIMEX}/src/SimEx/Utilities/. && \
    cp -av data/sim_example/sample/sample.h5 ${SIMEX}/unittest/TestFiles/. && \
    cp -av packages/pmi_demo/pmi_demo.py ${PYPATH}/. && \
	touch $@
	@echo "Installed ${SIMS2E}.\n"
