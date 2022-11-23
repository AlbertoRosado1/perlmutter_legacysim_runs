#!/bin/bash
#SBATCH -N 1
#SBATCH -C cpu
#SBATCH -q debug
#SBATCH -J injected_south_debug
#SBATCH --mail-user=ar652820@ohio.edu
#SBATCH --mail-type=ALL
#SBATCH -t 00:10:00
#SBATCH -L SCRATCH
#SBATCH --image=adematti/legacysim:DR9
#SBATCH --array=1-4

cd ${HOME}/perlmutter_legacysim_runs/Y1

echo $SLURM_ARRAY_TASK_ID
srun -n 1 shifter --volume ${HOME}:/homedir/ python preprocess_splitted_bricks.py --do injected --run south --index $SLURM_ARRAY_TASK_ID
