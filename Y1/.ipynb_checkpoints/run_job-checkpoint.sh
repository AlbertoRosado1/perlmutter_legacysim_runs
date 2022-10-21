#!/bin/bash
#SBATCH -q regular
#SBATCH -N 128
#SBATCH -t 24:00:00
#SBATCH -C haswell
#SBATCH -L SCRATCH,project
#SBATCH -J Y1_north_legacysim
srun -n 512 shifter --module=none --env=LD_LIBRARY_PATH='/global/common/software/nersc/cori-2022q1/sw/mpich-cle6/usr/lib/shifter/opt/mpich-7.7.3/lib64:/global/common/software/nersc/cori-2022q1/sw/mpich-cle6/usr/lib/shifter/opt/mpich-7.7.3/lib64/dep' --volume ${HOME}:/homedir/ --image=adematti/legacysim:DR9 ./mpi_runbricks.sh --run north
