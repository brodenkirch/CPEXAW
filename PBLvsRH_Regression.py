import os
import sys
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import scipy.stats

# matplotlib.rcParams['axes.labelsize'] = 14
# matplotlib.rcParams['axes.titlesize'] = 14
# matplotlib.rcParams['xtick.labelsize'] = 12
# matplotlib.rcParams['ytick.labelsize'] = 12
# matplotlib.rcParams['legend.fontsize'] = 12
#matplotlib.rcParams['legend.facecolor'] = 'w'
matplotlib.rcParams['font.family'] = 'arial'

drop_filepath = os.path.join(os.getcwd(), 'Dropsonde_PBL_MidRH_Correlation.csv')
df = pd.read_csv(drop_filepath)

# #change the old index (which still references non-sorted rows) to a new index (which references the sorted rows)
# new_index = np.arange(0, len(df1), 1)
# df_sort = df.sort_values(['Region', 'Case']).set_index(new_index)
# #^^^orders by region first, then by case within each region group

cindy_days = ['20170619','20170620','20210826','20210828','20210901','20210904']  #including TDs as TCs (from both CPEX and CPEX-AW)

rh_layers = ['Mid Layer RH [%]']

#######################################################################################################

#IMPORTANT:  HOW TO FIX 'KeyError: 0' error:  NEED .iloc[j] AND NOT JUST [j] BECAUSE [j] refers to the index, 
#not the integer position (IP), and groupby function only adjusts IP when making groups and not index!
 
#for convective type comparison of All Lifecycles dropsondes
def make_plot_onlyIsoOrg_RH(plotting_metric_name, ax):  #parameter will be a data column from df
    
    plotting_metric_PBL = df['PBL Top [mb]']
    plotting_metric = df[plotting_metric_name]
    
    for j in range(len(plotting_metric_PBL)):
        #if (df['Convective Lifecycle'][j] != 'Weakening') and (df['Environment Falling In'][j] == 'Clear Near' or df['Environment Falling In'][j] == 'In Cloud' or df['Environment Falling In'][j] == 'In Precip'):
        if df['Environment Falling In'][j] == 'Clear Near' or df['Environment Falling In'][j] == 'In Cloud':
            if df['Primary Convective Type'][j] == 'Isolated':
                color = 'red'
                if str(df['Date'][j]) in cindy_days:
                    continue
            elif df['Primary Convective Type'][j] == 'Organized':
                color = 'blue'
                if str(df['Date'][j]) in cindy_days:
                    continue
            else:
                continue
                  
            if df['Environment Falling In'][j] == 'In Cloud':
                mark = '$C$'
                outline = None
            else:
                mark = 'o'
                outline = 'black'
        
            ax.scatter(plotting_metric[j], plotting_metric_PBL[j], c = color, s = 150, marker = mark, edgecolor = outline)
  
    # Fit linear regression via least squares with numpy.polyfit
    # It returns a slope (a) and intercept (b)
    # deg = 1 means linear fit (i.e. polynomial of degree 1)
    #a, b = np.polyfit(plotting_metric, plotting_metric_PBL, deg = 1)
    
    #plotting metric is the independent variable, plotting_metric_PBL is the independent variable
    slope, intercept, Rvalue, pvalue, stderr = scipy.stats.linregress(plotting_metric, plotting_metric_PBL)
    
    #the below two lines DO NOT produce the same slope, intercept, and stderr
    #print (scipy.stats.linregress(plotting_metric, plotting_metric_PBL)) (slope = mb/%)
    #print (scipy.stats.linregress(plotting_metric_PBL, plotting_metric)) (slope = %/mb)
    
    # Create sequence of 200 RHs from 0 to 100 
    xseq = np.linspace(0, 100, num=200)
    
    print ('Linear Regression Coefficient:', slope)
    print ('Pearson Correlation Coefficient:', Rvalue)
    #print ('Pearson Correlation coefficient:', scipy.stats.pearsonr(plotting_metric, plotting_metric_PBL)) #same as above
    #print ('Pearson Correlation coefficient:', scipy.stats.pearsonr(plotting_metric_PBL, plotting_metric)) #same as above

    # Plot regression line
    ax.plot(xseq, intercept + slope * xseq, color = 'k', linestyle = '--', linewidth = 3)         
  
    ax.grid(True)
    ax.set_title('PBL Depth vs. ' + plotting_metric_name[:-4], fontsize = 33, fontweight = 'bold')
    ax.set_xlabel(plotting_metric_name, fontsize = 30, fontweight = 'bold')
    ax.set_ylabel('PBL Depth [hPa]', fontsize = 30, fontweight = 'bold')
    ax.set_xlim([30,90])
    ax.set_ylim([1005,900])
    #ax.invert_yaxis()
    ax.set_yticks(np.arange(1000,899,-10))
    ax.tick_params(length = 15, width = 5, labelsize = 25)
    
    #custom legend
    legend_elements = [Line2D([], [], color='k', linewidth = 3, linestyle = '--', label=f'$y = {slope:.1f}x {intercept:+.1f}$'),
                       Line2D([], [], color='red', linewidth = 0, marker = 'o', markersize = 15, label='Isolated (Clear)'),
                       Line2D([], [], color='red', linewidth = 0, marker = '$C$', markersize = 15, label='Isolated (In Cloud)'),
                       Line2D([], [], color='blue', linewidth = 0, marker = 'o', markersize = 15, label='Organized (Clear)'),
                       Line2D([], [], color='blue', linewidth = 0, marker = '$C$', markersize = 15, label='Organized (In Cloud)')]
    
    ax.legend(handles = legend_elements, loc = 'lower left', fontsize = 25)
 
group_fig = plt.figure(figsize=(16,16))

for i, layer in enumerate(rh_layers):
    ax = group_fig.add_subplot(1,1,i+1)
    make_plot_onlyIsoOrg_RH(layer, ax)

plt.savefig('/Users/brodenkirch/Desktop/RHvsPBL.png', bbox_inches = 'tight')
plt.close()
