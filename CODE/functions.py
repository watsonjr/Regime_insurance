# -*- coding: utf-8 -*-
"""
Created on Fri Jul  1 09:12:15 2022

@author: AndrewTilman
"""

import numpy as np
# from multiprocessing import Pool

def dfdt(x,y1,y2,y3,P,c):
    
    dt = P['dt']
    r = P['r']
    K = P['K']
    h = P['h']
    mu = P['mu']
    sigma = P['sigma']
    l1 = P['l_low']
    l2 = P['l_mid']
    l3 = P['l_high']
    

    #! Growth
    x_r = (r*x)*(1-(x/K))
    
    #! Grazing
    x_g = c * np.divide( pow(x,2),(pow(x,2) + pow(h,2)))
    
    #! dW White noise
    noise = np.random.normal(mu,sigma,1)
    dW = sigma*x*noise

    #! time step change
    dx = (x_r - x_g + dW)*dt
    dy1 = l1 * (x - y1)*dt
    dy2 = l2 * (x - y2)*dt
    dy3 = l3 * (x - y3)*dt
    
    return dx, dy1, dy2, dy3

def dTime_multi(x,i,y1,y2,y3,P,c): 
    beta = P['beta']
    T = P['T']
    
    # Growth and grazing
    [dx , dy1 , dy2 , dy3] = dfdt(x,y1,y2,y3,P,c)
    
    # red noise
    noise = np.random.normal(0,beta,1)
    i = ((1-1/T)*i+noise)
    
    # new state
    x = np.maximum(x + dx + i*x,0)
    y1 = y1 + dy1
    y2 = y2 + dy2
    y3 = y3 + dy3
    return x,i,y1,y2,y3

def run_model_flickering(INIT_X,P):
    c = P['c']
    i0 = P['i0']
    NUMSTEPS=P['NUMSTEPS']
    y0 = P['y0']
    a = P['a']
    m = P['m']
    n = P['n']
    
    x = np.zeros((NUMSTEPS+1))
    y = np.zeros((NUMSTEPS+1))
    pi = np.zeros(NUMSTEPS)
    util = np.zeros((NUMSTEPS))
    i = np.zeros((NUMSTEPS+1))
    x[0] = INIT_X
    i[0] = i0
    y[0] = y0
    
    for step in np.arange(0,NUMSTEPS):
     
        pi[step] = m + n*x[step]
        
        #util[step] = pi[step]*np.exp(-a*np.abs(x[step] - y[step])) #exponential decay for maladaptation
        util[step] = pi[step]*np.exp(-np.log(2)*(x[step] - y[step])**2/(a**2)) #gaussian fn to govern maladaptation
        
        [x[step+1],i[step+1],Temp, y[step+1], temp] = dTime_multi(x[step],i[step],0,y[step],0,P,c)
        
    return x,i,y,util,pi

def run_flickering_c_sweep(INIT_X,P):
    c_sweep = P['c_sweep']
    i0 = P['i0']
    NUMSTEPS=P['NUMSTEPS']
    y0 = P['y0']
    a = P['a']
    m = P['m']
    n = P['n']
    
    x = np.zeros((NUMSTEPS+1))
    y = np.zeros((NUMSTEPS+1))
    pi = np.zeros(NUMSTEPS)
    util = np.zeros((NUMSTEPS))
    i = np.zeros((NUMSTEPS+1))
    x[0] = INIT_X
    i[0] = i0
    y[0] = y0
    
    for step in np.arange(0,NUMSTEPS):
     
        pi[step] = m + n*x[step]
        
        #util[step] = pi[step]*np.exp(-a*np.abs(x[step] - y[step])) #exponential decay for maladaptation
        util[step] = pi[step]*np.exp(-np.log(2)*(x[step] - y[step])**2/(a**2)) #gaussian fn to govern maladaptation
        
        [x[step+1],i[step+1],y[step+1], temp, temp] = dTime_multi(x[step],i[step],y[step],0,0,P,c_sweep[step])
        
    return x,i,y,util,pi

