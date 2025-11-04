# -*- coding: utf-8 -*-

import importlib
import numpy as np
from matplotlib import pyplot as plt
import functions as fn
import parameters
# plt.rc('font', **{'family': 'sans-serif', 'sans-serif': ['Helvetica']})
# plt.rc('text', usetex=True)
#%%

"C VALUES FOR SIMULATION"
#c_vals = [ 1 ,   1.95,  2.45,  3.1   ]
c_vals = np.linspace(0.5,3.5,50)
frac = np.zeros(len(c_vals))

"PLOT OPTIONS"
golden  = np.sqrt(2)
scale = 6
linWidth = 2.5
opac = .75
fig1 = plt.figure(figsize=(scale*golden,scale))
ax1 = fig1.add_subplot(111)
#ax2 = fig1.add_subplot(222)
#ax3 = fig1.add_subplot(223)
#ax4 = fig1.add_subplot(224)
#AX = [ax1,ax2,ax3,ax4]

"RUN SIMULATIONS ONLY FOR CASES MARKED TRUE ABOVE"
for i in range(len(c_vals)):
    print(i)
    importlib.reload(parameters)
    from parameters import params_dict
    x0 = params_dict['INIT_X']
    params_dict['c'] = c_vals[i]
    #simTag = str(c_vals[i]).replace('.','')
    
    x_array, i_array, y_array, util_array, pi_array = fn.run_model_flickering(x0,params_dict)
    #np.save('../DATA/envData'+simTag,x_array)
    #np.save('../DATA/adapData'+simTag,y_array)
        
    "lOAD PLOT DATA"
    #env_array = np.load('../DATA/envData'+simTag+'.npy')
    #adap_array = np.load('../DATA/adapData'+simTag+'.npy')

    "QUANTIFY FRACTION OF TIME IN REGIME III"
    frac[i] = len(np.where(x_array<1.5)[0]) / len(x_array)

    "MAKE FIGS"
    #AX[i].plot(adap_array,label='Adaptation',color='k', linewidth = linWidth,alpha=opac)
    #AX[i].plot(env_array,label='Environment',color='#005745', linewidth = linWidth,alpha = opac)
    #AX[i].set_ylabel('Environmental state, $x$')
    #AX[i].set_xlabel('Time')
    #AX[i].set_ylim((-.05,20.05))
    #AX[i].set_title(str(frac*100)[0:4]+"%")
    
    t_start = 0;
    t_end = np.min((2000,params_dict['NUMSTEPS']));
    #AX[i].set_xlim(t_start,t_end);
#ax4.legend(loc='upper right')
ax1.plot(c_vals,frac,color='#005745', linewidth = linWidth,alpha = opac)
ax1.set_ylabel('Fraction of time spent in Regime III')
ax1.set_xlabel('Value of c (bifurcation parameter)')

#fig1.text(0.07, .87, 'a',weight='bold', fontsize = 16)
#fig1.text(.495, .87, 'b', weight='bold',fontsize = 16)
#fig1.text(.07, .46, 'c', weight='bold',fontsize = 16) 
#fig1.text(.495, .46, 'd', weight='bold',fontsize = 16)

"SAVE FIGS"
data = np.vstack((c_vals,frac)).transpose()
save = True
if save == True:
    fig1.savefig("../FIGS/prob_regimeIII.pdf",bbox_inches='tight')
    fig1.savefig("../FIGS/prob_regimeIII.png", bbox_inches='tight',dpi=1500)
    np.savetxt('../DATA/Data_prob.csv', data, delimiter=',', fmt='%s', header='c,p', comments='')

