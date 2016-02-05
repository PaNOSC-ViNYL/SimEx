S2EFILES=s2e_files
S2EFILES_DIR=${PACKAGES}/${S2EFILES}
S2EFILES_SRC_DIR=${SRC}/${S2EFILES}

s2e_files: ${PACKAGES}/s2e_files_install.stamp

${PACKAGES}/s2e_files_package.stamp:
	@echo "\nFetching ${S2EFILES}."
	cd ${PACKAGES} && \
    wget https://github.com/chuckie82/simS2E/blob/master/data/sim_example/diffr/s2e.beam && \
    wget https://github.com/chuckie82/simS2E/blob/master/data/sim_example/diffr/s2e.geom && \
	wget https://github.com/chuckie82/simS2E/blob/master/modules/diffr/prepHDF5.py && \
	wget https://github.com/chuckie82/simS2E/blob/master/data/sim_example/sample/sample.h5 && \
	touch $@
	@echo "Fetched ${S2EFILES}.\n"

${PACKAGES}/s2e_files_install.stamp: ${PACKAGES}/s2e_files_package.stamp
	@echo "\nInstalling ${S2EFILES}."
	cp -av ${PACKAGES}/s2e.* ${SIMEX}/unittest/TestFiles/.
	cp -av ${PACKAGES}/sample.h5 ${SIMEX}/unittest/TestFiles/.
	cp -av ${PACKAGES}/prepHDF5.py ${SIMEX}/src/SimEx/Utilities/.
	touch $@
	@echo "Installed ${S2EFILES}.\n"
