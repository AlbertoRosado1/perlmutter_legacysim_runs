#!/bin/bash
#SBATCH -q regular
#SBATCH -N 128
#SBATCH -t 24:00:00
#SBATCH -C haswell
#SBATCH -L SCRATCH,project
#SBATCH -J Y1_north_legacysim
srun -n 512 shifter --module=mpich --volume ${HOME}:/homedir/ --image=adematti/legacysim:DR9 ./mpi_runbricks.sh --run north
#srun -n 5 shifter --volume ${HOME}:/homedir/ --image=adematti/legacysim:DR9 ./mpi_runbricks.sh --run north