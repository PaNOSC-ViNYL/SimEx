#!/usr/bin/env bash
containername="cloudbusting/simex"
J_PORT=8897
TRASIT_HOST=max-exfl-display.desy.de
HOST_PATH=/gpfs/exfel/data/user/
MOUNT_PATH=/home/xfeluser
JUPYTER_START_PATH=/home/xfeluser/juncheng

# To forward to external host
DISPHOST=`dig +short $TRASIT_HOST |head -1`
DISPHOST=${DISPHOST%.}
echo "Transit host: " $DISPHOST
ssh -f -N -T -R  ${J_PORT}:localhost:$J_PORT $DISPHOST  & 

docker run -v  ${HOST_PATH}:${MOUNT_PATH} -e HOME=${JUPYTER_START_PATH}  -u `id -u`:`id -g` --userns=host --security-opt no-new-privileges -ti -e JUPYTER_RUNTIME_DIR=/tmp  -p ${J_PORT}:${J_PORT} $containername jupyter notebook --no-browser --ip 0.0.0.0 --port ${J_PORT} ${JUPYTER_START_PATH}
