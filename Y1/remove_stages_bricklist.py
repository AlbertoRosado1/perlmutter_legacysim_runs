# script to remove bricks using stages8,9,10 from bricklists
import argparse
import os
import numpy as np

parser = argparse.ArgumentParser(description='remove bricks from stages8,9,10')
parser.add_argument('-r','--run',type=str,choices=['north','south'],required=True,help='Run?')
opt = parser.parse_args()

fn_runlist = os.path.join(f'/global/homes/a/arosado/perlmutter_legacysim_runs/Y1/runlist_{opt.run}.txt')
fn_bricklist = os.path.join(f'/global/homes/a/arosado/perlmutter_legacysim_runs/Y1/bricklist_{opt.run}.txt')

# Read txt files
with open(fn_bricklist, 'r') as file:
    print(f'reading', fn_bricklist)
    text = file.readlines()
    #text = np.array(text)

with open(fn_runlist, 'r') as file:
    print(f'reading', fn_runlist)
    runlist = file.readlines()
    #text_to_remove = np.array(text_to_remove)

new_text = text.copy()
removed = ['bricks removed because they were in stages8,9,10\n']
#"""
for line in runlist:
    if ("stages8" in line) or ("stages9" in line) or ("stages10" in line):
        brick = line.split()[0]
        if brick[0]!="#":
            new_text.remove(brick+"\n")
            removed.append(line)
        else:
            removed.append(line)

print(f'removed {len(text) - len(new_text)}')
# save bricks removed because of stages
np.savetxt(f'bricks_removed_{opt.run}.txt', removed, newline='', fmt='%s')
# save remaining bricks to file
np.savetxt(f'bricklist_{opt.run}_new.txt', new_text, newline='', fmt='%s')
#"""