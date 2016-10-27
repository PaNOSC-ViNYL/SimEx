FROM centos:7
MAINTAINER Sergey Yakubov <sergey.yakubov@desy.de>

#
# An centos-based image with ssh,infiniband and openmpi installed. Allows passwordless ssh login for DOCKER_USER
#

# install ssh
RUN yum install -y openssh-clients openssh-server && ssh-keygen -A && \
	sed -i 's/required\(.*pam_loginuid\)/optional\1/' /etc/pam.d/sshd && \
	echo StrictHostKeyChecking no >> /etc/ssh/ssh_config && \
	ssh-keygen -f /root/id_rsa -t rsa -N ''



# install infiniband
RUN yum install -y ibibverbs-utils libibverbs-devel libibverbs-devel-static libmlx4 \
 	libmlx5 ibutils libibcm libibcommon libibmad libibumad rdma  librdmacm-utils \
	librdmacm-devel librdmacm libibumad-devel perftest

# install mpi
RUN yum install -y openmpi openmpi-devel make
ENV PATH=/usr/lib64/openmpi/bin:$PATH
ENV LD_LIBRARY_PATH=/usr/lib64/openmpi/lib:$LD_LIBRARY_PATH  
RUN echo "export PATH=/usr/lib64/openmpi/bin:${PATH}" > /etc/profile.d/scripts-path.sh && \
echo "export LD_LIBRARY_PATH=/usr/lib64/openmpi/lib:$LD_LIBRARY_PATH" >> /etc/profile.d/scripts-path.sh && \
chmod 755 /etc/profile.d/scripts-path.sh


COPY docker-entrypoint.sh /bin/docker-entrypoint.sh
ENV DOCKER_USER=dockeruser

# set entry point
ENTRYPOINT ["/bin/docker-entrypoint.sh"]



