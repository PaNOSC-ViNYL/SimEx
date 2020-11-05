# dsw@cloudbusting.io - Daniel Webster
FROM chuckie82/centos_env
LABEL maintainer="Chunhong Yoon <yoon82@stanford.edu>"

ADD requirements.txt /opt/requirements.txt
ADD python_install.sh /opt/python_install.sh
RUN yum remove -y cmake && yum install -y cmake3 hdf5-devel flex bison   && \
    yum clean all && rm -rf /var/cache/yum                               && \
    update-alternatives --install /usr/bin/cmake cmake /usr/bin/cmake3 3 && \
    /opt/python_install.sh
ENV PATH /opt/miniconda/bin:$PATH

ARG simex_script=simex_install.sh
ADD $simex_script /opt/simex_install.sh

RUN ["bash", "/opt/simex_install.sh"]

ENV MKLROOT=/opt/miniconda
ENV MKL_ROOT=/opt/miniconda
ENV PYPATH=/opt/miniconda
ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/miniconda/lib
ENV SIMEX_ROOT=/opt/SimEx-master
ENV PATH=$SIMEX_ROOT/bin:$PATH
ENV PYTHONPATH=$SIMEX_ROOT/Sources/python:$SIMEX_ROOT/lib/python3.7:$PYTHONPATH:/opt/SimEx-master/build/Modules/Others/sdf/sdf-prefix/src/sdf-build/lib/python3.7/site-packages/lib/python
ENV SIMEX_TESTS=$SIMEX_ROOT/Tests
ENV PYFAI_TESTIMAGES=/tmp

RUN useradd -m jovyan
