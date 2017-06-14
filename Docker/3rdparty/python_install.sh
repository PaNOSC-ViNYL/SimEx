#!/usr/bin/env bash

URL=http://repo.continuum.io/miniconda/Miniconda2-4.0.5-Linux-x86_64.sh


# Install dir
PREFIX=/opt/miniconda2


# Download Miniconda
wget -q $URL

# Extract packages

chmod +x Miniconda2-4.0.5-Linux-x86_64.sh
./Miniconda2-4.0.5-Linux-x86_64.sh -b -p $PREFIX
rm ./Miniconda2-4.0.5-Linux-x86_64.sh
cd $PREFIX

# config
export PATH=$PREFIX/bin:$PATH
conda config --set always_yes True

# pip cannot install pyqt
conda install --no-update-deps pyqt=4

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


echo "export PATH=/opt/miniconda2/bin:${PATH}" >> /etc/profile.d/scripts-path.sh
