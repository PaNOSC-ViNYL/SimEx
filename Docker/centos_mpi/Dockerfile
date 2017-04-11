FROM centos:7
MAINTAINER Sergey Yakubov <sergey.yakubov@desy.de>

#
# An centos-based image with ssh,infiniband and openmpi installed. Allows passwordless ssh login for DOCKER_USER
#

# install ssh
RUN yum install -y openssh-clients openssh-server && ssh-keygen -A && \
	sed -i 's/required\(.*pam_loginuid\)/optional\1/' /etc/pam.d/sshd



# install infiniband
RUN yum install -y ibibverbs-utils libibverbs-devel libibverbs-devel-static libmlx4 \
 	libmlx5 ibutils libibcm libibcommon libibmad libibumad rdma  librdmacm-utils \
	librdmacm-devel librdmacm libibumad-devel perftest

# install mpi
RUN yum install -y wget make gcc-c++ gcc-gfortran
ADD openmpi_install.sh /opt/openmpi_install.sh
RUN ["bash", "/opt/openmpi_install.sh"]
#RUN yum install -y openmpi openmpi-devel make
#RUN echo "mtl = ^ofi" >> /etc/openmpi-x86_64/openmpi-mca-params.conf

ENV PATH=/usr/lib64/openmpi/bin:$PATH
ENV LD_LIBRARY_PATH=/usr/lib64/openmpi/lib:$LD_LIBRARY_PATH  
RUN echo "export PATH=/usr/lib64/openmpi/bin:${PATH}" > /etc/profile.d/scripts-path.sh && \
echo "export LD_LIBRARY_PATH=/usr/lib64/openmpi/lib:$LD_LIBRARY_PATH" >> /etc/profile.d/scripts-path.sh && \
chmod 755 /etc/profile.d/scripts-path.sh




