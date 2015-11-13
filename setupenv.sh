#!/bin/bash

export PATH=${PWD}/sw/bin:${PATH}
echo ${PATH}
export LD_LIBRARY_PATH=${PWD}/sw/lib:/opt/intel/mkl/lib/intel64:${LD_LIBRARY_PATH}
echo ${LD_LIBRARY_PATH}
