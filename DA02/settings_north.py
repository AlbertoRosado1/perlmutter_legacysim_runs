import os

run = 'north'
survey_dir = os.getenv('LEGACY_SURVEY_DIR')
output_dir = os.path.join(os.getenv('CSCRATCH'),'legacysim','dr9','DA02',run)
#output_dir = os.path.join(os.getenv('CSCRATCH'),'legacysim','dr9','DA02','test')
truth_fn = os.path.join(os.getenv('CSCRATCH'),'legacysim','dr9','data','truth_cosmos_deep.fits')
injected_fn = os.path.join(output_dir,'file0_rs0_skip0','injected.fits')
#injected_fn = os.path.join(os.getenv('CSCRATCH'),'legacysim','dr9','DA02',run,'file0_rs0_skip0','injected.fits')
bricklist_fn = 'bricklist_{}.txt'.format(run)
runlist_fn = 'runlist_{}.txt'.format(run)
#runlist_fn = 'runlist_{}_64.txt'.format(run)
#runlist_fn = 'runlist_{}_tmp.txt'.format(run)

def get_bricknames():
    return [brickname[:-len('\n')] for brickname in open(bricklist_fn,'r')]

legacypipe_output_dir = os.path.join(os.getenv('LEGACYPIPE_SURVEY_DIR'),run)
