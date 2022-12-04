import os
from glob import glob
from time import time
from astropy.table import Table, vstack
import argparse

parser = argparse.ArgumentParser(description='legacysim main runbrick')
parser.add_argument('-r','--run',type=str,choices=['north','south'],required=True,help='Run?')
opt = parser.parse_args()

t0 = time()
# get Y1 matched input file
Y1_merged_dir = os.path.join(os.getenv('PSCRATCH'),'legacysim','dr9','Y1',opt.run,'file0_rs0_skip0','merged')
Y1_fn = os.path.join(Y1_merged_dir, "matched_input.fits")
print(f"using {Y1_fn}")

# get DA02 matched input files
img_sim_dir = "/global/cfs/cdirs/desi/survey/catalogs/image_simulations/ELG/"
DA02_merged_dir = os.path.join(img_sim_dir,'dr9','DA02',opt.run,'file0_rs0_skip0','merged')
DA02_fns = glob(os.path.join(DA02_merged_dir, "matched_inputs_**.fits"))
print(f"matched input files in DA02 merged dir {len(DA02_fns)}")

#Read in the fits table you want to append 
print(f"reading {Y1_fn}")
Y1 = Table.read(Y1_fn)

print(f"Start concatenating DA02 matched input files")
t = time()
DA02 = vstack([Table.read(fn, format='fits') for fn in DA02_fns])
print(f"Finished concatenating DA02 matched input files at {time() - t:.2f}")

print(f"Start concatenating Y1 and DA02 files")
t = time()
concat_legacysim = vstack([Y1, DA02])
print(f"Finished concatenating Y1 and DA02 files at {time()-t:.2f}")

# Create fits file with new concatenated files
fn = os.path.join(Y1_merged_dir,'matched_input_full.fits')
print(f"saving {fn}")
concat_legacysim.write(fn, format='fits', overwrite=False)
print(f"saved {fn}")

print(f"time to run script {time()-t0:.2f}")