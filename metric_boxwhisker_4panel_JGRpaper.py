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

cindy_days = [20170619, 20170620, 20210826, 20210828, 20210901, 20210904]  #including TDs as TCs (from both CPEX and CPEX-AW)

drop_filepath = os.path.join(os.getcwd(), 'Dropsonde_Metric_Calculations.csv')
#drop_filepath = os.path.join(os.getcwd(), 'Dropsonde_Metric_Calculations_CPEXCV.csv')
df = pd.read_csv(drop_filepath)
df_noTC = df[~df['Date'].isin(cindy_days)].copy()  #filter out cases associated with a TD/TC

dawn_filepath = os.path.join(os.getcwd(), 'DAWN_Shear_Calculations.csv')
#dawn_filepath = os.path.join(os.getcwd(), 'DAWN_Shear_Calculations_CPEXCV.csv')
df_dawn = pd.read_csv(dawn_filepath)

df1 = pd.concat([df, df_dawn], ignore_index = True)  #concatenates fields with same heading
df1_noTC = df1[~df1['Date'].isin(cindy_days)].copy()  #filter out cases associated with a TD/TC

#df1_noTC = df_noTC.copy() #not sure what this was for....probably can delete

rh_layers = ['Deep Layer RH [%]', 'PBL RH [%]', 'Mid Layer RH [%]', 'Upper Layer RH [%]']
speed_shear_layers = ['SHARPpy Direct Method Deep Layer Speed Shear [kts]', 'SHARPpy Direct Method PBL Speed Shear [kts]', 
                      'SHARPpy Direct Method Mid Layer Speed Shear [kts]', 'SHARPpy Direct Method Upper Layer Speed Shear [kts]']
cape_layers = ['Deep Layer MUCAPE [J/kg]', 'Deep Layer MLCAPE [J/kg]', 'Above FZL MUCAPE [J/kg]', 'Above FZL MLCAPE [J/kg]']

use_alpha = 0.25  #alpha for box plots with all sondes, not just inflow sondes

#for convective type comparison of All Lifecycles dropsondes
def box_plot_onlyIsoOrg_RH(plotting_metric_name, ax):  #parameter will be a data column from df
    
    if plotting_metric_name == 'Upper Layer RH [%]':  #include "In Precip" sondes if "Partially In Precip" == Yes
        df_use0 = df_noTC[df_noTC['Environment Falling In'] != 'Clear Far'].copy()  #filter out Clear Far dropsondes
        df_use1 = df_use0[(df_use0['Environment Falling In'] != 'In Precip') | (df_use0['Partially In Precip'] == 'Yes')].copy()  #filter out In Precip, unless "Partially In Precip" == Yes
        df_use = df_use1[(df_use1['Low-level Inflow Sonde'] == 'Yes') | (df_use1['Mid-level Inflow Sonde'] == 'Yes')].copy()
        #df_use = df_noTC[(df_noTC['Environment Falling In'] != 'In Precip') & (df_noTC['Environment Falling In'] != 'Clear Far')].copy()  #filter out In Precip and Clear Far dropsondes
    else:
        df_use1 = df_noTC[(df_noTC['Environment Falling In'] != 'In Precip') & (df_noTC['Environment Falling In'] != 'Clear Far')].copy()  #filter out In Precip and Clear Far dropsondes
        df_use = df_use1[(df_use1['Low-level Inflow Sonde'] == 'Yes') | (df_use1['Mid-level Inflow Sonde'] == 'Yes')].copy()

    #all sondes
    df_iso_all = df_use1[df_use1['Primary Convective Type'] == 'Isolated'].copy()
    df_org_all = df_use1[df_use1['Primary Convective Type'] == 'Organized'].copy()
    df_scat_all = df_use1[df_use1['Primary Convective Type'] == 'Scattered'].copy()
        
    #just inflow sondes
    df_iso = df_use[df_use['Primary Convective Type'] == 'Isolated'].copy()
    df_org = df_use[df_use['Primary Convective Type'] == 'Organized'].copy()
    df_scat = df_use[df_use['Primary Convective Type'] == 'Scattered'].copy()
    
    #need to filter out NaN values (using dropna()), otherwise the boxplot() won't create anything
    # bp = ax.boxplot([df_iso[plotting_metric_name].dropna().values, df_org[plotting_metric_name].dropna().values, df_scat[plotting_metric_name].dropna().values], notch = True, bootstrap = 10000,
    #                 patch_artist = True, vert = True, widths = 0.65, labels = ['Isolated', 'Organized', 'Scattered'])
    bp = ax.boxplot([df_iso[plotting_metric_name].dropna().values, df_iso_all[plotting_metric_name].dropna().values, df_org[plotting_metric_name].dropna().values, df_org_all[plotting_metric_name].dropna().values], notch = True, bootstrap = 10000,
                    patch_artist = True, vert = True, widths = 0.65, labels = ['Isolated\n(Inflow)', 'Isolated', 'Organized\n(Inflow)', 'Organized'])
        
    print (f'Isolated {plotting_metric_name} median:', df_iso[plotting_metric_name].median(skipna = True))
    print (f'Organized {plotting_metric_name} median:', df_org[plotting_metric_name].median(skipna = True))
    print (f'Scattered {plotting_metric_name} median:', df_scat[plotting_metric_name].median(skipna = True))

    # colors = ['red', 'blue', 'black']
    colors = ['red', 'red', 'blue', 'blue']
    nums = list(range(len(colors)))
     
    for ii, patch, color in zip(nums, bp['boxes'], colors):
        if ii % 2 == 0:
            patch.set_facecolor(color)
        else:
            patch.set_facecolor(color)
            patch.set_alpha(use_alpha)

    #changing color and linewidth of medians
    for ii, median in enumerate(bp['medians']):
        if ii % 2 == 0:
            median.set(color = 'k', linewidth = 3)
        else:
            median.set(color = 'k', alpha = use_alpha, linewidth = 3)        

    #changing color and linewidth of whiskers
    for ii, whisker in enumerate(bp['whiskers']):
        if ii in [0, 1, 4, 5]:  #8 whiskers, not 4
            whisker.set(color = 'k', linewidth = 2, linestyle = "-")
        else:
            whisker.set(color = 'k', alpha = use_alpha, linewidth = 2, linestyle = "-")
     
    #changing color and linewidth of caps
    for ii, cap in enumerate(bp['caps']):
        if ii in [0, 1, 4, 5]:  #8 caps, not 4
            cap.set(color = 'k', linewidth = 2)
        else:
            cap.set(color = 'k', alpha = use_alpha, linewidth = 2)
     
    #changing style of fliers
    for ii, flier, color in zip(nums, bp['fliers'], colors):
        if ii % 2 == 0:
            flier.set(marker = 'o', color = 'k', markersize = 13, markerfacecolor = color)
        else:
            flier.set(marker = 'o', color = 'k', alpha = use_alpha, markersize = 13, markerfacecolor = color)
            
    ax.grid(True, axis = 'y')
    ax.set_title(plotting_metric_name[:-4], fontsize = 33, fontweight = 'bold')
    #ax.set_xlabel('Convective Type', fontsize = 30, fontweight = 'bold')
    ax.set_ylabel('[%]', fontsize = 30, fontweight = 'bold')
    #ax.set_ylim([15,100])
    ax.tick_params(length = 15, width = 5, labelsize = 25)
 
    