def flickering_util(PARS):
    INIT_X = PARS['INIT_X']
    c = PARS['c']
    i0 = PARS['i0']
    NUMSTEPS=PARS['NUMSTEPS']
    y0 = PARS['y0']
    a = PARS['a']
    m = PARS['m']
    n = PARS['n']
    K = PARS['K']
    h = PARS['h']
    r = PARS['r']
    p=[-1/K,1,-(h**2/K+c/r),h**2,0]
    eq_temp = np.roots(p)
    for j in range(len(eq_temp)):
        if np.abs(np.imag(eq_temp[j])) > .05:
            eq_temp[j] = np.nan
    eq = np.real(eq_temp)
    x = np.zeros((NUMSTEPS+1))
    y1 = np.zeros((NUMSTEPS+1))
    y2 = np.zeros((NUMSTEPS+1))
    y3 = np.zeros((NUMSTEPS+1))
    pi = np.zeros(NUMSTEPS)
    util1 = np.zeros((NUMSTEPS))
    util2 = np.zeros((NUMSTEPS))
    util3 = np.zeros((NUMSTEPS))
    util4 = np.zeros((NUMSTEPS))
    util5 = np.zeros((NUMSTEPS))
    i = np.zeros((NUMSTEPS+1))
    x[0] = INIT_X
    i[0] = i0
    y1[0] = y0
    y2[0] = y0
    y3[0] = y0
    y4 = eq[0]
    y5 = eq[2]
    
    for step in np.arange(0,NUMSTEPS):
        #current Util
        pi[step] = m + n*x[step]
        #util[step] = pi[step]*np.exp(-a*np.abs(x[step] - y[step])) #exponential decay for maladaptation
        util1[step] = pi[step]*np.exp(-np.log(2)*(x[step] - y1[step])**2/(a**2)) #gaussian fn to govern maladaptation
        util2[step] = pi[step]*np.exp(-np.log(2)*(x[step] - y2[step])**2/(a**2)) #gaussian fn to govern maladaptation
        util3[step] = pi[step]*np.exp(-np.log(2)*(x[step] - y3[step])**2/(a**2)) #gaussian fn to govern maladaptation
        util4[step] = pi[step]*np.exp(-np.log(2)*(x[step] - y4)**2/(a**2)) #gaussian fn to govern maladaptation
        util5[step] = pi[step]*np.exp(-np.log(2)*(x[step] - y5)**2/(a**2)) #gaussian fn to govern maladaptation

        #dynamics
        [x[step+1],i[step+1] , y1[step+1] ,y2[step+1],y3[step+1]] = dTime_multi(x[step],i[step],y1[step],y2[step],y3[step],PARS,c)

    avg_pi = np.average(pi)
    avg_util1 = np.average(util1)
    avg_util2 = np.average(util2)
    avg_util3 = np.average(util3)
    avg_util4 = np.average(util4)
    avg_util5 = np.average(util5)
    
    return avg_util1, avg_util2, avg_util3, avg_pi, avg_util4, avg_util5

def flickering_util_trans(PARS):
    INIT_X = PARS['INIT_X']
    c = PARS['c']
    i0 = PARS['i0']
    NUMSTEPS=PARS['NUMSTEPS']
    y0 = PARS['y0']
    a = PARS['a']
    m = PARS['m']
    n = PARS['n']
    m_tr = PARS['m_tr']
    n_tr = PARS['n_tr']
    a_tr = PARS['a_tr']
    
    x = np.zeros((NUMSTEPS+1))
    y1 = np.zeros((NUMSTEPS+1))
    y2 = np.zeros((NUMSTEPS+1))
    util_a = np.zeros((NUMSTEPS))
    util_tr = np.zeros((NUMSTEPS))
    pi_a = np.zeros((NUMSTEPS))
    pi_tr = np.zeros((NUMSTEPS))
    i = np.zeros((NUMSTEPS+1))
    x[0] = INIT_X
    i[0] = i0
    y1[0] = y0
    y2[0] = y0

    
    for step in np.arange(0,NUMSTEPS):
        #current Util
        pi_a[step] = m + n*x[step]
        pi_tr[step] = m_tr + n_tr*x[step]
        # pi_a[step] = m + n*c * np.divide( pow(x[step],2),(pow(x[step],2) + pow(h,2)))
        # pi_tr[step] = m_tr + n_tr*c * np.divide( pow(x[step],2),(pow(x[step],2) + pow(h,2)))
        #util[step] = pi[step]*np.exp(-a*np.abs(x[step] - y[step])) #exponential decay for maladaptation
        util_a[step] = pi_a[step]*np.exp(-np.log(2)*(x[step] - y1[step])**2/(a**2)) #gaussian fn to govern maladaptation
        util_tr[step] = pi_tr[step]*np.exp(-np.log(2)*(x[step] - y2[step])**2/(a_tr**2)) #gaussian fn to govern maladaptation

        #dynamics
        [x[step+1],i[step+1] , y1[step+1] ,y2[step+1], temp] = dTime_multi(x[step],i[step],y1[step],y2[step],0,PARS,c)

    avg_util_a = np.average(util_a)
    avg_util_tr = np.average(util_tr)
    avg_pi_a = np.average(pi_a)
    avg_pi_tr = np.average(pi_tr)

    
    return avg_util_a, avg_util_tr, avg_pi_a, avg_pi_tr

