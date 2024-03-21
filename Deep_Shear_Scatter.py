import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.lines import Line2D
import matplotlib.gridspec as gridspec
import numpy as np

matplotlib.rcParams['axes.labelsize'] = 14
matplotlib.rcParams['axes.titlesize'] = 14
matplotlib.rcParams['xtick.labelsize'] = 12
matplotlib.rcParams['ytick.labelsize'] = 12
matplotlib.rcParams['legend.fontsize'] = 12
#matplotlib.rcParams['legend.facecolor'] = 'w'
matplotlib.rcParams['font.family'] = 'arial'

#drop_filepath = os.path.join(os.getcwd(), 'Dropsonde_Metric_Calculations.csv')
drop_filepath = os.path.join(os.getcwd(), 'Dropsonde_Metric_Calculations_CPEXCV.csv')
df_drop = pd.read_csv(drop_filepath)

#dawn_filepath = os.path.join(os.getcwd(), 'DAWN_Shear_Calculations.csv')
dawn_filepath = os.path.join(os.getcwd(), 'DAWN_Shear_Calculations_CPEXCV.csv')
df_dawn = pd.read_csv(dawn_filepath)

cindy_days = ['20170619','20170620','20210826','20210828','20210901','20210904']  #including TDs as TCs (from both CPEX and CPEX-AW)

#IMPORTANT:  HOW TO FIX 'KeyError: 0' error:  NEED .iloc[j] AND NOT JUST [j] BECAUSE [j] refers to the index, 
#not the integer position (IP), and groupby function only adjusts IP when making groups and not index!

#for convective type comparison of All Lifecycles dropsondes
def make_plot(plotting_metric):  #parameter will be a data column from df1
    xlist = []
    for i in range(len(df1)):
        xstring = str(df1['Case'][i])
        xlist.append(xstring)
    
    fig = plt.figure(figsize=(16,21))
    
    #custom legend
    legend_elements = [Line2D([], [], color='red', label='Isolated'), 
                       Line2D([], [], color='blue', label='Organized'),
                       #Line2D([], [], color='#1E90FF', label='Organized (TS Cindy)'),
                       Line2D([], [], color='black', label='Scattered')]
    
    #the lighter shades account for TS Cindy organized cases and, further, TS Cindy cases that were away from the main organized convection and instead near the cyclonic center
    for j in range(len(plotting_metric)):
        #if (df1['Convective Lifecycle'][j] != 'Weakening') and (df1['Environment Falling In'][j] == 'Clear Near' or df1['Environment Falling In'][j] == 'In Cloud' or df1['Environment Falling In'][j] == 'In Precip'):
        if df1['Environment Falling In'][j] == 'Clear Near' or df1['Environment Falling In'][j] == 'In Cloud' or df1['Environment Falling In'][j] == 'In Precip':
            if df1['Primary Convective Type'][j] == 'Isolated':
                color = 'red'
                if str(df1['Date'][j]) in cindy_days:
                    color = '#FF6A6A'  #hex code for lighter red
                    if str(df1['Date'][j]) == '20170620' and (185600 < df1['Time'][j] < 205200):
                        color = '#FFB6C1'  #hex code for even lighter red (pink)
            elif df1['Primary Convective Type'][j] == 'Organized':
                color = 'blue'
                if str(df1['Date'][j]) in cindy_days:
                    color = '#1E90FF'  #hex code for lighter blue
                    if str(df1['Date'][j]) == '20170620' and (185600 < df1['Time'][j] < 205200):
                        color = '#98F5FF'  #hex code for even lighter blue
            else:  #df1['Primary Convective Type'][j] == 'Scattered':
                color = 'black'
                if str(df1['Date'][j]) in cindy_days:
                    color = '#808080'  #hex code for gray
                    if str(df1['Date'][j]) == '20170620' and (185600 < df1['Time'][j] < 205200):
                        color = '#CCCCCC'  #hex code for even lighter gray
                
            if df1['Environment Falling In Ambiguous'][j] == 'Yes' and df1['Convective Lifecycle'][j] == 'Growing':
                mark = '$?G$'
                outline = None
            elif df1['Environment Falling In Ambiguous'][j] == 'Yes' and df1['Environment Falling In'][j] == 'In Precip':
                mark = '$?P$'
                outline = None
            elif df1['Convective Lifecycle'][j] == 'Growing' and df1['Environment Falling In'][j] == 'In Precip':
                mark = '$GP$'
                outline = None
            elif df1['Environment Falling In Ambiguous'][j] == 'Yes':
                mark = '$?$'
                outline = None 
            elif df1['Convective Lifecycle'][j] == 'Growing':
                mark = '$G$'
                outline = None   
            elif df1['Environment Falling In'][j] == 'In Precip':
                mark = '$P$'
                outline = None
            else:
                mark = 'o'
                outline = 'black'
            
            #distinguishes the least complete profile (data down to only 942mb)
            if str(df1['Date'][j]) == '20170611' and str(df1['Time'][j]) == '213013':
                mark = '$?x$'      #? because this dropsonde is also ambiguous
                outline = None
            
            # #distinguishes the profile that does not reach the lowest max height (this dropsonde max height is ~1km lower than the next lowest)
            # if str(df1['Date'][j]) == '20170606' and str(df1['Time'][j]) == '212211':
            #     mark = 'x'
            #     outline = None
        
            plt.scatter(xlist[j], plotting_metric[j], c = color, s = 60, marker = mark, edgecolor = outline)
            
    plt.grid(True)
    plt.xlabel('Case', fontsize = 30, fontweight = 'bold')
    #plt.ylim([0,50])
    plt.tick_params(length = 15, width = 5, labelsize = 25)
    plt.legend(handles = legend_elements, fontsize = 25)
 