group_fig = plt.figure(figsize=(22,24))

for i, layer in enumerate(rh_layers):
    ax = group_fig.add_subplot(2,2,i+1)
    box_plot_onlyIsoOrg_RH(layer, ax)
    
#custom legend
# legend_elements = [Line2D([], [], color='red', linewidth = 0, marker = 's', markersize = 13, label='Isolated (In Precip Profiles Excluded)'),
#                    Line2D([], [], color='blue', linewidth = 0, marker = 's', markersize = 13, label='Organized (In Precip Profiles Excluded)')]
# group_fig.legend(handles = legend_elements, loc = 'center', fontsize = 25)

group_fig.text(0.5, 0.5, 'In Precip Profiles Excluded', horizontalalignment='center', verticalalignment='center', 
               fontsize = 40, bbox={'facecolor': 'white', 'alpha': 0.5, 'pad': 10})
plt.subplots_adjust(hspace = 0.45, wspace = 0.35)
plt.savefig('/Users/brodenkirch/Desktop/RH_box_4panel.png', bbox_inches = 'tight')
plt.close()
print ('')

#for convective type comparison of All Lifecycles dropsondes
def box_plot_onlyIsoOrg_SS(plotting_metric_name, ax):  #parameter will be a data column from df
    
    df_use1 = df_noTC[df_noTC['Environment Falling In'] != 'Clear Far'].copy()  #filter out Clear Far dropsondes
    df_use = df_use1[(df_use1['Low-level Inflow Sonde'] == 'Yes') | (df_use1['Mid-level Inflow Sonde'] == 'Yes')].copy()
    
    #all sondes
    df_iso_all = df_use1[df_use1['Primary Convective Type'] == 'Isolated'].copy()
    df_org_all = df_use1[df_use1['Primary Convective Type'] == 'Organized'].copy()
    df_scat_all = df_use1[df_use1['Primary Convective Type'] == 'Scattered'].copy()
        
    #just inflow sondes
    df_iso = df_use[df_use['Primary Convective Type'] == 'Isolated'].copy()
    df_org = df_use[df_use['Primary Convective Type'] == 'Organized'].copy()
    df_scat = df_use[df_use['Primary Convective Type'] == 'Scattered'].copy()
    
    #need to filter out NaN values (using dropna()), otherwise the boxplot() won't create anything
    # bp = ax.boxplot([df_iso[plotting_metric_name].dropna().values, df_org[plotting_metric_name].dropna().values, df_scat[plotting_metric_name].dropna().values], notch = True, bootstrap = 10000,
    #                 patch_artist = True, vert = True, widths = 0.65, labels = ['Isolated', 'Organized', 'Scattered'])
    bp = ax.boxplot([df_iso[plotting_metric_name].dropna().values, df_iso_all[plotting_metric_name].dropna().values, df_org[plotting_metric_name].dropna().values, df_org_all[plotting_metric_name].dropna().values], notch = True, bootstrap = 10000,
                    patch_artist = True, vert = True, widths = 0.65, labels = ['Isolated\n(Inflow)', 'Isolated', 'Organized\n(Inflow)', 'Organized'])
        
    print (f'Isolated {plotting_metric_name} median:', df_iso[plotting_metric_name].median(skipna = True))
    print (f'Organized {plotting_metric_name} median:', df_org[plotting_metric_name].median(skipna = True))
    print (f'Scattered {plotting_metric_name} median:', df_scat[plotting_metric_name].median(skipna = True))

    # colors = ['red', 'blue', 'black']
    colors = ['red', 'red', 'blue', 'blue']
    nums = list(range(len(colors)))
     
    for ii, patch, color in zip(nums, bp['boxes'], colors):
        if ii % 2 == 0:
            patch.set_facecolor(color)
        else:
            patch.set_facecolor(color)
            patch.set_alpha(use_alpha)

    #changing color and linewidth of medians
    for ii, median in enumerate(bp['medians']):
        if ii % 2 == 0:
            median.set(color = 'k', linewidth = 3)
        else:
            median.set(color = 'k', alpha = use_alpha, linewidth = 3)        

    #changing color and linewidth of whiskers
    for ii, whisker in enumerate(bp['whiskers']):
        if ii in [0, 1, 4, 5]:  #8 whiskers, not 4
            whisker.set(color = 'k', linewidth = 2, linestyle = "-")
        else:
            whisker.set(color = 'k', alpha = use_alpha, linewidth = 2, linestyle = "-")
     
    #changing color and linewidth of caps
    for ii, cap in enumerate(bp['caps']):
        if ii in [0, 1, 4, 5]:  #8 caps, not 4
            cap.set(color = 'k', linewidth = 2)
        else:
            cap.set(color = 'k', alpha = use_alpha, linewidth = 2)
     
    #changing style of fliers
    for ii, flier, color in zip(nums, bp['fliers'], colors):
        if ii % 2 == 0:
            flier.set(marker = 'o', color = 'k', markersize = 13, markerfacecolor = color)
        else:
            flier.set(marker = 'o', color = 'k', alpha = use_alpha, markersize = 13, markerfacecolor = color)
            
    ax.grid(True, axis = 'y')
    ax.set_title(plotting_metric_name[22:-18] + ' Shear', fontsize = 33, fontweight = 'bold')
    #ax.set_xlabel('Convective Type', fontsize = 30, fontweight = 'bold')
    ax.set_ylabel('[kts]', fontsize = 30, fontweight = 'bold')
    #ax.set_ylim([0,50])
    ax.tick_params(length = 15, width = 5, labelsize = 25)
 
