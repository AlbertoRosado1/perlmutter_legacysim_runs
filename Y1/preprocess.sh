#!/bin/bash
# EXAMPLE bash preprocess.sh south 1 4
run=$1 # [north or south]
start_idx=$2
end_idx=$3 

cd ${HOME}/perlmutter_legacysim_runs/Y1
source legacypipe-env.sh

for (( VARIABLE=$start_idx; VARIABLE<=$end_idx; VARIABLE++ )) do {
    sleep 3
    index=$VARIABLE
    echo running $VARIABLE of $end_idx
    srun -N 1 -n 1 shifter --volume ${HOME}:/homedir/ --image=adematti/legacysim:DR9 python preprocess_splitted_bricks.py --do injected --run $run --index $index
    
} & done
wait
