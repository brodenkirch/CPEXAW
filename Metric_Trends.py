import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.lines import Line2D
import matplotlib.gridspec as gridspec
import numpy as np

filepath = os.path.join(os.getcwd(), 'Dropsonde_Metric_Calculations.csv')
df1 = pd.read_csv(filepath)

dawn_filepath = os.path.join(os.getcwd(), 'DAWN_Shear_Calculations.csv')
df_dawn = pd.read_csv(dawn_filepath)

#change the old index (which still references non-sorted rows) to a new index (which references the sorted rows)
new_index = np.arange(0, len(df1), 1)
df2 = df1.sort_values(['Region', 'Case']).set_index(new_index)
#^^^orders by region first, then by case within each region group

cindy_days = ['20170619','20170620','20210826','20210828','20210901','20210904']  #including TDs as TCs (from both CPEX and CPEX-AW)


#######################################################################################################
#THE NEXT 3 FUNCTIONS ARE USED TO MAKE TIME SERIES PLOTS (INCLUDING DAWN DEEP SHEAR TIME SERIES)

#creating a custom legend
def create_proxy(label):
    line = Line2D([0], [0], linestyle='none', mfc='black',
                mec='none', marker=r'$\mathregular{{{}}}$'.format(label))
    return line

#IMPORTANT:  HOW TO FIX 'KeyError: 0' error:  NEED .iloc[j] AND NOT JUST [j] BECAUSE [j] refers to the index, 
#not the integer position (IP), and groupby function only adjusts IP when making groups and not index!
def plot_points(case, time, metric, ax):   #plots the scatter plot with correct marks based on Env't Falling In
    for j in range(len(time)):
        if (str(case[1]['Date'].iloc[j]) == '20170620') and (185600 < time.iloc[j] < 205200):  #dropsonde was dropped in TS Cindy cyclonic center; not representative of rain band environment
            color = '#00BFFF'  #hex code for lighter blue
        else:
            color = 'b'
            
        if case[1]['Environment Falling In Ambiguous'].iloc[j] == 'Yes':
            if case[1]['Environment Falling In'].iloc[j] == 'Clear Near':
                mark = '$?N$'
            elif case[1]['Environment Falling In'].iloc[j] == 'In Cloud':
                mark = '$?C$'
            elif case[1]['Environment Falling In'].iloc[j] == 'In Precip':
                mark = '$?P$'
            elif case[1]['Environment Falling In'].iloc[j] == 'Clear Far':
                mark = '$?F$'
                color = '#98F5FF'  #hex code for even lighter blue
        else:
            if case[1]['Environment Falling In'].iloc[j] == 'Clear Near':
                mark = '$N$'
            elif case[1]['Environment Falling In'].iloc[j] == 'In Cloud':
                mark = '$C$'
            elif case[1]['Environment Falling In'].iloc[j] == 'In Precip':
                mark = '$P$'
            elif case[1]['Environment Falling In'].iloc[j] == 'Clear Far':
                mark = '$F$'
                color = '#98F5FF'  #hex code for even lighter blue
        
        #distinguishes the least complete profile (data down to only 942mb)
        if str(case[1]['Date'].iloc[j]) == '20170611' and str(time.iloc[j]) == '213013':
            mark = '$?x$'      #? because this dropsonde is also ambiguous
        
        # #distinguishes the profile that does not reach the lowest max height (this dropsonde max height is ~1km lower than the next lowest)
        # if str(case[1]['Date'].iloc[j]) == '20170606' and str(time.iloc[j]) == '212211':
        #     mark = 'x'
    
        ax.scatter(time.iloc[j], case[1][metric].iloc[j], c = color, s = 40, marker = mark)