group_fig = plt.figure(figsize=(22,24))

for i, layer in enumerate(speed_shear_layers):
    ax = group_fig.add_subplot(2,2,i+1)
    box_plot_onlyIsoOrg_SS(layer, ax)

#custom legend
# legend_elements = [Line2D([], [], color='red', linewidth = 0, marker = 's', markersize = 13, label='Isolated'),
#                    Line2D([], [], color='blue', linewidth = 0, marker = 's', markersize = 13, label='Organized')]
# group_fig.legend(handles = legend_elements, loc = 'center', fontsize = 25)

group_fig.text(0.5, 0.5, 'In Precip Profiles Included', horizontalalignment='center', verticalalignment='center', 
               fontsize = 40, bbox={'facecolor': 'white', 'alpha': 0.5, 'pad': 10})
plt.subplots_adjust(hspace = 0.45, wspace = 0.35)
plt.savefig('/Users/brodenkirch/Desktop/SS_box_4panel.png', bbox_inches = 'tight')
plt.close()
print ('')

#for convective type comparison of All Lifecycles dropsondes
def box_plot_onlyIsoOrg_CAPE(plotting_metric_name, ax):  #parameter will be a data column from df
    
    df_use1 = df_noTC[(df_noTC['Environment Falling In'] != 'In Precip') & (df_noTC['Environment Falling In'] != 'Clear Far')].copy()  #filter out In Precip and Clear Far dropsondes
    df_use = df_use1[(df_use1['Low-level Inflow Sonde'] == 'Yes') | (df_use1['Mid-level Inflow Sonde'] == 'Yes')].copy()
    
    #all sondes
    df_iso_all = df_use1[df_use1['Primary Convective Type'] == 'Isolated'].copy()
    df_org_all = df_use1[df_use1['Primary Convective Type'] == 'Organized'].copy()
    df_scat_all = df_use1[df_use1['Primary Convective Type'] == 'Scattered'].copy()
        
    #just inflow sondes
    df_iso = df_use[df_use['Primary Convective Type'] == 'Isolated'].copy()
    df_org = df_use[df_use['Primary Convective Type'] == 'Organized'].copy()
    df_scat = df_use[df_use['Primary Convective Type'] == 'Scattered'].copy()
    
    #need to filter out NaN values (using dropna()), otherwise the boxplot() won't create anything
    # bp = ax.boxplot([df_iso[plotting_metric_name].dropna().values, df_org[plotting_metric_name].dropna().values, df_scat[plotting_metric_name].dropna().values], notch = True, bootstrap = 10000,
    #                 patch_artist = True, vert = True, widths = 0.65, labels = ['Isolated', 'Organized', 'Scattered'])
    bp = ax.boxplot([df_iso[plotting_metric_name].dropna().values, df_iso_all[plotting_metric_name].dropna().values, df_org[plotting_metric_name].dropna().values, df_org_all[plotting_metric_name].dropna().values], notch = True, bootstrap = 10000,
                    patch_artist = True, vert = True, widths = 0.65, labels = ['Isolated\n(Inflow)', 'Isolated', 'Organized\n(Inflow)', 'Organized'])
        
    print (f'Isolated {plotting_metric_name} median:', df_iso[plotting_metric_name].median(skipna = True))
    print (f'Organized {plotting_metric_name} median:', df_org[plotting_metric_name].median(skipna = True))
    print (f'Scattered {plotting_metric_name} median:', df_scat[plotting_metric_name].median(skipna = True))

    # colors = ['red', 'blue', 'black']
    colors = ['red', 'red', 'blue', 'blue']
    nums = list(range(len(colors)))
     
    for ii, patch, color in zip(nums, bp['boxes'], colors):
        if ii % 2 == 0:
            patch.set_facecolor(color)
        else:
            patch.set_facecolor(color)
            patch.set_alpha(use_alpha)

    #changing color and linewidth of medians
    for ii, median in enumerate(bp['medians']):
        if ii % 2 == 0:
            median.set(color = 'k', linewidth = 3)
        else:
            median.set(color = 'k', alpha = use_alpha, linewidth = 3)        

    #changing color and linewidth of whiskers
    for ii, whisker in enumerate(bp['whiskers']):
        if ii in [0, 1, 4, 5]:  #8 whiskers, not 4
            whisker.set(color = 'k', linewidth = 2, linestyle = "-")
        else:
            whisker.set(color = 'k', alpha = use_alpha, linewidth = 2, linestyle = "-")
     
    #changing color and linewidth of caps
    for ii, cap in enumerate(bp['caps']):
        if ii in [0, 1, 4, 5]:  #8 caps, not 4
            cap.set(color = 'k', linewidth = 2)
        else:
            cap.set(color = 'k', alpha = use_alpha, linewidth = 2)
     
    #changing style of fliers
    for ii, flier, color in zip(nums, bp['fliers'], colors):
        if ii % 2 == 0:
            flier.set(marker = 'o', color = 'k', markersize = 13, markerfacecolor = color)
        else:
            flier.set(marker = 'o', color = 'k', alpha = use_alpha, markersize = 13, markerfacecolor = color)
            
    ax.grid(True, axis = 'y')
    if 'Above FZL' in plotting_metric_name:
        ax.set_title('Upper Layer' + plotting_metric_name[9:-7], fontsize = 33, fontweight = 'bold')
    else:
        ax.set_title(plotting_metric_name[:-7], fontsize = 33, fontweight = 'bold')
    #ax.set_xlabel('Convective Type', fontsize = 30, fontweight = 'bold')
    ax.set_ylabel('[J kg$^{-1}$]', fontsize = 30, fontweight = 'bold')
    #ax.set_ylim([15,100])
    ax.tick_params(length = 15, width = 5, labelsize = 25)
    
    #make the deep layer plot axes range the same and the above FZL plot axes the same for easier comparison
    if plotting_metric_name[:4] == 'Deep':
        ax.set_ylim([-30,1450])
    else:
        ax.set_ylim([-30,1000])
 
