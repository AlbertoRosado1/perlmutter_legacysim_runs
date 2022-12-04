import os

run = 'north'
survey_dir = os.getenv('LEGACY_SURVEY_DIR')
output_dir = os.path.join(os.getenv('PSCRATCH'),'legacysim','dr9','TEST',run)
truth_fn = "/pscratch/sd/a/arosado/legacysim_test_files/truth_cosmos_deep.fits"
injected_fn = "/pscratch/sd/a/arosado/legacysim_test_files/injected.fits"
bricklist_fn = 'bricklist_{}.txt'.format(run)
runlist_fn = 'runlist_{}.txt'.format(run)


def get_bricknames():
    return [brickname[:-len('\n')] for brickname in open(bricklist_fn,'r')]

legacypipe_output_dir = os.path.join(os.getenv('LEGACYPIPE_SURVEY_DIR'),run)
