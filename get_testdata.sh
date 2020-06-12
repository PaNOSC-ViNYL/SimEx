#!/bin/sh

wget https://zenodo.org/record/3750541/files/simex_testdata?download=1 -O - | gunzip - > Tests/python/unittest/TestFiles.tar
cd  Tests/python/unittest
tar -xvf TestFiles.tar
rm -v TestFiles.tar 
wget https://github.com/PaNOSC-ViNYL/neutrontools/raw/master/Data/0010.sdf
wget https://github.com/PaNOSC-ViNYL/neutrontools/raw/master/Data/D_D_-_3He_n.txt
mv -v 0010.sdf D_D_-_3He_n.txt TestFiles
cd -
