# -*- coding: utf-8 -*-


import numpy as np
from matplotlib import pyplot as plt
# plt.rc('font', **{'family': 'sans-serif', 'sans-serif': ['Helvetica']})
# plt.rc('text', usetex=True)
"PARAMETERS"
K = 10
h = 1
r = 1
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

"DEFINE REGIME Boundaries"
R_12 = c_Vals[np.nanargmax(eq[:,2])]
R_23 = c_Vals[np.nanargmin(eq[:,0])]

"MAKE PLOTS"

ratio  = np.sqrt(2)
scale = 3

fig2 = plt.figure(figsize=(ratio*scale,scale))
ax_1 = fig2.add_subplot(111)

ax_1.plot((R_12,R_12),(0,11),'k',alpha=.4,linewidth = 1.25)
ax_1.plot((R_23,R_23),(0,11),'k',alpha=.4,linewidth = 1.25)
ax_1.plot(c_Vals,eq[:,0], color='k',linewidth = 2.5)
ax_1.plot(c_Vals,eq[:,2], color='k', label='Stable',linewidth = 2.5)
ax_1.plot(c_Vals,eq[:,1], 'k--', label='Unstable',linewidth = 2.5)
ax_1.plot(c_Vals,eq[:,3], 'k--',linewidth = 2.5)

"ADD TEXT"
ax_1.text(1.15, 9.75, 'Regime 1', fontsize = 10)
ax_1.text(1.93, 9.75, 'Regime 2', fontsize = 10)
ax_1.text(2.85, 9.75, 'Regime 3', fontsize = 10)

ax_1.set_ylim((-.05,11));
ax_1.set_xlim((1,3.6));

ax_1.set_xlabel('Extraction rate, $c$')
ax_1.set_ylabel('Environmental state, $x$');
ax_1.legend(loc='lower right', bbox_to_anchor=(1, 0.05))



"SAVE FIGS"
save = False

if save == True:
    fig2.savefig("../FIGS/basins.pdf", bbox_inches='tight',dpi=150)
    fig2.savefig("../FIGS/basins.png", bbox_inches='tight',dpi=1500)