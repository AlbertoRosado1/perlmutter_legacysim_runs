# script to remove bricks already ran on DA02 footprint from runlists, only works for first runlist
import argparse
import os
import numpy as np

parser = argparse.ArgumentParser(description='remove bricks from DA02')
parser.add_argument('-r','--run',type=str,choices=['north','south'],required=True,help='Run?')
opt = parser.parse_args()

fn_DA02 = os.path.join(f'/global/homes/a/arosado/perlmutter_legacysim_runs/Y1/DA02_bricklists/bricklist_{opt.run}.txt')
fn_Y1 = os.path.join(f'/global/homes/a/arosado/perlmutter_legacysim_runs/Y1/runlist_{opt.run}_stages.txt')

# Read txt files
with open(fn_Y1, 'r') as file:
    print(f'reading', fn_Y1)
    text = file.readlines()
    #text = np.array(text)

with open(fn_DA02, 'r') as file:
    print(f'reading', fn_DA02)
    text_to_remove = file.readlines()
    #text_to_remove = np.array(text_to_remove)

new_text = text.copy()
for brick in text_to_remove:
    for line in new_text:
        if brick.replace('\n', '') in line:
            new_text.remove(line)

print(f'removed {len(text) - len(new_text)}')

# save remaining bricks to file
np.savetxt(f'runlist_{opt.run}_new.txt', new_text, newline='', fmt='%s')
