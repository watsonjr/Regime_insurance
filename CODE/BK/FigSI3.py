# -*- coding: utf-8 -*-

import numpy as np
from matplotlib import pyplot as plt
import functions as fn
from parameters import params_dict
from multiprocessing import Pool

#%%
"SIMULATION PARAMS"
"Params are stored in parameters.py"
sims = len(params_dict['c_sweep'])
c_sweep = params_dict['c_sweep']

"SIMULATION DATA HOLDERS"
avg_util_low = np.zeros(sims)
avg_util_mid = np.zeros(sims)
avg_util_high = np.zeros(sims)
avg_util_fixed_low = np.zeros(sims)
avg_util_fixed_high = np.zeros(sims)
avg_util_a = np.zeros(sims)
avg_util_tr = np.zeros(sims)
avg_pi = np.zeros(sims)
avg_pi_a = np.zeros(sims)
avg_pi_tr = np.zeros(sims)

"CREATE NEW PARAMETER DICTIONARY FOR EACH SIMULATION"
A = np.empty((sims),dtype=dict)

for i in range(sims):
    A[i] = {'dt':params_dict['dt'],
            'INIT_X':params_dict['INIT_X'],
            'NUMSTEPS': params_dict['NUMSTEPS'], 
            'r': params_dict['r'], 
            'K': params_dict['K'],
            'c': params_dict['c_sweep'][i],
            'h': params_dict['h'],
            'mu': params_dict['mu'],
            'sigma': params_dict['sigma'],
            'i0':params_dict['i0'],
            'mu_i':params_dict['mu_i'],
            'T':params_dict['T'],
            'beta':params_dict['beta'],
            'y0':params_dict['y0'],
            'l_low': params_dict['l_low'],
            'l_mid': params_dict['l_mid'],
            'l_high': params_dict['l_high'],
            'a':params_dict['a'],
            'm':10,
            'n':-1/3,
            'm_tr':27/4,
            'n_tr':-1/15,
            'a_tr':params_dict['a_tr']
              }


#%%
runSim1 = False

"SIMULATION 1: Adaptive capacity and flickering induced welfare collapse"
if runSim1 == True:
    if __name__=='__main__':
        with Pool(7) as pool:        
            output = pool.map(fn.flickering_util,A)
            
        for i in range(sims):
            avg_util_low[i] = output[i][0]
            avg_util_mid[i] = output[i][1]
            avg_util_high[i] = output[i][2]
            avg_pi[i] = output[i][3]
            avg_util_fixed_high[i] = output[i][4]
            avg_util_fixed_low[i] = output[i][5]
        np.save('../DATA/avgUtil_ld',avg_util_low)
        np.save('../DATA/avgUtil_md',avg_util_mid)
        np.save('../DATA/avgUtil_hd',avg_util_high)
        np.save('../DATA/avgUtil_fixed_hd',avg_util_fixed_high)
        np.save('../DATA/avgUtil_fixed_ld',avg_util_fixed_low)
        np.save('../DATA/avgPid',avg_pi)
        np.save('../DATA/cSweep_1d',params_dict['c_sweep'])
     



#%%
runSim2 = False
"SIMULATION 2: Adapt or transform!"
if runSim2 == True:
    if __name__=='__main__':
        with Pool(7) as pool:        
            output_tr = pool.map(fn.flickering_util_trans,A)
            
        for i in range(sims):
            avg_util_a[i] = output_tr[i][0]
            avg_util_tr[i] = output_tr[i][1]
            avg_pi_a[i] = output_tr[i][2]
            avg_pi_tr[i] = output_tr[i][3]
        np.save('../DATA/avgUtil_ad',avg_util_a)
        np.save('../DATA/avgUtil_trd',avg_util_tr)
        np.save('../DATA/avgPi_ad',avg_pi_a)
        np.save('../DATA/avgPi_trd',avg_pi_tr)
        np.save('../DATA/cSweep_2d',params_dict['c_sweep'])
#%%

"PLOTS"

