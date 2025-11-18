import importlib
import numpy as np
from matplotlib import pyplot as plt
import functions as fn
import parameters as p
import sys
import pandas as pd


def main(THRESHOLD, NUMSTEPS, c, window_size):
    x0 = 10
    p.params_dict['NUMSTEPS'] = NUMSTEPS 
    p.params_dict['c'] = c
    income_high = []
    income_low = []
    prob_high = []
    prob_low = []
    for r in p.params_dict['r_sweep']:
        p.params_dict['r'] = r
        x_array, i_array, y_array, util_array, pi_array = fn.run_model_flickering(x0,p.params_dict)
        income_array = fn.income(x_array,p.params_dict) 
        income_array_high_abundance = income_array[x_array>THRESHOLD].mean()
        income_array_low_abundance = income_array[x_array<=THRESHOLD].mean()
        prob_high_abundance = np.array(x_array>THRESHOLD).mean()
        prob_low_abundance = np.array(x_array<=THRESHOLD).mean()
        income_high.append(income_array_high_abundance)
        income_low.append(income_array_low_abundance)
        prob_high.append(prob_high_abundance)
        prob_low.append(prob_low_abundance)

    v_high = np.lib.stride_tricks.sliding_window_view(np.append(income_high, np.zeros(window_size-1)), window_size)
    v_low = np.lib.stride_tricks.sliding_window_view(np.append(income_low, np.zeros(window_size-1)), window_size)
    v_high = np.nanmean(v_high, axis=1)
    v_low = np.nanmean(v_low ,axis=1)

    p_low = np.lib.stride_tricks.sliding_window_view(np.append(prob_low, np.zeros(window_size-1)), window_size)
    p_low = np.nanmean(p_low ,axis=1)

    df = pd.DataFrame({'r': p.params_dict['r_sweep'],'c': p.params_dict['c'], 
                       'income_high': income_high, 'income_low': income_low,
                       'income_low_sliding_{w}'.format(w=window_size):v_low,
                       'income_high_sliding_{w}'.format(w=window_size):v_high,
                       'probability_low': prob_low, 
                       'probability_low_sliding_{w}'.format(w=window_size):p_low,})
    df.to_csv('DATA/income_c={c}.csv'.format(c=c))

    golden  = np.sqrt(2)
    scale = 6
    linWidth = 2.5
    opac = .75
    fig1 = plt.figure(figsize=(scale*golden,scale))
    ax1 = fig1.add_subplot(111)
    ax1.plot(df['r'],df['income_high'],color="#20A1B3", linewidth = linWidth,alpha = opac)
    ax1.plot(df['r'],df['income_low'],color="#f5ae50", linewidth = linWidth,alpha = opac)
    ax1.plot(df['r'],df['income_low_sliding_{w}'.format(w=window_size)],color="#bf720e", linewidth = linWidth,alpha = opac)
    ax1.plot(df['r'],df['income_high_sliding_{w}'.format(w=window_size)],color="#04526c", linewidth = linWidth,alpha = opac)
    ax1.set_ylabel('Income in high and low abundance regimes')
    ax1.set_xlabel('Growth rate (r)')
    ax1.set_title('Threshold = {THRESHOLD}, c = {c}'.format(THRESHOLD=THRESHOLD,c=c))
    fig1.savefig('FIGS/r_vs_income_c={c}.png'.format(c=c),bbox_inches='tight')

    fig2 = plt.figure(figsize=(scale*golden,scale))
    ax1 = fig2.add_subplot(111)
    ax1.plot(df['r'],df['probability_low'],color="#20A1B3", linewidth = linWidth,alpha = opac)
    ax1.plot(df['r'],df['probability_low_sliding_{w}'.format(w=window_size)],color="#04526c", linewidth = linWidth,alpha = opac)
    ax1.set_ylabel('Probablity of low abundnace regime')
    ax1.set_xlabel('Growth rate (r)')
    ax1.set_title('Threshold = {THRESHOLD}, c = {c}'.format(THRESHOLD=THRESHOLD,c=c))
    fig2.savefig('FIGS/r_vs_probability_c={c}.png'.format(c=c),bbox_inches='tight')
 
NUMSTEPS= int(sys.argv[1])
THRESHOLD= float(sys.argv[2])
c= float(sys.argv[3])
WINDOWSIZE = int(sys.argv[4])
main(THRESHOLD, NUMSTEPS,c,WINDOWSIZE)