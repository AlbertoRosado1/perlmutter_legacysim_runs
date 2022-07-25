#!/bin/bash
#SBATCH -q regular
#SBATCH -N 10
#SBATCH -t 8:00:00
#SBATCH -C haswell
#SBATCH -L SCRATCH,project
#SBATCH -J DA02_south_legacysim
srun -n 40 shifter --module=none --env=LD_LIBRARY_PATH='/global/common/software/nersc/cori-2022q1/sw/mpich-cle6/usr/lib/shifter/opt/mpich-7.7.3/lib64:/global/common/software/nersc/cori-2022q1/sw/mpich-cle6/usr/lib/shifter/opt/mpich-7.7.3/lib64/dep' --volume ${HOME}:/homedir/ --image=adematti/legacysim:DR9 ./mpi_runbricks.sh --run south