"Load data from Sim 1"
avg_util_low = np.load('../DATA/avgUtil_ld.npy')
avg_util_mid = np.load('../DATA/avgUtil_md.npy')
avg_util_high = np.load('../DATA/avgUtil_hd.npy')
avg_util_fixed_low = np.load('../DATA/avgUtil_fixed_ld.npy')
avg_util_fixed_high = np.load('../DATA/avgUtil_fixed_hd.npy')
avg_pi = np.load('../DATA/avgPid.npy')
c_sweep_1 = np.load('../DATA/cSweep_1d.npy')

"Load data from Sim 2"
avg_util_a = np.load('../DATA/avgUtil_ad.npy')
avg_util_tr = np.load('../DATA/avgUtil_trd.npy')
avg_pi_a = np.load('../DATA/avgPi_ad.npy')
avg_pi_tr = np.load('../DATA/avgPi_trd.npy')
c_sweep_2 = np.load('../DATA/cSweep_2d.npy')


ratio  = np.sqrt(2)
scale = 3
fig0 = plt.figure(figsize=(ratio*scale,scale));
ax0 = fig0.add_subplot(111);
ax0.scatter(c_sweep_1,avg_pi,label='$\overline{\pi}$',color='#005745',s=12,alpha=.75);
ax0.scatter(c_sweep_1,avg_util_high,label='$\overline{U}, (l = 0.1)$',color='#009175',s=12,alpha=.75);
ax0.scatter(c_sweep_1,avg_util_mid,label='$\overline{U}, (l = 0.01)$',color='#00cba7',s=12,alpha=.75);
ax0.scatter(c_sweep_1,avg_util_low,label='$\overline{U}, (l = 0.001)$',color='#86ffde',s=12,alpha=.75);

ax0.plot((1.78,1.78),(0,11),'k',alpha=.4,linewidth = 2)
ax0.plot((2.6,2.6),(0,11),'k',alpha=.4,linewidth = 2)
ax0.set_ylabel('Average utility')
ax0.set_xlabel('Extraction rate, $c$')
ax0.set_xlim((c_sweep[0],c_sweep[-1]))
ax0.set_ylim((1.8,10.2))
ax0.legend(bbox_to_anchor=(1,0), loc="lower left")




fig1 = plt.figure(figsize=(ratio*scale,scale));
bx = fig1.add_subplot(111);
bx.plot((1.78,1.78),(0,11),'k',alpha=.4,linewidth = 2)
bx.plot((2.6,2.6),(0,11),'k',alpha=.4,linewidth = 2)
bx.scatter(c_sweep_2,avg_pi_a,label='$\overline{\pi}$, Case 1',s=12,marker='o',c = '#005745',alpha=.75);
bx.scatter(c_sweep_2,avg_util_a,label='$\overline{U}$, Case 1',s=12,marker='o',c = '#00cba7',alpha=.75);
bx.scatter(c_sweep_2,avg_pi_tr,label='$\overline{\pi}$, Case 2',s=12,marker='o',c='#8400cd',alpha=.75);
bx.scatter(c_sweep_2,avg_util_tr,label='$\overline{U}$, Case 2',s=12,marker='o', c = '#ff92fd',alpha=.75);

bx.set_ylabel('Average utility')
bx.set_xlabel('Extraction rate, $c$')
bx.set_xlim((c_sweep[0],c_sweep[-1]))
bx.set_ylim((1.8,10.2))
bx.legend(bbox_to_anchor=(1,0), loc="lower left")

"TEXT"
ax0.text(.75, 3.5, 'Regime 1', fontsize = 10)
ax0.text(1.9, 3.5, 'Regime 2', fontsize = 10)
ax0.text(2.8, 3.5, 'Regime 3', fontsize = 10)

bx.text(.75, 3.5, 'Regime 1', fontsize = 10)
bx.text(1.9, 3.5, 'Regime 2', fontsize = 10)
bx.text(2.8, 3.5, 'Regime 3', fontsize = 10)

"SAVE FIGS"
save = False

if save == True:
    fig0.savefig("../FIGS/utility2.pdf",bbox_inches='tight')
    fig0.savefig("../FIGS/utility2.png",bbox_inches='tight', dpi=150)
    fig1.savefig("../FIGS/util_tr2.pdf", bbox_inches='tight')
    fig1.savefig("../FIGS/util_tr2.png", bbox_inches='tight',dpi=150)















