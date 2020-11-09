##function calculate dispatch and electrcity price of each slice.
import pandas as pd
import numpy as np
from p_plant import df_MarginalCost,pp_list,fuel_cost
from p_slice import demand_level,pp_avail_slice,slice_hours
from f_demand_supply2 import func_demand_supply2
from p_sys import CarbonTax_lst

def func_dispatch(annaul_capacity):
    yr = annaul_capacity.name ##which year.
    # ~ print('year is', yr)
    df_Cap_Cost = pd.concat([annaul_capacity, df_MarginalCost.iloc[:,yr]], axis=1,sort= True,copy=False, ignore_index=True) ##df1 and df2 concating: df2=df_MarginalCost.iloc[:,yr]
    # ~ print('df_Cap_Cost: ' ,df_Cap_Cost)
    df_Cap_Cost.rename(columns={0: "capacity", 1: "marginal_cost"},inplace=True, copy=False)##re-name the column names.
    df_Cap_Cost['avail_capacities'] = [df_Cap_Cost.loc[df_Cap_Cost.index == pp, 'capacity'].values * pp_avail_slice[pp] for pp in pp_list]
    # ~ df_pp_grouped['avail_capacities'] = [df_pp_grouped.loc[df_pp_grouped['plant_type'] == pp, 'capacity'].values * pp_avail_slice[pp] for pp in plant_order]
    fuel_cost_NatGas = fuel_cost['natural_gas']+ CarbonTax_lst[yr] * 0.00045##0.00045=gas_pp['emission_intensity']        
    df_Cap_Cost.loc['gas', 'marginal_cost'] = min(fuel_cost_NatGas,fuel_cost['biogas']) ##choose fuel type for running gas pp.
         
    df_Cap_Cost.sort_values('marginal_cost',inplace=True)
    # ~ df_Cap_Cost.reset_index(drop=False,inplace=True)   

    plant_order = df_Cap_Cost.index.tolist()
    # ~ print('\n' + 'plant_order: ' ,plant_order)
    maginal_cost_order = df_Cap_Cost['marginal_cost'].tolist()
    AvailCapacity_lst=df_Cap_Cost['avail_capacities'].tolist()
    avail_capacity_slice = list(zip(AvailCapacity_lst[0],AvailCapacity_lst[1],AvailCapacity_lst[2],AvailCapacity_lst[3],AvailCapacity_lst[4]))

    # ~ eq_price,last_dispatch_type,last_dispatch_amount,last_dispatch_percent = np.array([func_demand_supply2(supply,demand,plant_order,maginal_cost_order) for supply,demand in zip(avail_capacity_slice,demand_level)])
    res = np.array([func_demand_supply2(supply,demand,plant_order,maginal_cost_order) for supply,demand in zip(avail_capacity_slice,demand_level)])
    slice_ppProduction = [x[0] for x in res]##the first return element is production from each type pp.
    slice_price = [x[1] for x in res] ##the second element is price.
    slice_tot_Production = [x[2] for x in res] ##the third element is equilibrium production (production from all plants).
    
    avg_price_yr = sum(np.array(slice_tot_Production) * np.array(slice_price) * slice_hours)/ sum(np.array(slice_tot_Production)*slice_hours)

    # ~ dispatch_slice = {}
    dispatch_yr= {}
    cashIn_sys_yr = {}
    for pp in pp_list:
        dispatch_hr = np.array([x[pp] for x in slice_ppProduction])## production data.
        dispatch_slice = np.multiply(dispatch_hr,slice_hours)##KWh
        dispatch_yr[pp] = np.sum(np.multiply(dispatch_slice,slice_hours))
        
        revenue_yr = np.sum(dispatch_slice * slice_price)
        produceCost_yr = np.sum(dispatch_slice * df_Cap_Cost.loc[pp,'marginal_cost'])
        cashIn_sys_yr[pp] = revenue_yr - produceCost_yr
        
    return dispatch_yr,avg_price_yr,cashIn_sys_yr

