import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.lines import Line2D
import matplotlib.gridspec as gridspec
import numpy as np

# matplotlib.rcParams['axes.labelsize'] = 14
# matplotlib.rcParams['axes.titlesize'] = 14
# matplotlib.rcParams['xtick.labelsize'] = 12
# matplotlib.rcParams['ytick.labelsize'] = 12
# matplotlib.rcParams['legend.fontsize'] = 12
#matplotlib.rcParams['legend.facecolor'] = 'w'
matplotlib.rcParams['font.family'] = 'arial'

#drop_filepath = os.path.join(os.getcwd(), 'Dropsonde_Metric_Calculations.csv')
drop_filepath = os.path.join(os.getcwd(), 'Dropsonde_Metric_Calculations_CPEXCV.csv')
df = pd.read_csv(drop_filepath)

# #change the old index (which still references non-sorted rows) to a new index (which references the sorted rows)
# new_index = np.arange(0, len(df1), 1)
# df_sort = df.sort_values(['Region', 'Case']).set_index(new_index)
# #^^^orders by region first, then by case within each region group

cindy_days = ['20170619','20170620','20210826','20210828','20210901','20210904', '20220923']  #including TDs as TCs (from both CPEX and CPEX-AW)

rh_layers = ['Deep Layer RH [%]', 'PBL RH [%]', 'Mid Layer RH [%]', 'Upper Layer RH [%]']
speed_shear_layers = ['SHARPpy Direct Method Deep Layer Speed Shear [kts]', 'SHARPpy Direct Method PBL Speed Shear [kts]', 
                      'SHARPpy Direct Method Mid Layer Speed Shear [kts]', 'SHARPpy Direct Method Upper Layer Speed Shear [kts]']
cape_layers = ['Deep Layer MUCAPE [J/kg]', 'Deep Layer MLCAPE [J/kg]', 'Above FZL MUCAPE [J/kg]', 'Above FZL MLCAPE [J/kg]']

use_alpha = 0.25  #alpha for non-inflow sondes
use_alpha = 1.0

#custom legend
legend_elements = [Line2D([], [], color='red', linewidth = 0, marker = 'o', markersize = 15, label='Isolated (Clear)'),
                    Line2D([], [], color='red', linewidth = 0, marker = '$C$', markersize = 15, label='Isolated (In Cloud)'),
                    Line2D([], [], color='red', linewidth = 0, marker = '$P$', markersize = 15, label='Isolated (In Precip)'),
                    Line2D([], [], color='blue', linewidth = 0, marker = 'o', markersize = 15, label='Organized (Clear)'),
                    Line2D([], [], color='blue', linewidth = 0, marker = '$C$', markersize = 15, label='Organized (In Cloud)'),
                    Line2D([], [], color='blue', linewidth = 0, marker = '$P$', markersize = 15, label='Organized (In Precip)'),
                    Line2D([], [], color='black', linewidth = 0, marker = 'o', markersize = 15, label='Scattered (Clear)'),
                    Line2D([], [], color='black', linewidth = 0, marker = '$C$', markersize = 15, label='Scattered (In Cloud)'),
                    Line2D([], [], color='black', linewidth = 0, marker = '$P$', markersize = 15, label='Scattered (In Precip)')]

# legend_elements = [Line2D([], [], color='red', linewidth = 0, marker = 'o', markersize = 15, label='Isolated'),
#                    Line2D([], [], color='blue', linewidth = 0, marker = 'o', markersize = 15, label='Organized'),
#                    Line2D([], [], color='black', linewidth = 0, marker = 'o', markersize = 15, label='Scattered')]

#######################################################################################################

#IMPORTANT:  HOW TO FIX 'KeyError: 0' error:  NEED .iloc[j] AND NOT JUST [j] BECAUSE [j] refers to the index, 
#not the integer position (IP), and groupby function only adjusts IP when making groups and not index!
 
