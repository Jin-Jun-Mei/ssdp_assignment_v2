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

from p_plant import df_MarginalCost,pp_list

def func_plot_dispatch(df_dispatch,title):
    fig = plt.figure(figsize=(14,6)) ##set the size of the figure.
    print(df_dispatch)
    ## read-in the data
    cap_coal = df_dispatch.loc['coal'].to_numpy()/10**9 ##KWh to TWh (division of 10**6)
    cap_ngas = df_dispatch.loc['natural_gas'].to_numpy()/10**9
    cap_nuclear = df_dispatch.loc['nuclear'].to_numpy()/10**9
    cap_solar = df_dispatch.loc['solar'].to_numpy()/10**9
    cap_wind = df_dispatch.loc['wind'].to_numpy()/10**9
    cap_bgas = df_dispatch.loc['biogas'].to_numpy()/10**9 ##biogas
    
    ##set parameters of the stack bar plot.
    N = len(cap_coal)## nr of bars.
    ind = np.arange(N)+ 1 ## the x locations for the groups, start year from 1 instead of 0.
    width = 1      # the width of the bars.
    
    bar_ngas = cap_coal##natural gas bars are on top of coal bars.
    bar_bgas = np.add(bar_ngas,cap_ngas)##biogas bars .
    bar_solar = np.add(bar_bgas,cap_bgas)
    bar_wind = np.add(bar_solar,cap_solar)
    bar_nuclear = np.add(bar_wind,cap_wind)
    
    
    p_coal = plt.bar(ind, cap_coal, width,color='saddlebrown')
    p_ngas = plt.bar(ind, cap_ngas, width, bottom = bar_ngas, color='slateblue')
    p_bgas = plt.bar(ind, cap_bgas, width, bottom = bar_bgas, color='pink')
    p_solar = plt.bar(ind, cap_solar, width, bottom = bar_solar, color='gold')
    p_wind = plt.bar(ind, cap_wind, width, bottom = bar_wind, color='olivedrab')
    p_nuclear = plt.bar(ind, cap_nuclear, width, bottom = bar_nuclear, color='silver')
    
    ##set parameters of the figure.
    plt.legend((p_nuclear[0], p_wind[0],p_solar[0], p_ngas[0] ,p_bgas[0] ,p_coal[0]), ('nuclear','wind','solar', 'natural gas', 'biogas','coal'), framealpha=0,loc='center left', bbox_to_anchor=(1, 0.5))
    
    plt.xlabel('year', fontsize=12)
    plt.xticks(np.arange(0, 70, 5)) 
    # ~ plt.xticks(ind, fontsize=8)
    plt.ylabel('TWh', fontsize=14)
    plt.ylim(0,520) ##set y-axis range.
    plt.title(str(title), fontsize=14)
    plt.grid(axis='y')
   
    plt.show()
    plt.clf()
    plt.close()
    # ~ plt.savefig("output/figures/installed", dpi=600)
    # ~ plt.ticklabel_format(axis='y', style='sci', scilimits=(0,3), useMathText=True)
    # ~ plt.yticks(np.arange(0, ymax, ymax/10))
    return p_coal,p_ngas,p_bgas,p_solar,p_wind,p_nuclear


