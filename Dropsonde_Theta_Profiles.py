import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from datetime import datetime
import sharppy
import sharppy.sharptab.profile as profile
import sharppy.sharptab.interp as interp
import sharppy.sharptab.winds as winds
import sharppy.sharptab.utils as utils
import sharppy.sharptab.params as params
import sharppy.sharptab.thermo as thermo

filepath = os.getcwd() + '/' + 'Dropsonde_Metric_Calculations.csv'
df = pd.read_csv(filepath)
line_types = ['b-', 'r-', 'k-', 'y-', 'b--', 'r--', 'k--', 'y--', 'c-', 'c--', 'm-', 'm--', 'b:', 'r:', 'k:', 'y:', 'c:', 'm:', 'b-.', 'r-.', 'k-.', 'y-.', 'c-.', 'm-.', 'g-', 'g--', 'g:', 'g-.']

drop_days = []
for i in range(len(df)):
    date = str(df['Date'][i])
    if date not in drop_days:
        drop_days.append(date)

#Potential Temperature 
for day in drop_days:
    
    day_folder = os.getcwd() + '/' + day
    drop_csv_path = day_folder + '/final_dropsonde_' + day + '.csv'
    drop_csv = pd.read_csv(drop_csv_path)

    # for j in range(len(drop_csv['Time [UTC]'])):     #converts the drop_csv times from strings back to dates
    #     drop_csv['Time [UTC]'][j] = datetime.strptime(drop_csv['Time [UTC]'][j], "%Y-%m-%d %H:%M:%S")
    
    drop_times = []
    for i in range(len(df)):
        if str(df['Date'][i]) == day:
            valid_time = str(df['Time'][i])
            drop_times.append(valid_time)
    fig = plt.figure(figsize=(15,15))
    
    line_index = 0
    for time in drop_times:
        drop_output_time = day + time
        drop_output_time = datetime.strptime(drop_output_time, "%Y%m%d%H%M%S")
        drop_output_time = datetime.strftime(drop_output_time, "%Y-%m-%d %H:%M:%S")
        rel_data = drop_csv.loc[drop_csv['Time [UTC]'] == drop_output_time]
        rel_data2 = rel_data.iloc[::-1]  #reverses the dataframe (row-based) to go from surface to upper-level
        
        pres = rel_data2['Pressure [mb]']
        hght = rel_data2['Height [m]']
        tmpc = rel_data2['Temperature [C]']
        dwpc = rel_data2['Dew Point [C]']
        wspd = 1.94384449 * rel_data2['Wind Speed [m/s]']  #converts m/s to knots (also in SHARPpy sharptab.utils script)
        wdir = rel_data2['Wind Direction [deg]']
        
        if (drop_output_time == '2017-06-02 21:33:15') or (drop_output_time == '2017-06-02 21:25:45'):
            prof = profile.create_profile(profile='default', pres=pres, hght=hght, tmpc=tmpc, dwpc=dwpc, wspd=wspd, wdir=wdir, missing=-9999, strictQC=False)
        else:    
            prof = profile.create_profile(profile='default', pres=pres, hght=hght, tmpc=tmpc, dwpc=dwpc, wspd=wspd, wdir=wdir, missing=-9999, strictQC=True)
            
        plt.plot(rel_data2['Potential Temperature [K]'], prof.pres, line_types[line_index], label = drop_output_time[11:])
        plt.xlabel("Potential Temperature [K]", fontsize = 25)
        plt.ylabel("Pressure [mb]", fontsize = 25)
        plt.ylim([1050,190])
        plt.yticks(np.arange(1000,190,-50))
        plt.tick_params(labelsize = 15)
        plt.legend(fontsize = 'xx-large')
        plt.grid(True)
        plt.title(day + ' Dropsonde Theta Profiles', fontsize = 30)
        plt.savefig(day_folder + '/theta_profiles.png')
        line_index = line_index + 1
    plt.close()
  
