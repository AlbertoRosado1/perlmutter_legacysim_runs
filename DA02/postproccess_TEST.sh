#!/bin/bash
# EXAMPLE bash postproccess_test.sh north 0 13
run=$1 # [north or south]
start_idx=$2
end_idx=$3 

VOLUME=${HOME}:/homedir/
CAT_DIR=${CSCRATCH}/legacysim/dr9/DA02/$run/file0_rs0_skip0/merged
OUT_DIR=${CSCRATCH}/legacysim/dr9/DA02/$run

#for VARIABLE in {$start_idx..29} #{$start_idx..$end_idx}
for (( VARIABLE=$start_idx; VARIABLE<=$end_idx; VARIABLE++ ))
do
    echo running $VARIABLE of $end_idx
    
    if [ "$VARIABLE" -lt "10" ]
    then 
        index="0$VARIABLE"
    else
        index="$VARIABLE"
    fi 
    
    CAT_FN=$CAT_DIR/matched_inputs_$index.fits
    BRICK_FN=/global/homes/a/arosado/legacysim_runs/DA02/splitted_bricklists/bricklist_"$run"_$index 
    srun -N 1 -n 1 -c 64 shifter --volume $VOLUME --image=adematti/legacysim:DR9 python /src/legacysim/py/legacysim/scripts/match.py --cat-dir $CAT_DIR --outdir $OUT_DIR --cat-fn $CAT_FN --brick $BRICK_FN --plot-hist plots/hist_"$run"_$index.png &
    
done

wait
: '
usage: match.py [-h] [--injected INJECTED] [--tractor TRACTOR] [--tractor-legacypipe [TRACTOR_LEGACYPIPE]] [--radius RADIUS] [--base BASE] [--cat-dir CAT_DIR] [--cat-fn CAT_FN]
                [--plot-hist [PLOT_HIST]] [--plot-scatter [PLOT_SCATTER]] [--plot-fields [PLOT_FIELDS [PLOT_FIELDS ...]]] [-d OUTPUT_DIR] [--fileid [FILEID [FILEID ...]]]
                [--rowstart [ROWSTART [ROWSTART ...]]] [--skipid [SKIPID [SKIPID ...]]] [--brick [BRICK [BRICK ...]]] [--list [LIST [LIST ...]]]

Match input to output catalogs.

optional arguments:
  -h, --help            show this help message and exit
  --injected INJECTED   File name of merged injected sources (default: None)
  --tractor TRACTOR     File name of merged Tractor catalog (default: None)
  --tractor-legacypipe [TRACTOR_LEGACYPIPE]
                        Add legacypipe fitted sources to the random injected sources for the matching with legacysim Tractor catalogs. Load legacypipe fitted sources from legacypipe directory
                        or file name if provided. (default: False)
  --radius RADIUS       Matching radius in arcseconds (default: 1.5)
  --base BASE           Catalog to be used as base for merging (default: input)
  --cat-dir CAT_DIR     Directory for matched catalog (default: .)
  --cat-fn CAT_FN       Output file name. If not provided, defaults to cat-dir/matched_%(base)s.fits (default: None)
  --plot-hist [PLOT_HIST]
                        Plot histograms of difference (output-input) and residuals. If no file name provided, defaults to cat-dir + hist_output_input.png (default: False)
  --plot-scatter [PLOT_SCATTER]
                        Scatter plot difference (output-input). If no filename provided, defaults to cat-dir/scatter_output_input.png (default: False)
  --plot-fields [PLOT_FIELDS [PLOT_FIELDS ...]]
                        Fields to plot (default: ['ra', 'dec', 'flux_g', 'flux_r', 'flux_z'])
  -d OUTPUT_DIR, --outdir OUTPUT_DIR
                        Output base directory, default "." (default: .)
  --fileid [FILEID [FILEID ...]]
                        Use these fileids. (default: None)
  --rowstart [ROWSTART [ROWSTART ...]]
                        Use these rowstarts. (default: None)
  --skipid [SKIPID [SKIPID ...]]
                        Use these skipids. (default: None)
  --brick [BRICK [BRICK ...]]
                        Use these brick names. Can be a brick list file. (default: None)
  --list [LIST [LIST ...]]
                        Use these run lists. (default: None)
 '