#CODE TO CREATE THE TIME SERIES PLOTS
def make_time_series(same_ylims = True):  #same_ylims WILL NEED TO BE CHANGED IF YOU DO/DON'T WANT THE YLIMS TO BE UNIFORM FOR A GIVEN METRIC ACROSS CASES
    df_group = df1.groupby(df1.Case)
    df_dawn_group = df_dawn.groupby(['Case'])   
    
    # Create a legend with only labels
    labels = ['N:', 'C:', 'P:', 'F:']
    proxies = [create_proxy(item) for item in labels]
    descriptions = ['Clear Near', 'In Cloud', 'In Precip', 'Clear Far']
    
    #dictionary of rough lifecycle transition times (ex. mature to weakening) for each case
    lifecycle_dict = {1: [214100], 3: [204500], 4: [], 5: [195000], 6: [], 7: [], 9: [201500], 10: [183000], 11: [], 12: [], 13: [183000, 201000]}
    
    PBL_RH_metrics = ['PBL Top [mb]', 'Deep Layer RH [%]', 'PBL RH [%]', 'Mid Layer RH [%]']
    thermo_metrics = ['Deep Layer MLCAPE [J/kg]', 'Deep Layer MUCAPE [J/kg]',
                    'Below FZL MLCAPE [J/kg]', 'Below FZL MUCAPE [J/kg]',
                    'ML LCL [mb]', 'MU LCL [mb]']
    # shear_metrics = ['SHARPpy Direct Method Deep Layer Speed Shear [kts]',
    #                  'SHARPpy Direct Method Layer Directional Shear [deg]',
    #                  'SHARPpy Direct Method PBL Speed Shear [kts]',
    #                  'SHARPpy Direct Method PBL Directional Shear [deg]',
    #                  'SHARPpy Direct Method Mid Layer Speed Shear [kts]',
    #                  'SHARPpy Direct Method Mid Layer Directional Shear [deg]']
    shear_metrics = ['500m Bottom Cap Deep Layer Speed Shear [kts]',
                      '500m Bottom Cap Deep Layer Directional Shear [deg]',
                      'SHARPpy Direct Method PBL Speed Shear [kts]',
                      'SHARPpy Direct Method PBL Directional Shear [deg]',
                      'SHARPpy Direct Method Mid Layer Speed Shear [kts]',
                      'SHARPpy Direct Method Mid Layer Directional Shear [deg]']
    
    #height_metrics = ['Minimum Profile Height [m]', 'Upper Level Cap Height [m]']
    height_metrics = ['500m Bottom Cap Profile Height [m]', 'Upper Level Cap Height [m]']
    
    for case in df_group:
        if case[0] == 2 or case[0] == 8:  #only have one dropsonde for each of these cases
            continue
        time = case[1]['Time']
        
        group_fig = plt.figure(figsize = (16,16))
        for i, metric in enumerate(PBL_RH_metrics):
            ax = group_fig.add_subplot(2,2,i+1)
            plot_points(case, time, metric, ax)
            for z in lifecycle_dict[case[0]]:  #plotting rough lifecycle transition times
                ax.axvline(x = z, linestyle='--', linewidth = 2, color = 'red', zorder = 0)
            ax.set_title(metric[:-4])
            ax.set_xlabel('Time [UTC]')
            ax.tick_params(axis='x', rotation = 60)
            ax.set_ylabel(metric)
            ax.set_xticks(time)
            ax.legend(proxies, descriptions, numpoints = 1, markerscale = 2)
    
            if same_ylims:
                padding = 2  #the ylim padding so that the markers aren't cut off in the plots
                ax.set_ylim([df1[metric].min() - padding, df1[metric].max() + padding])  #NOTE: error will occur if there is a '--' value in the Pandas Series, as .min() will choose this string value as the minimum
            if metric[-4:] == '[mb]':  #inverty y-axis pressure metrics
                ax.invert_yaxis()                
        ts = plt.suptitle('Case ' + str(case[0]) + ' PBL and RH', size = 'xx-large')
        plt.subplots_adjust(hspace=0.5)
        #plt.savefig('/Users/brodenkirch/Desktop/Case' + str(case[0]) + 'PBLandRH.png')
        plt.close()
        
        group_fig = plt.figure(figsize = (16,16))
        for i, metric in enumerate(thermo_metrics):
            if i < 4:  #for title generation (omitting units in the metric's title)
                cutoff = -7  
            else:
                cutoff = -5
            ax = group_fig.add_subplot(3,2,i+1)
            plot_points(case, time, metric, ax)
            for z in lifecycle_dict[case[0]]:  #plotting rough lifecycle transition times
                ax.axvline(x = z, linestyle='--', linewidth = 2, color = 'red', zorder = 0)
            ax.set_title(metric[:cutoff])
            ax.set_xlabel('Time [UTC]')
            ax.tick_params(axis='x', rotation = 60)
            ax.set_ylabel(metric)
            ax.set_xticks(time)
            ax.legend(proxies, descriptions, numpoints = 1, markerscale = 2)
            
            if same_ylims:
                if metric[-4:] == '[mb]':  #LCL
                    padding = 10  #the ylim padding so that the markers aren't cut off in the plots
                else:  #CAPE
                    padding = 50
                ax.set_ylim([df1[metric].min() - padding, df1[metric].max() + padding])  #NOTE: error will occur if there is a '--' value in the Pandas Series, as .min() will choose this string value as the minimum  
            if metric[-4:] == '[mb]':  #inverty y-axis pressure metrics
                ax.invert_yaxis()                
        ts = plt.suptitle('Case ' + str(case[0]) + ' CAPE and LCL', size = 'xx-large')
        plt.subplots_adjust(hspace=0.5)
        #plt.savefig('/Users/brodenkirch/Desktop/Case' + str(case[0]) + 'CAPEandLCL.png')
        plt.close()
        
        group_fig = plt.figure(figsize = (16,16))
        for i, metric in enumerate(shear_metrics):
            ax = group_fig.add_subplot(3,2,i+1)
    
            #overlay DAWN shear data
            case_num = str(case[0])
            dawn_case = df_dawn['Case']
            new_xticks = False
            if case_num in dawn_case.values:
                new_xticks = True
                dawn_times = df_dawn[dawn_case == case_num]['Time']
                dawn_deep_speed = df_dawn[dawn_case == case_num]['DAWN Deep Layer Speed Shear [kts]']
                dawn_deep_dir = df_dawn[dawn_case == case_num]['DAWN Deep Layer Directional Shear [deg]']
                if 'Deep Layer Speed Shear' in metric:
                    ax.scatter(dawn_times, dawn_deep_speed, color = 'k', s = 40)
                elif 'Deep Layer Directional Shear' in metric:
                    ax.scatter(dawn_times, dawn_deep_dir, color = 'k', s = 40)
            
            plot_points(case, time, metric, ax)        
            for z in lifecycle_dict[case[0]]:  #plotting rough lifecycle transition times
                ax.axvline(x = z, linestyle='--', linewidth = 2, color = 'red', zorder = 0)
            if 'Bottom Cap' in metric:
                ax.set_title(metric[16:-6])
            else:
                ax.set_title(metric[22:-6])
    
            if 'Bottom Cap' in metric:
                ax.set_ylabel(metric[16:])
            else:
                ax.set_ylabel(metric[22:])
                
            ax.set_xlabel('Time [UTC]')
            ax.tick_params(axis='x', rotation = 60)
            ax.legend(proxies, descriptions, numpoints = 1, markerscale = 2)
            if new_xticks:
                xtick_list = list(time) + list(dawn_times)
                ax.set_xticks(xtick_list[::8])  #only label every 8th time
            else:
                ax.set_xticks(time)
                
            if case_num == '13':
                ax.set_xlim([175500, 210000])  #time range (in UTC) of case 13
                
            if same_ylims:
                if metric[-5:] == '[deg]':  #directional shear
                    padding = 10  #the ylim padding so that the markers aren't cut off in the plots
                else:  #speed shear
                    padding = 2
                #get the min/max of the metric for both DAWN and dropsonde Series (if the dropsonde shear metric is also a calculated DAWN shear metric)
                if 'Deep Layer Speed Shear' in metric:
                    dawn_deep_spd = df_dawn['DAWN Deep Layer Speed Shear [kts]']
                    metric_min = min(df1[metric].min(), dawn_deep_spd.min())
                    metric_max = max(df1[metric].max(), dawn_deep_spd.max())
                    ax.set_ylim([metric_min - padding, metric_max + padding])                #NOTE: error will occur if there is a '--' value in the Pandas Series, as .min() will choose this string value as the minimum
                elif 'Deep Layer Directional Shear' in metric:
                    dawn_deep_dir = df_dawn['DAWN Deep Layer Directional Shear [deg]']
                    metric_min = min(df1[metric].min(), dawn_deep_dir.min())
                    metric_max = max(df1[metric].max(), dawn_deep_dir.max())
                    ax.set_ylim([metric_min - padding, metric_max + padding])                #NOTE: error will occur if there is a '--' value in the Pandas Series, as .min() will choose this string value as the minimum
                else:
                    ax.set_ylim([df1[metric].min() - padding, df1[metric].max() + padding])  #NOTE: error will occur if there is a '--' value in the Pandas Series, as .min() will choose this string value as the minimum
       
        ts = plt.suptitle('Case ' + str(case[0]) + ' Shear', size = 'xx-large')
        plt.subplots_adjust(hspace=0.5)
        if case_num in ['1', '7', '13']:
            plt.savefig('/Users/brodenkirch/Desktop/Case' + case_num + 'Shear.png')
        plt.close()
        
        
        group_fig = plt.figure(figsize = (16,16))
        for i, metric in enumerate(height_metrics):
            ax = group_fig.add_subplot(2,1,i+1)
    
            #overlay DAWN height data
            case_num = str(case[0])
            dawn_case = df_dawn['Case']
            new_xticks = False
            if case_num in dawn_case.values:
                new_xticks = True
                dawn_times = df_dawn[dawn_case == case_num]['Time']
                dawn_height = df_dawn[dawn_case == case_num][metric]
                ax.scatter(dawn_times, dawn_height, color = 'k', s = 40)
            
            plot_points(case, time, metric, ax)        
            for z in lifecycle_dict[case[0]]:  #plotting rough lifecycle transition times
                ax.axvline(x = z, linestyle='--', linewidth = 2, color = 'red', zorder = 0)
            ax.set_title(metric[:-4])
            ax.set_xlabel('Time [UTC]')
            ax.tick_params(axis='x', rotation = 60)
            ax.set_ylabel(metric)
            ax.legend(proxies, descriptions, numpoints = 1, markerscale = 2)
            if new_xticks:
                xtick_list = list(time) + list(dawn_times)
                ax.set_xticks(xtick_list[::8])  #only label every 8th time
            else:
                ax.set_xticks(time)
                
            if case_num == '13':
                ax.set_xlim([175500, 210000])  #time range (in UTC) of case 13
                
            if same_ylims:
                padding = 20  #the ylim padding so that the markers aren't cut off in the plots
                
                #get the min/max of the metric for both DAWN and dropsonde height Series
                dawn_heights = df_dawn[metric]
                metric_min = min(df1[metric].min(), dawn_heights.min())
                metric_max = max(df1[metric].max(), dawn_heights.max())
                ax.set_ylim([metric_min - padding, metric_max + padding])                #NOTE: error will occur if there is a '--' value in the Pandas Series, as .min() will choose this string value as the minimum
       
        ts = plt.suptitle('Case ' + str(case[0]) + ' Height Variance', size = 'xx-large')
        plt.subplots_adjust(hspace=0.5)
        plt.savefig('/Users/brodenkirch/Desktop/Case' + case_num + '_500mHeightVariance.png')
        plt.close()

