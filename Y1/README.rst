Y1
======

Run legacysim on Y1.

On NERSC (Perlmutter)
--------

Set up data::

  mkdir -p ${PSCRATCH}/legacysim/dr9/data/
  cp /global/cfs/cdirs/cosmo/data/legacysurvey/dr9/ccds-annotated-* ${PSCRATCH}/legacysim/dr9/data/
  cp /global/cfs/cdirs/cosmo/data/legacysurvey/dr9/survey-* ${PSCRATCH}/legacysim/dr9/data/
  ln -s /global/cfs/cdirs/cosmo/data/legacysurvey/dr9/calib/ ${PSCRATCH}/legacysim/dr9/data/
  ln -s /global/cfs/cdirs/cosmo/work/legacysurvey/dr9/images/ ${PSCRATCH}/legacysim/dr9/data/

Pull Docker image::

  shifterimg -v pull adematti/legacysim:DR9

Set up catalogs of sources to be injected::

  source legacypipe-env.sh
  shifter --volume ${HOME}:/homedir/ --image=adematti/legacysim:DR9 python preprocess.py --do injected --run north
  shifter --volume ${HOME}:/homedir/ --image=adematti/legacysim:DR9 python preprocess.py --do injected --run south

Then create run lists::

  shifter --volume ${HOME}:/homedir/ --image=adematti/legacysim:DR9 python /src/legacysim/py/legacysim/scripts/runlist.py --outdir /global/cfs/cdirs/cosmo/data/legacysurvey/dr9/north --brick bricklist_north.txt --write-list runlist_north.txt --modules docker
  shifter --volume ${HOME}:/homedir/ --image=adematti/legacysim:DR9 python /src/legacysim/py/legacysim/batch/environment_manager.py --outdir /global/cfs/cdirs/cosmo/data/legacysurvey/dr9/north --brick bricklist_north.txt --modules docker
  shifter --volume ${HOME}:/homedir/ --image=adematti/legacysim:DR9 python /src/legacysim/py/legacysim/scripts/runlist.py --outdir /global/cfs/cdirs/cosmo/data/legacysurvey/dr9/south --brick bricklist_south.txt --write-list runlist_south.txt --modules docker
  shifter --volume ${HOME}:/homedir/ --image=adematti/legacysim:DR9 python /src/legacysim/py/legacysim/batch/environment_manager.py --outdir /global/cfs/cdirs/cosmo/data/legacysurvey/dr9/south --brick bricklist_south.txt --modules docker

Run::

  chmod u+x ./mpi_runbricks.sh
  salloc -N 1 -C cpu -q interactive -t 04:00:00 -L SCRATCH -J Y1north
  srun -n 17 --mpi=pmi2 shifter --module=none --volume ${HOME}:/homedir/ --image=adematti/legacysim:DR9 ./mpi_runbricks.sh --run north
  srun -n 17 --mpi=pmi2 shifter --module=none --volume ${HOME}:/homedir/ --image=adematti/legacysim:DR9 ./mpi_runbricks.sh --run south

.. note::

  With 101 tasks ``srun -n 101``, there will be 1 root and 100 workers, hence 100 bricks run in parallel.

Check everything ran and match::

  shifter --volume ${HOME}:/homedir/ --image=adematti/legacysim:DR9 /bin/bash
  python /src/legacysim/py/legacysim/scripts/check.py --outdir ${PSCRATCH}/legacysim/dr9/Y1/north --list runlist_north.txt --write-list runlist_north_2.txt
  python /src/legacysim/py/legacysim/scripts/check.py --outdir ${PSCRATCH}/legacysim/dr9/Y1/south --list runlist_south.txt --write-list runlist_south_2.txt
  python /src/legacysim/py/legacysim/scripts/match.py --cat-dir ${PSCRATCH}/legacysim/dr9/Y1/north/file0_rs0_skip0/merged --outdir ${PSCRATCH}/legacysim/dr9/Y1/north --plot-hist plots/hist_north.png
  python /src/legacysim/py/legacysim/scripts/match.py --cat-dir ${PSCRATCH}/legacysim/dr9/Y1/south/file0_rs0_skip0/merged --outdir ${PSCRATCH}/legacysim/dr9/Y1/south --plot-hist plots/hist_south.png
  exit

