import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.lines import Line2D
#from matplotlib.patches import Patch
import numpy as np

import matplotlib.ticker as ticker
from datetime import datetime


#RH/shear 4-panel plots

# matplotlib.rcParams['axes.labelsize'] = 14
# matplotlib.rcParams['axes.titlesize'] = 14
# matplotlib.rcParams['xtick.labelsize'] = 12
# matplotlib.rcParams['ytick.labelsize'] = 12
# matplotlib.rcParams['legend.fontsize'] = 12
#matplotlib.rcParams['legend.facecolor'] = 'w'
matplotlib.rcParams['font.family'] = 'arial'

drop_filepath = os.path.join(os.getcwd(), 'Dropsonde_Metric_Calculations_OnlyCases13and16.csv')
df = pd.read_csv(drop_filepath)

rh_layers = ['Deep Layer RH [%]', 'PBL RH [%]', 'Mid Layer RH [%]', 'Upper Layer RH [%]']
speed_shear_layers = ['SHARPpy Direct Method Deep Layer Speed Shear [kts]', 'SHARPpy Direct Method PBL Speed Shear [kts]', 
                      'SHARPpy Direct Method Mid Layer Speed Shear [kts]', 'SHARPpy Direct Method Upper Layer Speed Shear [kts]']
dir_shear_layers = ['SHARPpy Direct Method Deep Layer Directional Shear [deg]', 'SHARPpy Direct Method PBL Directional Shear [deg]', 
                    'SHARPpy Direct Method Mid Layer Directional Shear [deg]', 'SHARPpy Direct Method Upper Layer Directional Shear [deg]']

use_alpha = 0.25  #alpha for non-inflow sondes

#custom legend
legend_elements = [Line2D([], [], color='blue', linewidth = 0, marker = 'o', markersize = 15, label='Within TPW Gradient (Clear)'),
                   Line2D([], [], color='blue', linewidth = 0, marker = '$C$', markersize = 15, label='Within TPW Gradient (In Cloud)'),
                   Line2D([], [], color='blue', linewidth = 0, marker = '$P$', markersize = 15, label='Within TPW Gradient (In Precip)'),
                   Line2D([], [], color='green', linewidth = 0, marker = 'o', markersize = 15, label='Beyond TPW Gradient (Clear)'),
                   Line2D([], [], color='green', linewidth = 0, marker = '$C$', markersize = 15, label='Beyond TPW Gradient (In Cloud)'),
                   Line2D([], [], color='green', linewidth = 0, marker = '$P$', markersize = 15, label='Beyond TPW Gradient (In Precip)')]

#######################################################################################################

#IMPORTANT:  HOW TO FIX 'KeyError: 0' error:  NEED .iloc[j] AND NOT JUST [j] BECAUSE [j] refers to the index, 
#not the integer position (IP), and groupby function only adjusts IP when making groups and not index!
 
#for convective type comparison of All Lifecycles dropsondes
def make_plot_onlyCases13and16_RH(plotting_metric_name, ax):  #parameter will be a data column from df
    
    plotting_metric = df[plotting_metric_name]
    xlist = []
    for i in range(len(df)):
        xstring = str(df['Case'][i])
        xlist.append(xstring)
    
    for j in range(len(plotting_metric)):
        #if (df['Convective Lifecycle'][j] == 'Mature' or df['Convective Lifecycle'][j] == 'Growing') and (df['Environment Falling In'][j] == 'Clear Near' or df['Environment Falling In'][j] == 'In Cloud' or df['Environment Falling In'][j] == 'In Precip'):
        if df['Environment Falling In'][j] == 'Clear Near' or df['Environment Falling In'][j] == 'In Cloud' or df['Environment Falling In'][j] == 'In Precip':
        #if (df['Environment Falling In'][j] == 'Clear Near' or df['Environment Falling In'][j] == 'In Cloud' or df['Environment Falling In'][j] == 'In Precip') and (df['Mid-level Inflow Sonde'][j] == 'Yes'):
            if df['Beyond TPW Gradient'][j] == 'Yes':
                color = 'green'  #hex code for even lighter blue
            else:
                color = 'blue'
                  
            if df['Environment Falling In'][j] == 'In Precip':
                mark = '$P$'
                outline = None
            elif df['Environment Falling In'][j] == 'In Cloud':
                mark = '$C$'
                outline = None
            else:
                mark = 'o'
                outline = 'black'

            #using int(xlist[j]) to get rid of whitespace between cases in the plots by setting set_xticks() and set_xlim()
            if df['Low-level Inflow Sonde'][j] == 'Yes' or df['Mid-level Inflow Sonde'][j] == 'Yes':
                ax.scatter(int(xlist[j]), plotting_metric[j], c = color, s = 150, marker = mark, edgecolor = outline)
            else:
                ax.scatter(int(xlist[j]), plotting_metric[j], c = color, alpha = use_alpha, s = 150, marker = mark, edgecolor = outline)
            
    ax.grid(True)
    ax.set_title(plotting_metric_name[:-4], fontsize = 33, fontweight = 'bold')
    ax.set_xlabel('Case', fontsize = 30, fontweight = 'bold')
    ax.set_ylabel('[%]', fontsize = 30, fontweight = 'bold')
    #ax.set_ylim([15,100])
    ax.tick_params(length = 15, width = 5, labelsize = 25)
    ax.set_xticks([13,16])
    ax.set_xlim([11,18])
 