# make_time_series(same_ylims = False)
# sys.exit()

#######################################################################################################

#for convective type comparison of All Lifecycles dropsondes
def make_plot(plotting_metric):  #parameter will be a data column from df1
    xlist = []
    for i in range(len(df1)):
        #xlist.append(df1['Primary Convective Type'][i])  #use this x-axis labeling if you don't care about case #
        xstring = ', '.join([df1['Primary Convective Type'][i][:3], str(df1['Case'][i]), str(df1['Date'][i])])
        xlist.append(xstring)
    
    fig = plt.figure(figsize=(16,21))
    
    #custom legend
    legend_elements = [Line2D([], [], color='red', label='Isolated'), 
                       Line2D([], [], color='blue', label='Organized'),
                       #Line2D([], [], color='#1E90FF', label='Organized (TS Cindy)'),
                       Line2D([], [], color='black', label='Scattered')]
    
    #the lighter shades account for TS Cindy organized cases and, further, TS Cindy cases that were away from the main organized convection and instead near the cyclonic center
    for j in range(len(plotting_metric)):
        #if (df1['Convective Lifecycle'][j] == 'Mature' or df1['Convective Lifecycle'][j] == 'Growing') and (df1['Environment Falling In'][j] == 'Clear Near' or df1['Environment Falling In'][j] == 'In Cloud' or df1['Environment Falling In'][j] == 'In Precip'):
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
    plt.xlabel('Primary Convective Type, Case #, Date', fontsize = 25)
    plt.tick_params(axis='x', rotation = 60, length = 20, labelsize = 15)
    plt.legend(handles = legend_elements)
 