#Deep Layer Speed Shear (500m bottom cap) with DAWN shear too
# df1 = pd.concat([df_drop, df_dawn], ignore_index = True)  #concatenates fields with same heading
# make_plot(df1['500m Bottom Cap Deep Layer Speed Shear [kts]'])
# plt.title('Deep Layer Shear (Dropsonde & DAWN, ~0.5 - 7.6km)\n vs. Convective Type (All Lifecycles)', fontsize = 33, fontweight = 'bold')
# plt.ylabel('Deep Layer Speed Shear [kts]', fontsize = 30, fontweight = 'bold')
# plt.savefig('/Users/brodenkirch/Desktop/1SSwDAWN.png', bbox_inches = 'tight')
# plt.close()

# #Deep Layer Directional Shear (500m bottom cap) with DAWN shear too
# df1 = pd.concat([df_drop, df_dawn], ignore_index = True)  #concatenates fields with same heading
# make_plot(df1['500m Bottom Cap Deep Layer Directional Shear [deg]'])
# plt.ylim([0,360])
# plt.title('Deep Layer Shear (Dropsonde & DAWN, ~0.5 - 7.6km)\n vs. Convective Type (All Lifecycles)', fontsize = 33, fontweight = 'bold')
# plt.ylabel('Deep Layer Directional Shear [deg]', fontsize = 30, fontweight = 'bold')
# plt.savefig('/Users/brodenkirch/Desktop/1DSwDAWN.png', bbox_inches = 'tight')
# plt.close()

# FOR PASADENA STM (STYLE OF AMS TROPICAL POSTER)
#for convective type comparison of All Lifecycles dropsondes
def make_plot_onlyIsoOrg(plotting_metric):  #parameter will be a data column from df1
    xlist = []
    for i in range(len(df1)):
        xstring = str(df1['Case'][i])
        xlist.append(xstring)
    
    fig = plt.figure(figsize=(16,21))
    
    #custom legend
    legend_elements = [Line2D([], [], color='red', linewidth = 0, marker = 'o', markersize = 15, label='Isolated'),
                       Line2D([], [], color='red', linewidth = 0, marker = '$P$', markersize = 15, label='Isolated (In Precip)'),
                       Line2D([], [], color='blue', linewidth = 0, marker = 'o', markersize = 15, label='Organized'),
                       Line2D([], [], color='blue', linewidth = 0, marker = '$P$', markersize = 15, label='Organized (In Precip)')]
    
    #the lighter shades account for TS Cindy organized cases and, further, TS Cindy cases that were away from the main organized convection and instead near the cyclonic center
    for j in range(len(plotting_metric)):
        #if (df1['Convective Lifecycle'][j] != 'Weakening') and (df1['Environment Falling In'][j] == 'Clear Near' or df1['Environment Falling In'][j] == 'In Cloud' or df1['Environment Falling In'][j] == 'In Precip'):
        if df1['Environment Falling In'][j] == 'Clear Near' or df1['Environment Falling In'][j] == 'In Cloud' or df1['Environment Falling In'][j] == 'In Precip':
            if df1['Primary Convective Type'][j] == 'Isolated':
                color = 'red'
                if str(df1['Date'][j]) in cindy_days:
                    color = '#FF6A6A'  #hex code for lighter red
                    if str(df1['Date'][j]) == '20170620' and (185600 < df1['Time'][j] < 205200):
                        color = '#FFB6C1'  #hex code for even lighter red (pink)
                    continue
            elif df1['Primary Convective Type'][j] == 'Organized':
                color = 'blue'
                if str(df1['Date'][j]) in cindy_days:
                    continue
            else:
                continue
                  
            if df1['Environment Falling In'][j] == 'In Precip':
                mark = '$P$'
                outline = None
                #mark = 'o'
                #outline = 'black'
            else:
                mark = 'o'
                outline = 'black'
                
            plt.scatter(xlist[j], plotting_metric[j], c = color, s = 150, marker = mark, edgecolor = outline)
    
    plt.grid(True)
    plt.xlabel('Case', fontsize = 30, fontweight = 'bold')
    plt.tick_params(length = 15, width = 5, labelsize = 25)
    plt.legend(handles = legend_elements, fontsize = 25, ncol = 2)

    
