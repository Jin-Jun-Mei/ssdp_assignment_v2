#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
"""
plot module.
plot the results, i.e capacity installed and dispatches.

@author: jinxi
"""
#  
#import sys
#sys.path.append('C:\PhD_Chalmers\Python\Lib\site-packages') ## adding directory
import pdb
# ~ pdb.set_trace()
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


from f_plot_install import func_plot_install
from f_plot_dispatch import func_plot_dispatch

if __name__ == "__main__": 
    ##1.plot installed capacity
    file_path1 = "output/tables/installed/"
    file_name1 = "installed_homo_0309.xlsx"
    sheet_name1 = "Sheet1"
    
    df_InstallCapacity = pd.read_excel(io=file_path1+file_name1,sheet_name=sheet_name1,index_col=0) ##first column as index.
    func_plot_install(df_InstallCapacity,title="Installed Capacity- homogeneous case (r=0.8)")
    
    ##2.plot dispatched electricity
    file_path2 = "output/tables/dispatched/"
    file_name2 = "annual_el_dispatch_0309.xlsx"
    sheet_name2 = "Sheet2"
    df_dispatch = pd.read_excel(io=file_path2+file_name2,sheet_name=sheet_name2,index_col=0) ##first column as index.
    # ~ func_plot_dispatch(df_dispatch,title="Dispatched Electricity- homogeneous case (r=0.8)")

     ######plot with biogas##########
    file_path2 = "output/tables/dispatched/"
    file_name2 = "annual_el_dispatch.xlsx"
    sheet_name2 = "Sheet2"
    # ~ df_dispatch = pd.read_excel(io=file_path2+file_name2,sheet_name=sheet_name2,index_col=0) ##first column as index.
    # ~ func_plot_dispatch(df_dispatch,title="Dispatched Electricity - homogenous case")
    # ~ df_dispatch.T.plot(kind="bar", stacked=True) ##can directly plot from df.
    plt.show()