and similarly for south. Other commands::

  python /src/legacysim/py/legacysim/scripts/merge.py --filetype injected --cat-dir $PSCRATCH/legacysim/dr9/Y1/north/file0_rs0_skip0/merged --outdir $PSCRATCH/legacysim/dr9/Y1/north
  python /src/legacysim/py/legacysim/scripts/merge.py --filetype tractor --cat-dir $PSCRATCH/legacysim/dr9/Y1/north/file0_rs0_skip0/merged --outdir $PSCRATCH/legacysim/dr9/Y1/north
  python /src/legacysim/py/legacysim/scripts/merge.py --filetype injected --cat-dir $PSCRATCH/legacysim/dr9/Y1/south/file0_rs0_skip0/merged --outdir $PSCRATCH/legacysim/dr9/Y1/south
  python /src/legacysim/py/legacysim/scripts/merge.py --filetype tractor --cat-dir $PSCRATCH/legacysim/dr9/Y1/south/file0_rs0_skip0/merged --outdir $PSCRATCH/legacysim/dr9/Y1/south
  python /src/legacysim/py/legacysim/scripts/match.py --tractor-legacypipe /global/cfs/cdirs/cosmo/data/legacysurvey/dr9/south/ --outdir $PSCRATCH/legacysim/dr9/Y1/south --cat-fn $PSCRATCH/legacysim/dr9/Y1/south/file0_rs0_skip0/merged/matched_legacypipe_input.fits
  python /src/legacysim/py/legacysim/scripts/cutout.py --outdir $PSCRATCH/legacysim/dr9/Y1/south --plot-fn "plots/cutout_south-%(brickname)s-%(icut)d.png" --ncuts 2
  python /src/legacysim/py/legacysim/scripts/resources.py --outdir $PSCRATCH/legacysim/dr9/Y1/south --plot-fn plots/resources-summary_south.png

Merge legacypipe catalogs::

    shifter --module=mpich-cle6 --volume ${HOME}:/homedir/ --image=adematti/legacysim:DR9 python /src/legacysim/py/legacysim/scripts/merge.py --filetype tractor --source legacypipe --list runlist_north.txt --cat-dir $PSCRATCH/legacypipe/dr9/Y1/north/merged --outdir $LEGACYPIPE_SURVEY_DIR/north/
    shifter --module=mpich-cle6 --volume ${HOME}:/homedir/ --image=adematti/legacysim:DR9 python /src/legacysim/py/legacysim/scripts/merge.py --filetype tractor --source legacypipe --list runlist_south.txt --cat-dir $PSCRATCH/legacypipe/dr9/Y1/south/merged --outdir $LEGACYPIPE_SURVEY_DIR/south/

--------
Job array runs:
first create subrunlists and take note of how many subrunlists are created::

    python create_subrunlists.py --run north --filename runlist_north.txt --index 1
    
.. note::

  Must have created first runlist, i.e. `runlist_north.txt`. Also, check that correct runlist is specficied in settings_runname.py file,
  for example `runlist_fn = 'runlist_{}.txt'.format(run)` . 
    
Now in the settings_runname.py change the INDEX of the run (reference below), for example if you are in the first run the use INDEX of 1::

    subrunlist_fn = os.path.join(subrunlist_dir,'subrunlist!_{}_INDEX.txt'.format(run))
   
Modify the --array=1-N argument in the `job_array.sh` file, where N is the number of subarrays created in the orevious step. Also notice
that you can change the -o  and -e arguments to desired directories, change. according to region. Then run::

    chmod u+x ./mpi_runbricks_runlist.sh
    sbatch job_array.sh
    
After the run has finished change the INDEX in the `subrunlist_fn` in the `settings_runname.py` to reflect the following run, for example change from 1 to 2.

Now you have to create an updated runlist (run indices are to be changed to corresponding run, i.e. change the 2 according to run)::

    shifter --volume ${HOME}:/homedir/ --image=adematti/legacysim:DR9 /bin/bash
    python /src/legacysim/py/legacysim/scripts/check.py --outdir ${PSCRATCH}/legacysim/dr9/Y1/north --list runlist_north.txt --write-list runlist_north_2.txt
    
Change the `runlist_fn` in the `settings_runname.py` to this new runlist created above. Now create new subrunlists::

    python create_subrunlists.py --run region --filename runlist_north_2.txt --index 2
    
Again modify --array option in `run_job.sh` and run. If bricks are taking too much time you can change -t 01:00:00 to -t 02:00:00.

    