#for regional comparison of All Lifecycles dropsondes for a given convective type
def make_regional_plot(plotting_metric, convective_type = 'Isolated'):  #parameter will be a data column from df2
    xlist2 = []
    for i in range(len(df2)):
        #xlist2.append(df2['Region'][i])  #use this x-axis labeling if you don't care about case #
        xstring2 = ', '.join([df2['Region'][i][:4], str(df2['Case'][i]), str(df2['Date'][i])])
        xlist2.append(xstring2)

    fig = plt.figure(figsize=(16,21))
    
    #custom legend
    legend_elements = [Line2D([], [], color='red', label='Western Atlantic'), 
                       Line2D([], [], color='blue', label='GoM'),
                       Line2D([], [], color='black', label='Caribbean')]
    
    #the lighter shades account for TS Cindy organized cases and, further, TS Cindy cases that were away from the main organized convection and instead near the cyclonic center
    for j in range(len(plotting_metric)):
        #if (df2['Convective Lifecycle'][j] == 'Mature' or df2['Convective Lifecycle'][j] == 'Growing') and (df2['Environment Falling In'][j] == 'Clear Near' or df2['Environment Falling In'][j] == 'In Cloud' or df2['Environment Falling In'][j] == 'In Precip'):
        if df2['Environment Falling In'][j] == 'Clear Near' or df2['Environment Falling In'][j] == 'In Cloud' or df2['Environment Falling In'][j] == 'In Precip':
            if df2['Primary Convective Type'][j] == convective_type:
                if df2['Region'][j] == 'Western Atlantic':
                    color = 'red'
                    if str(df2['Date'][j]) in cindy_days:
                        color = '#FF6A6A'  #hex code for lighter red
                        if str(df2['Date'][j]) == '20170620' and (185600 < df2['Time'][j] < 205200):
                            color = '#FFB6C1'  #hex code for even lighter red (pink)
                elif df2['Region'][j] == 'Gulf':
                    color = 'blue'
                    if str(df2['Date'][j]) in cindy_days:
                        color = '#1E90FF'  #hex code for lighter blue
                        if str(df2['Date'][j]) == '20170620' and (185600 < df2['Time'][j] < 205200):
                            color = '#98F5FF'  #hex code for even lighter blue
                else:  #df2['Region'][j] == 'Caribbean':
                    color = 'black'
                    if str(df2['Date'][j]) in cindy_days:
                        color = '#808080'  #hex code for gray
                        if str(df2['Date'][j]) == '20170620' and (185600 < df2['Time'][j] < 205200):
                            color = '#CCCCCC'  #hex code for even lighter gray
                    
                if df2['Environment Falling In Ambiguous'][j] == 'Yes' and df2['Convective Lifecycle'][j] == 'Growing':
                    mark = '$?G$'
                    outline = None
                elif df2['Environment Falling In Ambiguous'][j] == 'Yes' and df2['Environment Falling In'][j] == 'In Precip':
                    mark = '$?P$'
                    outline = None
                elif df2['Convective Lifecycle'][j] == 'Growing' and df2['Environment Falling In'][j] == 'In Precip':
                    mark = '$GP$'
                    outline = None
                elif df2['Environment Falling In Ambiguous'][j] == 'Yes':
                    mark = '$?$'
                    outline = None 
                elif df2['Convective Lifecycle'][j] == 'Growing':
                    mark = '$G$'
                    outline = None    
                elif df2['Environment Falling In'][j] == 'In Precip':
                    mark = '$P$'
                    outline = None
                else:
                    mark = 'o'
                    outline = 'black'
                
                #distinguishes the least complete profile (data down to only 942mb)
                if str(df2['Date'][j]) == '20170611' and str(df2['Time'][j]) == '213013':
                    mark = '$?x$'      #? because this dropsonde is also ambiguous
                    outline = None
                
                # #distinguishes the profile that does not reach the lowest max height (this dropsonde max height is ~1km lower than the next lowest)
                # if str(df2['Date'][j]) == '20170606' and str(df2['Time'][j]) == '212211':
                #     mark = 'x'
                #     outline = None
            
                plt.scatter(xlist2[j], plotting_metric[j], c = color, s = 60, marker = mark, edgecolor = outline)
                
    plt.grid(True)
    plt.xlabel('Region, Case #, Date', fontsize = 25)
    plt.tick_params(axis='x', rotation = 60, length = 20, labelsize = 15)
    plt.legend(handles = legend_elements)
    
#for intra-case convective lifecycle influence on metrics
def intracase_plot(plotting_metric):  #parameter will be a data column from df1
    xlist = []
    for i in range(len(df1)):
        #xlist.append(df1['Primary Convective Type'][i])  #use this x-axis labeling if you don't care about case #
        xstring = ', '.join([df1['Primary Convective Type'][i][:3], str(df1['Case'][i]), str(df1['Date'][i])])
        xlist.append(xstring)
    
    fig = plt.figure(figsize=(16,21))
    
    #custom legend
    legend_elements = [Line2D([], [], color='red', label='Isolated'), 
                        Line2D([], [], color='blue', label='Organized'),
                        #Line2D([], [], color='#1E90FF', label='Organized (TS Cindy)'),
                        Line2D([], [], color='black', label='Scattered')]
    
    #the lighter shades account for TS Cindy organized cases and, further, TS Cindy cases that were away from the main organized convection and instead near the cyclonic center
    for j in range(len(plotting_metric)):
        if df1['Environment Falling In'][j] == 'Clear Far':
            continue
        else:
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
                
            if df1['Convective Lifecycle'][j] == 'Growing':
                mark = '$G$'
            elif df1['Convective Lifecycle'][j] == 'Mature':
                mark = '$M$'
            elif df1['Convective Lifecycle'][j] == 'Weakening':
                mark = '$W$'
            
            #distinguishes the least complete profile (data down to only 942mb)
            if str(df1['Date'][j]) == '20170611' and str(df1['Time'][j]) == '213013':
                mark = '$XW$'      #? because this dropsonde is also ambiguous
            
            # #distinguishes the profile that does not reach the lowest max height (this dropsonde max height is ~1km lower than the next lowest)
            # if str(df1['Date'][j]) == '20170606' and str(df1['Time'][j]) == '212211':
            #     mark = '$XM$'
        
            plt.scatter(xlist[j], plotting_metric[j], c = color, s = 60, marker = mark)
            
    plt.grid(True)
    plt.xlabel('Primary Convective Type, Case #, Date', fontsize = 25)
    plt.tick_params(axis='x', rotation = 60, length = 20, labelsize = 15)
    plt.legend(handles = legend_elements)