#group_fig = plt.figure(figsize=(15,24))
group_fig = plt.figure(figsize=(8,24))

for i, layer in enumerate(rh_layers):
    ax = group_fig.add_subplot(2,2,i+1)
    make_plot_onlyCases13and16_RH(layer, ax)

group_fig.legend(handles = legend_elements, loc = 'center', fontsize = 25, ncol = 2)
plt.subplots_adjust(hspace = 0.6, wspace = 1.2)  #wspace = 0.35
plt.savefig('/Users/brodenkirch/Desktop/RH_4panel_onlyCases13and16.png', bbox_inches = 'tight')
plt.close()

def make_plot_onlyCases13and16_SS(plotting_metric_name, ax):  #parameter will be a data column from df
    
    plotting_metric = df[plotting_metric_name]
    xlist = []
    for i in range(len(df)):
        xstring = str(df['Case'][i])
        xlist.append(xstring)
    
    for j in range(len(plotting_metric)):
        #if (df['Convective Lifecycle'][j] == 'Mature' or df['Convective Lifecycle'][j] == 'Growing') and (df['Environment Falling In'][j] == 'Clear Near' or df['Environment Falling In'][j] == 'In Cloud' or df['Environment Falling In'][j] == 'In Precip'):
        if df['Environment Falling In'][j] == 'Clear Near' or df['Environment Falling In'][j] == 'In Cloud' or df['Environment Falling In'][j] == 'In Precip':
        #if (df['Environment Falling In'][j] == 'Clear Near' or df['Environment Falling In'][j] == 'In Cloud' or df['Environment Falling In'][j] == 'In Precip') and (df['Mid-level Inflow Sonde'][j] == 'Yes'):
            if df['Beyond TPW Gradient'][j] == 'Yes':
                color = 'green'  #hex code for even lighter blue
            else:
                color = 'blue'
                  
            if df['Environment Falling In'][j] == 'In Precip':
                mark = '$P$'
                outline = None
            elif df['Environment Falling In'][j] == 'In Cloud':
                mark = '$C$'
                outline = None
            else:
                mark = 'o'
                outline = 'black'
        
            #using int(xlist[j]) to get rid of whitespace between cases in the plots by setting set_xticks() and set_xlim()
            if df['Low-level Inflow Sonde'][j] == 'Yes' or df['Mid-level Inflow Sonde'][j] == 'Yes':
                ax.scatter(int(xlist[j]), plotting_metric[j], c = color, s = 150, marker = mark, edgecolor = outline)
            else:
                ax.scatter(int(xlist[j]), plotting_metric[j], c = color, alpha = use_alpha, s = 150, marker = mark, edgecolor = outline)
            
    ax.grid(True)
    ax.set_title(plotting_metric_name[22:-18] + ' Shear', fontsize = 33, fontweight = 'bold')
    ax.set_xlabel('Case', fontsize = 30, fontweight = 'bold')
    ax.set_ylabel('[kts]', fontsize = 30, fontweight = 'bold')
    #ax.set_ylim([0,50])
    ax.tick_params(length = 15, width = 5, labelsize = 25)
    ax.set_xticks([13,16])
    ax.set_xlim([11,18])
 

group_fig = plt.figure(figsize=(8,24))

for i, layer in enumerate(speed_shear_layers):
    ax = group_fig.add_subplot(2,2,i+1)
    make_plot_onlyCases13and16_SS(layer, ax)

group_fig.legend(handles = legend_elements, loc = 'center', fontsize = 25, ncol = 2)
plt.subplots_adjust(hspace = 0.6, wspace = 1.2)
plt.savefig('/Users/brodenkirch/Desktop/SS_4panel_onlyCases13and16.png', bbox_inches = 'tight')
plt.close()


