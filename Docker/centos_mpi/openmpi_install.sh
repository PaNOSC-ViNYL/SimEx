VER=2.1.0
URL=http://www.open-mpi.de/software/ompi/v2.1/downloads/openmpi-$VER.tar.gz

wget -q $URL

tar -xf openmpi-$VER.tar.gz
cd openmpi-$VER
./configure --prefix=/usr/lib64/openmpi --disable-getpwuid --enable-orterun-prefix-by-default
make
make install
cd ..

rm -rf openmpi-$VER.tar.gz openmpi-$VER


