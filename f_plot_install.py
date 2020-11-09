#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
"""
plot module.
plot the results, i.e capacity installed and dispatches.

@author: jinxi
"""
#  
import sys
sys.path.append('C:\PhD_Chalmers\Python\Lib\site-packages') ## adding directory
import pdb
# ~ pdb.set_trace()
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def func_plot_install(df_installed,title):
    fig = plt.figure(figsize=(12,6)) ##set the size of the figure.
    
    ## read-in the data
    cap_coal = df_installed.loc['coal'].to_numpy()/10**6 ##KW to GW (division of 10**6)
    cap_gas = df_installed.loc['gas'].to_numpy()/10**6
    cap_nuclear = df_installed.loc['nuclear'].to_numpy()/10**6
    cap_solar = df_installed.loc['solar'].to_numpy()/10**6
    cap_wind = df_installed.loc['wind'].to_numpy()/10**6
    
    ##set parameters of the stack bar plot.
    N = len(cap_coal)## nr of bars.
    ind = np.arange(N)+ 1 ## the x locations for the groups, start year from 1 instead of 0.
    width = 0.9      # the width of the bars.
    
    bar_gas = cap_coal##gas bars are on top of coal bars.
    bar_solar = np.add(cap_coal,cap_gas)
    bar_wind = np.add(bar_solar,cap_solar)
    bar_nuclear = np.add(bar_wind,cap_wind)
    
    p_coal = plt.bar(ind, cap_coal, width,color='saddlebrown')
    p_gas = plt.bar(ind, cap_gas, width, bottom = bar_gas, color='slateblue')
    p_solar = plt.bar(ind, cap_solar, width, bottom = bar_solar, color='gold')
    p_wind = plt.bar(ind, cap_wind, width, bottom = bar_wind, color='olivedrab')
    p_nuclear = plt.bar(ind, cap_nuclear, width, bottom = bar_nuclear, color='silver')
    
    ##set parameters of the figure.
    plt.legend((p_nuclear[0], p_wind[0],p_solar[0], p_gas[0] ,p_coal[0]), ('nuclear','wind','solar', 'gas','coal'), framealpha=0,loc='upper left')
    
    plt.xlabel('year', fontsize=12)
    plt.xticks(np.arange(0, 70, 5)) 
    # ~ plt.xticks(ind, fontsize=8)
    plt.ylabel('GW', fontsize=14)
    # ~ plt.ylim(0,40) ##set y-axis range.
    plt.title(str(title), fontsize=14)
    plt.grid(axis='y')
   
    plt.show()
    plt.clf()
    plt.close()
    # ~ plt.savefig("output/figures/installed", dpi=600)
    # ~ plt.ticklabel_format(axis='y', style='sci', scilimits=(0,3), useMathText=True)
    # ~ plt.yticks(np.arange(0, ymax, ymax/10))
    return p_coal,p_gas,p_solar,p_wind,p_nuclear


