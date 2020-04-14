#!/bin/sh

wget https://zenodo.org/record/3750541/files/simex_testdata?download=1 -O - | gunzip - > Tests/python/unittest/TestFiles.tar
cd  Tests/python/unittest
tar -xvf TestFiles.tar
rm -v TestFiles.tar 
cd -
