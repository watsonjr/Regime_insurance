# -*- coding: utf-8 -*-

import numpy as np
from matplotlib import pyplot as plt

# plt.rc('font', **{'family': 'sans-serif', 'sans-serif': ['Helvetica']})
# plt.rc('text', usetex=True)
"ECOLOGICAL PARAMETERS"
r = 1
K = 10

"UTILITY PARAMETERS CASE 1"
a = 3 # importance of adaptation (range of reasonable outcomes)
m = 5
n = 1/2

"UTILITY PARAMETERS CASE 2"
m_tr = 23/4
n_tr = 1/10
a_tr = 5

"PAYOFFS"
env = np.linspace(0,10,200)
pi_adapt = m + n * env
pi_trans = m_tr + n_tr * env

"FRACTION OF PAYOFF REALIZED AS UTILITY"
maladaptation = np.linspace(-7,7,1000)
util_adapt = np.exp(-np.log(2)*(maladaptation)**2/(a**2)) 
util_trans = np.exp(-np.log(2)*(maladaptation)**2/(a_tr**2))

"UTILITY"
current_adapt = 7
current_env = np.linspace(0,10,200)
adapt_realized_U = (m + n * current_env)*(np.exp(-np.log(2)*(current_adapt-current_env)**2/(a**2)))
trans_realized_U = (m_tr + n_tr * current_env)*(np.exp(-np.log(2)*(current_adapt-current_env)**2/(a_tr**2)))

"PLOT OPTIONS"
opacity=1
linwid = 3
color1 = '#009175'
color2 = '#da00fd'

"PLOTS"
fig3 = plt.figure(figsize=(5.5,5.5))

cx_1 = fig3.add_subplot(221)
cx_2 = fig3.add_subplot(222)
cx_3 = fig3.add_subplot(212)

cx_1.plot(env, pi_adapt,label="Case 1",linewidth=linwid, alpha=opacity,color=color1)
cx_1.plot(env,pi_trans,label='Case 2',linewidth=linwid, alpha=opacity,color=color2)

cx_2.plot(maladaptation,util_adapt,label='Case 1',linewidth=linwid, alpha=opacity,color=color1)
cx_2.plot(maladaptation,util_trans,label='Case 2',linewidth=linwid, alpha=opacity,color=color2)

cx_3.plot(current_env,adapt_realized_U,label="Case 1",linewidth=linwid, alpha=opacity,color=color1)
cx_3.plot(current_env,trans_realized_U,label="Case 2",linewidth=linwid, alpha=opacity,color=color2)
cx_3.plot((current_adapt,current_adapt),(0,10),"--k",linewidth=3)

"LABELS"
cx_1.set_xlabel('Environmental state, $x$');
cx_1.set_ylabel('Payoff, $\pi(x)$');
cx_1.legend()

cx_2.set_xlabel('Degree of maladaptation, $x-y$');
cx_2.set_ylabel('Frac. of payoff realized');


cx_3.set_xlabel('Environmental state, $x$ ');
cx_3.set_ylabel('Realized utility, $U(x,y)$')
cx_3.text(current_adapt-.4, .5, 'Adaptation state, $y$', fontsize=12,rotation=90);
cx_3.set_ylim(0,10)
cx_3.set_xlim(0,10);
fig3.tight_layout()

fig3.text(0.035, .95, 'a',weight='bold', fontsize = 14)
fig3.text(.5, .95, 'b', weight='bold',fontsize = 14)
fig3.text(.035, .46, 'c', weight='bold',fontsize = 14)

"SAVE FIGS"
save = False
if save == True:
    fig3.savefig("../FIGS/utilFunction.pdf", dpi=150)
    fig3.savefig("../FIGS/utilFunction.png", dpi=150)