#PBL top
make_plot(df1['PBL Top [mb]'])
plt.title('PBL Top Distribution vs. Primary Convective Type (All Lifecycles)', fontsize = 30)
plt.ylabel('Pressure [mb]', fontsize = 25)
plt.ylim([1005,900])
plt.yticks(np.arange(1000,899,-10))
plt.savefig('/Users/brodenkirch/Desktop/1PBL.png')
plt.close()

#Deep Layer RH
make_plot(df1['Deep Layer RH [%]'])
plt.title('Deep Layer RH vs. Primary Convective Type (All Lifecycles)', fontsize = 30)
plt.ylabel('Deep Layer RH [%]', fontsize = 25)
plt.savefig('/Users/brodenkirch/Desktop/1RH.png')
plt.close()

#PBL RH
make_plot(df1['PBL RH [%]'])
plt.title('PBL RH vs. Primary Convective Type (All Lifecycles)', fontsize = 30)
plt.ylabel('PBL RH [%]', fontsize = 25)
plt.savefig('/Users/brodenkirch/Desktop/2RH.png')
plt.close()

#Mid Layer RH
make_plot(df1['Mid Layer RH [%]'])
plt.title('Mid Layer RH vs. Primary Convective Type (All Lifecycles)', fontsize = 30)
plt.ylabel('Mid Layer RH [%]', fontsize = 25)
plt.savefig('/Users/brodenkirch/Desktop/3RH.png')
plt.close()

#Upper Layer RH
make_plot(df1['Upper Layer RH [%]'])
plt.title('Upper Layer RH vs. Primary Convective Type (All Lifecycles)', fontsize = 30)
plt.ylabel('Upper Layer RH [%]', fontsize = 25)
plt.savefig('/Users/brodenkirch/Desktop/4RH.png')
plt.close()

#Deep Layer Speed Shear
make_plot(df1['SHARPpy Direct Method Deep Layer Speed Shear [kts]'])
plt.title('Deep Layer Speed Shear vs. Primary Convective Type (All Lifecycles)', fontsize = 30)
plt.ylabel('Deep Layer Speed Shear [kts]', fontsize = 25)
plt.savefig('/Users/brodenkirch/Desktop/1SS.png')
plt.close()

#PBL Layer Speed Shear
make_plot(df1['SHARPpy Direct Method PBL Speed Shear [kts]'])
plt.title('PBL Speed Shear vs. Primary Convective Type (All Lifecycles)', fontsize = 30)
plt.ylabel('PBL Speed Shear [kts]', fontsize = 25)
plt.savefig('/Users/brodenkirch/Desktop/2SS.png')
plt.close()

#Mid Layer Speed Shear
make_plot(df1['SHARPpy Direct Method Mid Layer Speed Shear [kts]'])
plt.title('Mid Layer Speed Shear vs. Primary Convective Type (All Lifecycles)', fontsize = 30)
plt.ylabel('Mid Layer Speed Shear [kts]', fontsize = 25)
plt.savefig('/Users/brodenkirch/Desktop/3SS.png')
plt.close()

#Upper Layer Speed Shear
make_plot(df1['SHARPpy Direct Method Upper Layer Speed Shear [kts]'])
plt.title('Upper Layer Speed Shear vs. Primary Convective Type (All Lifecycles)', fontsize = 30)
plt.ylabel('Upper Layer Speed Shear [kts]', fontsize = 25)
plt.savefig('/Users/brodenkirch/Desktop/4SS.png')
plt.close()

#Deep Layer Directional Shear
make_plot(df1['SHARPpy Direct Method Deep Layer Directional Shear [deg]'])
plt.title('Deep Layer Directional Shear vs. Primary Convective Type (All Lifecycles)', fontsize = 30)
plt.ylabel('Deep Layer Directional Shear [deg]', fontsize = 25)
plt.savefig('/Users/brodenkirch/Desktop/1DS.png')
plt.close()

#PBL Layer Directional Shear
make_plot(df1['SHARPpy Direct Method PBL Directional Shear [deg]'])
plt.title('PBL Directional Shear vs. Primary Convective Type (All Lifecycles)', fontsize = 30)
plt.ylabel('PBL Directional Shear [kts]', fontsize = 25)
plt.savefig('/Users/brodenkirch/Desktop/2DS.png')
plt.close()

#Mid Layer Directional Shear
make_plot(df1['SHARPpy Direct Method Mid Layer Directional Shear [deg]'])
plt.title('Mid Layer Directional Shear vs. Primary Convective Type (All Lifecycles)', fontsize = 30)
plt.ylabel('Mid Layer Directional Shear [kts]', fontsize = 25)
plt.savefig('/Users/brodenkirch/Desktop/3DS.png')
plt.close()

#Upper Layer Directional Shear
make_plot(df1['SHARPpy Direct Method Upper Layer Directional Shear [deg]'])
plt.title('Upper Layer Directional Shear vs. Primary Convective Type (All Lifecycles)', fontsize = 30)
plt.ylabel('Upper Layer Directional Shear [kts]', fontsize = 25)
plt.savefig('/Users/brodenkirch/Desktop/4DS.png')
plt.close()

#Deep Layer MUCAPE
make_plot(df1['Deep Layer MUCAPE [J/kg]'])
plt.title('Deep Layer MUCAPE vs. Primary Convective Type (All Lifecycles)', fontsize = 30)
plt.ylabel('Deep Layer MUCAPE [J/kg]', fontsize = 25)
plt.savefig('/Users/brodenkirch/Desktop/1MUCAPE.png')
plt.close()

#Below Freezing Level MUCAPE
make_plot(df1['Below FZL MUCAPE [J/kg]'])
plt.title('Below FZL MUCAPE vs. Primary Convective Type (All Lifecycles)', fontsize = 30)
plt.ylabel('Below FZL MUCAPE [J/kg]', fontsize = 25)
plt.savefig('/Users/brodenkirch/Desktop/2MUCAPE.png')
plt.close()