#Equivalent Potential Temperature    
for day in drop_days:
    
    day_folder = os.getcwd() + '/' + day
    drop_csv_path = day_folder + '/final_dropsonde_' + day + '.csv'
    drop_csv = pd.read_csv(drop_csv_path)

    # for j in range(len(drop_csv['Time [UTC]'])):     #converts the drop_csv times from strings back to dates
    #     drop_csv['Time [UTC]'][j] = datetime.strptime(drop_csv['Time [UTC]'][j], "%Y-%m-%d %H:%M:%S")
    
    drop_times = []
    for i in range(len(df)):
        if str(df['Date'][i]) == day:
            valid_time = str(df['Time'][i])
            drop_times.append(valid_time)
    fig = plt.figure(figsize=(15,15))

    line_index = 0
    for time in drop_times:
        drop_output_time = day + time
        drop_output_time = datetime.strptime(drop_output_time, "%Y%m%d%H%M%S")
        drop_output_time = datetime.strftime(drop_output_time, "%Y-%m-%d %H:%M:%S")
        rel_data = drop_csv.loc[drop_csv['Time [UTC]'] == drop_output_time]
        rel_data2 = rel_data.iloc[::-1]  #reverses the dataframe (row-based) to go from surface to upper-level
        
        pres = rel_data2['Pressure [mb]']
        hght = rel_data2['Height [m]']
        tmpc = rel_data2['Temperature [C]']
        dwpc = rel_data2['Dew Point [C]']
        wspd = 1.94384449 * rel_data2['Wind Speed [m/s]']  #converts m/s to knots (also in SHARPpy sharptab.utils script)
        wdir = rel_data2['Wind Direction [deg]']
        
        if (drop_output_time == '2017-06-02 21:33:15') or (drop_output_time == '2017-06-02 21:25:45'):
            prof = profile.create_profile(profile='default', pres=pres, hght=hght, tmpc=tmpc, dwpc=dwpc, wspd=wspd, wdir=wdir, missing=-9999, strictQC=False)
        else:    
            prof = profile.create_profile(profile='default', pres=pres, hght=hght, tmpc=tmpc, dwpc=dwpc, wspd=wspd, wdir=wdir, missing=-9999, strictQC=True)
            
        plt.plot(prof.thetae, prof.pres, line_types[line_index], label = drop_output_time[11:])
        plt.xlabel("Equivalent Potential Temperature [K]", fontsize = 25)
        plt.ylabel("Pressure [mb]", fontsize = 25)
        plt.ylim([1050,190])
        plt.yticks(np.arange(1000,190,-50))
        plt.xlim([325, 365])
        plt.xticks(np.arange(325,366,5))
        plt.tick_params(labelsize = 15)
        plt.legend(fontsize = 'xx-large')
        plt.grid(True)
        plt.title(day + ' Dropsonde Theta-E Profiles', fontsize = 30)
        plt.savefig(day_folder + '/thetaE_profiles.png')
        line_index = line_index + 1
    plt.close()
    
    
#Virtual Potential Temperature    
for day in drop_days:
    
    day_folder = os.getcwd() + '/' + day
    drop_csv_path = day_folder + '/final_dropsonde_' + day + '.csv'
    drop_csv = pd.read_csv(drop_csv_path)

    # for j in range(len(drop_csv['Time [UTC]'])):     #converts the drop_csv times from strings back to dates
    #     drop_csv['Time [UTC]'][j] = datetime.strptime(drop_csv['Time [UTC]'][j], "%Y-%m-%d %H:%M:%S")
    
    drop_times = []
    for i in range(len(df)):
        if str(df['Date'][i]) == day:
            valid_time = str(df['Time'][i])
            drop_times.append(valid_time)
    fig = plt.figure(figsize=(15,15))
    
    line_index = 0
    for time in drop_times:
        drop_output_time = day + time
        drop_output_time = datetime.strptime(drop_output_time, "%Y%m%d%H%M%S")
        drop_output_time = datetime.strftime(drop_output_time, "%Y-%m-%d %H:%M:%S")
        rel_data = drop_csv.loc[drop_csv['Time [UTC]'] == drop_output_time]
        rel_data2 = rel_data.iloc[::-1]  #reverses the dataframe (row-based) to go from surface to upper-level
        
        pres = rel_data2['Pressure [mb]']
        hght = rel_data2['Height [m]']
        tmpc = rel_data2['Temperature [C]']
        dwpc = rel_data2['Dew Point [C]']
        wspd = 1.94384449 * rel_data2['Wind Speed [m/s]']  #converts m/s to knots (also in SHARPpy sharptab.utils script)
        wdir = rel_data2['Wind Direction [deg]']
        
        if (drop_output_time == '2017-06-02 21:33:15') or (drop_output_time == '2017-06-02 21:25:45'):
            prof = profile.create_profile(profile='default', pres=pres, hght=hght, tmpc=tmpc, dwpc=dwpc, wspd=wspd, wdir=wdir, missing=-9999, strictQC=False)
        else:    
            prof = profile.create_profile(profile='default', pres=pres, hght=hght, tmpc=tmpc, dwpc=dwpc, wspd=wspd, wdir=wdir, missing=-9999, strictQC=True)
        
        thetav = thermo.theta(prof.pres, thermo.virtemp(prof.pres, prof.tmpc, prof.dwpc))   
        thetav = thermo.ctok(thetav)  #convert from Celsius to Kelvin
        plt.plot(thetav, prof.pres, line_types[line_index], label = drop_output_time[11:])
        plt.xlabel("Virtual Potential Temperature [K]", fontsize = 25)
        plt.ylabel("Pressure [mb]", fontsize = 25)
        plt.ylim([1050,190])
        plt.yticks(np.arange(1000,190,-50))
        plt.tick_params(labelsize = 15)
        plt.legend(fontsize = 'xx-large')
        plt.grid(True)
        plt.title(day + ' Dropsonde Theta-V Profiles', fontsize = 30)
        plt.savefig(day_folder + '/thetaV_profiles.png')
        line_index = line_index + 1
    plt.close()


