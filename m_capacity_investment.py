#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  main.py
# =============================================================================
import sys
sys.path.append('C:\PhD_Chalmers\Python\Lib\site-packages') ## adding directory
import pandas as pd
import datetime
import time
import pdb
# ~ pdb.set_trace()
import numpy as np
from copy import deepcopy
from itertools import repeat
from multiprocessing import Pool,freeze_support
from operator import itemgetter 

from p_slice import pp_avail_slice
from p_plant import pp_list,marginal_cost
from p_sys import CarbonTax_lst, hurdle_r 
from f_ex_ante_evaluation import func_ex_ante_evaluation

pd.set_option('display.precision',3) ##dismal digits.
pd.set_option('display.max_columns', 12)
pd.options.mode.chained_assignment = None

# =============================================================================
t6_start = time.perf_counter() 
##initialization
initial_pp = pd.read_excel("input/company_initial_profile.xlsx",sheet_name="initial_pp",header=1) #initial pp.
df_pp = deepcopy(initial_pp)
new_pp_chioce = pd.read_excel("input/company_initial_profile.xlsx",sheet_name="new_pp",header=1)

tot_time_step = 2
ts = 0
# ~ investment_series = []
# ~ rounds = 0
# ~ tick = 0
annual_capacity = []
capacity_invest = [] ##recod invest typr and year (plotting purpose).
# ~ file1 = open("record2.txt","a") 
# ~ file1.truncate(0)
# =============================================================================
if __name__ == "__main__":    
    
    while ts < tot_time_step:
        # ==================================================
        print('\n' + 'tot=' + str(tot_time_step) +'------Current year is ' + str(ts))
        # ~ file1.write('Current year is: '+str(ts)+'\n')

        annual_tot_invest = []
        df_pp.reset_index(drop=True,inplace=True) ## reset the index
     # =============================================================================    
    #   1.check decommission and lifetime -1.
        df_pp.lifetime_remain -= 1 ## the lifetime of each plant is subtract by 1. 
        df_next_year = df_pp.query('lifetime_remain > 0')##dismentle all retired plants.
        
        if (df_pp['lifetime_remain']==0).any(): ##if any plant reaches end of the lifetime.
            dicommision_list = df_pp[df_pp['lifetime_remain']==0].sample(frac=1) ##list the to-be-retire pp to a new df, and shuffle the order by .sample()
            # ~ print('dicommision_list of current year:')
            # ~ print(dicommision_list[['name','plant_type','lifetime_remain']])
        df_pp_grouped = df_pp.groupby('plant_type',as_index=False).agg({'capacity':'sum','running_cost':'mean','emission_intensity':'mean'})##group the pp by plant type.
        # ~ print('capacity at beginning of this year is')
        # ~ print(df_pp_grouped.capacity)
        # ~ file1.write('Current capacity is: '+str(df_pp_grouped.capacity)+'\n')
        
        
        ##=======record2 capacity for plotting================##
        # ~ df.to_dict()
        annual_capacity.append(df_pp_grouped['capacity'])
        
        # ~ print('annual_capacity is ','\n',annual_capacity)

        ##====================================================#
        
        # ~ df_pp_grouped['marginal_cost'] = df_pp_grouped['running_cost'] + carbon_tax * df_pp_grouped['emission_intensity'] 
        for pp in pp_list:
            df_pp_grouped.loc[df_pp_grouped['plant_type'] == pp, 'marginal_cost'] = marginal_cost[pp][ts+1]##cost of next year.
                
        df_pp_grouped.sort_values('marginal_cost',inplace=True)
        df_pp_grouped.reset_index(drop=False,inplace=True)
        
        plant_order = df_pp_grouped['plant_type'].tolist()
        maginal_cost_order = df_pp_grouped['marginal_cost'].tolist()
            
        
    # =============================================================================
    #   3.Making invest decisions.
        while True:
            df_pp_grouped['avail_capacities'] = [df_pp_grouped.loc[df_pp_grouped['plant_type'] == pp, 'capacity'].values * pp_avail_slice[pp] for pp in plant_order]
            # ~ print('\n' +'df_pp_grouped capacity before investment is :')
            # ~ print(df_pp_grouped.capacity,'\n')
            # ~ print(df_pp_grouped.loc[df_pp_grouped['plant_type'] == 'wind','avail_capacities'])
        # =============================================================================
            ##----------------decision-making------------------------------------##
            # ~ invest_made = func_decision_making(df_pp_grouped,carbon_tax,plant_order) ##investment function: take investment decisions.
            # ~ print('--------Start investment process.------------')
            AvailCapacity_lst = df_pp_grouped['avail_capacities'].tolist() ##of each slice.
            # ~ print('\n' + 'The avail_capacities is: ' + str(avail_capacities))
            ##calculate profit for new pp
            with Pool(8) as p: ##/ mp.cpu_count()=8.
                NPV_CRF_reslts = p.starmap(func_ex_ante_evaluation, zip(pp_list, repeat(plant_order), repeat(AvailCapacity_lst), repeat(maginal_cost_order)))
                p.close()
                p.join()
            NPV_CRF_reslts.sort(key=itemgetter(1), reverse=True)
            # ~ print('\n' + 'The NPV_CRF_reslts is: ' + str(NPV_CRF_reslts))
            # ~ file1.write(str(NPV_CRF_reslts))
            # ~ file1.write('\n')
            # ~ file1.write('the NPVs are: '+str(NPV_CRF_reslts)+'\n')
            
            if NPV_CRF_reslts[0][1]> 0:
                # ~ print('\n' + 'The NPV_CRF_reslts[0][1] is: ' + str(NPV_CRF_reslts[0][1]))
                invest_made = NPV_CRF_reslts[0][0]
                # ~ file1.write('investment made is: '+str(invest_made)+'\n')
                df_pp_grouped.loc[df_pp_grouped['plant_type'] == invest_made,'capacity'] += 500000 ##add capacity of invested plant.
                print('\n' + 'invest_made is: ', invest_made)
                print('\n' + 'the df_pp_grouped after investment is ', '\n',df_pp_grouped['capacity'])

                annual_tot_invest.append(new_pp_chioce.loc[new_pp_chioce['plant_type'] == invest_made])
                capacity_invest.append((invest_made,ts))
                # ~ print('investment continue')
                continue
            
            
            else:
                invest_made = None
                # ~ file1.write('investment made is: '+str(invest_made)+'\n')
                # ~ print('investment is none')
                # ~ if invest_made is None:
                if (dicommision_list['lifetime_remain']==0).any():##if more pp needs to be retired this year.
                    # ~ print('dicommision_list')
                    # ~ print(dicommision_list.plant_type)
                    remove_plant = dicommision_list.iloc[-1]
                    df_pp_grouped.loc[df_pp_grouped['plant_type'] == remove_plant['plant_type'],'capacity'] -= remove_plant['capacity'] ##remove capacity of retired plant.
                    dicommision_list.drop(dicommision_list.index[-1],axis=0, inplace=True)
                    # ~ print('remove and continue')
                    # ~ file1.write('decommision plant is: '+str(remove_plant['plant_type'])+'\n')
                    continue
                        
                else:
                    print('break')
                    # ~ file1.write('break'+'\n')
                    break 
                    
        annual_tot_invest.append(df_next_year)
        
        df_pp = pd.concat(annual_tot_invest, axis=0, ignore_index=True,sort=False,copy=False)   
        # ~ print('\n' + 'df_next_year is ------------' + '\n' + str(df_pp))
        ts +=1 ##move to next year
        continue
        # =========================================
    print('(main module)end')

    t6_stop = time.perf_counter()
    t6 = t6_stop-t6_start
    print('the total elapsed time is ' + str(t6))
    # ~ file1.close() 
# ==================================================================#
##export the results
    today = datetime.date.today()##year-month-day
    installed_capacity_series = pd.DataFrame(index=[pp for pp in pp_list])
    installed_capacity_series = pd.concat(annual_capacity, axis=1, ignore_index=True,sort=False,copy=False)   
    df_capacity_invest = pd.DataFrame(capacity_invest, columns=['plant', 'year'])
    ##(1)export investment information about type of plant and its investment year. 
    # ~ df_capacity_invest.to_excel("output/tables/installed/invest_plant_year_0309.xlsx")
    
    ##(2)export annual total installed capacity.
    installed_capacity_series.index=pp_list
    # ~ installed_capacity_series.to_excel("output/tables/installed/installed_homo_0309.xlsx")  ##export the results as input for dispatch calculation.
   
    print(installed_capacity_series)
# ==================================================================#

##--------------END-----------------------##
