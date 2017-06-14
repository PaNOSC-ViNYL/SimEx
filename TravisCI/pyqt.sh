#!/usr/bin/env bash
# This hook is run after a new virtualenv is activated.

#set -e # abort after any errors
#set -u # exit after accessing an undefined variable

libs=(PyQt4 sip.so sip.x86_64-linux-gnu.so sipconfig.py)

python_version=python$(python -c "import sys; print (str(sys.version_info[0])+'.'+str(sys.version_info[1]))")
var=( $(which -a ${python_version}) )


get_python_lib_cmd="from distutils.sysconfig import get_python_lib; print (get_python_lib())"
lib_virtualenv_path=$(${var[0]} -c "${get_python_lib_cmd}")
lib_system_path=$(${var[-1]} -c "${get_python_lib_cmd}")

for lib in ${libs[@]}
do
 if [ -e "${lib_system_path}/${lib}" ]; then
    if [ ! -e "${lib_virtualenv_path}/${lib}" ]; then
        ln -s "${lib_system_path}/${lib}" "${lib_virtualenv_path}/${lib}"
    fi
 fi
done

