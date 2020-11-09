#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
##  p_slice.py
##================================================
import sys
#sys.path.append('C:\PhD_Chalmers\Python\Lib\site-packages') ## adding directory
import pandas as pd

if __name__ == "p_slice":
    df_slice_params = pd.read_excel("input/slice_param.xlsx",sheet_name="slice_params",header=0,index_col=0)
    demand_level = df_slice_params.loc['demand_level'].values
    slice_hours = df_slice_params.loc['slice_hours'].values
    

    avail_coal = df_slice_params.loc['coal_level'].values
    avail_gas = df_slice_params.loc['gas_level'].values
    avail_nuclear = df_slice_params.loc['nuclear_level'].values
    avail_solar = df_slice_params.loc['solar_level'].values
    avail_wind = df_slice_params.loc['wind_level'].values

    pp_avail_slice = {'coal':avail_coal,'gas':avail_gas,'nuclear':avail_nuclear,'solar':avail_solar,'wind':avail_wind}


    # ~ print(avail_wind)

# ~ comp0_initial_PP = pd.read_excel("input/company_initial_profile.xlsx",sheet_name="input_initial_500",header=1)
# ~ comp0_initial_PP = comp0_initial_PP.groupby('plant_type',as_index=False).agg({'capacity':'sum'})
# ~ aa = comp0_initial_PP['plant_type'].tolist()
# ~ print([aa]*64)
