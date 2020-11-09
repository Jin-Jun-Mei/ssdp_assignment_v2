#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  sys_params.py
#  
# ~ import sys
# ~ sys.path.append('C:\PhD_Chalmers\Python\Lib\site-packages') ## adding directory

eps = -0.05
p0 = 3.25
i_r = 0.04 ##interests rate.
hurdle_r = 0.08

CarbonTax_lst = []##set carbon tax (cent/ton co2).
for ts in range(0,155): ##ts is year.
    if ts < 10: tax = 0  ## carbon tax is 0 before year 10.
    elif 10 <= ts <= 50: tax = 250 * ts - 2500 ## from year 10 to 50, carbon tax increases linearly to 10000 cent/ton.
    else:tax = 10000   ## after year 50, carbon tax stays at 10000 cent/ton.
    CarbonTax_lst.append(tax)
# ~ for ts in range(0,100): ##ts is year.
    # ~ if ts <= 10: tax = 0 ## carbon tax is 0 before year 10.
    # ~ elif 10 <= ts <= 50: tax = 0 ## from year 10 to 50, carbon tax increases linearly to 10000 cent/ton.
    # ~ else:tax = 0 ## after year 50, carbon tax stays at 10000 cent/ton.
    # ~ CarbonTax_lst.append(tax)

# ~ print(CarbonTax_lst)
