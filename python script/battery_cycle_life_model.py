# -*- coding: utf-8 -*-
"""
Created on Fri Nov 30 09:53:40 2018

@author: dvsto
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#inputs
c_2ref = 3.9193e-3
b_c2 = 4.54
e_ac2 = -48260.0
c_0ref = 75.64
e_ac0 = 2224.0
t_amb = 273.0
q_rtd = 60.0

#constants
t_ref = 298.15
r_ug = 8.314

#time sequence variables
num_points = 2500
cycles = range(0,num_points)
dod_const = 0.8
sigma = 0.05
threshold = dod_const+sigma/3
dod_base = pd.Series((np.random.randn(num_points)*sigma+dod_const))
dod_base.loc[dod_base<0] = 0.0
dod_base.loc[dod_base>1] = 1.0

dod_1 = dod_base.copy()
dod_1.loc[dod_1>threshold] = threshold

q_neg_const = pd.Series([0.0]*num_points)
q_neg_base = pd.Series([0.0]*num_points)
q_neg_1 = pd.Series([0.0]*num_points)

#time series calculations
for n in range(0,num_points):
    #constant dod case
    c_2 = c_2ref*np.exp(-e_ac2/r_ug*(1/t_amb-1/t_ref))*(dod_const**b_c2)
    c_0 = c_0ref*np.exp(-e_ac0/r_ug*(1/t_amb-1/t_ref))
    q_neg_const[n] = np.sqrt(c_0**2 - 2*c_2*c_0*n)
    
    #base case
    c_2 = c_2ref*np.exp(-e_ac2/r_ug*(1/t_amb-1/t_ref))*(dod_base[n]**b_c2)
    #c_0 = c_0ref*np.exp(-e_ac0/r_ug*(1/t_amb-1/t_ref))
    q_neg_base[n] = np.sqrt(c_0**2 - 2*c_2*c_0*n)
    
    #simple threshold scenario  
    c_2 = c_2ref*np.exp(-e_ac2/r_ug*(1/t_amb-1/t_ref))*(dod_1[n]**b_c2)
    #c_0 = c_0ref*np.exp(-e_ac0/r_ug*(1/t_amb-1/t_ref))
    q_neg_1[n] = np.sqrt(c_0**2 - 2*c_2*c_0*n)
    
#normalize output
window = 100
q_pu_const = q_neg_const/q_rtd
q_pu_base = q_neg_base/q_rtd
q_pu_base_avg = q_pu_base.rolling(window,min_periods=5).mean()
q_pu_1 = q_neg_1/q_rtd
q_pu_1_avg = q_pu_1.rolling(window,min_periods=5).mean()

#calculate EOL
for index in cycles:
    if q_pu_const[index] < 0.8:
        const_eol = index
        print('EOL for q_pu_const: '+str(index))
        break
for index in cycles:
    if q_pu_base_avg[index] < 0.8:
        base_eol = index
        print('EOL for q_pu_base_avg: '+str(index))
        break
for index in cycles:
    if q_pu_1_avg[index] < 0.8:
        case1_eol = index
        print('EOL for q_pu_1_avg: '+str(index))
        break

#plot average capacity depletion
fig,ax = plt.subplots()
ax.plot(cycles,q_pu_base_avg)
ax.plot(cycles,q_pu_1_avg)
ax.plot(cycles,q_pu_const)
ax.set(xlabel='Cycles',ylabel='Relative Capacity')
#ax.set_xticks([])
ax.legend(['no load shifting','load shifting','expected value at average DOD'])
ax.annotate('base EOL',
            xy=(base_eol, q_pu_base_avg[base_eol]), xycoords='data',
            xytext=(-45, -25), textcoords='offset points',
            arrowprops=dict(arrowstyle='->')
            )
ax.annotate('new EOL',
            xy=(case1_eol, q_pu_1_avg[case1_eol]), xycoords='data',
            xytext=(-5, 20), textcoords='offset points',
            arrowprops=dict(arrowstyle='->')
            )
plt.show()

'''
#plot capacity depletion 
fig = plt.figure()
ax1 = fig.add_subplot(211)
ax1.plot(cycles,q_pu_base)
ax1.plot(cycles,q_pu_base_avg)

ax2 = fig.add_subplot(212)
ax2.plot(cycles,q_pu_1)
ax2.plot(cycles,q_pu_1_avg)

plt.show()

#plot DOD
fig = plt.figure()
plt.plot(cycles,dod_base)
plt.plot(cycles,dod_1)
plt.show()
'''