group_fig = plt.figure(figsize=(22,24))

for i, layer in enumerate(cape_layers):
    ax = group_fig.add_subplot(2,2,i+1)
    box_plot_onlyIsoOrg_CAPE(layer, ax)
    
#custom legend
# legend_elements = [Line2D([], [], color='red', linewidth = 0, marker = 's', markersize = 13, label='Isolated (In Precip Profiles Excluded)'),
#                    Line2D([], [], color='blue', linewidth = 0, marker = 's', markersize = 13, label='Organized (In Precip Profiles Excluded)')]
# group_fig.legend(handles = legend_elements, loc = 'center', fontsize = 25)

group_fig.text(0.5, 0.5, 'In Precip Profiles Excluded', horizontalalignment='center', verticalalignment='center', 
               fontsize = 40, bbox={'facecolor': 'white', 'alpha': 0.5, 'pad': 10})
plt.subplots_adjust(hspace = 0.45, wspace = 0.35)
plt.savefig('/Users/brodenkirch/Desktop/CAPE_box_4panel.png', bbox_inches = 'tight')
plt.close()
print ('')
  
#for convective type comparison of All Lifecycles dropsondes
def box_plot_onlyIsoOrg_PBL(plotting_metric_name):  #parameter will be a data column from df

    group_fig = plt.figure(figsize=(32,21))
    
    #plot the PBL Top box and whisker plot
    ax = group_fig.add_subplot(1,2,1)
    
    df_use1 = df_noTC[(df_noTC['Environment Falling In'] != 'In Precip') & (df_noTC['Environment Falling In'] != 'Clear Far')].copy()  #filter out In Precip and Clear Far dropsondes
    df_use = df_use1[(df_use1['Low-level Inflow Sonde'] == 'Yes') | (df_use1['Mid-level Inflow Sonde'] == 'Yes')].copy()
    
    #all sondes
    df_iso_all = df_use1[df_use1['Primary Convective Type'] == 'Isolated'].copy()
    df_org_all = df_use1[df_use1['Primary Convective Type'] == 'Organized'].copy()
    df_scat_all = df_use1[df_use1['Primary Convective Type'] == 'Scattered'].copy()
        
    #just inflow sondes
    df_iso = df_use[df_use['Primary Convective Type'] == 'Isolated'].copy()
    df_org = df_use[df_use['Primary Convective Type'] == 'Organized'].copy()
    df_scat = df_use[df_use['Primary Convective Type'] == 'Scattered'].copy()
    
    #need to filter out NaN values (using dropna()), otherwise the boxplot() won't create anything
    # bp = ax.boxplot([df_iso[plotting_metric_name].dropna().values, df_org[plotting_metric_name].dropna().values, df_scat[plotting_metric_name].dropna().values], notch = True, bootstrap = 10000,
    #                 patch_artist = True, vert = True, widths = 0.65, labels = ['Isolated', 'Organized', 'Scattered'])
    bp = ax.boxplot([df_iso[plotting_metric_name].dropna().values, df_iso_all[plotting_metric_name].dropna().values, df_org[plotting_metric_name].dropna().values, df_org_all[plotting_metric_name].dropna().values], notch = True, bootstrap = 10000,
                    patch_artist = True, vert = True, widths = 0.65, labels = ['Isolated\n(Inflow)', 'Isolated', 'Organized\n(Inflow)', 'Organized'])
        
    print (f'Isolated {plotting_metric_name} median:', df_iso[plotting_metric_name].median(skipna = True))
    print (f'Organized {plotting_metric_name} median:', df_org[plotting_metric_name].median(skipna = True))
    print (f'Scattered {plotting_metric_name} median:', df_scat[plotting_metric_name].median(skipna = True))

    # colors = ['red', 'blue', 'black']
    colors = ['red', 'red', 'blue', 'blue']
    nums = list(range(len(colors)))
     
    for ii, patch, color in zip(nums, bp['boxes'], colors):
        if ii % 2 == 0:
            patch.set_facecolor(color)
        else:
            patch.set_facecolor(color)
            patch.set_alpha(use_alpha)

    #changing color and linewidth of medians
    for ii, median in enumerate(bp['medians']):
        if ii % 2 == 0:
            median.set(color = 'k', linewidth = 3)
        else:
            median.set(color = 'k', alpha = use_alpha, linewidth = 3)        

    #changing color and linewidth of whiskers
    for ii, whisker in enumerate(bp['whiskers']):
        if ii in [0, 1, 4, 5]:  #8 whiskers, not 4
            whisker.set(color = 'k', linewidth = 2, linestyle = "-")
        else:
            whisker.set(color = 'k', alpha = use_alpha, linewidth = 2, linestyle = "-")
     
    #changing color and linewidth of caps
    for ii, cap in enumerate(bp['caps']):
        if ii in [0, 1, 4, 5]:  #8 caps, not 4
            cap.set(color = 'k', linewidth = 2)
        else:
            cap.set(color = 'k', alpha = use_alpha, linewidth = 2)
     
    #changing style of fliers
    for ii, flier, color in zip(nums, bp['fliers'], colors):
        if ii % 2 == 0:
            flier.set(marker = 'o', color = 'k', markersize = 13, markerfacecolor = color)
        else:
            flier.set(marker = 'o', color = 'k', alpha = use_alpha, markersize = 13, markerfacecolor = color)
            
    ax.grid(True, axis = 'y')
    ax.set_title('PBL Depth', fontsize = 33, fontweight = 'bold')
    ax.set_xlabel('Convective Type', fontsize = 30, fontweight = 'bold')
    ax.set_ylabel('[mb]', fontsize = 30, fontweight = 'bold')
    #ax.set_ylim([1010,900])
    ax.invert_yaxis()
    ax.set_yticks(np.arange(1010,899,-10))
    ax.tick_params(length = 15, width = 5, labelsize = 25)
    ax.text(0.50, 0.97, 'In Precip Profiles Excluded', horizontalalignment='center', verticalalignment='center', 
            transform=ax.transAxes, fontsize = 30, bbox={'facecolor': 'white', 'alpha': 0.5, 'pad': 5})
    
    #plot the PBL Top scatter plot
    ax = group_fig.add_subplot(1,2,2)
    
    plotting_metric = df[plotting_metric_name]
    xlist = []
    for i in range(len(df)):
        xstring = str(df['Case'][i])
        xlist.append(xstring)
    
    legend_elements_PBL = [Line2D([], [], color='red', linewidth = 0, marker = 'o', markersize = 13, label='Isolated (Clear)'),
                          Line2D([], [], color='red', linewidth = 0, marker = '$C$', markersize = 13, label='Isolated (In Cloud)'),
                          Line2D([], [], color='red', linewidth = 0, marker = '$P$', markersize = 13, label='Isolated (In Precip)'),
                          Line2D([], [], color='blue', linewidth = 0, marker = 'o', markersize = 13, label='Organized (Clear)'),
                          Line2D([], [], color='blue', linewidth = 0, marker = '$C$', markersize = 13, label='Organized (In Cloud)'),
                          Line2D([], [], color='blue', linewidth = 0, marker = '$P$', markersize = 13, label='Organized (In Precip)')]
    
    # legend_elements_PBL = [Line2D([], [], color='red', linewidth = 0, marker = 'o', markersize = 13, label='Isolated'),
    #                Line2D([], [], color='blue', linewidth = 0, marker = 'o', markersize = 13, label='Organized'),
    #                Line2D([], [], color='black', linewidth = 0, marker = 'o', markersize = 13, label='Scattered')]
    
    #the lighter shades account for TS Cindy organized cases and, further, TS Cindy cases that were away from the main organized convection and instead near the cyclonic center
    for j in range(len(plotting_metric)):
        #if (df['Convective Lifecycle'][j] != 'Weakening') and (df['Environment Falling In'][j] == 'Clear Near' or df['Environment Falling In'][j] == 'In Cloud' or df['Environment Falling In'][j] == 'In Precip'):
        if df['Environment Falling In'][j] == 'Clear Near' or df['Environment Falling In'][j] == 'In Cloud' or df['Environment Falling In'][j] == 'In Precip':
        #if (df['Environment Falling In'][j] == 'Clear Near' or df['Environment Falling In'][j] == 'In Cloud' or df['Environment Falling In'][j] == 'In Precip') and (df['Low-level Inflow Sonde'][j] == 'Yes' or df['Mid-level Inflow Sonde'][j] == 'Yes'):
            if df['Primary Convective Type'][j] == 'Isolated':
                color = 'red'
                if df['Date'][j] in cindy_days:
                    continue
            elif df['Primary Convective Type'][j] == 'Organized':
                color = 'blue'
                if df['Date'][j] in cindy_days:
                    continue
            # elif df['Primary Convective Type'][j] == 'Scattered':
            #     color = 'black'
            #     if df['Date'][j] in cindy_days:
            #         continue                
            else:
                continue
                  
            if df['Environment Falling In'][j] == 'In Precip':
                if df['Partially In Precip'][j] == 'Yes':
                    mark = '$*P$'
                else:
                    mark = '$P$'
                outline = None
            elif df['Environment Falling In'][j] == 'In Cloud':
                if df['Falling Through Evaporating/Dissipating Stratiform'][j] == 'Yes':
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
            
    ax.grid(True)
    ax.set_title('PBL Depth', fontsize = 33, fontweight = 'bold')
    ax.set_xlabel('Case', fontsize = 30, fontweight = 'bold')
    ax.set_ylabel('[mb]', fontsize = 30, fontweight = 'bold')
    #ax.set_ylim([1010,900])
    ax.invert_yaxis()
    ax.set_yticks(np.arange(1010,899,-10))
    ax.tick_params(length = 15, width = 5, labelsize = 25)
    ax.legend(handles = legend_elements_PBL, fontsize = 20, loc = 'upper left', ncol = 1)

