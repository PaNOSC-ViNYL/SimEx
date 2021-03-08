#! /bin/bash

function usage()
{
	cat <<EOF
usage: $0 MODE [conda_env_name]
	MODE includes:
	conda-env: create a conda virtual environment with the name of [conda_env_name].
                   default name: simex
	conda: install SimEx in current conda environment
	conda-develop: install SimEx in current conda environment with DEVELOPER_MODE=ON
	maxwell
	develop
note: modules can be (de)selected in the "CMake section" in this $0 file.
EOF
    exit
}

function conda_config()
{
    echo $MODE
    CONDA_BIN=`which conda`
    CONDA_BIN=${CONDA_BIN%/*}
    source ${CONDA_BIN%/*}/etc/profile.d/conda.sh
    INSTALL_PREFIX=$CONDA_PREFIX
    PYVERSION=`python -V | tr  '[:upper:]' '[:lower:]' | tr -d ' '`
    PYLIB=${PYVERSION%.*}
    XCSIT=OFF
    export HDF5_ROOT=$CONDA_PREFIX
    #export ZLIB_ROOT=$CONDA_PREFIX
    #export LD_LIBRARY_PATH=$CONDA_PREFIX/lib:$LD_LIBRARY_PATH
    # THIRD_PARTY_ROOT=/gpfs/exfel/data/group/spb-sfx/spb_simulation/simex
    # export PYTHONPATH=$CONDA_PREFIX/lib/$PYLIB:$CONDA_PREFIX/lib/$PYLIB/site-packages:$PYTHONPATH
    # echo "PYTHONPATH="$PYTHONPATH
    
}

HOSTNAME=`hostname`

if [ -z $1 ]; then
    usage
fi



MODE=$1
if [ $MODE = "maxwell" ]
then
    echo $MODE
    INSTALL_PREFIX=/data/netapp/s2e/simex
    DEVELOPER_MODE=OFF
    XCSIT=OFF
    git apply patch_for_maxwell
elif [ $MODE = "develop" ]
then
    echo $MODE
    INSTALL_PREFIX=..
    DEVELOPER_MODE=ON
    XCSIT=ON
    THIRD_PARTY_ROOT=/data/netapp/s2e/simex
elif [ $MODE = "conda-env" ]
# conda-env: create conda simex virtual environment
then
    echo $MODE
    if [ -z $2 ]; then
        INSTALL_CONDA_ENV=simex
    else
        INSTALL_CONDA_ENV=$2
    fi
    echo "Create conda environment $INSTALL_CONDA_ENV"
    CONDA_BIN=`which conda`
    CONDA_BIN=${CONDA_BIN%/*}
    source ${CONDA_BIN%/*}/etc/profile.d/conda.sh
    conda env create -n $INSTALL_CONDA_ENV -f environment.yml || {
        echo "[ERROR] conda environment was NOT deployed."
        exit 1
    }
    echo "conda environment was deployed. Please run the following to install SIMEX Platform:"
    echo ""
    echo " conda activate $INSTALL_CONDA_ENV"
    echo " $0 conda"
    exit 0
elif [ $MODE = "conda" ]
# conda: install SimEx in current conda environment
then
    conda_config
    DEVELOPER_MODE=OFF
elif [ $MODE = "conda-develop" ]
# conda-develop: install SimEx in current conda environment with DEVELOPER_MODE=ON
then
    conda_config
    DEVELOPER_MODE=ON
else
    usage
fi


# Check for existing build directory, remove if found
if [ -d build ]
then
    echo "Found build/ directory, will remove it now."
    rm -rvf build
fi

# Create new build dir and cd into it.
mkdir -v build
cd build
echo "Changed dir to $PWD."

# Uncomment the next line if you want to use Intel Fotran compiler
# (otherwise gfortran will be used). Make sure $MKLROOT is set. This can be achieved by
# $> source `which compilervars.sh` <arch>
# where <arch> is either intel64 or ia32
#export FC=ifort

# Some needed environment variables.
export BOOST_ROOT=${THIRD_PARTY_ROOT}
export Boost_NO_SYSTEM_PATHS=ON
export XERCESC_ROOT=${THIRD_PARTY_ROOT}
export GEANT4_ROOT=${THIRD_PARTY_ROOT}
export Geant4_DIR=${THIRD_PARTY_ROOT}/lib64/Geant4-10.4.0
export XCSIT_ROOT=${THIRD_PARTY_ROOT}

# CMake section to manage modules
cmake -DSRW_OPTIMIZED=ON \
      -DDEVELOPER_INSTALL=$DEVELOPER_MODE \
      -DCMAKE_INSTALL_PREFIX=$INSTALL_PREFIX \
      -DUSE_SingFELPhotonDiffractor=ON \
      -DUSE_CrystFELPhotonDiffractor=ON \
      -DUSE_GAPDPhotonDiffractor=OFF \
      -DUSE_sdf=ON \
      -DUSE_s2e=OFF \
      -DUSE_S2EReconstruction_EMC=ON \
      -DUSE_S2EReconstruction_DM=ON \
      -DUSE_wpg=ON \
      -DUSE_GenesisPhotonSource=OFF \
      -DXERCESC_ROOT=$XERCESC_ROOT \
      -DGEANT4_ROOT=$GEANT4_ROOT \
      -DXCSIT_ROOT=$XCSIT_ROOT \
      -DBOOST_ROOT=$BOOST_ROOT \
      ..
#     -DUSE_XCSITPhotonDetector=$XCSIT \ # requires GEANT
#     -DUSE_FEFFPhotonInteractor=ON \     # does not compile

# Build the project.
cmake --build . -- -j32 || exit 1

# Install the project.
cmake --build . --target install

# Back to root dir.
cd ..

# make and make install should be exec'ed not in this script (crystfel fails to compile).
#if [ $MODE = "conda" ] || [ $MODE = "conda-env " ]
#then
#echo "In case of error in compiling crystfel, rerun make in the build dir."
#fi

if [ $MODE = "develop" ] || [ $MODE = "conda-develop" ]; then
    echo "Please run 'source build/simex_vars.sh' before developing"
fi
