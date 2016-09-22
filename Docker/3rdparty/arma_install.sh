URL=http://sourceforge.net/projects/arma/files/armadillo-6.600.4.tar.gz

wget -q $URL

tar -xf armadillo-6.600.4.tar.gz
cd armadillo-6.600.4 
./configure
make install

rm -rf armadillo-6.600.4.tar.gz armadillo-6.600.4