#for convective type comparison of All Lifecycles dropsondes
def make_plot_onlyIsoOrg_RH(plotting_metric_name, ax):  #parameter will be a data column from df
    
    plotting_metric = df[plotting_metric_name]
    xlist = []
    for i in range(len(df)):
        xstring = str(df['Case'][i])
        xlist.append(xstring)
    
    for j in range(len(plotting_metric)):
        #if (df['Convective Lifecycle'][j] != 'Weakening') and (df['Environment Falling In'][j] == 'Clear Near' or df['Environment Falling In'][j] == 'In Cloud' or df['Environment Falling In'][j] == 'In Precip'):
        if df['Environment Falling In'][j] == 'Clear Near' or df['Environment Falling In'][j] == 'In Cloud' or df['Environment Falling In'][j] == 'In Precip':
        #if (df['Environment Falling In'][j] == 'Clear Near' or df['Environment Falling In'][j] == 'In Cloud' or df['Environment Falling In'][j] == 'In Precip') and (df['Low-level Inflow Sonde'][j] == 'Yes' or df['Mid-level Inflow Sonde'][j] == 'Yes'):
            if df['Primary Convective Type'][j] == 'Isolated':
                color = 'red'
                if str(df['Date'][j]) in cindy_days:
                    continue
            elif df['Primary Convective Type'][j] == 'Organized':
                color = 'blue'
                if str(df['Date'][j]) in cindy_days:
                    continue
            elif df['Primary Convective Type'][j] == 'Scattered':
                color = 'black'
                if str(df['Date'][j]) in cindy_days:
                    continue                
            else:
                continue                
            
            if df['Environment Falling In'][j] == 'In Precip':
                if df['Partially In Precip'][j] == 'Yes':
                    mark = '$*P$'
                else:
                    mark = '$P$'
                outline = None
            elif df['Environment Falling In'][j] == 'In Cloud':
                if df['Falling Through Weak Stratiform (Onion-ish Profile (Typically On Outer Edge of Storm))'][j] == 'Yes':
                    mark = '$*C$'
                else:
                    mark = '$C$'
                outline = None
            else:
                mark = 'o'
                outline = 'black'
            
            #if the metric is not NaN (need this filter, otherwise Python raises an error when showing/saving the figure)
            if not np.isnan(plotting_metric[j]):  #could also use pd.isna(plotting_metric[j])
                if df['Low-level Inflow Sonde'][j] == 'Yes' or df['Mid-level Inflow Sonde'][j] == 'Yes':
                    ax.scatter(xlist[j], plotting_metric[j], c = color, s = 150, marker = mark, edgecolor = outline)
                else:
                    ax.scatter(xlist[j], plotting_metric[j], c = color, alpha = use_alpha, s = 150, marker = mark, edgecolor = outline)
            else:   #use this if you want each case to show up in the plot, regardless if it has data or not
                ax.scatter(xlist[j], 80, c = color, alpha = 0.0, s = 150)
            
    ax.grid(True)
    ax.set_title(plotting_metric_name[:-4], fontsize = 33, fontweight = 'bold')
    ax.set_xlabel('Case', fontsize = 30, fontweight = 'bold')
    ax.set_ylabel('[%]', fontsize = 30, fontweight = 'bold')
    #ax.set_ylim([15,100])
    ax.tick_params(length = 15, width = 5, labelsize = 25)
 
#group_fig = plt.figure(figsize=(15,24))
group_fig = plt.figure(figsize=(32,24))   #CPEX-CV with isolated, organized, and scattered cases

for i, layer in enumerate(rh_layers):
    ax = group_fig.add_subplot(2,2,i+1)
    make_plot_onlyIsoOrg_RH(layer, ax)

#group_fig.legend(handles = legend_elements, loc = 'center', fontsize = 28, title = '$\\bf{Convective Type}$', title_fontsize = 30, ncol = 3)
group_fig.legend(handles = legend_elements, loc = 'center', fontsize = 28, ncol = 3)
plt.subplots_adjust(hspace=0.6, wspace = 0.35)
plt.savefig('/Users/brodenkirch/Desktop/RH_4panel.png', bbox_inches = 'tight')
plt.close()


