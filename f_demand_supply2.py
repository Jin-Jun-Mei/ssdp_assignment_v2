
##demand_supply module2
## for dispatch calculation.

from p_sys import eps,p0
import pdb

def func_demand_supply2(supply_lst,q0,plant_order_all,marginal_cost):##q0 = demand
    ##remove the pp type with 0 capacity.
    marginal_cost = [c for s,c in zip(supply_lst,marginal_cost) if s>0]##remove plant type has 0 capacity.
    plant_order = [p for s,p in zip(supply_lst,plant_order_all) if s>0]##remove plant type has 0 capacity.
    supply_lst = [s for s in supply_lst if s !=0 ]  
    
    total_avail_capacity = sum(supply_lst)
    # ~ print('\n' + 'The total_avail_capacity is: ' + str(total_avail_capacity))
    
    eq_production = 0
# =============================================================================
    for pos, pp_capacity in enumerate(supply_lst, start=0):
        if pp_capacity == 0: continue
        eq_production += pp_capacity
        # ~ if eq_production == 0 or pp_capacity == 0: continue
        demand_price = p0 * q0 ** (-1 / eps) * eq_production ** (1 / eps)
        
        if demand_price <= marginal_cost[pos]:
            eq_price = marginal_cost[pos]## means price will be the running cost of first type.
            eq_production = q0 * (eq_price / p0) ** eps 
            break
            
        else: ##if demand_price > run_costs[i]
            eq_price = demand_price
            if total_avail_capacity - eq_production > 0 and demand_price > marginal_cost[pos+1]: continue
                ## first if :## if there is still remaining/unruned production/plants.second if: check if on the vertical line
            else: break ## if demand_price <= run_costs[i+1] or total_avail_capacity=max
    # ~ print('eq_price',eq_price)
   
    
    last_dispatch_type = plant_order[pos]  ##get the name of the last supply plant type.
    last_dispatch_amount = eq_production - sum(supply_lst[0:pos])##dispatch amount from the last running type.
    last_dispatch_avail = supply_lst[pos] #available capacity of the last running type.
    
    
    last_dispatch_percent = last_dispatch_amount/last_dispatch_avail
    # ~ print('last_dispatch_type', last_dispatch_type)
    # ~ print('last_dispatch_amount', last_dispatch_amount)
    # ~ print('last_dispatch_avail', last_dispatch_avail)
    
    production ={}
    for i in range(len(plant_order)):
        if pos > i: production[plant_order[i]]= supply_lst[i]
        elif pos == i:production[plant_order[i]] = last_dispatch_amount
        elif pos < i:production[plant_order[i]] = 0
    
    removed_plant = list(set(plant_order_all)-set(plant_order))
    # ~ print('removed_plant: ',removed_plant)
    for pp in removed_plant:
        production[pp]=0 ##removed plant has 0 capacity.
    
    return production,eq_price,eq_production#,last_dispatch_amount,last_dispatch_percent#,last_dispatch_type

# ~ print('production', production)
    
    # ~ pdb.set_trace()