#Above Freezing Level MUCAPE
make_plot(df1['Above FZL MUCAPE [J/kg]'])
plt.title('Above FZL MUCAPE vs. Primary Convective Type (All Lifecycles)', fontsize = 30)
plt.ylabel('Above FZL MUCAPE [J/kg]', fontsize = 25)
plt.savefig('/Users/brodenkirch/Desktop/3MUCAPE.png')
plt.close()

#Deep Layer MLCAPE
make_plot(df1['Deep Layer MLCAPE [J/kg]'])
plt.title('Deep Layer MLCAPE vs. Primary Convective Type (All Lifecycles)', fontsize = 30)
plt.ylabel('Deep Layer MLCAPE [J/kg]', fontsize = 25)
plt.savefig('/Users/brodenkirch/Desktop/1MLCAPE.png')
plt.close()

#Below Freezing Level MLCAPE
make_plot(df1['Below FZL MLCAPE [J/kg]'])
plt.title('Below FZL MLCAPE vs. Primary Convective Type (All Lifecycles)', fontsize = 30)
plt.ylabel('Below FZL MLCAPE [J/kg]', fontsize = 25)
plt.savefig('/Users/brodenkirch/Desktop/2MLCAPE.png')
plt.close()

#Above Freezing Level MLCAPE
make_plot(df1['Above FZL MLCAPE [J/kg]'])
plt.title('Above FZL MLCAPE vs. Primary Convective Type (All Lifecycles)', fontsize = 30)
plt.ylabel('Above FZL MLCAPE [J/kg]', fontsize = 25)
plt.savefig('/Users/brodenkirch/Desktop/3MLCAPE.png')
plt.close()


###################Regional Variability Plots


#Regional PBL top for isolated cases
make_regional_plot(df2['PBL Top [mb]'])
plt.title('PBL Top Distribution vs. Region (Isolated, All Lifecycles)', fontsize = 30)
plt.ylabel('Pressure [mb]', fontsize = 25)
plt.ylim([1005,900])
plt.yticks(np.arange(1000,899,-10))
plt.savefig('/Users/brodenkirch/Desktop/RegIso1PBL.png')
plt.close()

#Regional Deep Layer RH for isolated cases
make_regional_plot(df2['Deep Layer RH [%]'])
plt.title('Deep Layer RH vs. Region (Isolated, All Lifecycles)', fontsize = 30)
plt.ylabel('Deep Layer RH [%]', fontsize = 25)
plt.savefig('/Users/brodenkirch/Desktop/RegIso1RH.png')
plt.close()

#Regional PBL RH for isolated cases
make_regional_plot(df2['PBL RH [%]'])
plt.title('PBL RH vs. Region (Isolated, All Lifecycles)', fontsize = 30)
plt.ylabel('PBL RH [%]', fontsize = 25)
plt.savefig('/Users/brodenkirch/Desktop/RegIso2RH.png')
plt.close()

#Regional Mid Layer RH for isolated cases
make_regional_plot(df2['Mid Layer RH [%]'])
plt.title('Mid Layer RH vs. Region (Isolated, All Lifecycles)', fontsize = 30)
plt.ylabel('Mid Layer RH [%]', fontsize = 25)
plt.savefig('/Users/brodenkirch/Desktop/RegIso3RH.png')
plt.close()

#Regional Upper Layer RH for isolated cases
make_regional_plot(df2['Upper Layer RH [%]'])
plt.title('Upper Layer RH vs. Region (Isolated, All Lifecycles)', fontsize = 30)
plt.ylabel('Upper Layer RH [%]', fontsize = 25)
plt.savefig('/Users/brodenkirch/Desktop/RegIso4RH.png')
plt.close()

#Regional Deep Layer Speed Shear for isolated cases
make_regional_plot(df2['SHARPpy Direct Method Deep Layer Speed Shear [kts]'])
plt.title('Deep Layer Speed Shear vs. Region (Isolated, All Lifecycles)', fontsize = 30)
plt.ylabel('Deep Layer Speed Shear [kts]', fontsize = 25)
plt.savefig('/Users/brodenkirch/Desktop/RegIso1SS.png')
plt.close()

#Regional PBL Layer Speed Shear for isolated cases
make_regional_plot(df2['SHARPpy Direct Method PBL Speed Shear [kts]'])
plt.title('PBL Speed Shear vs. Region (Isolated, All Lifecycles)', fontsize = 30)
plt.ylabel('PBL Speed Shear [kts]', fontsize = 25)
plt.savefig('/Users/brodenkirch/Desktop/RegIso2SS.png')
plt.close()

#Regional Mid Layer Speed Shear for isolated cases
make_regional_plot(df2['SHARPpy Direct Method Mid Layer Speed Shear [kts]'])
plt.title('Mid Layer Speed Shear vs. Region (Isolated, All Lifecycles)', fontsize = 30)
plt.ylabel('Mid Layer Speed Shear [kts]', fontsize = 25)
plt.savefig('/Users/brodenkirch/Desktop/RegIso3SS.png')
plt.close()

#Regional Upper Layer Speed Shear for isolated cases
make_regional_plot(df2['SHARPpy Direct Method Upper Layer Speed Shear [kts]'])
plt.title('Upper Layer Speed Shear vs. Region (Isolated, All Lifecycles)', fontsize = 30)
plt.ylabel('Upper Layer Speed Shear [kts]', fontsize = 25)
plt.savefig('/Users/brodenkirch/Desktop/RegIso4SS.png')
plt.close()

#Regional Deep Layer Directional Shear for isolated cases
make_regional_plot(df2['SHARPpy Direct Method Deep Layer Directional Shear [deg]'])
plt.title('Deep Layer Directional Shear vs. Region (Isolated, All Lifecycles)', fontsize = 30)
plt.ylabel('Deep Layer Directional Shear [deg]', fontsize = 25)
plt.savefig('/Users/brodenkirch/Desktop/RegIso1DS.png')
plt.close()

#Regional PBL Layer Directional Shear for isolated cases
make_regional_plot(df2['SHARPpy Direct Method PBL Directional Shear [deg]'])
plt.title('PBL Directional Shear vs. Region (Isolated, All Lifecycles)', fontsize = 30)
plt.ylabel('PBL Directional Shear [kts]', fontsize = 25)
plt.savefig('/Users/brodenkirch/Desktop/RegIso2DS.png')
plt.close()

