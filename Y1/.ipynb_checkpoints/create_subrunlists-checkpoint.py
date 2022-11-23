# script to create subrunlists 'subrunlist!_{}_1.txt'.format(run) where ! goes 1-opt.narrays
# example
# python create_subrunlists.py --run north --index #--narrays 500
import argparse
import os
import numpy as np
from math import ceil

parser = argparse.ArgumentParser(description='create subrunlists from a single runlist')
parser.add_argument('-r','--run',type=str,choices=['north','south'],required=True,help='Run?')
parser.add_argument('-i','--index',type=int,required=True,help='specify latest run index of subrunlists')
parser.add_argument('-fn','--filename',type=str,required=True,help='runlist filename')
#parser.add_argument('-na','--narrays',type=int,required=True,help='number of subrunlists desired')
opt = parser.parse_args()

    
base_dir = '/global/homes/a/arosado/perlmutter_legacysim_runs/Y1'
subrunlist_dir = os.path.join(base_dir,'subrunlists',f'{opt.run}')
fn_Y1 = opt.filename #os.path.join(base_dir, f'runlist_{opt.run}_5.txt')

# Read txt files
with open(fn_Y1, 'r') as file:
    print(f'reading', fn_Y1)
    text = file.readlines()
    text = np.array(text)
    header = []
    for i, line in enumerate(text[:20]):
        if line[0]=='#':
            header.append(line)
    h_end_ind = len(header) # index at which header ends in file
    header_array = text[:h_end_ind]
    # remove header
    print(f'header has {h_end_ind} lines.')
    text_no_header = text[h_end_ind:]

# now split into opt.narrays samples
nbricks_per_array = 16*4
nsplit = ceil(len(text_no_header)/nbricks_per_array) # should give roughly the number of subarrays so each contains approx nbricks_per_array.
brick_arrays = np.array_split(text_no_header, nsplit)#opt.narrays) 

# add back header and save to .txt file
for i, bricks in enumerate(brick_arrays):
    subrunlist = np.insert(bricks, 0, header_array) # add header before bricks for each array
    fn = os.path.join(subrunlist_dir, f'subrunlist{i+1}_{opt.run}_{opt.index}.txt')
    print(f'saving {fn}')
    np.savetxt(fn, subrunlist, newline='', fmt='%s')
    
print(f'splitted {fn_Y1} into {nsplit} subarrays')