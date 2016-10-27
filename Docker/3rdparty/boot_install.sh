URL=http://downloads.sourceforge.net/project/boost/boost/1.60.0/boost_1_60_0.tar.gz

export PATH=/opt/miniconda2/bin:$PATH

wget $URL
tar xfv boost_1_60_0.tar.gz 
cd boost_1_60_0 
./bootstrap.sh --prefix=/opt/boost/
echo "using mpi ;">>project-config.jam
./b2 install

cd ..


rm -rf boost_1_60_0.tar.gz boost_1_60_0


