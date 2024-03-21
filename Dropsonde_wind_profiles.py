#This script plots vertical profiles of the dropsonde component winds
import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.ticker as ticker

matplotlib.rcParams['axes.labelsize'] = 14
matplotlib.rcParams['axes.titlesize'] = 14
matplotlib.rcParams['xtick.labelsize'] = 12
matplotlib.rcParams['ytick.labelsize'] = 12
# matplotlib.rcParams['legend.fontsize'] = 12
#matplotlib.rcParams['legend.facecolor'] = 'w'
matplotlib.rcParams['axes.prop_cycle'] = matplotlib.cycler(color = 'r')
matplotlib.rcParams['font.family'] = 'arial'
matplotlib.rcParams['axes.grid'] = True

dropsonde_filepath = os.path.join(os.getcwd(), 'Dropsonde_Metric_Calculations.csv')
df_drop = pd.read_csv(dropsonde_filepath)
drop_days = df_drop.Date.unique()


for day in drop_days:
    drop_good_times = list(df_drop[df_drop['Date'] == day]['Time'].astype('str'))  #good dropsonde profiles
    day_filepath = os.path.join(os.getcwd(), str(day), 'final_dropsonde_{}.csv'.format(day))  #grab the given day's QCed dropsonde data
    df_day = pd.read_csv(day_filepath)
    drop_all_times = df_day['Time [UTC]'].unique()  #grabs each unique dropsonde profile time
    
    for time in drop_all_times:
        if time[-8:].replace(':', '') not in drop_good_times:  #if the dropsonde profile/time is a bad profile (i.e., not in Dropsonde_Metric_Calculations.csv), then don't plot the wind profile
            continue
        else:
            df_time = df_day[df_day['Time [UTC]'] == time]
            prof_heights = df_time['Height [m]']
            prof_pres = df_time['Pressure [mb]']
            prof_u = df_time['U Comp of Wind [m/s]'] * 1.94384449  #wind in knots
            prof_v = df_time['V Comp of Wind [m/s]'] * 1.94384449  #wind in knots
            prof_spd = df_time['Wind Speed [m/s]'] * 1.94384449  #wind in knots
            
            fig, ax = plt.subplots(2,3, figsize = (16,16))
            ax = ax.flatten()
            
            ax[0].plot(prof_u, prof_heights)
            ax[0].set_xlim([-90,90])
            ax[0].set_ylim([0,13300])
            ax[0].set_xlabel('Knots')
            ax[0].set_ylabel('Height [m]')
            ax[0].set_title('U Component of Wind')
            
            ax[1].plot(prof_v, prof_heights)
            ax[1].set_xlim([-90,90])
            ax[1].set_ylim([0,13300])
            ax[1].set_xlabel('Knots')
            ax[1].set_ylabel('Height [m]')   
            ax[1].set_title('V Component of Wind')            
            
            ax[2].plot(prof_spd, prof_heights)
            ax[2].set_xlim([0,100])
            ax[2].set_ylim([0,13300])  
            ax[2].set_xlabel('Knots')
            ax[2].set_ylabel('Height [m]')
            ax[2].set_title('Wind Speed')            
            
            ax[3].semilogy(prof_u, prof_pres)
            ax[3].set_xlim([-90,90])
            ax[3].set_ylim([1020,175]) 
            ax[3].set_xlabel('Knots')
            ax[3].set_ylabel('Pressure [mb]') 
            ax[3].set_title('U Component of Wind')
            
            ax[4].semilogy(prof_v, prof_pres)
            ax[4].set_xlim([-90,90])
            ax[4].set_ylim([1020,175]) 
            ax[4].set_xlabel('Knots')
            ax[4].set_ylabel('Pressure [mb]') 
            ax[4].set_title('V Component of Wind')
            
            ax[5].semilogy(prof_spd, prof_pres)
            ax[5].set_xlim([0,100])
            ax[5].set_ylim([1020,175])
            ax[5].set_xlabel('Knots')
            ax[5].set_ylabel('Pressure [mb]')             
            ax[5].set_title('Wind Speed')
            
            ax[0].set_xticks(np.arange(-80, 81, 20))
            ax[0].set_yticks(np.arange(0, 13001, 1000))
            
            ax[1].set_xticks(np.arange(-80, 81, 20))
            ax[1].set_yticks(np.arange(0, 13001, 1000))
            
            ax[2].set_xticks(np.arange(0, 101, 10))
            ax[2].set_yticks(np.arange(0, 13001, 1000))
            
            ax[3].set_xticks(np.arange(-80, 81, 20))
            ax[3].set_yticks(np.arange(1000, 199, -100))
            ax[3].get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
            
            ax[4].set_xticks(np.arange(-80, 81, 20))
            ax[4].set_yticks(np.arange(1000, 199, -100))
            ax[4].get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
            
            ax[5].set_xticks(np.arange(0, 101, 10))
            ax[5].set_yticks(np.arange(1000, 199, -100))
            ax[5].get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
            
            plt.suptitle(time + ' Dropsonde Wind Profile', size = 35, fontweight = 'bold')
            plt.subplots_adjust(wspace=0.5, hspace = 0.2)
            plt.savefig('/Users/brodenkirch/Desktop/' + str(day) + '_' + time[-8:].replace(':', '') + '.png')
            plt.close()

