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
            'r':.7, 
            'K': params_dict['K'],
            'c': params_dict['c_sweep'][i],
            'h': 2.1,
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
            'm':params_dict['m'],
            'n':params_dict['n'],
            'm_tr':params_dict['m_tr'],
            'n_tr':params_dict['n_tr'],
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
        np.save('../DATA/avgUtil_l1',avg_util_low)
        np.save('../DATA/avgUtil_m1',avg_util_mid)
        np.save('../DATA/avgUtil_h1',avg_util_high)
        np.save('../DATA/avgUtil_fixed_h1',avg_util_fixed_high)
        np.save('../DATA/avgUtil_fixed_l1',avg_util_fixed_low)
        np.save('../DATA/avgPi1',avg_pi)
        np.save('../DATA/cSweep_11',params_dict['c_sweep'])
     



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
        np.save('../DATA/avgUtil_a1',avg_util_a)
        np.save('../DATA/avgUtil_tr1',avg_util_tr)
        np.save('../DATA/avgPi_a1',avg_pi_a)
        np.save('../DATA/avgPi_tr1',avg_pi_tr)
        np.save('../DATA/cSweep_21',params_dict['c_sweep'])
#%%

"PLOTS"

"Load data from Sim 1"
avg_util_low = np.load('../DATA/avgUtil_l1.npy')
avg_util_mid = np.load('../DATA/avgUtil_m1.npy')
avg_util_high = np.load('../DATA/avgUtil_h1.npy')
avg_util_fixed_low = np.load('../DATA/avgUtil_fixed_l1.npy')
avg_util_fixed_high = np.load('../DATA/avgUtil_fixed_h1.npy')
avg_pi = np.load('../DATA/avgPi1.npy')
c_sweep_1 = np.load('../DATA/cSweep_11.npy')

"Load data from Sim 2"
avg_util_a = np.load('../DATA/avgUtil_a1.npy')
avg_util_tr = np.load('../DATA/avgUtil_tr1.npy')
avg_pi_a = np.load('../DATA/avgPi_a1.npy')
avg_pi_tr = np.load('../DATA/avgPi_tr1.npy')
c_sweep_2 = np.load('../DATA/cSweep_21.npy')


ratio  = np.sqrt(2)
scale = 3
fig0 = plt.figure(figsize=(ratio*scale,scale));
ax0 = fig0.add_subplot(111);
ax0.scatter(c_sweep_1,avg_pi,label='$\overline{\pi}$',color='#005745',s=12,alpha=.75);
ax0.scatter(c_sweep_1,avg_util_high,label='$\overline{U}, (l = 0.1)$',color='#009175',s=12,alpha=.75);
ax0.scatter(c_sweep_1,avg_util_mid,label='$\overline{U}, (l = 0.01)$',color='#00cba7',s=12,alpha=.75);
ax0.scatter(c_sweep_1,avg_util_low,label='$\overline{U}, (l = 0.001)$',color='#86ffde',s=12,alpha=.75);


ax0.set_xlabel('Extraction rate, $c$')
ax0.set_xlim((c_sweep[0],c_sweep[-1]))
ax0.set_ylim((0,10))


K = 10
h = 2.1
r = .7
c_Vals = np.linspace(0,4,num=10000)
eq = np.zeros((len(c_Vals),4))

i=0

"FIND EQUILIBRIA"

for i in range(len(c_Vals)):
    c = c_Vals[i]
    p=[-1/K,1,-(h**2/K+c/r),h**2,0]
    eq_temp = np.roots(p)
    for j in range(len(eq_temp)):
        if np.abs(np.imag(eq_temp[j])) > .025:
            eq_temp[j] = np.nan
    eq[i,:] = np.real(eq_temp)
ax0.plot(c_Vals,eq[:,0], color='k',linewidth = 2.5)
ax0.plot(c_Vals,eq[:,2], color='k', label='Env. EQ',linewidth = 2.5)
ax0.legend(bbox_to_anchor=(1,0), loc="lower left")


"SAVE FIGS"
save = False

if save == True:
    fig0.savefig("../FIGS/utility11.pdf",bbox_inches='tight')
    fig0.savefig("../FIGS/utility11.png",bbox_inches='tight', dpi=150)
















