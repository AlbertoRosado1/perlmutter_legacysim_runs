TEST
======

Run legacysim on test sample.

On NERSC (Perlmutter)
--------

Set up data::

  mkdir -p ${PSCRATCH}/legacysim/dr9/data/
  cp /dvs_ro/cfs/cdirs/cosmo/data/legacysurvey/dr9/ccds-annotated-* ${PSCRATCH}/legacysim/dr9/data/
  cp /dvs_ro/cfs/cdirs/cosmo/data/legacysurvey/dr9/survey-* ${PSCRATCH}/legacysim/dr9/data/
  ln -s /dvs_ro/cfs/cdirs/cosmo/data/legacysurvey/dr9/calib/ ${PSCRATCH}/legacysim/dr9/data/
  ln -s /dvs_ro/cfs/cdirs/cosmo/work/legacysurvey/dr9/images/ ${PSCRATCH}/legacysim/dr9/data/
  
Please make change in ``legacypipe_env.sh``, change ``export LEGACY_SURVEY_DIR=/your_pscratch_dir/legacysim/dr9/data/``.

Pull Docker image::

  shifterimg -v pull adematti/legacysim:DR9

Run::

  chmod u+x ./mpi_runbricks.sh
  salloc -N 1 -C cpu -q interactive -t 04:00:00 -L SCRATCH -J legacysim_test
  srun -n 17 --mpi=pmi2 shifter --module=none --volume ${HOME}:/homedir/ --image=adematti/legacysim:DR9 ./mpi_runbricks.sh --run north

.. note::

  With 101 tasks ``srun -n 101``, there will be 1 root and 100 workers, hence 100 bricks run in parallel.
