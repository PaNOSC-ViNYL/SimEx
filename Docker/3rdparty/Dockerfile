FROM yakser/centos_mpi
MAINTAINER Sergey Yakubov <sergey.yakubov@desy.de>

RUN yum install -y epel-release gfortran bash bzip2 zlib wget cmake fftw fftw-devel file which patch unzip gsl-devel blas-devel lapack-devel gcc-c++ git && yum clean all

ADD python_install.sh /opt/python_install.sh
RUN ["bash", "/opt/python_install.sh"]
ENV PATH /opt/miniconda2/bin:$PATH

ADD arma_install.sh /opt/arma_install.sh
RUN ["bash", "/opt/arma_install.sh"]

ADD boot_install.sh /opt/boot_install.sh
RUN ["bash", "/opt/boot_install.sh"]

