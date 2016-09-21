FROM max-adm01:5000/centos_mpi
MAINTAINER Sergey Yakubov <sergey.yakubov@desy.de>

RUN yum install -y epel-release bash bzip2 zlib wget cmake fftw fftw-devel file which patch unzip gsl-devel blas-devel lapack-devel gcc-c++ git && yum clean all

ADD python_install.sh /opt/python_install.sh
RUN ["bash", "/opt/python_install.sh"]
ENV PATH /opt/miniconda2/bin:$PATH

ADD arma_install.sh /opt/arma_install.sh
RUN ["bash", "/opt/arma_install.sh"]

ADD boot_install.sh /opt/boot_install.sh
RUN ["bash", "/opt/boot_install.sh"]

ARG simex_script=simex_install.sh
ADD $simex_script /opt/simex_install.sh
RUN ["bash", "/opt/simex_install.sh"]
ENV SIMEX_ROOT=/opt/simex_platform
ENV PATH=$SIMEX_ROOT/bin:$PATH
ENV PYTHONPATH=$SIMEX_ROOT/Sources/python:$SIMEX_ROOT/lib/python2.7:$PYTHONPATH
ENV SIMEX_TESTS=$SIMEX_ROOT/Tests
RUN echo "source /opt/simex_platform/bin/simex_vars.sh" > /etc/profile.d/scripts-simex.sh && \
chmod 755 /etc/profile.d/scripts-simex.sh