def make_plot_onlyCases13and16_DS(plotting_metric_name, ax):  #parameter will be a data column from df
    
    plotting_metric = df[plotting_metric_name]
    xlist = []
    for i in range(len(df)):
        xstring = str(df['Case'][i])
        xlist.append(xstring)
    
    for j in range(len(plotting_metric)):
        #if (df['Convective Lifecycle'][j] == 'Mature' or df['Convective Lifecycle'][j] == 'Growing') and (df['Environment Falling In'][j] == 'Clear Near' or df['Environment Falling In'][j] == 'In Cloud' or df['Environment Falling In'][j] == 'In Precip'):
        if df['Environment Falling In'][j] == 'Clear Near' or df['Environment Falling In'][j] == 'In Cloud' or df['Environment Falling In'][j] == 'In Precip':
        #if (df['Environment Falling In'][j] == 'Clear Near' or df['Environment Falling In'][j] == 'In Cloud' or df['Environment Falling In'][j] == 'In Precip') and (df['Mid-level Inflow Sonde'][j] == 'Yes'):
            if df['Beyond TPW Gradient'][j] == 'Yes':
                color = 'green'  #hex code for even lighter blue
            else:
                color = 'blue'
                  
            if df['Environment Falling In'][j] == 'In Precip':
                mark = '$P$'
                outline = None
            elif df['Environment Falling In'][j] == 'In Cloud':
                mark = '$C$'
                outline = None
            else:
                mark = 'o'
                outline = 'black'
        
            #using int(xlist[j]) to get rid of whitespace between cases in the plots by setting set_xticks() and set_xlim()
            if df['Low-level Inflow Sonde'][j] == 'Yes' or df['Mid-level Inflow Sonde'][j] == 'Yes':
                ax.scatter(int(xlist[j]), plotting_metric[j], c = color, s = 150, marker = mark, edgecolor = outline)
            else:
                ax.scatter(int(xlist[j]), plotting_metric[j], c = color, alpha = use_alpha, s = 150, marker = mark, edgecolor = outline)
            
    ax.grid(True)
    ax.set_title(plotting_metric_name[22:-18] + ' Shear', fontsize = 33, fontweight = 'bold')
    ax.set_xlabel('Case', fontsize = 30, fontweight = 'bold')
    ax.set_ylabel('[deg]', fontsize = 30, fontweight = 'bold')
    ax.set_ylim([-5,365])
    ax.tick_params(length = 15, width = 5, labelsize = 25)
    ax.set_xticks([13,16])
    ax.set_xlim([11,18])
    

group_fig = plt.figure(figsize=(8,24))

for i, layer in enumerate(dir_shear_layers):
    ax = group_fig.add_subplot(2,2,i+1)
    make_plot_onlyCases13and16_DS(layer, ax)

group_fig.legend(handles = legend_elements, loc = 'center', fontsize = 25, ncol = 2)
plt.subplots_adjust(hspace = 0.6, wspace = 1.2)
plt.savefig('/Users/brodenkirch/Desktop/DS_4panel_onlyCases13and16.png', bbox_inches = 'tight')
plt.close()


###########################################################################################
###########################################################################################
###########################################################################################

#Dropsonde/DAWN deep shear scatter
matplotlib.rcParams['axes.labelsize'] = 14
matplotlib.rcParams['axes.titlesize'] = 14
matplotlib.rcParams['xtick.labelsize'] = 12
matplotlib.rcParams['ytick.labelsize'] = 12
matplotlib.rcParams['legend.fontsize'] = 12
#matplotlib.rcParams['legend.facecolor'] = 'w'
matplotlib.rcParams['font.family'] = 'arial'

drop_filepath = os.path.join(os.getcwd(), 'Dropsonde_Metric_Calculations_OnlyCases13and16.csv')
df_drop = pd.read_csv(drop_filepath)

dawn_filepath = os.path.join(os.getcwd(), 'DAWN_Shear_Calculations_OnlyCases13and16.csv')
df_dawn = pd.read_csv(dawn_filepath)

#IMPORTANT:  HOW TO FIX 'KeyError: 0' error:  NEED .iloc[j] AND NOT JUST [j] BECAUSE [j] refers to the index, 
#not the integer position (IP), and groupby function only adjusts IP when making groups and not index!