def make_plot_onlyIsoOrg_SS(plotting_metric_name, ax):  #parameter will be a data column from df
    
    plotting_metric = df[plotting_metric_name]
    xlist = []
    for i in range(len(df)):
        xstring = str(df['Case'][i])
        xlist.append(xstring)
    
    for j in range(len(plotting_metric)):
        #if (df['Convective Lifecycle'][j] != 'Weakening') and (df['Environment Falling In'][j] == 'Clear Near' or df['Environment Falling In'][j] == 'In Cloud' or df['Environment Falling In'][j] == 'In Precip'):
        if df['Environment Falling In'][j] == 'Clear Near' or df['Environment Falling In'][j] == 'In Cloud' or df['Environment Falling In'][j] == 'In Precip':
        #if (df['Environment Falling In'][j] == 'Clear Near' or df['Environment Falling In'][j] == 'In Cloud' or df['Environment Falling In'][j] == 'In Precip') and (df['Low-level Inflow Sonde'][j] == 'Yes' or df['Mid-level Inflow Sonde'][j] == 'Yes'):
            if df['Primary Convective Type'][j] == 'Isolated':
                color = 'red'
                if str(df['Date'][j]) in cindy_days:
                    continue
            elif df['Primary Convective Type'][j] == 'Organized':
                color = 'blue'
                if str(df['Date'][j]) in cindy_days:
                    continue
            elif df['Primary Convective Type'][j] == 'Scattered':
                color = 'black'
                if str(df['Date'][j]) in cindy_days:
                    continue                
            else:
                continue              
                  
            if df['Environment Falling In'][j] == 'In Precip':
                if df['Partially In Precip'][j] == 'Yes':
                    mark = '$*P$'
                else:
                    mark = '$P$'
                outline = None
            elif df['Environment Falling In'][j] == 'In Cloud':
                if df['Falling Through Weak Stratiform (Onion-ish Profile (Typically On Outer Edge of Storm))'][j] == 'Yes':
                    mark = '$*C$'
                else:
                    mark = '$C$'
                outline = None
            else:
                mark = 'o'
                outline = 'black'
        
            #if the metric is not NaN (need this filter, otherwise Python raises an error when showing/saving the figure)
            if not np.isnan(plotting_metric[j]):  #could also use pd.isna(plotting_metric[j])
                if df['Low-level Inflow Sonde'][j] == 'Yes' or df['Mid-level Inflow Sonde'][j] == 'Yes':
                    ax.scatter(xlist[j], plotting_metric[j], c = color, s = 150, marker = mark, edgecolor = outline)
                else:
                    ax.scatter(xlist[j], plotting_metric[j], c = color, alpha = use_alpha, s = 150, marker = mark, edgecolor = outline)
            else:   #use this if you want each case to show up in the plot, regardless if it has data or not
                ax.scatter(xlist[j], 10, c = color, alpha = 0.0, s = 150)
                
    ax.grid(True)
    ax.set_title(plotting_metric_name[22:-18] + ' Shear', fontsize = 33, fontweight = 'bold')
    ax.set_xlabel('Case', fontsize = 30, fontweight = 'bold')
    ax.set_ylabel('[kts]', fontsize = 30, fontweight = 'bold')
    #ax.set_ylim([0,50])
    ax.tick_params(length = 15, width = 5, labelsize = 25)
 
#group_fig = plt.figure(figsize=(15,24))
group_fig = plt.figure(figsize=(32,24))   #CPEX-CV with isolated, organized, and scattered cases

for i, layer in enumerate(speed_shear_layers):
    ax = group_fig.add_subplot(2,2,i+1)
    make_plot_onlyIsoOrg_SS(layer, ax)

#group_fig.legend(handles = legend_elements, loc = 'center', fontsize = 28, title = '$\\bf{Convective Type}$', title_fontsize = 30, ncol = 3)
group_fig.legend(handles = legend_elements, loc = 'center', fontsize = 28, ncol = 3)
plt.subplots_adjust(hspace = 0.6, wspace = 0.35)
plt.savefig('/Users/brodenkirch/Desktop/SS_4panel.png', bbox_inches = 'tight')
plt.close()


