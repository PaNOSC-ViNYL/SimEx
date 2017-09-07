FROM yakser/centos_mpi
MAINTAINER Sergey Yakubov <sergey.yakubov@desy.de>


RUN yum install -y epel-release
RUN yum install -y gcc-gfortran bash bzip2 zlib wget cmake fftw fftw-devel file which patch unzip gsl-devel blas-devel lapack-devel gcc-c++ hdf5-devel git && yum clean all

ADD requirements.txt /opt/requirements.txt
ADD python_install.sh /opt/python_install.sh
RUN ["bash", "/opt/python_install.sh"]
ENV PATH /opt/miniconda2/bin:$PATH