#for convective type comparison of All Lifecycles dropsondes
def make_plot_only13and16(plotting_metric):  #parameter will be a data column from df1
    xlist = []
    for i in range(len(df1)):
        xstring = str(df1['Case'][i])
        xlist.append(xstring)
    
    fig = plt.figure(figsize=(8,21))
    
    #custom legend
    legend_elements = [Line2D([], [], color='blue', linewidth = 0, marker = 'o', markersize = 15, label='Within TPW Gradient'),
                       Line2D([], [], color='green', linewidth = 0, marker = 'o', markersize = 15, label='Beyond TPW Gradient')]
    
    for j in range(len(plotting_metric)):
        #if (df1['Convective Lifecycle'][j] == 'Mature' or df1['Convective Lifecycle'][j] == 'Growing') and (df1['Environment Falling In'][j] == 'Clear Near' or df1['Environment Falling In'][j] == 'In Cloud' or df1['Environment Falling In'][j] == 'In Precip'):
        if df1['Environment Falling In'][j] == 'Clear Near' or df1['Environment Falling In'][j] == 'In Cloud' or df1['Environment Falling In'][j] == 'In Precip':
        #if (df1['Environment Falling In'][j] == 'Clear Near' or df1['Environment Falling In'][j] == 'In Cloud' or df1['Environment Falling In'][j] == 'In Precip') and (df1['Mid-level Inflow Sonde'][j] != 'No'):
            
            if df1['Beyond TPW Gradient'][j] == 'Yes':
                color = 'green'  #hex code for even lighter blue
            else:
                color = 'blue'
                
            # if df1['Environment Falling In Ambiguous'][j] == 'Yes' and df1['Convective Lifecycle'][j] == 'Growing':
            #     mark = '$?G$'
            #     outline = None
            # elif df1['Environment Falling In Ambiguous'][j] == 'Yes' and df1['Environment Falling In'][j] == 'In Precip':
            #     mark = '$?P$'
            #     outline = None
            # elif df1['Convective Lifecycle'][j] == 'Growing' and df1['Environment Falling In'][j] == 'In Precip':
            #     mark = '$GP$'
            #     outline = None
            # elif df1['Environment Falling In Ambiguous'][j] == 'Yes':
            #     mark = '$?$'
            #     outline = None 
            # elif df1['Convective Lifecycle'][j] == 'Growing':
            #     mark = '$G$'
            #     outline = None   
            # elif df1['Environment Falling In'][j] == 'In Precip':
            #     mark = '$P$'
            #     outline = None
            # else:
            #     mark = 'o'
            #     outline = 'black'
            
            # #distinguishes the least complete profile (data down to only 942mb)
            # if str(df1['Date'][j]) == '20170611' and str(df1['Time'][j]) == '213013':
            #     mark = '$?x$'      #? because this dropsonde is also ambiguous
            #     outline = None
            
            # #distinguishes the profile that does not reach the lowest max height (this dropsonde max height is ~1km lower than the next lowest)
            # if str(df1['Date'][j]) == '20170606' and str(df1['Time'][j]) == '212211':
            #     mark = 'x'
            #     outline = None
                
            #plt.scatter(xlist[j], plotting_metric[j], c = color, s = 150, marker = mark, edgecolor = outline)
            
            #using int(xlist[j]) to get rid of whitespace between cases in the plots by setting set_xticks() and set_xlim()
            if df1['Low-level Inflow Sonde'][j] != 'No' or df1['Mid-level Inflow Sonde'][j] != 'No':
                plt.scatter(int(xlist[j]), plotting_metric[j], c = color, s = 150, edgecolor = 'k')
            else:
                plt.scatter(int(xlist[j]), plotting_metric[j], c = color, alpha = use_alpha, s = 150, edgecolor = 'k')
            
    plt.grid(True)
    #plt.xlabel('Case', fontsize = 30, fontweight = 'bold')
    #plt.tick_params(length = 15, width = 5, labelsize = 25)
    plt.xlabel('Case', fontsize = 45, fontweight = 'bold')
    plt.tick_params(length = 15, width = 5, labelsize = 40)
    #plt.tick_params(length = 30, width = 11, labelsize = 56)
    plt.xticks([13,16])
    plt.xlim([11,18])
    #plt.legend(handles = legend_elements, fontsize = 21, loc = 'upper left')
    

