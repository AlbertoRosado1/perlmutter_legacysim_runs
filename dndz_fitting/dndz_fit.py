import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit, minimize
import scipy.special as sp
from astropy.table import Table

def get_legacysim_data(z_col='INPUT_HSC_MIZUKI_PHOTOZ_BEST', zmin=0.6,zmax=1.6,region='south'):
        # legacysim data
        legacysim = Table.read(f"/pscratch/sd/a/arosado/legacysim_masked_ELG_data/legacysim_data_{region}.fits")
        z = legacysim[z_col]
        depth = legacysim['GALDEPTH_R']
        mask = z>zmin
        mask &= z<zmax
        mask &= legacysim['GALDEPTH_R'] > 0
        mask &= legacysim['GALDEPTH_G'] > 0
        legacysim = legacysim[mask]
       
        return legacysim
    
def get_ELG_clustering_data(zmin=0.6,zmax=1.6,region='south'):
        r = region.capitalize()[0]
        #full_dir = '/global/cscratch1/sd/arosado/catalogs/edav1/da02/'
        base_dir = '/global/cscratch1/sd/arosado/catalogs/DA02/LSS/guadalupe/LSScats/test/'
    
        data_full = Table.read(os.path.join(base_dir,'ELG_LOPnotqso_full.dat.fits'))
        data_full = data_full[data_full['PHOTSYS'] == r]
        data_clustering = Table.read(os.path.join(base_dir, f'ELG_LOPnotqso_{r}_clustering.dat.fits'))
        ind1, ind2 = utils.overlap(data_clustering['TARGETID'], data_full['TARGETID'])
        cat = data_clustering[ind1]
        z = cat['Z']
        depth_r = data_full['GALDEPTH_R'][ind2]
        depth_g = data_full['GALDEPTH_G'][ind2]
        
        #mask = z>zmin
        #mask &= z<zmax
        #mask = depth > 0
        #print(f"removed {cat['RA'].size - cat[mask]['RA'].size} objects with zcut")
        #cat = cat[mask]
        #depth = depth[mask]
        cat['GALDEPTH_R'] = depth_r
        cat['GALDEPTH_G'] = depth_g
        
        return cat
    
def get_ELG_clustering_data(fn, zmin=0.6,zmax=1.6,region='south'):
        r = region.capitalize()[0]
        #full_dir = '/global/cscratch1/sd/arosado/catalogs/edav1/da02/'
        base_dir = '/global/cscratch1/sd/arosado/catalogs/DA02/LSS/guadalupe/LSScats/test/'
    
        data_full = Table.read(os.path.join(base_dir,'ELG_LOPnotqso_full.dat.fits'))
        data_full = data_full[data_full['PHOTSYS'] == r]
        data_clustering = Table.read(os.path.join(base_dir, f'ELG_LOPnotqso_{r}_clustering.dat.fits'))
        ind1, ind2 = utils.overlap(data_clustering['TARGETID'], data_full['TARGETID'])
        cat = data_clustering[ind1]
        z = cat['Z']
        depth_r = data_full['GALDEPTH_R'][ind2]
        depth_g = data_full['GALDEPTH_G'][ind2]
        
        #mask = z>zmin
        #mask &= z<zmax
        #mask = depth > 0
        #print(f"removed {cat['RA'].size - cat[mask]['RA'].size} objects with zcut")
        #cat = cat[mask]
        #depth = depth[mask]
        cat['GALDEPTH_R'] = depth_r
        cat['GALDEPTH_G'] = depth_g
        
        return cat
    
def get_ELG_data(fn, zmin=0.6,zmax=1.6,region='south'):
        r = region.capitalize()[0]

        data_full = Table.read(fn)
        data_full = data_full[data_full['PHOTSYS'] == r]
        z = data_full['Z_not4clus']#data_full['Z']
        zgood = z>zmin
        zgood &= z<zmax
        data_full[zgood]
        
        return data_full
    