box_plot_onlyIsoOrg_PBL('PBL Top [mb]')
plt.subplots_adjust(wspace = 0.20)
plt.savefig('/Users/brodenkirch/Desktop/PBL_box_scatter.png', bbox_inches = 'tight')
plt.close()
print ('')

#for convective type comparison of All Lifecycles dropsondes
def box_plot_onlyIsoOrg_SSwDAWN(plotting_metric_name):  #parameter will be a data column from df1

    group_fig = plt.figure(figsize=(32,21))
    ax = group_fig.add_subplot(1,2,1)
    
    df_use1 = df1_noTC[df1_noTC['Environment Falling In'] != 'Clear Far'].copy()  #filter out Clear Far dropsondes
    df_use = df_use1[(df_use1['Low-level Inflow Sonde'] != 'No') | (df_use1['Mid-level Inflow Sonde'] != 'No')].copy()
    
    #all sondes
    df_iso_all = df_use1[df_use1['Primary Convective Type'] == 'Isolated'].copy()
    df_org_all = df_use1[df_use1['Primary Convective Type'] == 'Organized'].copy()
    df_scat_all = df_use1[df_use1['Primary Convective Type'] == 'Scattered'].copy()
        
    #just inflow sondes
    df_iso = df_use[df_use['Primary Convective Type'] == 'Isolated'].copy()
    df_org = df_use[df_use['Primary Convective Type'] == 'Organized'].copy()
    df_scat = df_use[df_use['Primary Convective Type'] == 'Scattered'].copy()
    
    #need to filter out NaN values (using dropna()), otherwise the boxplot() won't create anything
    # bp = ax.boxplot([df_iso[plotting_metric_name].dropna().values, df_org[plotting_metric_name].dropna().values, df_scat[plotting_metric_name].dropna().values], notch = True, bootstrap = 10000,
    #                 patch_artist = True, vert = True, widths = 0.65, labels = ['Isolated', 'Organized', 'Scattered'])
    bp = ax.boxplot([df_iso[plotting_metric_name].dropna().values, df_iso_all[plotting_metric_name].dropna().values, df_org[plotting_metric_name].dropna().values, df_org_all[plotting_metric_name].dropna().values], notch = True, bootstrap = 10000,
                    patch_artist = True, vert = True, widths = 0.65, labels = ['Isolated\n(Inflow)', 'Isolated', 'Organized\n(Inflow)', 'Organized'])
        
    print (f'Isolated {plotting_metric_name} median:', df_iso[plotting_metric_name].median(skipna = True))
    print (f'Organized {plotting_metric_name} median:', df_org[plotting_metric_name].median(skipna = True))
    print (f'Scattered {plotting_metric_name} median:', df_scat[plotting_metric_name].median(skipna = True))

    # colors = ['red', 'blue', 'black']
    colors = ['red', 'red', 'blue', 'blue']
    nums = list(range(len(colors)))
     
    for ii, patch, color in zip(nums, bp['boxes'], colors):
        if ii % 2 == 0:
            patch.set_facecolor(color)
        else:
            patch.set_facecolor(color)
            patch.set_alpha(use_alpha)

    #changing color and linewidth of medians
    for ii, median in enumerate(bp['medians']):
        if ii % 2 == 0:
            median.set(color = 'k', linewidth = 3)
        else:
            median.set(color = 'k', alpha = use_alpha, linewidth = 3)        

    #changing color and linewidth of whiskers
    for ii, whisker in enumerate(bp['whiskers']):
        if ii in [0, 1, 4, 5]:  #8 whiskers, not 4
            whisker.set(color = 'k', linewidth = 2, linestyle = "-")
        else:
            whisker.set(color = 'k', alpha = use_alpha, linewidth = 2, linestyle = "-")
     
    #changing color and linewidth of caps
    for ii, cap in enumerate(bp['caps']):
        if ii in [0, 1, 4, 5]:  #8 caps, not 4
            cap.set(color = 'k', linewidth = 2)
        else:
            cap.set(color = 'k', alpha = use_alpha, linewidth = 2)
     
    #changing style of fliers
    for ii, flier, color in zip(nums, bp['fliers'], colors):
        if ii % 2 == 0:
            flier.set(marker = 'o', color = 'k', markersize = 13, markerfacecolor = color)
        else:
            flier.set(marker = 'o', color = 'k', alpha = use_alpha, markersize = 13, markerfacecolor = color)
        
    ax.grid(True, axis = 'y')
    ax.set_title('Deep Layer Shear (Dropsonde & DAWN, 0.5km - 7.6km)', fontsize = 30, fontweight = 'bold')
    ax.set_xlabel('Convective Type', fontsize = 30, fontweight = 'bold')
    ax.set_ylabel('[kts]', fontsize = 30, fontweight = 'bold')
    #ax.set_ylim([0,50])
    ax.tick_params(length = 15, width = 5, labelsize = 25)
    ax.text(0.25, 0.97, 'In Precip Profiles Included', horizontalalignment='center', verticalalignment='center', 
            transform=ax.transAxes, fontsize = 30, bbox={'facecolor': 'white', 'alpha': 0.5, 'pad': 5})
    
    #plot the DAWN/dropsonde speed shear scatter plot
    ax = group_fig.add_subplot(1,2,2)
    
    plotting_metric = df1[plotting_metric_name]   #both dropsonde and DAWN data
    xlist = []
    for i in range(len(df1)):
        xstring = str(df1['Case'][i])
        xlist.append(xstring)
    
    #custom legend
    legend_elements = [Line2D([], [], color='red', linewidth = 0, marker = 'o', markersize = 15, label='Isolated'),
                        Line2D([], [], color='red', linewidth = 0, marker = '$P$', markersize = 15, label='Isolated (In Precip)'),
                        Line2D([], [], color='blue', linewidth = 0, marker = 'o', markersize = 15, label='Organized'),
                        Line2D([], [], color='blue', linewidth = 0, marker = '$P$', markersize = 15, label='Organized (In Precip)')]
    # legend_elements = [Line2D([], [], color='red', linewidth = 0, marker = 'o', markersize = 15, label='Isolated'),
    #                     Line2D([], [], color='red', linewidth = 0, marker = '$P$', markersize = 15, label='Isolated (In Precip)'),
    #                     Line2D([], [], color='blue', linewidth = 0, marker = 'o', markersize = 15, label='Organized'),
    #                     Line2D([], [], color='blue', linewidth = 0, marker = '$P$', markersize = 15, label='Organized (In Precip)'),
    #                     Line2D([], [], color='black', linewidth = 0, marker = 'o', markersize = 15, label='Scattered'),
    #                     Line2D([], [], color='black', linewidth = 0, marker = '$P$', markersize = 15, label='Scattered (In Precip)')]
    
    #the lighter shades account for TS Cindy organized cases and, further, TS Cindy cases that were away from the main organized convection and instead near the cyclonic center
    for j in range(len(plotting_metric)):
        #if (df1['Convective Lifecycle'][j] != 'Weakening') and (df1['Environment Falling In'][j] == 'Clear Near' or df1['Environment Falling In'][j] == 'In Cloud' or df1['Environment Falling In'][j] == 'In Precip'):
        if df1['Environment Falling In'][j] == 'Clear Near' or df1['Environment Falling In'][j] == 'In Cloud' or df1['Environment Falling In'][j] == 'In Precip':
        #if (df1['Environment Falling In'][j] == 'Clear Near' or df1['Environment Falling In'][j] == 'In Cloud' or df1['Environment Falling In'][j] == 'In Precip') and (df1['Low-level Inflow Sonde'][j] != 'No' or df1['Mid-level Inflow Sonde'][j] != 'No'):
            if df1['Primary Convective Type'][j] == 'Isolated':
                color = 'red'
                if df1['Date'][j] in cindy_days:
                    continue
            elif df1['Primary Convective Type'][j] == 'Organized':
                color = 'blue'
                if df1['Date'][j] in cindy_days:
                    continue
            # elif df1['Primary Convective Type'][j] == 'Scattered':
            #     color = 'black'
            #     if df1['Date'][j] in cindy_days:
            #         continue 
            else:
                continue
                  
            if df1['Environment Falling In'][j] == 'In Precip':
                if df1['Partially In Precip'][j] == 'Yes':
                    mark = '$*P$'
                else:
                    mark = '$P$'
                outline = None
            elif df1['Environment Falling In'][j] == 'In Cloud':
                if df1['Falling Through Evaporating/Dissipating Stratiform'][j] == 'Yes':
                    mark = '$*C$'
                else:
                    mark = '$C$'
                outline = None
            else:
                mark = 'o'
                outline = 'black'

            #if the metric is not NaN (need this filter, otherwise Python raises an error when showing/saving the figure)
            if not np.isnan(plotting_metric[j]):  #could also use pd.isna(plotting_metric[j]) 
                if df1['Low-level Inflow Sonde'][j] != 'No' or df1['Mid-level Inflow Sonde'][j] != 'No':               
                    ax.scatter(xlist[j], plotting_metric[j], c = color, s = 150, marker = mark, edgecolor = outline)
                else:
                    ax.scatter(xlist[j], plotting_metric[j], c = color, alpha = use_alpha, s = 150, marker = mark, edgecolor = outline)
    
    ax.grid(True)
    ax.set_title('Deep Layer Shear (Dropsonde & DAWN, 0.5km - 7.6km)', fontsize = 30, fontweight = 'bold')
    ax.set_xlabel('Case', fontsize = 30, fontweight = 'bold')
    ax.set_ylabel('[kts]', fontsize = 30, fontweight = 'bold')
    #ax.set_ylim([0,50])
    ax.tick_params(length = 15, width = 5, labelsize = 25)
    ax.legend(handles = legend_elements, fontsize = 25, ncol = 1)

box_plot_onlyIsoOrg_SSwDAWN('500m Bottom Cap Deep Layer Speed Shear [kts]')
plt.subplots_adjust(wspace = 0.20)
plt.savefig('/Users/brodenkirch/Desktop/SSwDAWN_box_scatter.png', bbox_inches = 'tight')
plt.close()



