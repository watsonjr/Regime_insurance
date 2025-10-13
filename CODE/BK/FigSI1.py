# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 09:01:02 2024

@author: AndrewTilman
"""

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

avg_util_l1 = np.zeros(sims)
avg_util_l2 = np.zeros(sims)
avg_util_l3 = np.zeros(sims)
avg_util_l4 = np.zeros(sims)
avg_util_l5 = np.zeros(sims)

avg_util_fixed_low = np.zeros(sims)
avg_util_fixed_high = np.zeros(sims)


avg_pi = np.zeros(sims)


"PARAMETER DICT"
A = np.empty((sims),dtype=dict)

for i in range(sims):
    # c_arr = np.linspace(c_sweep[i],c_sweep[i], NUMSTEPS)
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
            'l_1': 1,
            'l_2': .1,
            'l_3': .01,
            'l_4': .001,
            'l_5': .0001,
            'a':params_dict['a'],
            'm':params_dict['m'],
            'n':params_dict['n'],
            'm_tr':params_dict['m_tr'],
            'n_tr':params_dict['n_tr'],
            'a_tr':params_dict['a_tr']
              }


#%%
runSim1 = False

"SIMULATION 1: Adaptive capacity and flickering induced welfare collapse as well as consideration of fixed adaptation states"
if runSim1 == True:
    if __name__=='__main__':
        with Pool(7) as pool:        
            output = pool.map(fn.flickering_utilSI,A)
            
        for i in range(sims):
            avg_pi[i] = output[i][0]
            avg_util_l1[i] = output[i][1]
            avg_util_l2[i] = output[i][2]
            avg_util_l3[i] = output[i][3]
            avg_util_l4[i] = output[i][4]
            avg_util_l5[i] = output[i][5]
            avg_util_fixed_high[i] = output[i][6]
            avg_util_fixed_low[i] = output[i][7]
        np.save('../DATA/SIavgUtil_l1',avg_util_l1)
        np.save('../DATA/SIavgUtil_l2',avg_util_l2)
        np.save('../DATA/SIavgUtil_l3',avg_util_l3)
        np.save('../DATA/SIavgUtil_l4',avg_util_l4)
        np.save('../DATA/SIavgUtil_l5',avg_util_l5)
        np.save('../DATA/SIavgUtil_fixed_h',avg_util_fixed_high)
        np.save('../DATA/SIavgUtil_fixed_l',avg_util_fixed_low)
        np.save('../DATA/SIavgPi',avg_pi)
        np.save('../DATA/SIcSweep_1',params_dict['c_sweep'])
     

#%%

"PLOTS"

"Load data from Sim 1"
avg_util_l1 = np.load('../DATA/SIavgUtil_l1.npy')
avg_util_l2 = np.load('../DATA/SIavgUtil_l2.npy')
avg_util_l3 = np.load('../DATA/SIavgUtil_l3.npy')
avg_util_l4 = np.load('../DATA/SIavgUtil_l4.npy')
avg_util_l5 = np.load('../DATA/SIavgUtil_l5.npy')
avg_util_fixed_low = np.load('../DATA/SIavgUtil_fixed_l.npy')
avg_util_fixed_high = np.load('../DATA/SIavgUtil_fixed_h.npy')
avg_pi = np.load('../DATA/SIavgPi.npy')
c_sweep_1 = np.load('../DATA/SIcSweep_1.npy')



ratio  = np.sqrt(2)
scale = 3
fig0 = plt.figure(figsize=(ratio*scale,scale));
ax0 = fig0.add_subplot(111);
ax0.scatter(c_sweep_1,avg_pi,label='$\overline{\pi}$',color='#005745',s=12,alpha=.75);
ax0.scatter(c_sweep_1,avg_util_l2,label='$\overline{U}, (l = 0.1)$',color='#009175',s=12,alpha=.75);
ax0.scatter(c_sweep_1,avg_util_l3,label='$\overline{U}, (l = 0.01)$',color='#00cba7',s=12,alpha=.75);
ax0.scatter(c_sweep_1,avg_util_l4,label='$\overline{U}, (l = 0.001)$',color='#86ffde',s=12,alpha=.75);
ax0.scatter(c_sweep_1,avg_util_fixed_high,label='$\overline{U}$, high EQ',color='#8400cd',s=12,alpha=.75);
ax0.scatter(c_sweep_1,avg_util_fixed_low,label='$\overline{U}$, low EQ',color='#ff92fd',s=12,alpha=.75);


ax0.plot((1.78,1.78),(0,11),'k',alpha=.4,linewidth = 2)
ax0.plot((2.6,2.6),(0,11),'k',alpha=.4,linewidth = 2)
ax0.set_ylabel('Average utility')
ax0.set_xlabel('Extraction rate, $c$')
ax0.set_xlim((c_sweep[0],c_sweep[-1]))
ax0.set_ylim((0,11))
ax0.legend(bbox_to_anchor=(1,0), loc="lower left")
ax0.text(.7, .35, 'Regime 1', fontsize = 10)
ax0.text(1.86, .35, 'Regime 2', fontsize = 10)
ax0.text(2.73,.35, 'Regime 3', fontsize = 10)

fig1 = plt.figure(figsize=(ratio*scale,scale));
ax1 = fig1.add_subplot(111);

ax1.scatter(c_sweep_1,avg_pi,label='$\overline{U}, (l = 1)$',color='#005745',s=12,alpha=.75);
ax1.scatter(c_sweep_1,avg_util_l2,label='$\overline{U}, (l = 0.1)$',color='#22816C',s=12,alpha=.75);
ax1.scatter(c_sweep_1,avg_util_l3,label='$\overline{U}, (l = 0.01)$',color='#43AB92',s=12,alpha=.75);
ax1.scatter(c_sweep_1,avg_util_l4,label='$\overline{U}, (l = 0.001)$',color='#65D5B8',s=12,alpha=.75);
ax1.scatter(c_sweep_1,avg_util_l5,label='$\overline{U}, (l = 0.0001)$',color='#86ffde',s=12,alpha=.75);

ax1.plot((1.78,1.78),(0,11),'k',alpha=.4,linewidth = 2)
ax1.plot((2.6,2.6),(0,11),'k',alpha=.4,linewidth = 2)
ax1.set_ylabel('Average utility')
ax1.set_xlabel('Extraction rate, $c$')
ax1.set_xlim((c_sweep[0],c_sweep[-1]))
ax1.set_ylim((0,11))
ax1.legend(bbox_to_anchor=(1,0), loc="lower left")
ax1.text(.7, .35, 'Regime 1', fontsize = 10)
ax1.text(1.86, .35, 'Regime 2', fontsize = 10)
ax1.text(2.73,.35, 'Regime 3', fontsize = 10)


"SAVE FIGS"
save = False

if save == True:
    fig0.savefig("../FIGS/utilFixedy.pdf",bbox_inches='tight')
    fig0.savefig("../FIGS/utilFixedy.png",bbox_inches='tight', dpi=1500)
    fig1.savefig("../FIGS/utilWideRange.pdf",bbox_inches='tight')
    fig1.savefig("../FIGS/utilWideRange.png",bbox_inches='tight', dpi=150)