class ELG_dndz:
    def __init__(self, data_fn, sim_weights=None, zmin=0.6, zmax=1.6, bins=50,run='south', depth_type='GALDEPTH_R', fit_both=False):
        self.region = run[0].upper()
        
        # legacysim data
        z_col = 'INPUT_HSC_MIZUKI_PHOTOZ_BEST'
        self.legacysim = get_legacysim_data(z_col=z_col,zmin=zmin,zmax=zmax,region=run)
        self.z = self.legacysim[z_col]
        self.depth = self.legacysim[depth_type]
        self.weights = None

        # ELG data
        self.cat = get_ELG_data(data_fn,zmin=zmin,zmax=zmax,region=run)
        self.z_cat = self.cat['Z_not4clus'] # self.cat['Z']
        self.depth_cat = self.cat[depth_type]
        #self.weights_cat = self.cat['WEIGHT_COMP']*self.cat['WEIGHT_FKP']*self.cat['WEIGHT_RF'] # for old cat
        self.weights_cat = (1/self.cat['FRACZ_TILELOCID']) * self.cat['WEIGHT_SYS'] * self.cat['WEIGHT_ZFAIL'] #self.cat['WEIGHT'] #self.cat['WEIGHT_COMP']*self.cat['WEIGHT_SYS']

        # redshif bins
        self.bins = bins+1
        self.zbins = np.linspace(zmin, zmax, self.bins)
        self.bc = (self.zbins[:-1] + self.zbins[1:])/2.

        self.quantiles = np.quantile(self.depth, q=np.linspace(0., 1., 6))
        self.labels = ['{:.0f} < {} < {:.0f}'.format(low, depth_type, high) for low, high in zip(self.quantiles[:-1], self.quantiles[1:])]
        self.samples = np.clip(np.digitize(self.depth, self.quantiles) - 1, 0, len(self.quantiles) - 1)
        self.usamples = np.unique(self.samples)
        self.nsamples = len(self.usamples)-1  

        self.bin_data_dndz()
        self.new_weights = self.get_pred_weights()# 
        self.sim_weights = self.get_sim_weights() # 
        if fit_both:
            if 'r' in depth_type.lower():
                d = 'GALDEPTH_G'
                print(f"redoing fit with {d}")
            else:
                d = 'GALDEPTH_R'
                print(f"redoing fit with {d}")
            self.both_fit = ELG_dndz(data_fn, sim_weights=self.sim_weights, zmin=zmin, zmax=zmax, bins=bins,run=run, depth_type=d)
            
    
    def dndz_model_old(self,X, a, b, c, d, e, f, g):
        #[1.0, 1.0, 0.8, 1.0, 1.0, 0.0, 1.0]
        z_, depth_base = X
        depth_ = np.log10(depth_base)
        res = []
        for z, depth in zip(z_, depth_):
            if z < c:
                res.append((a + b*z) * (d*sp.erf(depth/e+f) + g))
            elif z >= c:
                res.append((a + b*c) * (d*sp.erf(depth/e+f) + g))
        res = np.array(res)
        return res
    
    def dndz_model(self,X, a, b, c, d, e, f, g):
        #[1.0, 1.0, 0.8, 1.0, 1.0, 0.0, 1.0]
        z_, depth_base = X
        res = []
        for z, depth in zip(z_, depth_base):
            if depth<=0:
                #print(f'depth={depth} is bad value')
                res.append(0) # no negative or 0 depth values
            elif z < c:
                depth = np.log10(depth)
                res.append((a + b*z) * (d*sp.erf(depth/e+f) + g))
            elif z >= c:
                depth = np.log10(depth)
                res.append((a + b*c) * (d*sp.erf(depth/e+f) + g))
        res = np.array(res)
        return res

    def cost(self, params):
        # get chi2 using simulated data
        dndz_pred = self.dndz_model((self.z_h, self.depth_h), *params)
        c = np.sum(((self.dndz_h - dndz_pred)/(self.yerr))**2)
        return c
    
    def test(self):
        # minimize cost function using binned simulated data
        options = {'maxfev': 4*7*200, 'maxiter': 1000}
        return minimize(self.cost,[1.0, 1.0, 0.8, 1.0, 1.0, 0.0, 1.0], method='Powell', tol=1e-6, options=options) 
                           
    def bin_data_dndz(self):
        # function to bin simulated data into 5 depth bins, each depth bin with `self.bins` number of bins
        dndzw = np.histogram(self.z, bins=self.zbins, weights=self.weights)[0]
        dndz = np.histogram(self.z, bins=self.zbins)[0]
        
        z_list = []
        depth_list = []
        dndz_list = []
        yerr_list = []

        for isample, sample in enumerate(self.usamples):
            mask = self.samples == sample
            depth_sample = np.full_like(self.bc, self.depth[mask].mean())
            
            dndzw_sample = np.histogram(self.z[mask], bins=self.zbins, weights=self.weights[mask] if self.weights is not None else None)[0]
            ratio = dndzw_sample.sum()/dndzw.sum()
            dndz_norm =  1./ratio*dndzw_sample/dndzw - 1.

            if isample < self.nsamples:
                #print(f'max depth in bin {isample}: {self.depth[mask].max()}')
                z_list.append(self.bc)
                depth_list.append(depth_sample)
                dndz_list.append(dndz_norm)
                yerr_ = 1 / np.sqrt(dndzw_sample)
                yerr_list.append(yerr_)
            
        self.z_h = np.concatenate(z_list)
        self.depth_h = np.concatenate(depth_list)
        self.dndz_h = np.concatenate(dndz_list)
        self.yerr = np.concatenate(yerr_list)
    
    def get_pred_weights(self):
        # apply fit at catalog level using optimal parameters obtained from fitting binned simulated data
        self.res = self.test()
        self.params = self.res.x
        f = self.dndz_model((self.z_cat, self.depth_cat),*self.params)
        #print(f'min depth used when calculating weights {self.depth_cat.min()}')
        #print(f'min f when calculating weights {f.min()}')
        self.dndz_vals = f
        print(f'min(dndz - 1): {f.min()}, max(dndz - 1): {f.max()}')
        w = 1/(f+1)
        return w
    
    def get_sim_weights(self): #
        # apply fit to obiwan data using optimal parameters obtained from fitting binned obiwan data
        res = self.test()
        params = self.res.x
        f = self.dndz_model((self.z, self.depth),*params)
        self.dndz_vals_obiwan = f
        print(f'min(dndz - 1): {f.min()}, max(dndz - 1): {f.max()}')
        w = 1/(f+1)
        return w
    
    def get_chi2(self):
        #
        N,n = len(self.dndz_h), len(self.params)
        print(f'number of data points: {N}')
        print (f'number of free parameters: {n}')
        chi2 = self.res.fun / (N-n)
        print(f'reduced $\chi^2$: {chi2}')
        return chi2
        
    # below is code for visualization
    def plot_dndz(self, z, depth, depth_type='depth_r', zbins=np.linspace(0.6,1.6,18), quantiles=None, weights=None, legend=False, yerr=False, ls='-'):
        # depth_type can be 'depth_r' for example, it is just used for the label
        bc = (zbins[:-1] + zbins[1:])/2
        ax = plt.gca()
        fig = plt.gcf()
        #fig.set_size_inches(7, 5)
        #ax.plot([], [], linestyle=ls, color='k', label='using pred weights')
        if quantiles is None:
            quantiles = np.quantile(depth, q=np.linspace(0., 1., 6))
        labels = ['{:.0f} < {} < {:.0f}'.format(low, depth_type, high) for low, high in zip(quantiles[:-1], quantiles[1:])]
        samples = np.clip(np.digitize(depth, quantiles) - 1, 0, len(quantiles) - 1)
        usamples = np.unique(samples)
        nsamples = len(usamples)-1  
        
        dndzw = np.histogram(z, bins=zbins, weights=weights)[0]
        dndz = np.histogram(z, bins=zbins)[0]
        
        z_list = []
        depth_list = []
        dndz_list = []
        yerr_list = []

        for isample, (sample, label) in enumerate(zip(usamples, labels)):
            mask = samples == sample
            depth_sample = np.full_like(self.bc, depth[mask].mean())
            dndzw_sample = np.histogram(z[mask], bins=zbins, weights=weights[mask] if weights is not None else None)[0]
            ratio = dndzw_sample.sum()/dndzw.sum()
            dndz_norm =  1./ratio*dndzw_sample/dndzw - 1.
            
            if isample <= nsamples:
                if yerr:
                    yerr_ = 1 / np.sqrt(dndzw_sample)
                    if legend:
                        ax.errorbar(bc, dndz_norm, yerr=yerr_, color='C{:d}'.format(isample), ls=ls, label=label)
                    else:
                        ax.plot(bc, dndz_norm, color='C{:d}'.format(isample), ls=ls)
                else:
                    if legend:
                        ax.plot(bc, dndz_norm, color='C{:d}'.format(isample), ls=ls, label=label)
                    else:
                        ax.plot(bc, dndz_norm, color='C{:d}'.format(isample), ls=ls)
            
        
        #ax.set_title('Southern part of DA02 {}'.format('ELG_LOPnotqso'))
        if legend:
            ax.legend(loc='upper right', ncol=2)