# FOR CPEX-CV STM (STYLE OF AMS TROPICAL POSTER)
#for convective type comparison of All Lifecycles dropsondes
def make_plot_CPEXCV(plotting_metric):  #parameter will be a data column from df1
    xlist = []
    for i in range(len(df1)):
        xstring = str(df1['Case'][i])
        xlist.append(xstring)
    
    fig = plt.figure(figsize=(16,21))
    
    #custom legend
    legend_elements = [Line2D([], [], color='red', linewidth = 0, marker = 'o', markersize = 15, label='Isolated'),
                       Line2D([], [], color='red', linewidth = 0, marker = '$P$', markersize = 15, label='Isolated (In Precip)'),
                       Line2D([], [], color='blue', linewidth = 0, marker = 'o', markersize = 15, label='Organized'),
                       Line2D([], [], color='blue', linewidth = 0, marker = '$P$', markersize = 15, label='Organized (In Precip)'),
                       Line2D([], [], color='black', linewidth = 0, marker = 'o', markersize = 15, label='Scattered'),
                       Line2D([], [], color='black', linewidth = 0, marker = '$P$', markersize = 15, label='Scattered (In Precip)')]
    
    #the lighter shades account for TS Cindy organized cases and, further, TS Cindy cases that were away from the main organized convection and instead near the cyclonic center
    for j in range(len(plotting_metric)):
        #if (df1['Convective Lifecycle'][j] != 'Weakening') and (df1['Environment Falling In'][j] == 'Clear Near' or df1['Environment Falling In'][j] == 'In Cloud' or df1['Environment Falling In'][j] == 'In Precip'):
        if df1['Environment Falling In'][j] == 'Clear Near' or df1['Environment Falling In'][j] == 'In Cloud' or df1['Environment Falling In'][j] == 'In Precip':
            if df1['Primary Convective Type'][j] == 'Isolated':
                color = 'red'
            elif df1['Primary Convective Type'][j] == 'Organized':
                color = 'blue'
            else:  #convective type is Scattered
                color = 'black'
                  
            if df1['Environment Falling In'][j] == 'In Precip':
                mark = '$P$'
                outline = None
                #mark = 'o'
                #outline = 'black'
            else:
                mark = 'o'
                outline = 'black'
                
            plt.scatter(xlist[j], plotting_metric[j], c = color, s = 150, marker = mark, edgecolor = outline)
    
    plt.grid(True)
    plt.xlabel('Case', fontsize = 30, fontweight = 'bold')
    plt.tick_params(length = 15, width = 5, labelsize = 25)
    plt.legend(handles = legend_elements, fontsize = 25, ncol = 1)

#Deep Layer Speed Shear (500m bottom cap) with DAWN shear too
df1 = pd.concat([df_drop, df_dawn], ignore_index = True)  #concatenates fields with same heading
make_plot_CPEXCV(df1['500m Bottom Cap Deep Layer Speed Shear [kts]'])
#plt.ylim([0,55])
plt.title('Deep Layer Shear (Dropsonde & DAWN, 0.5km - 7.6km)', fontsize = 33, fontweight = 'bold')
plt.ylabel('Deep Layer Speed Shear [kts]', fontsize = 30, fontweight = 'bold')
plt.savefig('/Users/brodenkirch/Desktop/1SSwDAWN_poster.png', bbox_inches = 'tight')
plt.close()

#Deep Layer Directional Shear (500m bottom cap) with DAWN shear too
df1 = pd.concat([df_drop, df_dawn], ignore_index = True)  #concatenates fields with same heading
make_plot_CPEXCV(df1['500m Bottom Cap Deep Layer Directional Shear [deg]'])
plt.ylim([0,360])
plt.title('Deep Layer Shear (Dropsonde & DAWN, 0.5 - 7.6km)\n vs. Convective Type (All Lifecycles)', fontsize = 33, fontweight = 'bold')
plt.ylabel('Deep Layer Directional Shear [deg]', fontsize = 30, fontweight = 'bold')
plt.savefig('/Users/brodenkirch/Desktop/1DSwDAWN_poster.png', bbox_inches = 'tight')
plt.close()



