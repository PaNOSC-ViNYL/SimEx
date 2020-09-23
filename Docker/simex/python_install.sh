#!/usr/bin/env bash

#export myminiconda=Miniconda3-4.4.10-Linux-x86_64.sh
export myminiconda=Miniconda3-py37_4.8.3-Linux-x86_64.sh
URL=https://repo.continuum.io/miniconda/$myminiconda

# Install dir
PREFIX=/opt/miniconda

# Download Miniconda
wget -q $URL

# Extract packages

chmod +x $myminiconda
./$myminiconda -b -p $PREFIX
rm ./$myminiconda
cd $PREFIX

# config
export PATH=$PREFIX/bin:$PATH
conda config --set always_yes True

# pip cannot install pyqt
conda install --no-update-deps pyqt=5.9.2

# delete tests
find . -type d -name tests -depth -exec rm -rf {} \;
find . -type d -name test -depth -exec rm -rf {} \;

conda clean --tarballs

# install requirements from file (in given order)
#$PREFIX/bin/pip install -r /opt/requirements.txt
xargs -L 1 pip install < /opt/requirements.txt

# remove .pyc
find . -name \__pycache__ -depth -exec rm -rf {} \;
find . -name "*.pyc" -exec rm -rf {} \;


# remove cache
rm -r pkgs/*
rm -rf /root/.cache/pip


echo "export PATH=/opt/miniconda/bin:${PATH}" >> /etc/profile.d/scripts-path.sh