def dfdtSI(x,y1,y2,y3,y4,y5,P,c):
    
    dt = P['dt']
    r = P['r']
    K = P['K']
    h = P['h']
    mu = P['mu']
    sigma = P['sigma']
    l1 = P['l_1']
    l2 = P['l_2']
    l3 = P['l_3']
    l4 = P['l_4']
    l5 = P['l_5']    

    #! Growth
    x_r = (r*x)*(1-(x/K))
    
    #! Grazing
    x_g = c * np.divide( pow(x,2),(pow(x,2) + pow(h,2)))
    
    #! dW White noise
    noise = np.random.normal(mu,sigma,1)
    dW = sigma*x*noise

    #! time step change
    dx = (x_r - x_g + dW)*dt
    dy1 = l1 * (x - y1)*dt
    dy2 = l2 * (x - y2)*dt
    dy3 = l3 * (x - y3)*dt
    dy4 = l4 * (x - y4)*dt
    dy5 = l5 * (x - y5)*dt
    
    return dx, dy1, dy2, dy3, dy4, dy5

def dTime_multiSI(x,i,y1,y2,y3,y4,y5,P,c): 
    beta = P['beta']
    T = P['T']
    # Growth and grazing
    [dx , dy1 , dy2 , dy3, dy4, dy5] = dfdtSI(x,y1,y2,y3,y4,y5,P,c)
    
    # red noise
    noise = np.random.normal(0,beta,1)
    i = ((1-1/T)*i+noise)
    # new state
    x = np.maximum(x + dx + i*x,0)
    y1 = y1 + dy1
    y2 = y2 + dy2
    y3 = y3 + dy3
    y4 = y4 + dy4
    y5 = y5 + dy5
    return x,i,y1,y2,y3,y4,y5

def flickering_utilSI(PARS):
    INIT_X = PARS['INIT_X']
    c = PARS['c']
    i0 = PARS['i0']
    NUMSTEPS=PARS['NUMSTEPS']
    y0 = PARS['y0']
    a = PARS['a']
    m = PARS['m']
    n = PARS['n']
    K = PARS['K']
    h = PARS['h']
    r = PARS['r']
    p=[-1/K,1,-(h**2/K+c/r),h**2,0]
    eq_temp = np.roots(p)
    for j in range(len(eq_temp)):
        if np.abs(np.imag(eq_temp[j])) > .05:
            eq_temp[j] = np.nan
    eq = np.real(eq_temp)
    x = np.zeros((NUMSTEPS+1))
    y1 = np.zeros((NUMSTEPS+1))
    y2 = np.zeros((NUMSTEPS+1))
    y3 = np.zeros((NUMSTEPS+1))
    y4 = np.zeros((NUMSTEPS+1))
    y5 = np.zeros((NUMSTEPS+1))
    pi = np.zeros(NUMSTEPS)
    util1 = np.zeros((NUMSTEPS))
    util2 = np.zeros((NUMSTEPS))
    util3 = np.zeros((NUMSTEPS))
    util4 = np.zeros((NUMSTEPS))
    util5 = np.zeros((NUMSTEPS))
    util6 = np.zeros((NUMSTEPS))
    util7 = np.zeros((NUMSTEPS))
    
    i = np.zeros((NUMSTEPS+1))
    x[0] = INIT_X
    i[0] = i0
    y1[0] = y0
    y2[0] = y0
    y3[0] = y0
    y4[0] = y0
    y5[0] = y0
    y6 = eq[0]
    y7 = eq[2]
    
    for step in np.arange(0,NUMSTEPS):
        #current Util
        pi[step] = m + n*x[step]
        util1[step] = pi[step]*np.exp(-np.log(2)*(x[step] - y1[step])**2/(a**2)) #gaussian fn to govern maladaptation
        util2[step] = pi[step]*np.exp(-np.log(2)*(x[step] - y2[step])**2/(a**2)) #gaussian fn to govern maladaptation
        util3[step] = pi[step]*np.exp(-np.log(2)*(x[step] - y3[step])**2/(a**2)) #gaussian fn to govern maladaptation
        util4[step] = pi[step]*np.exp(-np.log(2)*(x[step] - y4[step])**2/(a**2)) #gaussian fn to govern maladaptation
        util5[step] = pi[step]*np.exp(-np.log(2)*(x[step] - y5[step])**2/(a**2)) #gaussian fn to govern maladaptation
        util6[step] = pi[step]*np.exp(-np.log(2)*(x[step] - y6)**2/(a**2)) #gaussian fn to govern maladaptation
        util7[step] = pi[step]*np.exp(-np.log(2)*(x[step] - y7)**2/(a**2)) #gaussian fn to govern maladaptation

        #dynamics
        [x[step+1],i[step+1] , y1[step+1] ,y2[step+1],y3[step+1],y4[step+1],y5[step+1]] = dTime_multiSI(x[step],i[step],y1[step],y2[step],y3[step],y4[step],y5[step],PARS,c)

    avg_pi = np.average(pi)
    avg_util1 = np.average(util1)
    avg_util2 = np.average(util2)
    avg_util3 = np.average(util3)
    avg_util4 = np.average(util4)
    avg_util5 = np.average(util5)
    avg_util6 = np.average(util6)
    avg_util7 = np.average(util7)
    
    return  avg_pi, avg_util1, avg_util2, avg_util3, avg_util4, avg_util5,avg_util6, avg_util7
