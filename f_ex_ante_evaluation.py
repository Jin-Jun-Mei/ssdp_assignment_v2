## evaluate coal
import numpy as np
from f_demand_supply import func_demand_supply
from p_sys import hurdle_r as h_r
from p_slice import demand_level
from p_plant import investment_cost,lifetime,CRF_pp
import pdb
from multiprocessing import Pool
from p_slice import pp_avail_slice,slice_hours
# ~ from m_capacity_investment import file1

def func_ex_ante_evaluation (new_pp,plant_order,AvailCapacity_lst,maginal_cost_order): 
    new_pp_index = plant_order.index(new_pp)
    
    avail_capacity_new_pp = 500000 * pp_avail_slice[new_pp]
    AvailCapacity_lst[new_pp_index] += avail_capacity_new_pp
    
    avail_capacity_slice = list(zip(AvailCapacity_lst[0],AvailCapacity_lst[1],AvailCapacity_lst[2],AvailCapacity_lst[3],AvailCapacity_lst[4]))
    ##available capacity of each slice.
    # ~ print('avail_capacity_slice is ','\n',avail_capacity_slice)
    eq_price_lst = np.array([func_demand_supply(supply,demand,plant_order,maginal_cost_order) for supply,demand in zip(avail_capacity_slice,demand_level)])
    price_diff= eq_price_lst- maginal_cost_order[new_pp_index] ##electricity price minus the marginal cost of the plant.
    slice_profit = price_diff * avail_capacity_new_pp
    slice_profit = np.where(slice_profit < 0, 0, slice_profit)
    # ~ active_capacity =  avail_capacity_new_pp
    # ~ active_capacity = np.where(price_diff == 0, 500000/AvailCapacity_lst[new_pp_index]*500000, active_capacity)
    # ~ active_capacity = np.where(price_diff < 0, 0, active_capacity)
        
    annual_profit = (slice_profit * slice_hours).sum()
    
    if new_pp == 'wind':
        # ~ file1.write('electricity price is: '+ str(eq_price_lst)+'\n')
        # ~ file1.write('annual profit from wind is: '+ str(annual_profit)+'\n')
        # ~ print('electricity price is: '+ str(eq_price_lst)+'\n')
        # ~ print('annual profit from wind is: '+ str(annual_profit)+'\n')
        wind_produce = (slice_hours* avail_capacity_new_pp).sum()
        # ~ print('annual production from wind is: '+ str(wind_produce)+'\n')
        
    # ~ NPV_new_pp = annual_profit * (1-(1-h_r)**(1*lifetime[str(new_pp)])) / h_r - investment_cost[str(new_pp)]##NPV minus investment_cost
    NPV_new_pp = annual_profit * (1-(1+h_r)**(-1*lifetime[str(new_pp)])) / h_r - investment_cost[str(new_pp)]##NPV minus investment_cost
    # ~ NPV_profit = acc_profit_year * (1-(1-r)**new_pp.total_lifetime.item()) / r - new_pp.investment_cost.item() * new_pp.capacity.item() ##NPV minus investment_cost
        
    # ~ if NPV_new_pp >0 :
        # ~ NPV_CRF = NPV_new_pp * CRF_pp[new_pp]/investment_cost[str(new_pp)]
    # ~ else: NPV_CRF = -0
    NPV_CRF = NPV_new_pp * CRF_pp[new_pp]/investment_cost[str(new_pp)]
    # ~ print('plant tpye: ',new_pp,'NPV is: ',NPV_CRF)
    # ~ else: NPV_CRF = -0
    
    return (new_pp,NPV_CRF)
    