#Deep Layer Speed Shear (500m bottom cap) with DAWN shear too
df1 = pd.concat([df_drop, df_dawn], ignore_index = True)  #concatenates fields with same heading
make_plot_only13and16(df1['500m Bottom Cap Deep Layer Speed Shear [kts]'])
#plt.ylim([0,55])
#plt.title('Deep Layer Shear (Dropsonde & DAWN, ~0.5km - 7.6km)\n vs. TPW Gradient Status (All Lifecycles)', fontsize = 33, fontweight = 'bold')
plt.title('Deep Layer Shear\n(Dropsonde & DAWN, ~0.5km - 7.6km)', fontsize = 48, fontweight = 'bold')
#plt.ylabel('Deep Layer Speed Shear [kts]', fontsize = 30, fontweight = 'bold')
plt.ylabel('[kts]', fontsize = 45, fontweight = 'bold')
plt.savefig('/Users/brodenkirch/Desktop/1SSwDAWN_only13and16.png', bbox_inches = 'tight')
plt.close()

sys.exit()

#Deep Layer Directional Shear (500m bottom cap) with DAWN shear too
df1 = pd.concat([df_drop, df_dawn], ignore_index = True)  #concatenates fields with same heading
make_plot_only13and16(df1['500m Bottom Cap Deep Layer Directional Shear [deg]'])
plt.ylim([0,360])
#plt.title('Deep Layer Shear (Dropsonde & DAWN, ~0.5 - 7.6km)\n vs. TPW Gradient Status (All Lifecycles)', fontsize = 33, fontweight = 'bold')
plt.title('Deep Layer Shear\n(Dropsonde & DAWN, ~0.5 - 7.6km)', fontsize = 48, fontweight = 'bold')
#plt.ylabel('Deep Layer Directional Shear [deg]', fontsize = 30, fontweight = 'bold')
plt.ylabel('[deg]', fontsize = 45, fontweight = 'bold')
plt.savefig('/Users/brodenkirch/Desktop/1DSwDAWN_only13and16.png', bbox_inches = 'tight')
plt.close()

###########################################################################################
###########################################################################################
###########################################################################################

#This script creates time series plots of DAWN/dropsonde mean-layer RH/shear

dawn_filepath = os.path.join(os.getcwd(), 'DAWN_Shear_Calculations_OnlyCases13and16.csv')
df_dawn = pd.read_csv(dawn_filepath)

drop_filepath = os.path.join(os.getcwd(), 'Dropsonde_Metric_Calculations_OnlyCases13and16.csv')
df_drop = pd.read_csv(drop_filepath)

df_all = pd.concat([df_drop, df_dawn], ignore_index = True)  #concatenates fields with same heading

cases = df_all.Case.unique()
same_ylims = True

#custom legend
# legend_elements = [Line2D([0], [0], marker='o', color='w', label='Within TPW Gradient',
#                           markerfacecolor='blue', markersize=10),
#                     Line2D([0], [0], marker='o', color='w', label='Beyond TPW Gradient',
#                           markerfacecolor='green', markersize=10)]
legend_elements = [Line2D([], [], color='blue', linewidth = 0, marker = 'o', markersize = 10, label='Within TPW Gradient'),
                   Line2D([], [], color='green', linewidth = 0, marker = 'o', markersize = 10, label='Beyond TPW Gradient')]

RH_metrics = ['Deep Layer RH [%]', 'Deep Layer RH [%]', 'PBL RH [%]', 'PBL RH [%]',
              'Mid Layer RH [%]', 'Mid Layer RH [%]', 'Upper Layer RH [%]', 'Upper Layer RH [%]']

shear_metrics = ['500m Bottom Cap Deep Layer Speed Shear [kts]', '500m Bottom Cap Deep Layer Speed Shear [kts]',
                 'SHARPpy Direct Method PBL Speed Shear [kts]', 'SHARPpy Direct Method PBL Speed Shear [kts]',
                 'SHARPpy Direct Method Mid Layer Speed Shear [kts]', 'SHARPpy Direct Method Mid Layer Speed Shear [kts]',
                 'SHARPpy Direct Method Upper Layer Speed Shear [kts]', 'SHARPpy Direct Method Upper Layer Speed Shear [kts]']

#IMPORTANT:  HOW TO FIX 'KeyError: 0' error:  NEED .iloc[j] AND NOT JUST [j] BECAUSE [j] refers to the index, 
#not the integer position (IP), and groupby function only adjusts IP when making groups and not index!

#create a Series of datetimes for the merged DAWN/dropsonde DataFrame
times = df_all['Date'].astype(str) + df_all['Time'].astype(str)
for i in range(len(df_all)):  #converting the times to datetime objects
    times.iloc[i] = datetime.strptime(times.iloc[i], "%Y%m%d%H%M%S")

