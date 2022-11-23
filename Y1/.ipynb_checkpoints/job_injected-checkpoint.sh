#!/bin/bash
#SBATCH -N 1
#SBATCH -C cpu
#SBATCH -q regular
#SBATCH -J injected_south
#SBATCH --mail-user=ar652820@ohio.edu
#SBATCH --mail-type=ALL
#SBATCH -t 04:00:00
#SBATCH -L SCRATCH
#SBATCH --image=adematti/legacysim:DR9
#SBATCH --array=1-4

cd ${HOME}/perlmutter_legacysim_runs/Y1
source legacypipe-env.sh

echo $SLURM_ARRAY_TASK_ID
srun -n 1 shifter --volume ${HOME}:/homedir/ python preprocess_splitted_bricks.py --do injected --run south --index $SLURM_ARRAY_TASK_ID
