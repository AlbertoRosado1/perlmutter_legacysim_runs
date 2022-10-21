# script to count bricks completed by reading latest subrunlists and compare them to previous subrunlist
# index corresponds to the run 
# example
# python compute_completed_bricks.py --run $run --index $new_list_index --narrays $number_job_arrays --save True 
# python compute_completed_bricks.py --run north --index 2 --narrays 500 --save True 
import argparse
import os
import numpy as np

parser = argparse.ArgumentParser(description='create subrunlists from a single runlist')
parser.add_argument('-r','--run',type=str,choices=['north','south'],required=True,help='Run?')
parser.add_argument('-i','--index',type=int,required=True,help='specify latest run index of subrunlists')
parser.add_argument('-na','--narrays',type=int,required=True,help='Number of jobs submitted in job array')
parser.add_argument('-s','--save',type=bool,required=False,default=False,help='Save info')
opt = parser.parse_args()

base_dir = '/global/homes/a/arosado/perlmutter_legacysim_runs/Y1'
subrunlist_dir = os.path.join(base_dir,'subrunlists',f'{opt.run}')

# Read txt files
bricks_before_run = []
bricks_after_run = []
bricks_completed = []
for i in range(1,opt.narrays +1): # AJRM changed 20 to opt.narrays 
    fn = os.path.join(subrunlist_dir, f'subrunlist{i}_{opt.run}_{opt.index}.txt')
    fn_before = os.path.join(subrunlist_dir, f'subrunlist{i}_{opt.run}_{opt.index-1}.txt')
    if os.path.exists(fn):
        with open(fn_before, 'r') as file:
            #print(f'reading', fn_before)
            text_before = file.readlines()
            header = []
            for i, line in enumerate(text_before[:20]):
                if line[0]=='#':
                    header.append(line)
            h_end_ind = len(header) # index at which header ends in file
            # remove header
            text_before = text_before[h_end_ind:] # without header

        with open(fn, 'r') as file:
            #print(f'reading', fn)
            text = file.readlines()
            header = []
            for i, line in enumerate(text[:20]):
                if line[0]=='#':
                    header.append(line)
            h_end_ind = len(header) # index at which header ends in file
            # remove header
            text = text[h_end_ind:] # without header
        
        bricks_before_run.append(len(text_before))
        bricks_after_run.append(len(text))
        bricks_completed.append(len(text_before) - len(text))
    else:
        with open(fn_before, 'r') as file:
            #print(f'reading', fn_before)
            text_before = file.readlines()
            header = []
            for i, line in enumerate(text_before[:20]):
                if line[0]=='#':
                    header.append(line)
            h_end_ind = len(header) # index at which header ends in file
            # remove header
            text_before = text_before[h_end_ind:] # without header
        text = []
        bricks_before_run.append(len(text_before))
        bricks_after_run.append(len(text))
        bricks_completed.append(len(text_before) - len(text))
    
print(f'Bricks completed from each subrunlist through 1-{opt.narrays}:')
for i, bnumber in enumerate(bricks_completed):
    print(f'from subrunlist{i+1}_{opt.run}_{opt.index-1}.txt {bnumber}/{bricks_before_run[i]} bricks completed')
print(f'Total bricks completed for {opt.run.capitalize()} run {opt.index} is {np.sum(bricks_completed)} from {np.sum(bricks_before_run)}')
print(f'Bricks remaining for {opt.run.capitalize()} is {np.sum(bricks_after_run)}')


if opt.save==True:
    out_fn = os.path.join(subrunlist_dir, f'brickinfo_{opt.run}_{opt.index-1}.txt')
    with open(out_fn, 'w') as file:
        file.write(f'Bricks completed from each subrunlist through 1-{opt.narrays}:\n')
        for i, bnumber in enumerate(bricks_completed):
            file.write(f'from subrunlist{i+1}_{opt.run}_{opt.index-1}.txt {bnumber}/{bricks_before_run[i]} bricks completed\n')
        file.write(f'Total bricks completed for {opt.run.capitalize()} run {opt.index} is {np.sum(bricks_completed)} from {np.sum(bricks_before_run)}\n')
        file.write(f'Bricks remaining for {opt.run.capitalize()} is {np.sum(bricks_after_run)}\n')
        file.close()