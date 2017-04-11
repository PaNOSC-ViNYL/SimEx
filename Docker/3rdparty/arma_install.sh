URL=http://sourceforge.net/projects/arma/files/armadillo-7.800.2.tar.xz

wget -q $URL

tar -xf armadillo-7.800.2.tar.xz
cd armadillo-7.800.2 
./configure
make install
cd ..
rm -rf armadillo-7.800.2.tar.gz armadillo-7.800.2