#Regional Mid Layer Directional Shear for isolated cases
make_regional_plot(df2['SHARPpy Direct Method Mid Layer Directional Shear [deg]'])
plt.title('Mid Layer Directional Shear vs. Region (Isolated, All Lifecycles)', fontsize = 30)
plt.ylabel('Mid Layer Directional Shear [kts]', fontsize = 25)
plt.savefig('/Users/brodenkirch/Desktop/RegIso3DS.png')
plt.close()

#Regional Upper Layer Directional Shear for isolated cases
make_regional_plot(df2['SHARPpy Direct Method Upper Layer Directional Shear [deg]'])
plt.title('Upper Layer Directional Shear vs. Region (Isolated, All Lifecycles)', fontsize = 30)
plt.ylabel('Upper Layer Directional Shear [kts]', fontsize = 25)
plt.savefig('/Users/brodenkirch/Desktop/RegIso4DS.png')
plt.close()

#Regional PBL top for organized cases
make_regional_plot(df2['PBL Top [mb]'], 'Organized')
plt.title('PBL Top Distribution vs. Region (Organized, All Lifecycles)', fontsize = 30)
plt.ylabel('Pressure [mb]', fontsize = 25)
plt.ylim([1005,900])
plt.yticks(np.arange(1000,899,-10))
plt.savefig('/Users/brodenkirch/Desktop/RegOrg1PBL.png')
plt.close()

#Regional Deep Layer RH for organized cases
make_regional_plot(df2['Deep Layer RH [%]'], 'Organized')
plt.title('Deep Layer RH vs. Region (Organized, All Lifecycles)', fontsize = 30)
plt.ylabel('Deep Layer RH [%]', fontsize = 25)
plt.savefig('/Users/brodenkirch/Desktop/RegOrg1RH.png')
plt.close()

#Regional PBL RH for organized cases
make_regional_plot(df2['PBL RH [%]'], 'Organized')
plt.title('PBL RH vs. Region (Organized, All Lifecycles)', fontsize = 30)
plt.ylabel('PBL RH [%]', fontsize = 25)
plt.savefig('/Users/brodenkirch/Desktop/RegOrg2RH.png')
plt.close()

#Regional Mid Layer RH for organized cases
make_regional_plot(df2['Mid Layer RH [%]'], 'Organized')
plt.title('Mid Layer RH vs. Region (Organized, All Lifecycles)', fontsize = 30)
plt.ylabel('Mid Layer RH [%]', fontsize = 25)
plt.savefig('/Users/brodenkirch/Desktop/RegOrg3RH.png')
plt.close()

#Regional Upper Layer RH for organized cases
make_regional_plot(df2['Upper Layer RH [%]'], 'Organized')
plt.title('Upper Layer RH vs. Region (Organized, All Lifecycles)', fontsize = 30)
plt.ylabel('Upper Layer RH [%]', fontsize = 25)
plt.savefig('/Users/brodenkirch/Desktop/RegOrg4RH.png')
plt.close()

#Regional Deep Layer Speed Shear for organized cases
make_regional_plot(df2['SHARPpy Direct Method Deep Layer Speed Shear [kts]'], 'Organized')
plt.title('Deep Layer Speed Shear vs. Region (Organized, All Lifecycles)', fontsize = 30)
plt.ylabel('Deep Layer Speed Shear [kts]', fontsize = 25)
plt.savefig('/Users/brodenkirch/Desktop/RegOrg1SS.png')
plt.close()

#Regional PBL Layer Speed Shear for organized cases
make_regional_plot(df2['SHARPpy Direct Method PBL Speed Shear [kts]'], 'Organized')
plt.title('PBL Speed Shear vs. Region (Organized, All Lifecycles)', fontsize = 30)
plt.ylabel('PBL Speed Shear [kts]', fontsize = 25)
plt.savefig('/Users/brodenkirch/Desktop/RegOrg2SS.png')
plt.close()

#Regional Mid Layer Speed Shear for organized cases
make_regional_plot(df2['SHARPpy Direct Method Mid Layer Speed Shear [kts]'], 'Organized')
plt.title('Mid Layer Speed Shear vs. Region (Organized, All Lifecycles)', fontsize = 30)
plt.ylabel('Mid Layer Speed Shear [kts]', fontsize = 25)
plt.savefig('/Users/brodenkirch/Desktop/RegOrg3SS.png')
plt.close()

#Regional Upper Layer Speed Shear for organized cases
make_regional_plot(df2['SHARPpy Direct Method Upper Layer Speed Shear [kts]'], 'Organized')
plt.title('Upper Layer Speed Shear vs. Region (Organized, All Lifecycles)', fontsize = 30)
plt.ylabel('Upper Layer Speed Shear [kts]', fontsize = 25)
plt.savefig('/Users/brodenkirch/Desktop/RegOrg4SS.png')
plt.close()

#Regional Deep Layer Directional Shear for organized cases
make_regional_plot(df2['SHARPpy Direct Method Deep Layer Directional Shear [deg]'], 'Organized')
plt.title('Deep Layer Directional Shear vs. Region (Organized, All Lifecycles)', fontsize = 30)
plt.ylabel('Deep Layer Directional Shear [deg]', fontsize = 25)
plt.savefig('/Users/brodenkirch/Desktop/RegOrg1DS.png')
plt.close()

#Regional PBL Layer Directional Shear for organized cases
make_regional_plot(df2['SHARPpy Direct Method PBL Directional Shear [deg]'], 'Organized')
plt.title('PBL Directional Shear vs. Region (Organized, All Lifecycles)', fontsize = 30)
plt.ylabel('PBL Directional Shear [kts]', fontsize = 25)
plt.savefig('/Users/brodenkirch/Desktop/RegOrg2DS.png')
plt.close()

