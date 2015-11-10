###################
#     WPG/SRW     #
###################
#include ${ROOT_DIR}/packages/environment.mk

WPG=wpg
WPG_DIR=${PACKAGES}/WPG-develop
WPG_SRC_DIR=${SRC}/WPG-develop

wpg: ${WPG_SRC_DIR}/install.stamp

${PACKAGES}/wpg_package.stamp:
	${call header2start,"Fetching ${WPG}."}
	cd ${PACKAGES} && \
	wget http://github.com/samoylv/WPG/archive/develop.zip -O wpg-develop.zip && \
	wget https://github.com/samoylv/prop/archive/develop.zip -O prop-develop.zip && \
	touch $@
	${call header2end,"Fetched ${WPG}."}

${WPG_SRC_DIR}/unpack.stamp: ${PACKAGES}/wpg_package.stamp
	${call header2start,"Unpacking ${WPG}."}
	cd ${SRC} && \
	unzip -o ${PACKAGES}/wpg-develop.zip && \
	unzip -o ${PACKAGES}/prop-develop.zip && \
	touch $@
	${call header2end,"Unpacked ${WPG}."}

${WPG_SRC_DIR}/patch.stamp: ${WPG_SRC_DIR}/unpack.stamp
	${call header2start,"Patching ${WPG}."}
	cd ${SRC}/prop-develop && \
	patch propagateSE.py ${PATCHES}/wpg/propagateSE.py.patch && \
	patch diagnostics.py ${PATCHES}/wpg/diagnostics.py.patch && \
	touch $@
	${call header2end,"Patched ${WPG}."}

${WPG_SRC_DIR}/build.stamp: ${WPG_SRC_DIR}/patch.stamp
	${call header2start,"Building ${WPG}."}
	cd ${SRC}/WPG-develop && make all
	touch $@
	${call header2end,"Built ${WPG}."}

${WPG_SRC_DIR}/install.stamp: ${WPG_SRC_DIR}/build.stamp
	${call header2start,"Building ${WPG}."}
	cd ${SRC} && \
	cp -r prop-develop ${PYTHON_LIBDIR}/prop && \
	cp -r WPG-develop/wpg ${PYTHON_LIBDIR} && \
	touch $@
	${call header2end,"Installed ${WPG}."}
