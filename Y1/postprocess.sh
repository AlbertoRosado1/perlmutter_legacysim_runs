#!/bin/bash
# EXAMPLE bash postprocess.sh north 1 4
run=$1 # [north or south]
start_idx=$2
end_idx=$3 

VOLUME=${HOME}:/homedir/
CAT_DIR=${PSCRATCH}/legacysim/dr9/Y1/$run/file0_rs0_skip0/merged
OUT_DIR=${PSCRATCH}/legacysim/dr9/Y1/$run

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
    BRICK_FN=global/homes/a/arosado/perlmutter_legacysim_runs/Y1/splitted_bricklists/bricklist_"$run"_"$index".txt
    echo using $BRICK_FN for match.py
    srun -N 1 -n 1 shifter --volume $VOLUME --image=adematti/legacysim:DR9 python /src/legacysim/py/legacysim/scripts/match.py --cat-dir $CAT_DIR --outdir $OUT_DIR --cat-fn $CAT_FN --brick $BRICK_FN --plot-hist plots/hist_"$run"_"$index".png &
    
done
wait
