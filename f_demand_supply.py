#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
demand_supply module.
calculate equilibrium prduction and price in each hour.

@author: jinxi
"""
from p_sys import eps,p0
import pdb

def func_demand_supply(supply_lst,q0,plant_order,marginal_cost):##q0 = demand
    # ~ print('\n' + 'The ranked_dispatch is: ' + str(plant_order))
    # ~ print('\n' + 'The demand_lst is: ' + str(q0))
    # ~ print('\n' + 'The marginal_cost is: ' + str(marginal_cost))
    # ~ print('\n' + 'The supply_lst is: ' + str(supply_lst))
    marginal_cost = [c for s,c in zip(supply_lst,marginal_cost) if s>0]##remove plant type has 0 capacity.
    plant_order = [p for s,p in zip(supply_lst,plant_order) if s>0]##remove plant type has 0 capacity.
    supply_lst = [s for s in supply_lst if s !=0 ]  
    
    
    total_avail_capacity = sum(supply_lst)
    # ~ print('\n' + 'The total_avail_capacity is: ' + str(total_avail_capacity))
    eq_production = 0
# =============================================================================
    for pos, pp_capacity in enumerate(supply_lst, start=0):
        # ~ print('\n' + 'The pos is: ' + str(pos))
        if pp_capacity == 0: continue
        eq_production += pp_capacity
        # ~ if eq_production == 0: continue
        demand_price = p0 * q0 ** (-1 / eps) * eq_production ** (1 / eps)
        
        if demand_price <= marginal_cost[pos]:
            eq_price = marginal_cost[pos]## means price will be the running cost of first type.
            eq_production = q0 * (eq_price / p0) ** eps 
            break
            
        else: ##if demand_price > run_costs[i]
            eq_price = demand_price
            # ~ if eq_price <= marginal_cost[pos+1]:
                
            if total_avail_capacity - eq_production > 0 and demand_price > marginal_cost[pos+1]:
                # ~ print('continue')
                continue
                ## first if :## if there is still remaining/unruned production/plants.second if: check if on the vertical line
            else: break ## if demand_price <= run_costs[i+1] or total_avail_capacity=max
    
    last_dispatch_type = plant_order[pos]  ##get the name of the last supply plant type.
    last_tp_dispatch_amount = eq_production - sum(supply_lst[0:pos])##dispatch amount from the last running type.
    last_dispatch_avail = supply_lst[pos] #available capacity of the last running type.

    # ~ print('\n' + 'last_tp_dispatch_amount is : ' + str(last_tp_dispatch_amount))
    # ~ print('\n' + 'Thelast_dispatch_type is: ' + str(last_dispatch_type))
    # ~ print('\n' + 'The eq_production is: ' + str(eq_production))
    
    return eq_price#,last_supply_percent,last_dispatch_type,eq_production
