RECON=recon
RECON_DIR = ${PACKAGES}/${RECON}
RECON_SRC_DIR=${SRC}/${RECON}

${RECON}: ${HDF5_SRC_DIR}/install.stamp \
	${RECON_SRC_DIR}/install.stamp

${PACKAGES}/${RECON}_package.stamp:
	@echo "\nFetching ${RECON}."
	cd ${PACKAGES} && \
	wget https://db.tt/8CTthFkw -O ${RECON}.tar.gz
	touch $@
	@echo "Fetched ${RECON}.\n"

${RECON_SRC_DIR}/unpack.stamp: ${PACKAGES}/${RECON}_package.stamp
	@echo "\nUnpacking ${RECON}."
	if [ ! -d ${RECON_SRC_DIR} ]; then \
		mkdir ${RECON_SRC_DIR}; \
	fi
	cd ${RECON_SRC_DIR} && \
	tar xzvf ${PACKAGES}/${RECON}.zip && \
	touch $@
	@echo "Unpacked ${RECON}.\n"


${RECON_SRC_DIR}/build.stamp:${RECON_SRC_DIR}/unpack.stamp
	@echo "\nUnpacking ${RECON}."
	cd ${RECON_SRC_DIR}/s2e_recon/EMC_Src && \
	./compile_EMC && \
	touch $@
	@echo "Built ${RECON}.\n"


${RECON_SRC_DIR}/install.stamp:${RECON_SRC_DIR}/build.stamp
	touch $@
	@echo "Installed ${RECON}.\n"
