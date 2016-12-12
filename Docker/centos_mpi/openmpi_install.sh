URL=http://www.open-mpi.de/software/ompi/v2.0/downloads/openmpi-2.0.1.tar.gz

wget -q $URL

tar -xf openmpi-2.0.1.tar.gz
cd openmpi-2.0.1
./configure --prefix=/usr/lib64/openmpi --disable-getpwuid
make
make install
cd ..

rm -rf openmpi-2.0.1.tar.gz openmpi-2.0.1


