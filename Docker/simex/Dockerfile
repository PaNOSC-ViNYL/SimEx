# dsw@cloudbusting.io - Daniel Webster
FROM chuckie82/centos_env
LABEL maintainer="Carsten Fortmann-Grote carsten.grote@xfel.eu github:CFGrote dockerhub:cfgrote"

ADD requirements.txt /opt/requirements.txt
ADD python_install.sh /opt/python_install.sh
RUN yum remove -y cmake && yum install -y cmake3 hdf5-devel flex sudo  bison git   && \
    yum clean all && rm -rf /var/cache/yum                               && \
    update-alternatives --install /usr/bin/cmake cmake /usr/bin/cmake3 3
 
RUN ["chmod", "a+x", "/opt/python_install.sh"]
RUN "/opt/python_install.sh"
ENV PATH /opt/miniconda/bin:$PATH

ARG simex_script=simex_install.sh
ADD $simex_script /opt/simex_install.sh

RUN ["sudo", "bash", "/opt/simex_install.sh"]

ENV MKLROOT=/opt/miniconda
ENV MKL_ROOT=/opt/miniconda
ENV PYPATH=/opt/miniconda
ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/miniconda/lib
ENV SIMEX_ROOT=/opt/SimEx-master
ENV PATH=$SIMEX_ROOT/bin:$PATH
ENV PYTHONPATH=$SIMEX_ROOT/Sources/python:$SIMEX_ROOT/lib/python3.7:$PYTHONPATH:/opt/SimEx-master/build/Modules/Others/sdf/sdf-prefix/src/sdf-build/lib/python3.7/site-packages/lib/python
ENV SIMEX_TESTS=$SIMEX_ROOT/Tests
ENV PYFAI_TESTIMAGES=/tmp

RUN ["pip3", "install", "jupyter"]

RUN useradd -m jovyan

RUN ["git", "clone", "--depth", "1", "https://github.com/PaNOSC-ViNYL/SimEx-notebooks.git", "/home/jovyan/simex_notebooks"]

WORKDIR /home/jovyan/simex_notebooks

CMD ["jupyter", "notebook", "--port=24306", "--no-browser", "--ip=0.0.0.0", "--allow-root"]


