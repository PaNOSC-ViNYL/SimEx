###################
#     WPG/SRW     #
###################
#include ${ROOT_DIR}/packages/environment.mk

WPG=wpg
WPG_DIR=${PACKAGES}/WPG-develop
WPG_SRC_DIR=${SRC}/WPG-develop

wpg: ${WPG_SRC_DIR}/install.stamp

${PACKAGES}/wpg_package.stamp:
	@echo "\nFetching ${WPG}."
	cd ${PACKAGES} && \
	wget http://github.com/samoylv/WPG/archive/develop.zip -O wpg-develop.zip && \
	wget https://github.com/samoylv/prop/archive/develop.zip -O prop-develop.zip && \
	touch $@
	@echo "Fetched ${WPG}.\n"

${WPG_SRC_DIR}/unpack.stamp: ${PACKAGES}/wpg_package.stamp
	@echo "\nUnpacking ${WPG}."
	cd ${SRC} && \
	unzip -o ${PACKAGES}/wpg-develop.zip && \
	unzip -o ${PACKAGES}/prop-develop.zip && \
	touch $@
	@echo "Unpacked ${WPG}.\n"

${WPG_SRC_DIR}/patch.stamp: ${WPG_SRC_DIR}/unpack.stamp
	@echo "\nPatching ${WPG}."
	cd ${SRC}/prop-develop && \
	patch propagateSE.py ${PATCHES}/wpg/propagateSE.py.patch && \
	patch diagnostics.py ${PATCHES}/wpg/diagnostics.py.patch && \
	touch $@
	@echo "Patched ${WPG}.\n"

${WPG_SRC_DIR}/build.stamp: ${WPG_SRC_DIR}/patch.stamp
	@echo "\nBuilding ${WPG}."
	cd ${SRC}/WPG-develop && make all
	touch $@
	@echo "Built ${WPG}.\n"

${WPG_SRC_DIR}/install.stamp: ${WPG_SRC_DIR}/build.stamp
	@echo "\nInstalling ${WPG}."
	cd ${SRC} && \
	if [ -d ${PYPATH}/prop ]; then \
		rm -rf ${PYPATH}/prop; \
	fi && \
	cp -r prop-develop ${PYPATH}/prop && \
	touch ${PYPATH}/prop/__init__.py && \
	cp -r WPG-develop/wpg ${PYPATH} && \
	touch $@
	@echo "Installed ${WPG}.\n"