#mean-layer relative humidity plot
groupRH_fig = plt.figure(figsize = (24,16))
for i, metric in enumerate(RH_metrics):
    ax = groupRH_fig.add_subplot(4,2,i+1)
    
    if i % 2 == 0:  #LHS plots will be case 13 plots
        case = 13
    elif i % 2 == 1:  #RHS plots will be case 16 plots
        case = 16
        
    for j in range(len(df_all)):
        
        if df_all['Case'].iloc[j] != case:  
            continue
        else:
            if df_all['Beyond TPW Gradient'].iloc[j] == 'Yes':
                color = 'green'
            else:
                color = 'blue'
        
            if df_all['Environment Falling In'].iloc[j] == 'Clear Near':
                mark = 'o'
            elif df_all['Environment Falling In'].iloc[j] == 'In Cloud':
                mark = '$C$'
            elif df_all['Environment Falling In'].iloc[j] == 'In Precip':
                mark = '$P$'
            elif df_all['Environment Falling In'].iloc[j] == 'Clear Far':
                mark = '$F$'
                color = 'k'
                
            ax.scatter(times.iloc[j], df_all[metric].iloc[j], c = color, s = 40, marker = mark)

    if same_ylims:
        padding = 2  #the ylim padding so that the markers aren't cut off in the plots
        ax.set_ylim([df_all[metric].min() - padding, df_all[metric].max() + padding])  #NOTE: error will occur if there is a '--' value in the Pandas Series (fine if there are NaN values though), as .min() will choose this string value as the minimum
        
    ax.set_title('Case ' + str(case) + ' ' + metric[:-4])
    ax.set_xlabel('Time [UTC]')
    ax.set_ylabel(metric)
    ax.legend(handles = legend_elements)
    ax.tick_params(axis='x', rotation = 50)
    ax.tick_params(length = 15, width = 5)
    ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%H:%M:%S"))
    ax.xaxis.set_major_locator(ticker.MaxNLocator(20))      #sets number of ticks
    #ax.set_xlim([np.datetime64(range_start),np.datetime64(range_end)])

ts = plt.suptitle('Case 13 vs. Case 16 Mean-layer RH Time Series', size = 'xx-large', fontweight = 'bold')
#groupRH_fig.legend(handles = legend_elements, loc = 'center', fontsize = 25)
#plt.subplots_adjust(hspace=0.5)
plt.tight_layout()
plt.savefig('/Users/brodenkirch/Desktop/Case13and16_RH_TimeSeries.png', bbox_inches = 'tight')
plt.close()


#mean-layer speed shear plot
groupSS_fig = plt.figure(figsize = (24,16))
for i, metric in enumerate(shear_metrics):
    ax = groupSS_fig.add_subplot(4,2,i+1)
    
    if i % 2 == 0:  #LHS plots will be case 13 plots
        case = 13
    elif i % 2 == 1:  #RHS plots will be case 16 plots
        case = 16
        
    for j in range(len(df_all)):
        
        if df_all['Case'].iloc[j] != case:  
            continue
        else:
            if df_all['Beyond TPW Gradient'].iloc[j] == 'Yes':
                color = 'green'
            else:
                color = 'blue'
        
            if df_all['Environment Falling In'].iloc[j] == 'Clear Near':
                mark = 'o'
            elif df_all['Environment Falling In'].iloc[j] == 'In Cloud':
                mark = '$C$'
            elif df_all['Environment Falling In'].iloc[j] == 'In Precip':
                mark = '$P$'
            elif df_all['Environment Falling In'].iloc[j] == 'Clear Far':
                mark = '$F$'
                color = 'k'
                
            ax.scatter(times.iloc[j], df_all[metric].iloc[j], c = color, s = 40, marker = mark)

    if same_ylims:
        padding = 2  #the ylim padding so that the markers aren't cut off in the plots
        ax.set_ylim([df_all[metric].min() - padding, df_all[metric].max() + padding])  #NOTE: error will occur if there is a '--' value in the Pandas Series (fine if there are NaN values though), as .min() will choose this string value as the minimum

    if 'Bottom Cap' in metric:
        ax.set_title('Case ' + str(case) + ' ' + metric[16:-6])
        ax.set_ylabel(metric[16:])
    else:
        ax.set_title('Case ' + str(case) + ' ' + metric[22:-6])
        ax.set_ylabel(metric[22:])
        
    ax.set_xlabel('Time [UTC]')
    ax.legend(handles = legend_elements)
    ax.tick_params(axis='x', rotation = 50)
    ax.tick_params(length = 15, width = 5)
    ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%H:%M:%S"))
    ax.xaxis.set_major_locator(ticker.MaxNLocator(20))      #sets number of ticks
    #ax.set_xlim([np.datetime64(range_start),np.datetime64(range_end)])

