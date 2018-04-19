FROM chuckie82/centos_env
MAINTAINER Chunhong Yoon <yoon82@stanford.edu>

ADD requirements.txt /opt/requirements.txt
ADD python_install.sh /opt/python_install.sh
RUN ["bash", "/opt/python_install.sh"]
ENV PATH /opt/miniconda/bin:$PATH

ARG simex_script=simex_install.sh
ADD $simex_script /opt/simex_install.sh

RUN ["bash", "/opt/simex_install.sh"]

ENV SIMEX_ROOT=/opt/simex_platform
ENV PATH=$SIMEX_ROOT/bin:$PATH
ENV PYTHONPATH=$SIMEX_ROOT/Sources/python:$SIMEX_ROOT/lib/python3.6:$PYTHONPATH
ENV SIMEX_TESTS=$SIMEX_ROOT/Tests
ENV PYFAI_TESTIMAGES=/tmp

