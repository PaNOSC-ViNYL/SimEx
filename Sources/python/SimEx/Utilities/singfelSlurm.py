"""Singfel slurm generator"""

import os
import shutil
import subprocess
from pathlib import Path


class singfelSlurm:
    def __init__(self,
                 job_name,
                 in_dir,
                 mpi_command,
                 slurm_path='./',
                 slurm_file='submit.slurm',
                 is_cleanup=False,
                 out_dir='diffr',
                 nodes=1,
                 time='1-01:00:00',
                 log_out='log.diffr-%j',
                 conda_path='/gpfs/exfel/data/user/juncheng/miniconda3',
                 scratch='/gpfs/exfel/data/scratch/juncheng'):

        self.slurm_path = slurm_path
        self.slurm_file = slurm_file
        self.out_dir = out_dir
        self.is_cleanup = is_cleanup
        conda_active = os.path.join(conda_path, 'bin/activate')
        Path(self.slurm_path).mkdir(parents=True, exist_ok=True)

        self.__script = f"""\
#!/bin/bash
#SBATCH --job-name={job_name}
#SBATCH --partition=exfel
#SBATCH --nodes={nodes}
#SBATCH --time={time}
#SBATCH --output={log_out}

export LD_PRELOAD=""                 # necessary on max-display nodes, harmless on others
source /etc/profile.d/modules.sh

module load maxwell openmpi/3.1.6
source  {conda_active} pysingfel0.3-mpi

# Print python environment
which python
module list

export UCX_LOG_LEVEL=error

# Set SCRATCH data path for fast data writting
DATADIR=./
SCRATCH={scratch}
SPATH=$SCRATCH/$SLURM_JOB_NAME.$SLURM_JOB_ID
echo SCRATCH_PATH=$SPATH

# Show nodes hostnames
mpirun --map-by node -np $SLURM_JOB_NUM_NODES  hostname

IN_DIR={in_dir}
OUT_DIR={out_dir}

mkdir -p $SPATH/$OUT_DIR
MCA=' --mca btl_openib_warn_no_device_params_found 0 --mca pml ucx --mca mpi_cuda_support 0 '
{mpi_command}
cp -r $SPATH/$OUT_DIR $DATADIR

err=$?
if  [ $err != 0 ]
then
    echo Copy is not successful, please check $SPATH
else
    python /gpfs/exfel/data/user/juncheng/hydratedProject/src/program/externalLink.py $OUT_DIR
    rm -rf $SPATH
fi
"""

    @property
    def script(self):
        return self.__script

    def submit(self):
        self.writeScript()
        wd = os.getcwd()
        os.chdir(self.slurm_path)
        is_exist = checkExist(self.out_dir)
        if is_exist:
            if self.is_cleanup:
                cleanUp(self.out_dir)
                print("Delete up above files...done")
            else:
                print("Above files will not be cleaned.")
                print("If you wish to clean them, please set is_cleanup=True")

        cmd_line = ['sbatch', self.slurm_file]
        # cmd_line = ['ls','.']
        print(*cmd_line)
        try:
            df = subprocess.Popen(cmd_line,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)
            output, err = df.communicate()
            print(output.decode('ascii'))
            if err:
                print(err.decode('ascii'))
        except subprocess.CalledProcessError as e:
            print(e.message)
        os.chdir(wd)

    def writeScript(self, new_name=None):
        if new_name:
            write_file = new_name
        else:
            write_file = os.path.join(self.slurm_path, self.slurm_file)
        print('Write to', write_file)
        with open(write_file, 'w') as f:
            f.write(self.script)


def getSingfelCommand(uniform_rotation=None,
                      back_rotation=None,
                      number_of_diffraction_patterns=1,
                      calculate_Compton=0,
                      orientation=None):
    MPI_command = f"""\
mpirun $MCA --map-by node --bind-to none -x OMP_NUM_THREADS=1 radiationDamageMPI \\
    --inputDir $IN_DIR  \\
    --outputDir $SPATH/$OUT_DIR  \\
    --geomFile ../tmp.geom   \\
    --configFile /dev/null     \\
    --sliceInterval 10   \\
    --numSlices 100   \\
    --pmiStartID 1   \\
    --pmiEndID 1000   \\
"""
    MPI_command += '--numDP {} '.format(number_of_diffraction_patterns)
    MPI_command += '--calculateCompton {} '.format(calculate_Compton)
    if uniform_rotation is not None:
        MPI_command += '--uniformRotation {} '.format(uniform_rotation)
    if back_rotation is not None:
        MPI_command += '--backRotation {} '.format(back_rotation)
    if orientation is not None:
        if isinstance(orientation, (list, tuple)) and len(orientation) == 4:
            MPI_command += '--orientation {} '.format(orientation)
        else:
            raise TypeError(
                "Orientation needs to be a 4-element list of a quaternion")
    return MPI_command


def checkExist(out_path):
    dir_to_remove = out_path
    file_to_remove = out_path + '.h5'

    is_exist = os.path.exists(dir_to_remove) or os.path.exists(file_to_remove)

    if is_exist:
        print(dir_to_remove, 'exists:', str(os.path.exists(dir_to_remove)))
        print(file_to_remove, 'exists:', str(os.path.exists(file_to_remove)))
    return is_exist


def cleanUp(out_path):
    dir_to_remove = out_path
    file_to_remove = out_path + '.h5'

    if os.path.isdir(dir_to_remove):
        shutil.rmtree(dir_to_remove)
    if os.path.isfile(file_to_remove):
        os.remove(file_to_remove)
