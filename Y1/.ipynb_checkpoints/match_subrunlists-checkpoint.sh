#!/bin/bash
# example 
# shifter --volume ${HOME}:/homedir/ --image=adematti/legacysim:DR9 /bin/bash
# bash match_subrunlists.sh north 3 500
run=$1               # region north or south
new_list_index=$2    # index that specifies the run iteration
number_job_arrays=$3 # number of job arrays submitted
subrunlist_dir=/global/homes/a/arosado/perlmutter_legacysim_runs/Y1/subrunlists/${run}

for((i=1; i<=$number_job_arrays; i++)); do {
    echo creating subrunlist${i}_${run}_${new_list_index}.txt
    python /src/legacysim/py/legacysim/scripts/check.py --outdir ${PSCRATCH}/legacysim/dr9/Y1/${run} --list ${subrunlist_dir}/subrunlist${i}_${run}_1.txt --write-list ${subrunlist_dir}/subrunlist${i}_${run}_${new_list_index}.txt
} done

python compute_completed_bricks.py --run $run --index $new_list_index --narrays $number_job_arrays --save True 