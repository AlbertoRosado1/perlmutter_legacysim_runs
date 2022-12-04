#!/bin/bash
# Set up the legacypipe environment

# set number of OpenMP threads here
export OMP_NUM_THREADS=16 # AJRM changed 10 to 16
source ./legacypipe-env.sh

python mpi_main_runbricks.py "$@"
