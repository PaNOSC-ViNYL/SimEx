URL=http://repo.continuum.io/miniconda/Miniconda2-4.0.5-Linux-x86_64.sh
#URL=http://repo.continuum.io/miniconda/Miniconda-3.8.3-Linux-x86_64.sh

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

conda install --no-deps nomkl numpy Cython matplotlib six scipy dateutil pyparsing cycler openblas libpng
conda install --no-deps libgfortran=1 
conda install --no-deps -c anaconda biopython=1.67
conda  install --no-update-deps pyqt
$PREFIX/bin/pip install periodictable mpi4py dill
#yum install -y hdf5-devel
## clean to reduce image size

# delete tests
find . -type d -name tests -depth -exec rm -rf {} \;
find . -type d -name test -depth -exec rm -rf {} \;

conda install --no-deps hdf5 h5py # after cleaning tests
#conda install --no-deps  h5py=2.3.1
#conda install --no-deps  hdf5

conda clean --tarballs


# remove .pyc
find . -name \__pycache__ -depth -exec rm -rf {} \;
find . -name "*.pyc" -exec rm -rf {} \;



# remove pkgs cache
rm -r pkgs/*

echo "export PATH=/opt/miniconda2/bin:${PATH}" >> /etc/profile.d/scripts-path.sh