ts = plt.suptitle('Case 13 vs. Case 16 Mean-layer Speed Shear Time Series', size = 'xx-large', fontweight = 'bold')
#groupSS_fig.legend(handles = legend_elements, loc = 'upper center', fontsize = 25)
#plt.subplots_adjust(hspace=0.5)
plt.tight_layout()
plt.savefig('/Users/brodenkirch/Desktop/Case13and16_SS_TimeSeries.png', bbox_inches = 'tight')
plt.close()



#This script creates time series plots of DAWN/dropsonde mean-layer RH/shear, labeled by quadrant relative to the convection

dawn_filepath = os.path.join(os.getcwd(), 'DAWN_Shear_Calculations_OnlyCases13and16.csv')
df_dawn = pd.read_csv(dawn_filepath)

drop_filepath = os.path.join(os.getcwd(), 'Dropsonde_Metric_Calculations_OnlyCases13and16.csv')
df_drop = pd.read_csv(drop_filepath)

df_all = pd.concat([df_drop, df_dawn], ignore_index = True)  #concatenates fields with same heading

cases = df_all.Case.unique()
same_ylims = True

#custom legend
legend_elements = [Line2D([], [], color='blue', linewidth = 0, marker = 'o', markersize = 10, label='Northwest'),
                   Line2D([], [], color='green', linewidth = 0, marker = 'o', markersize = 10, label='Northeast'),
                   Line2D([], [], color='orange', linewidth = 0, marker = 'o', markersize = 10, label='Southeast'),
                   Line2D([], [], color='black', linewidth = 0, marker = 'o', markersize = 10, label='Southwest')]

RH_metrics = ['Deep Layer RH [%]', 'Deep Layer RH [%]', 'PBL RH [%]', 'PBL RH [%]',
              'Mid Layer RH [%]', 'Mid Layer RH [%]', 'Upper Layer RH [%]', 'Upper Layer RH [%]']

shear_metrics = ['500m Bottom Cap Deep Layer Speed Shear [kts]', '500m Bottom Cap Deep Layer Speed Shear [kts]',
                 'SHARPpy Direct Method PBL Speed Shear [kts]', 'SHARPpy Direct Method PBL Speed Shear [kts]',
                 'SHARPpy Direct Method Mid Layer Speed Shear [kts]', 'SHARPpy Direct Method Mid Layer Speed Shear [kts]',
                 'SHARPpy Direct Method Upper Layer Speed Shear [kts]', 'SHARPpy Direct Method Upper Layer Speed Shear [kts]']

#IMPORTANT:  HOW TO FIX 'KeyError: 0' error:  NEED .iloc[j] AND NOT JUST [j] BECAUSE [j] refers to the index, 
#not the integer position (IP), and groupby function only adjusts IP when making groups and not index!

#create a Series of datetimes for the merged DAWN/dropsonde DataFrame
times = df_all['Date'].astype(str) + df_all['Time'].astype(str)
for i in range(len(df_all)):  #converting the times to datetime objects
    times.iloc[i] = datetime.strptime(times.iloc[i], "%Y%m%d%H%M%S")

#mean-layer relative humidity plot
groupRH_fig = plt.figure(figsize = (24,16))
for i, metric in enumerate(RH_metrics):
    ax = groupRH_fig.add_subplot(4,2,i+1)
    
    if i % 2 == 0:  #LHS plots will be case 13 plots
        case = 13
    elif i % 2 == 1:  #RHS plots will be case 16 plots
        case = 16
        
    for j in range(len(df_all)):
        
        if df_all['Case'].iloc[j] != case:  
            continue
        else:
            if df_all['Quadrant Relative to Convection'].iloc[j] == 'Northwest':
                color = 'blue'
            elif df_all['Quadrant Relative to Convection'].iloc[j] == 'Northeast':
                color = 'green'
            elif df_all['Quadrant Relative to Convection'].iloc[j] == 'Southeast':
                color = 'orange'
            elif df_all['Quadrant Relative to Convection'].iloc[j] == 'Southwest':
                color = 'black'
        
            if df_all['Environment Falling In'].iloc[j] == 'Clear Near':
                mark = 'o'
            elif df_all['Environment Falling In'].iloc[j] == 'In Cloud':
                mark = '$C$'
            elif df_all['Environment Falling In'].iloc[j] == 'In Precip':
                mark = '$P$'
            elif df_all['Environment Falling In'].iloc[j] == 'Clear Far':
                mark = '$F$'
                color = 'pink'
                
            ax.scatter(times.iloc[j], df_all[metric].iloc[j], c = color, s = 40, marker = mark)

    if same_ylims:
        padding = 2  #the ylim padding so that the markers aren't cut off in the plots
        ax.set_ylim([df_all[metric].min() - padding, df_all[metric].max() + padding])  #NOTE: error will occur if there is a '--' value in the Pandas Series (fine if there are NaN values though), as .min() will choose this string value as the minimum
        
    ax.set_title('Case ' + str(case) + ' ' + metric[:-4])
    ax.set_xlabel('Time [UTC]')
    ax.set_ylabel(metric)
    ax.legend(handles = legend_elements)
    ax.tick_params(axis='x', rotation = 50)
    ax.tick_params(length = 15, width = 5)
    ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%H:%M:%S"))
    ax.xaxis.set_major_locator(ticker.MaxNLocator(20))      #sets number of ticks
    #ax.set_xlim([np.datetime64(range_start),np.datetime64(range_end)])

