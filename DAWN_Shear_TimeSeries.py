#This script creates time series plots of DAWN deep layer shear and also 
#makes time series plots of DAWN upper- (upper level cap) and low-level (500m) winds
#(full wind, not just the components) that are used in the deep shear calculations
import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.gridspec as gridspec
import matplotlib.ticker as ticker
import numpy as np
from datetime import datetime

# matplotlib.rcParams['axes.labelsize'] = 14
# matplotlib.rcParams['axes.titlesize'] = 14
# matplotlib.rcParams['xtick.labelsize'] = 12
# matplotlib.rcParams['ytick.labelsize'] = 12
# matplotlib.rcParams['legend.fontsize'] = 12
# #matplotlib.rcParams['legend.facecolor'] = 'w'
# matplotlib.rcParams['font.family'] = 'arial'

dawn_filepath = os.path.join(os.getcwd(), 'DAWN_Shear_Calculations.csv')
df_dawn = pd.read_csv(dawn_filepath)

cases = df_dawn.Case.unique()
metrics = ['500m Bottom Cap Deep Layer Speed Shear [kts]', '500m Bottom Cap Deep Layer Directional Shear [deg]',
           '500m Wind Speed [kts]', '500m Wind Direction [deg]',
           'Upper Level Cap Wind Speed [kts]', 'Upper Level Cap Wind Direction [deg]']

for case_num in cases:
    group_fig = plt.figure(figsize = (16,16))
    
    #create a Series of DAWN profile datetimes
    dawn_times = df_dawn[df_dawn['Case'] == case_num]['Date'].astype(str) + df_dawn[df_dawn['Case'] == case_num]['Time'].astype(str)

    for i in range(len(dawn_times)):  #converting the times to datetime objects
        dawn_times.iloc[i] = datetime.strptime(dawn_times.iloc[i], "%Y%m%d%H%M%S")

    for i, metric in enumerate(metrics):
        ax = group_fig.add_subplot(3,2,i+1)
        dawn_metric = df_dawn[df_dawn['Case'] == case_num][metric]
        
        ax.scatter(dawn_times, dawn_metric, color = 'k', s = 40, zorder = 2)
        ax.set_title(metric[:-6])
    
        if '[kts]' in metric:
            ax.set_ylabel('Knots')
        elif '[deg]' in metric:
            ax.set_ylabel('Degrees')
            
        ax.set_xlabel('Time [UTC]')
        ax.tick_params(axis='x', rotation = 50)
        ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%H:%M:%S"))
        ax.xaxis.set_major_locator(ticker.MaxNLocator(20))
        #ax.set_xticks(dawn_times[::8])  #only label every 8th time
            
        if metric[-5:] == '[deg]':  #directional shear
            padding = 10  #the ylim padding so that the markers aren't cut off in the plots
        else:  #speed shear
            padding = 2
            
        #get the min/max of the metric
        metric_min = df_dawn[metric].min()
        metric_max = df_dawn[metric].max()
        
        ax.set_ylim([metric_min - padding, metric_max + padding])  #NOTE: error will occur if there is a '--' value in the Pandas Series, as .min() will choose this string value as the minimum
        ax.grid(axis='both', zorder = 1)
        
    #ts = plt.suptitle('Case ' + str(case_num) + ' Shear, 500m Wind, and Upper Level Cap Wind', size = 'xx-large')
    ts = plt.suptitle('Case ' + str(case_num) + ' Shear, 500m Wind, and Upper Level Cap Wind', size = 'xx-large')
    plt.subplots_adjust(hspace=0.5)
    plt.savefig('/Users/brodenkirch/Desktop/Case' + str(case_num) + 'Shear.png')
    plt.close()








