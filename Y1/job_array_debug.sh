#!/bin/bash
#SBATCH -N 1
#SBATCH -C cpu
#SBATCH -q debug
#SBATCH -J Y1north_debug
#SBATCH --mail-user=ar652820@ohio.edu
#SBATCH --mail-type=ALL
#SBATCH -t 00:10:00
#SBATCH -L SCRATCH
#SBATCH -o slurm_outputs/north/subrunlist%a_north_3_%J.out
#SBATCH -e slurm_outputs/north/subrunlist%a_north_3_%J.err
#SBATCH --image=adematti/legacysim:DR9
#SBATCH --array=1-4

echo $SLURM_ARRAY_TASK_ID
srun -n 17 --mpi=pmi2 shifter --module=none --volume ${HOME}:/homedir/ ./mpi_runbricks_subrunlist.sh --run north --index $SLURM_ARRAY_TASK_ID