def make_plot_onlyIsoOrg_CAPE(plotting_metric_name, ax):  #parameter will be a data column from df
    
    plotting_metric = df[plotting_metric_name]
    xlist = []
    for i in range(len(df)):
        xstring = str(df['Case'][i])
        xlist.append(xstring)
    
    for j in range(len(plotting_metric)):
        #if (df['Convective Lifecycle'][j] != 'Weakening') and (df['Environment Falling In'][j] == 'Clear Near' or df['Environment Falling In'][j] == 'In Cloud' or df['Environment Falling In'][j] == 'In Precip'):
        if df['Environment Falling In'][j] == 'Clear Near' or df['Environment Falling In'][j] == 'In Cloud' or df['Environment Falling In'][j] == 'In Precip':
        #if (df['Environment Falling In'][j] == 'Clear Near' or df['Environment Falling In'][j] == 'In Cloud' or df['Environment Falling In'][j] == 'In Precip') and (df['Low-level Inflow Sonde'][j] == 'Yes' or df['Mid-level Inflow Sonde'][j] == 'Yes'):            
            if df['Primary Convective Type'][j] == 'Isolated':
                color = 'red'
                if str(df['Date'][j]) in cindy_days:
                    continue
            elif df['Primary Convective Type'][j] == 'Organized':
                color = 'blue'
                if str(df['Date'][j]) in cindy_days:
                    continue
            elif df['Primary Convective Type'][j] == 'Scattered':
                color = 'black'
                if str(df['Date'][j]) in cindy_days:
                    continue                
            else:
                continue
                  
            if df['Environment Falling In'][j] == 'In Precip':
                if df['Partially In Precip'][j] == 'Yes':
                    mark = '$*P$'
                else:
                    mark = '$P$'
                outline = None
            elif df['Environment Falling In'][j] == 'In Cloud':
                if df['Falling Through Weak Stratiform (Onion-ish Profile (Typically On Outer Edge of Storm))'][j] == 'Yes':
                    mark = '$*C$'
                else:
                    mark = '$C$'
                outline = None
            else:
                mark = 'o'
                outline = 'black'

            #if the metric is not NaN (need this filter, otherwise Python raises an error when showing/saving the figure)
            if not np.isnan(plotting_metric[j]):  #could also use pd.isna(plotting_metric[j])
                if df['Low-level Inflow Sonde'][j] == 'Yes' or df['Mid-level Inflow Sonde'][j] == 'Yes':
                    ax.scatter(xlist[j], plotting_metric[j], c = color, s = 150, marker = mark, edgecolor = outline)
                else:
                    ax.scatter(xlist[j], plotting_metric[j], c = color, alpha = use_alpha, s = 150, marker = mark, edgecolor = outline)
            else:   #use this if you want each case to show up in the plot, regardless if it has data or not
                ax.scatter(xlist[j], 200, c = color, alpha = 0.0, s = 150)
                
    ax.grid(True)
    if 'Above FZL' in plotting_metric_name:
        ax.set_title('Upper Layer' + plotting_metric_name[9:-7], fontsize = 33, fontweight = 'bold')
    else:
        ax.set_title(plotting_metric_name[:-7], fontsize = 33, fontweight = 'bold')
    ax.set_xlabel('Case', fontsize = 30, fontweight = 'bold')
    ax.set_ylabel('[J kg$^{-1}$]', fontsize = 30, fontweight = 'bold')
    ax.tick_params(length = 15, width = 5, labelsize = 25)
    
    #make the deep layer plot axes range the same and the above FZL plot axes the same for easier comparison
    if plotting_metric_name[:4] == 'Deep':
        ax.set_ylim([-30,1450])
    else:
        ax.set_ylim([-30,1000])

 
#group_fig = plt.figure(figsize=(15,24))
group_fig = plt.figure(figsize=(32,24))   #CPEX-CV with isolated, organized, and scattered cases

for i, layer in enumerate(cape_layers):
    ax = group_fig.add_subplot(2,2,i+1)
    make_plot_onlyIsoOrg_CAPE(layer, ax)

#group_fig.legend(handles = legend_elements, loc = 'center', fontsize = 28, title = '$\\bf{Convective Type}$', title_fontsize = 30, ncol = 3)
group_fig.legend(handles = legend_elements, loc = 'center', fontsize = 28, ncol = 3)
plt.subplots_adjust(hspace=0.6, wspace = 0.45)
plt.savefig('/Users/brodenkirch/Desktop/CAPE_4panel.png', bbox_inches = 'tight')
plt.close()



