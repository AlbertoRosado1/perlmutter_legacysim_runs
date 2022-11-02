#!/bin/bash
#SBATCH -N 1
#SBATCH -C cpu
#SBATCH -q regular
#SBATCH -J Y1south_legacysim
#SBATCH --mail-user=ar652820@ohio.edu
#SBATCH --mail-type=ALL
#SBATCH -t 01:00:00
#SBATCH -L SCRATCH
#SBATCH -o slurm_outputs/south/subrunlist%a_south_1_%A.out
#SBATCH -e slurm_outputs/south/subrunlist%a_south_1_%A.err
#SBATCH --image=adematti/legacysim:DR9
#SBATCH --array=1-1517

echo $SLURM_ARRAY_TASK_ID
srun -n 17 --mpi=pmi2 shifter --module=none --volume ${HOME}:/homedir/ ./mpi_runbricks_subrunlist.sh --run south --index $SLURM_ARRAY_TASK_ID