ts = plt.suptitle('Case 13 vs. Case 16 Mean-layer RH Time Series', size = 'xx-large', fontweight = 'bold')
#groupRH_fig.legend(handles = legend_elements, loc = 'center', fontsize = 25)
#plt.subplots_adjust(hspace=0.5)
plt.tight_layout()
plt.savefig('/Users/brodenkirch/Desktop/Case13and16_RH_TimeSeries_Quadrant.png', bbox_inches = 'tight')
plt.close()


#mean-layer speed shear plot
groupSS_fig = plt.figure(figsize = (24,16))
for i, metric in enumerate(shear_metrics):
    ax = groupSS_fig.add_subplot(4,2,i+1)
    
    if i % 2 == 0:  #LHS plots will be case 13 plots
        case = 13
    elif i % 2 == 1:  #RHS plots will be case 16 plots
        case = 16
        
    for j in range(len(df_all)):
        
        if df_all['Case'].iloc[j] != case:  
            continue
        else:
            if df_all['Quadrant Relative to Convection'].iloc[j] == 'Northwest':
                color = 'blue'
            elif df_all['Quadrant Relative to Convection'].iloc[j] == 'Northeast':
                color = 'green'
            elif df_all['Quadrant Relative to Convection'].iloc[j] == 'Southeast':
                color = 'orange'
            elif df_all['Quadrant Relative to Convection'].iloc[j] == 'Southwest':
                color = 'black'
        
            if df_all['Environment Falling In'].iloc[j] == 'Clear Near':
                mark = 'o'
            elif df_all['Environment Falling In'].iloc[j] == 'In Cloud':
                mark = '$C$'
            elif df_all['Environment Falling In'].iloc[j] == 'In Precip':
                mark = '$P$'
            elif df_all['Environment Falling In'].iloc[j] == 'Clear Far':
                mark = '$F$'
                color = 'pink'
                
            ax.scatter(times.iloc[j], df_all[metric].iloc[j], c = color, s = 40, marker = mark)

    if same_ylims:
        padding = 2  #the ylim padding so that the markers aren't cut off in the plots
        ax.set_ylim([df_all[metric].min() - padding, df_all[metric].max() + padding])  #NOTE: error will occur if there is a '--' value in the Pandas Series (fine if there are NaN values though), as .min() will choose this string value as the minimum

    if 'Bottom Cap' in metric:
        ax.set_title('Case ' + str(case) + ' ' + metric[16:-6])
        ax.set_ylabel(metric[16:])
    else:
        ax.set_title('Case ' + str(case) + ' ' + metric[22:-6])
        ax.set_ylabel(metric[22:])
        
    ax.set_xlabel('Time [UTC]')
    ax.legend(handles = legend_elements)
    ax.tick_params(axis='x', rotation = 50)
    ax.tick_params(length = 15, width = 5)
    ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%H:%M:%S"))
    ax.xaxis.set_major_locator(ticker.MaxNLocator(20))      #sets number of ticks
    #ax.set_xlim([np.datetime64(range_start),np.datetime64(range_end)])

ts = plt.suptitle('Case 13 vs. Case 16 Mean-layer Speed Shear Time Series', size = 'xx-large', fontweight = 'bold')
#groupSS_fig.legend(handles = legend_elements, loc = 'upper center', fontsize = 25)
#plt.subplots_adjust(hspace=0.5)
plt.tight_layout()
plt.savefig('/Users/brodenkirch/Desktop/Case13and16_SS_TimeSeries_Quadrant.png', bbox_inches = 'tight')
plt.close()


