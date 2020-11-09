#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
##  plant_params.py
##================================================
# ~ capacity ## unit:KWe
# ~ running_cost ## unit: cent/kWh
# ~ investment_cost ## unit: cent = cent/KW * KW
# ~ lifetime ## unit:year
# ~ emission_intensity ## unit: ton CO2eq/kWh
##================================================

import pandas as pd
from p_sys import CarbonTax_lst ,hurdle_r as h_r

pp_list =['coal','gas','nuclear','solar','wind']
##================================================
coal_pp = {'plant_type': 'coal', 'capacity':500*10**3,'running_cost': 2,'investment_cost':145000*500*10**3,'lifetime':40,'emission_intensity':0.001}
gas_pp = {'plant_type': 'gas', 'capacity':500*10**3,'running_cost': 4.5,'investment_cost':90000*500*10**3,'lifetime':30,'emission_intensity':0.00045}
nuclear_pp = {'plant_type': 'nuclear', 'capacity':500*10**3,'running_cost': 1,'investment_cost':600000*500*10**3,'lifetime':40,'emission_intensity':0}
solar_pp = {'plant_type': 'solar', 'capacity':500*10**3,'running_cost': 0,'investment_cost':80000*500*10**3,'lifetime':25,'emission_intensity':0}
wind_pp = {'plant_type': 'wind', 'capacity':500*10**3,'running_cost': 0,'investment_cost':150000*500*10**3,'lifetime':25,'emission_intensity':0}
##================================================
capacity = {'nuclear':500*10**3,'coal':500*10**3,'gas':500*10**3,'solar':500*10**3,'wind':500*10**3}
investment_cost = {'nuclear':600000*500*10**3,'coal':145000*500*10**3,'gas':90000*500*10**3,'solar':80000*500*10**3,'wind':150000*500*10**3}
lifetime = {'nuclear':40,'coal':40,'gas':30,'solar':25,'wind':25}
fuel_cost = {'biogas': 8,'nuclear':1,'coal':2,'natural_gas':4.5,'wind':0,'solar':0}
running_cost = {'nuclear':1,'coal':2,'gas':4.5,'wind':0,'solar':0}
emission_intensity = {'nuclear':0,'coal':0.001,'gas':0.00045,'solar':0,'wind':0}
##================================================

CRF_pp = {str(pp) : h_r*(1+h_r)**lifetime[pp]/((1+h_r)**lifetime[pp]-1) for pp in pp_list}
# ~ print(CRF_pp)
i_r=0.04
annuitized_cost={pp : investment_cost[pp]* (i_r/(1-(1+i_r)**-lifetime[pp])) for pp in pp_list}


marginal_cost = {}##marginal cost of each type of plant over years.
for pp in pp_list:
    marginal_cost[pp] = [running_cost[pp]+ CarbonTax * emission_intensity[pp] for CarbonTax in CarbonTax_lst]
marginal_cost['gas'] = [fuel_cost['biogas'] if cost >fuel_cost['biogas'] else cost for cost in marginal_cost['gas']]

df_MarginalCost=pd.DataFrame.from_dict(marginal_cost,orient='index')
mask = df_MarginalCost[df_MarginalCost.index == 'gas'] < fuel_cost['biogas'] ##if biogas is cheaper than Nat_gas.

df_MarginalCost.where(mask, fuel_cost['biogas'],inplace=True)##Entries where cond is False are replaced with corresponding value 
# ~ print(marginal_cost['gas'][52])
# ~ print(df_MarginalCost.iloc[:,30:55])
##end##
