#!/bin/bash
# Set up the legacypipe environment

# add here legacysim to python path if necessary
#export PYTHONPATH=$HOME/legacysim/py:$PYTHONPATH

# set number of OpenMP threads here
export OMP_NUM_THREADS=16
#export OMP_PLACES=threads # AJRM
#export OMP_PROC_BIND=true # AJRM
source ./legacypipe-env.sh
#chmod u+x ./runbrick.sh

python mpi_main_runbricks_subrunlist.py "$@"

# NERSC / Cray / Cori / Cori KNL things
#export KMP_AFFINITY=disabled
#export MPICH_GNI_FORK_MODE=FULLCOPY
#export MKL_NUM_THREADS=1
#export OMP_NUM_THREADS=1
