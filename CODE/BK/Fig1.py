# -*- coding: utf-8 -*-


import numpy as np
from matplotlib import pyplot as plt
import matplotlib.patches as patches

# plt.rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
# plt.rc('font', **{'family': 'sans-serif', 'sans-serif': ['Helvetica']})
# plt.rc('text', usetex=True)
# plt.rcParams['text.latex.preamble']=[r"\usepackage{amsmath}"]
"PARAMETERS"
r = 1
K = 10
m = 5
n = 1/2



"PLOT OPTIONS"
opacity=.75
linwid = 3
fig = plt.figure(figsize=(4*np.sqrt(2),4*np.sqrt(2)))
ax0 = fig.add_subplot(211)
ax = fig.add_subplot(212)
style1 = "Simple, tail_width=0.5, head_width=4, head_length=8"
style2 = "Simple, tail_width=0.5, head_width=4, head_length=8"
kw1 = dict(arrowstyle=style1, color="k")
kw2 = dict(arrowstyle=style2, color="k",alpha=.2)

"DOUBLE WELL POTENTIAL"
x = np.linspace(-2,2.2,200)
v = .25*x**4 - x**2 - .3*x
ax0.plot(x,v,linewidth=linwid, alpha=opacity,color='k')

ax0.plot((-1), (-.17), 'o', color='#005838',markersize=20)
ax0.plot((1.1), (-.87), 'o', color='#005838',markersize=20,alpha=.4)
a1 = patches.FancyArrowPatch((-.8, 0), (.5, -.15),connectionstyle="arc3,rad=-.35",**kw1)
a2 = patches.FancyArrowPatch((1.1, -.6), (-.5, .5),connectionstyle="arc3,rad=.35",**kw2)
ax0.add_patch(a1)
ax0.add_patch(a2)

ax0.set_ylabel('Potential',fontsize='16')
ax0.set_xlabel('Environmental State',fontsize='16')
ax0.set_xticks([])
ax0.set_yticks([])



"UTILITY CURVES"
current_adapt1 = 2
current_adapt2 = 5
current_adapt3 = 8

env1 = np.linspace(0,10,200)
env2 = np.linspace(0,10,200)
env3 = np.linspace(0,10,200)

current_adapt = np.linspace(0,10,200)
U1 = (m + n * env1)*(np.exp(-np.log(2)*(current_adapt1-env1)**2/(1.2**2)))
U2 = (.66*m + n/2 * env2)*(np.exp(-np.log(2)*(current_adapt2-env2)**2/(3**2)))
U3 = (m + n * env3)*(np.exp(-np.log(2)*(current_adapt3-env3)**2/(2.5**2)))
ax.plot(env1,U1,label="Tech. 1",linewidth=linwid, alpha=.8,color='k')
ax.plot(env2,U2,label="Tech. 2",linewidth=linwid, alpha=.5,color='k')
ax.plot(env3,U3,label="Tech. 3",linewidth=linwid, alpha=.2,color='k')
ax.set_ylabel('Utility',fontsize='16')
ax.set_xlabel('Environmental State',fontsize='16')
ax.legend(loc=4)
ax.set_xticks([])
ax.set_yticks([])

fig.text(.08, .85, 'a',weight='bold', fontsize = 16)
fig.text(.08, .425, 'b', weight='bold',fontsize = 16)


"SAVE FIGS"
save = False
if save == True:
    fig.savefig("../FIGS/Concept.pdf",bbox_inches='tight', dpi=150)
    fig.savefig("../FIGS/Concept.png", bbox_inches='tight',dpi=150)
