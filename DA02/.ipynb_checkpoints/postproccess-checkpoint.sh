#!/bin/bash
# EXAMPLE bash postproccess_test.sh north 0 13
run=$1 # [north or south]
start_idx=$2
end_idx=$3 

VOLUME=${HOME}:/homedir/
CAT_DIR=${CSCRATCH}/legacysim/dr9/DA02/$run/file0_rs0_skip0/merged
OUT_DIR=${CSCRATCH}/legacysim/dr9/DA02/$run

for (( VARIABLE=$start_idx; VARIABLE<=$end_idx; VARIABLE++ ))
do  
    if [ "$VARIABLE" -lt "10" ]
    then 
        index="0$VARIABLE"
    else
        index="$VARIABLE"
    fi 
    echo running $VARIABLE of $end_idx
    CAT_FN=$CAT_DIR/matched_inputs_$index.fits
    BRICK_FN=/global/homes/a/arosado/legacysim_runs/DA02/splitted_bricklists/bricklist_"$run"_"$index" 
    echo using $BRICK_FN for match.py
    srun -N 1 -n 1 -c 64 shifter --volume $VOLUME --image=adematti/legacysim:DR9 python /src/legacysim/py/legacysim/scripts/match.py --cat-dir $CAT_DIR --outdir $OUT_DIR --cat-fn $CAT_FN --brick $BRICK_FN --plot-hist plots/hist_"$run"_"$index".png &
    
done

wait

# srun -N 1 -n 1 -c 64 shifter --volume ${HOME}:/homedir/ --image=adematti/legacysim:DR9 python /src/legacysim/py/legacysim/scripts/match.py --cat-dir ${CSCRATCH}/legacysim/dr9/DA02/south/file0_rs0_skip0/merged --outdir ${CSCRATCH}/legacysim/dr9/DA02/south --cat-fn ${CSCRATCH}/legacysim/dr9/DA02/south/file0_rs0_skip0/merged/matched_inputs_20.fits --brick /global/homes/a/arosado/legacysim_runs/DA02/splitted_bricklists/bricklist_south_20 --plot-hist plots/hist_south_20.png