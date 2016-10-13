#!/bin/sh


#
# creates user, copies ssh keys, starts sshd
#

COMMAND="$DOCKER_USER"
if [ -n "$DOCKER_UID" ]; then
	COMMAND="$COMMAND -u $DOCKER_UID"
fi

if [ -n "$DOCKER_GID" ]; then
	groupadd -g $DOCKER_GID $DOCKER_GID
	COMMAND="$COMMAND -g $DOCKER_GID"
fi

useradd $COMMAND
mkdir /home/${DOCKER_USER}/.ssh
cp /root/id_rsa* /home/${DOCKER_USER}/.ssh
mv /home/${DOCKER_USER}/.ssh/id_rsa.pub /home/${DOCKER_USER}/.ssh/authorized_keys
chown -R ${DOCKER_USER}:${DOCKER_GID} /home/${DOCKER_USER}/.ssh
chmod 600 /home/${DOCKER_USER}/.ssh/id_rsa 
chmod 700  /home/${DOCKER_USER}/.ssh
chmod 600 /home/${DOCKER_USER}/.ssh/authorized_keys

chown root:root /var/empty/sshd
chmod 711 /var/empty/sshd
/usr/sbin/sshd -D

                                                                                                                                          
                                                            
