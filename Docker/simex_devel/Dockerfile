FROM yakser/simex_3rdparty
MAINTAINER Sergey Yakubov <sergey.yakubov@desy.de>

ARG simex_script=simex_install_devel.sh
ADD $simex_script /opt/simex_install.sh
RUN ["bash", "/opt/simex_install.sh"]
ENV SIMEX_ROOT=/opt/simex_platform
ENV PATH=$SIMEX_ROOT/bin:$PATH
ENV PYTHONPATH=$SIMEX_ROOT/Sources/python:$SIMEX_ROOT/lib/python2.7:$PYTHONPATH
ENV SIMEX_TESTS=$SIMEX_ROOT/Tests
ENV PYFAI_TESTIMAGES=/tmp
ENTRYPOINT ["python"]
