FROM yakser/centos_mpi
MAINTAINER Sergey Yakubov <sergey.yakubov@desy.de>

RUN yum install -y epel-release
RUN yum install -y gcc-gfortran bash bzip2 zlib wget cmake fftw fftw-devel file which patch unzip gsl-devel blas-devel lapack-devel gcc-c++ hdf5-devel git && yum clean all

ADD requirements.txt /opt/requirements.txt
ADD python_install.sh /opt/python_install.sh
RUN ["bash", "/opt/python_install.sh"]
ENV PATH /opt/miniconda/bin:$PATH

ARG simex_script=simex_install.sh
ADD $simex_script /opt/simex_install.sh

RUN echo "### Start bash /opt/simex_install.sh"

RUN ["bash", "/opt/simex_install.sh"]

RUN echo "### Done bash /opt/simex_install.sh"

ENV SIMEX_ROOT=/opt/simex_platform
ENV PATH=$SIMEX_ROOT/bin:$PATH
ENV PYTHONPATH=$SIMEX_ROOT/Sources/python:$SIMEX_ROOT/lib/python3.6:$PYTHONPATH
ENV SIMEX_TESTS=$SIMEX_ROOT/Tests
ENV PYFAI_TESTIMAGES=/tmp

#ENTRYPOINT ["python"]
