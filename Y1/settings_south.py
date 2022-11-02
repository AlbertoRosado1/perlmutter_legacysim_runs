import os

run = 'south'
survey_dir = os.getenv('LEGACY_SURVEY_DIR')
output_dir = os.path.join(os.getenv('PSCRATCH'),'legacysim','dr9','Y1',run)
truth_fn = os.path.join(os.getenv('PSCRATCH'),'legacysim','dr9','data','truth_cosmos_deep.fits')
injected_fn = os.path.join(output_dir,'file0_rs0_skip0','injected.fits')
bricklist_fn = 'bricklist_{}_stages.txt'.format(run)
#bricklist_fn = f'splitted_bricklists/bricklist_{run}_00.txt'
runlist_fn = 'runlist_{}_new.txt'.format(run)
#runlist_fn = 'runlist_{}_124.txt'.format(run)
#runlist_fn = 'runlist_{}_tmp.txt'.format(run)

# for subrunlist runs
subrunlist_dir = os.path.join('subrunlists',f'{run}') # AJRM
subrunlist_fn = os.path.join(subrunlist_dir,'subrunlist!_{}_1.txt'.format(run)) # AJRM

def get_bricknames():
    return [brickname[:-len('\n')] for brickname in open(bricklist_fn,'r')]

legacypipe_output_dir = os.path.join(os.getenv('LEGACYPIPE_SURVEY_DIR'),run)
