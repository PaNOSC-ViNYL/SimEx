
# create debian package

SET(CPACK_BINARY_DEB ON)
SET (CPACK_DEBIAN_PACKAGE_MAINTAINER "Sergey Yakubov (sergey.yakubov@desy.de)")
SET(CPACK_DEBIAN_PACKAGE_ARCHITECTURE "amd64")

SET(CPACK_PACKAGE_NAME "simex")
SET(CPACK_PACKAGE_VENDOR "XEFL")
SET(CPACK_PACKAGE_VERSION_MAJOR "0")
SET(CPACK_PACKAGE_VERSION_MINOR "2")
SET(CPACK_PACKAGE_VERSION_PATCH "0")

SET(CPACK_PACKAGE_DESCRIPTION_SUMMARY "SimEx Debian package")

#(>= 2.3.1-6), libgcc1 (>= 1:3.4.2-12)")
SET (PACKAGE_DEPENDS
"libarmadillo-dev"
"python2.7"
"python-numpy"
"python-scipy"
"python-h5py"
"python-setuptools"
"python-matplotlib"
"libbz2-dev"
"libgsl0-dev"
"libfftw3-dev"
"liblapack-dev"
"libhdf5-dev"
"libopenmpi-dev"
"ssh"
"libboost1.55-all-dev"
"python-biopython"
)

STRING(REGEX REPLACE ";" "," PACKAGE_DEPENDS "${PACKAGE_DEPENDS}")

SET(CPACK_DEBIAN_PACKAGE_DEPENDS ${PACKAGE_DEPENDS})


SET(CPACK_BINARY_STGZ OFF)
SET(CPACK_BINARY_TBZ2 OFF)
SET(CPACK_BINARY_TGZ OFF)
SET(CPACK_BINARY_TZ OFF)


INCLUDE(CPack)