#Regional Mid Layer Directional Shear for organized cases
make_regional_plot(df2['SHARPpy Direct Method Mid Layer Directional Shear [deg]'], 'Organized')
plt.title('Mid Layer Directional Shear vs. Region (Organized, All Lifecycles)', fontsize = 30)
plt.ylabel('Mid Layer Directional Shear [kts]', fontsize = 25)
plt.savefig('/Users/brodenkirch/Desktop/RegOrg3DS.png')
plt.close()

#Regional Upper Layer Directional Shear for organized cases
make_regional_plot(df2['SHARPpy Direct Method Upper Layer Directional Shear [deg]'], 'Organized')
plt.title('Upper Layer Directional Shear vs. Region (Organized, All Lifecycles)', fontsize = 30)
plt.ylabel('Upper Layer Directional Shear [kts]', fontsize = 25)
plt.savefig('/Users/brodenkirch/Desktop/RegOrg4DS.png')
plt.close()


###################Intra-case comparison plots

#PBL top
intracase_plot(df1['PBL Top [mb]'])
plt.title('PBL Top Distribution vs. Convective Lifecycle', fontsize = 30)
plt.ylabel('Pressure [mb]', fontsize = 25)
plt.ylim([1005,900])
plt.yticks(np.arange(1000,899,-10))
plt.savefig('/Users/brodenkirch/Desktop/Intra1PBL.png')
plt.close()

#Deep Layer RH
intracase_plot(df1['Deep Layer RH [%]'])
plt.title('Deep Layer RH vs. Convective Lifecycle', fontsize = 30)
plt.ylabel('Deep Layer RH [%]', fontsize = 25)
plt.savefig('/Users/brodenkirch/Desktop/Intra1RH.png')
plt.close()

#PBL RH
intracase_plot(df1['PBL RH [%]'])
plt.title('PBL RH vs. Convective Lifecycle', fontsize = 30)
plt.ylabel('PBL RH [%]', fontsize = 25)
plt.savefig('/Users/brodenkirch/Desktop/Intra2RH.png')
plt.close()

#Mid Layer RH
intracase_plot(df1['Mid Layer RH [%]'])
plt.title('Mid Layer RH vs. Convective Lifecycle', fontsize = 30)
plt.ylabel('Mid Layer RH [%]', fontsize = 25)
plt.savefig('/Users/brodenkirch/Desktop/Intra3RH.png')
plt.close()

#Upper Layer RH
intracase_plot(df1['Upper Layer RH [%]'])
plt.title('Upper Layer RH vs. Convective Lifecycle', fontsize = 30)
plt.ylabel('Upper Layer RH [%]', fontsize = 25)
plt.savefig('/Users/brodenkirch/Desktop/Intra4RH.png')
plt.close()

#Deep Layer Speed Shear
intracase_plot(df1['SHARPpy Direct Method Deep Layer Speed Shear [kts]'])
plt.title('Deep Layer Speed Shear vs. Convective Lifecycle', fontsize = 30)
plt.ylabel('Deep Layer Speed Shear [kts]', fontsize = 25)
plt.savefig('/Users/brodenkirch/Desktop/Intra1SS.png')
plt.close()

#PBL Layer Speed Shear
intracase_plot(df1['SHARPpy Direct Method PBL Speed Shear [kts]'])
plt.title('PBL Speed Shear vs. Convective Lifecycle', fontsize = 30)
plt.ylabel('PBL Speed Shear [kts]', fontsize = 25)
plt.savefig('/Users/brodenkirch/Desktop/Intra2SS.png')
plt.close()

#Mid Layer Speed Shear
intracase_plot(df1['SHARPpy Direct Method Mid Layer Speed Shear [kts]'])
plt.title('Mid Layer Speed Shear vs. Convective Lifecycle', fontsize = 30)
plt.ylabel('Mid Layer Speed Shear [kts]', fontsize = 25)
plt.savefig('/Users/brodenkirch/Desktop/Intra3SS.png')
plt.close()

#Upper Layer Speed Shear
intracase_plot(df1['SHARPpy Direct Method Upper Layer Speed Shear [kts]'])
plt.title('Upper Layer Speed Shear vs. Convective Lifecycle', fontsize = 30)
plt.ylabel('Upper Layer Speed Shear [kts]', fontsize = 25)
plt.savefig('/Users/brodenkirch/Desktop/Intra4SS.png')
plt.close()

#Deep Layer Directional Shear
intracase_plot(df1['SHARPpy Direct Method Deep Layer Directional Shear [deg]'])
plt.title('Deep Layer Directional Shear vs. Convective Lifecycle', fontsize = 30)
plt.ylabel('Deep Layer Directional Shear [deg]', fontsize = 25)
plt.savefig('/Users/brodenkirch/Desktop/Intra1DS.png')
plt.close()

#PBL Layer Directional Shear
intracase_plot(df1['SHARPpy Direct Method PBL Directional Shear [deg]'])
plt.title('PBL Directional Shear vs. Convective Lifecycle', fontsize = 30)
plt.ylabel('PBL Directional Shear [kts]', fontsize = 25)
plt.savefig('/Users/brodenkirch/Desktop/Intra2DS.png')
plt.close()

#Mid Layer Directional Shear
intracase_plot(df1['SHARPpy Direct Method Mid Layer Directional Shear [deg]'])
plt.title('Mid Layer Directional Shear vs. Convective Lifecycle', fontsize = 30)
plt.ylabel('Mid Layer Directional Shear [kts]', fontsize = 25)
plt.savefig('/Users/brodenkirch/Desktop/Intra3DS.png')
plt.close()

#Upper Layer Directional Shear
intracase_plot(df1['SHARPpy Direct Method Upper Layer Directional Shear [deg]'])
plt.title('Upper Layer Directional Shear vs. Convective Lifecycle', fontsize = 30)
plt.ylabel('Upper Layer Directional Shear [kts]', fontsize = 25)
plt.savefig('/Users/brodenkirch/Desktop/Intra4DS.png')
plt.close()
