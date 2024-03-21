#this script contains functions to make median/mean dropsonde Ku-band reflectivity profile plots for your M.S. thesis
#for additional code to make mean dropsonde Ku-band reflectivity profile plots and 
    #APR reflectivity vs. dropsonde metric scatter plots, see Dropsonde_vs_MeanDBZ.py

import os
import sys
import numpy as np
import pandas as pd
import datetime
import h5py
import itertools
import matplotlib
from matplotlib import pyplot as plt


matplotlib.rcParams['font.family'] = 'arial'
# matplotlib.rcParams['axes.labelsize'] = 18
# matplotlib.rcParams['axes.titlesize'] = 20
# matplotlib.rcParams['xtick.labelsize'] = 15
# matplotlib.rcParams['ytick.labelsize'] = 15
matplotlib.rcParams['legend.fontsize'] = 14
matplotlib.rcParams['legend.title_fontsize'] = 14


def median_dbz_profile(df_use, timedelta_cap, use_median = True, lowest_allowed_hght = 1500):
    """"Calculate median/mean dBZ profiles of Ku-reflectivity for a DataFrame of dropsondes
    
    Parameters
    -----------
    
    df_use: the filtered Pandas DataFrame of dropsondes to use to calculate median/mean Ku-reflectivity profiles
    
    timedelta_cap: time delta (in SECONDS) on EITHER side of the dropsonde for 
                   determining the APR profiles to use in the median/mean Ku-reflectivity profile calculation
                   
    use_median: if True, then calculate median Ku-reflectivity profiles
                if False, then calculate mean Ku-reflectivitiy profiles
                
    lowest_allowed_hght: height below which APR data may be spurious, so don't use
    
    return: a dictionary containing median/mean dBZ and height profiles for each dropsonde
    """
    
    #initialize the dictionary for the to-be-plotted data
    dropsonde_medianDBZ_dict = {}
    
    #for each non-TC isolated/organized dropsonde, calculate its mean/median dBZ and height profiles and
        #add both to dropsonde_medianDBZ_dict dictionary
    
    for ip in range(len(df_use)):
        prof_time = str(df_use['Time'].iloc[ip]).zfill(6)  #adds zeros to the front of the string until its length = 6
        prof_date = str(df_use['Date'].iloc[ip])
        prof_time_use = datetime.datetime.strptime(prof_date + prof_time, '%Y%m%d%H%M%S')
        
        #skip CPEX(-AW) dropsondes that lack reflectivity data within 10-minutes on either side
        #For 20210821, keep an eye on all sondes (does the noise noticeably contaminate the median dBZ profiles?)
        if (prof_date == '20210821') and (prof_time in ['223238']):  #maybe include 230907??
            continue        
        if (prof_date == '20210824') and (prof_time in ['180143', '190312', '190929', '201249']):
            continue
        if (prof_date == '20170610') and (prof_time in ['202102']):
            continue
        if (prof_date == '20170624') and (prof_time in ['202405']):
            continue
        if (prof_date == '20170615') and (prof_time in ['']):
            continue
        if (prof_date == '20170616') and (prof_time in ['']):
            continue
        if (prof_date == '20170601') and (prof_time in ['']):
            continue
        if (prof_date == '20170606') and (prof_time in ['204223']):
            continue
        if (prof_date == '20170617') and (prof_time in ['']):
            continue
        if (prof_date == '20170611') and (prof_time in ['194957', '204602']):
            continue
        
        #have some data, but very little...doesn't look pretty on the plots, so omitting for thesis
        if (prof_date == '20170611') and (prof_time in ['181534', '185332']):
            continue
            
        #calculate the dropsonde's mean/median dBZ and height profiles and add to dropsonde_medianDBZ_dict dict
        new_ku_array = True
        
        start_time0 = prof_time_use - datetime.timedelta(seconds = timedelta_cap)
        start_time = datetime.datetime.strftime(start_time0, '%H%M%S')  #convert datetime back to a time string
        end_time0 = prof_time_use + datetime.timedelta(seconds = timedelta_cap)
        end_time = datetime.datetime.strftime(end_time0, '%H%M%S')
    
        #find the APR files of interest (for the desired date and time ranges)
        apr_folder = os.path.join(prof_date, 'APR_files')
        apr_file_list = sorted(os.listdir(apr_folder))
        
        if prof_date[:4] == '2017':
            ray_angles = np.linspace(-25,25,24)[:-1]  #in degrees; omits 24th ray, which doesn't have data for Ku/Ka bands
        
            #find the list of APR files that have data for the desired time range
            apr_files_use = []
            first_file = 'blank'
            for file in apr_file_list:        #sorted() makes sure the code goes through the files in alphabetical order
                if file[0:3] == '.DS':         #delete possible .DS_Store files
                    os.remove(os.path.join(apr_folder, file))
                elif file[22:28] <= start_time:
                    first_file = file     #first_file will always be the file immediately before (or equal to) range_start
                elif file[22:28] >= end_time:
                    continue
                else:
                    if (first_file not in apr_files_use) and (first_file != 'blank'):
                        apr_files_use.append(first_file)
                    apr_files_use.append(file)
                    
            if apr_files_use == []:             #accounts for if start_time is greater than all of the file times, but still within the last file's time range; also accounts for start/end times equaling the times of adjacent files
                apr_files_use.append(first_file)
        
        elif prof_date[:4] == '2021':
            ray_angles = np.linspace(-25,25,25)
            
            #create a list of all the given day's desired range's APR files:    #for APR_plots.py
            for x in os.listdir(apr_folder):
                if x[0:3] == '.DS':         #delete hidden .DS_Store files if they come up (will show up if you delete a file)
                    os.remove(os.path.join(apr_folder, x))
            
            #find the starting APR file in apr_folder
            first_file_index = None       
            for i, x in enumerate(apr_file_list):
                file_start_time = datetime.datetime.strptime(x[13:21] + x[22:28], '%Y%m%d%H%M%S')
                file_end_time = datetime.datetime.strptime(x[29:37] + x[38:44], '%Y%m%d%H%M%S')
            
                if start_time0 <= file_start_time:  #if start_time0 is before the APR file start time and not within any previous APR file's time ranges
                    first_file_index = i
                    break
                elif (start_time0 >= file_start_time) and (start_time0 < file_end_time):
                    first_file_index = i
                    break
                else:
                    continue
            if first_file_index == None:
                sys.exit('Requested start_time is beyond all available APR files')
                
            #find the ending APR file in apr_folder
            last_file_index = None       
            for i, x in enumerate(apr_file_list):  
                file_start_time = datetime.datetime.strptime(x[13:21] + x[22:28], '%Y%m%d%H%M%S')
                file_end_time = datetime.datetime.strptime(x[29:37] + x[38:44], '%Y%m%d%H%M%S')
            
                if end_time0 <= file_start_time:  #if end_time0 is before the APR file start time and not within any previous APR file's time ranges
                    last_file_index = i - 1
                    break
                elif (end_time0 > file_start_time) and (end_time0 <= file_end_time):
                    last_file_index = i
                    break
                else:
                    continue
            if last_file_index == None:  #the end_time is after all available APR files
                last_file_index = len(apr_file_list) - 1  #the last available APR file's index
            if last_file_index == -1:
                sys.exit('Requested end_time is before all available APR files')
            
            apr_files_use = apr_file_list[first_file_index:last_file_index + 1]
            
        else:
            sys.exit('Not a CPEX or CPEX-AW case')            
    
        #Low resolution ('lores') radar variables in APR hdf files
        ku_band = 'zhh14' #Ku
        # ka_band = 'zhh35' #Ka
        # ldr = 'ldr14' #LDR
        # vel = 'vel14c' #Doppler Velocity   #should we use vel14? Not unless a solution is find for lack of data in vel14
        # vel_ka = 'vel35' #or should we use dealiased vel35c???        

        for apr_filepath in apr_files_use:
            apr_file = h5py.File(os.path.join(apr_folder, apr_filepath), 'r')
            
            if ('lores' in apr_file.keys()) and (ku_band in apr_file['lores'].keys()):
                
                try:   #some CPEX-AW APR files have corrupted Ku-band data; if so, skip the Ku-band for 
                       #that file (corrupted: "OSError: Can't read data (inflate() failed)")
                    ku_data = apr_file['lores'][ku_band][:]
                except:
                    continue
                
                #grab the radar variables of interest
                time = apr_file['lores']['scantime'][:]
                alt3d = apr_file['lores']['alt3D'][:]
                roll = apr_file['lores']['roll'][:] 
            
                if apr_filepath == apr_files_use[0] or apr_filepath == apr_files_use[-1]:
                #the complete APR file time range may not need to be used, so need to locate the closest time (and corresponding index) to the desired start/end time
                    
                    #Convert APR times to datetimes
                    time_dates = np.empty(time.shape, dtype=object)
                    for i in np.arange(0, time.shape[0]):
                        for j in np.arange(0, time.shape[1]):
                            #tmp = datetime(time[i,j])
                            tmp = datetime.datetime.utcfromtimestamp(time[i,j])
                            time_dates[i,j] = tmp
                    
                    unique_apr_times = time_dates[12,:]  #all the times in the given APR file
                    
                    if len(apr_files_use) == 1:  #i.e. apr_filepath == apr_files_use[0] and apr_filepath == apr_files_use[-1]
                    
                        #find the closest time (and its corresponding index) to the desired start_time
                        desired_start_time = start_time0
                        start_time_idx = np.argmin(abs(unique_apr_times - desired_start_time))
                    
                        #find the closest time (and its corresponding index) to the desired end_time
                        desired_end_time = end_time0
                        end_time_idx = np.argmin(abs(unique_apr_times - desired_end_time))
                                
                    elif apr_filepath == apr_files_use[0]:  #i.e. the first APR file in the apr_files_use list
                        end_time_idx = time.shape[1] - 1
                        
                        #find the closest time (and its corresponding index) to the desired start_time
                        desired_start_time = start_time0
                        start_time_idx = np.argmin(abs(unique_apr_times - desired_start_time))
                                
                    else:  #apr_filepath == apr_files_use[-1]  #i.e. the last APR file in the apr_files_use list
                        start_time_idx = 0
                        
                        #find the closest time (and its corresponding index) to the desired end_time
                        desired_end_time = end_time0
                        end_time_idx = np.argmin(abs(unique_apr_times - desired_end_time))                
                        
                else:  #the entire APR file is within the desired time range, so set the start/end indices to the first/last indices of the APR file
                    start_time_idx = 0
                    end_time_idx = time.shape[1] - 1
        
                #loop through the given APR file’s valid times/scans/profiles
                for time_idx in range(start_time_idx, end_time_idx + 1):
                    
                    #choose the "nadir" ray factoring in aircraft roll
                    ac_roll = np.nanmean(roll[:,time_idx])  #roll varies slightly w/ray, so take the average roll value for a given scan and use that for ray adjustment
                    ray_use = np.argmin(np.abs(ray_angles - ac_roll))  #the index of the ray whose angle is closest to that of ac_roll
                        
                    prof_height = alt3d[:,ray_use,time_idx]
                    prof_dbz = ku_data[:,ray_use,time_idx]
                    
                    #locate the index of the height closest to the lowest allowed height (1500m)
                    idx_min_hght = np.argmin(np.abs(prof_height - lowest_allowed_hght))
    
                    prof_height_use = np.flip(prof_height[:idx_min_hght + 1])  #height profile from 1500m to top of profile
                    prof_dbz_use = np.flip(prof_dbz[:idx_min_hght + 1])  #Ku-band profile from 1500m to top of profile
                    
                    #store the profile's height and dbz data in Pandas DataFrames
                    if new_ku_array:
                        #if this is the first qualifying time of the first APR file for the given dropsonde time range
                        dbz_profiles_df = pd.DataFrame(prof_dbz_use)
                        height_profiles_df = pd.DataFrame(prof_height_use)
                        new_ku_array = False
                    else:
                        prof_height_use = pd.Series(prof_height_use)
                        prof_dbz_use = pd.Series(prof_dbz_use)
                        
                        #NOTE: WE ARE ASSUMING THAT EACH ROW CORRESPONDS TO A NEAR IDENTICAL HEIGHT LEVEL
                            #this is the best we can do, and should be fine given that each profile is starting from ~1500m and the height resolution is the same for each profile
                        dbz_profiles_df = pd.concat((dbz_profiles_df, prof_dbz_use), axis = 1)  #add profile as a new column to the df; differences in profile lengths are filled in with NaNs
                        height_profiles_df = pd.concat((height_profiles_df, prof_height_use), axis = 1)  #add profile as a new column to the df; differences in profile lengths are filled in with NaNs
                    
            apr_file.close()

        #replace blank data (-99.99) with NaNs
        dbz_profiles_df[dbz_profiles_df <= -99] = np.nan
        height_profiles_df[height_profiles_df < 0] = np.nan
        
        #convert all the dropsonde's Ku-band data from dBZ to mm^6 m^-3
        Z_df = 10**(dbz_profiles_df / 10)
        
        #calculate the dropsonde's median/mean heights and reflectivity (in mm^6 m^-3) and standard deviation at each height level
        #NOTE: WE ARE ASSUMING THAT EACH ROW CORRESPONDS TO A NEAR IDENTICAL HEIGHT LEVEL
            #this is the best we can do, and should be fine given that each profile is starting from ~1500m and the height resolution is the same for each profile
        if use_median:
            Z_median = Z_df.median(axis = 1)  #axis of 1 = across all columns (so for each row); NaNs are ignored by default in Pandas
            height_median_profile = height_profiles_df.median(axis = 1)  #axis of 1 = across all columns (so for each row); NaNs are ignored by default in Pandas
        else:
            Z_median = Z_df.mean(axis = 1)     #axis of 1 = across all columns (so for each row); NaNs are ignored by default in Pandas
            height_median_profile = height_profiles_df.mean(axis = 1)     #axis of 1 = across all columns (so for each row); NaNs are ignored by default in Pandas
        #Z_std = Z_df.std(axis = 1)
        
        #convert the dropsonde's median/mean reflectivity and standard deviation profile back to dBZ
        drop_medianDBZ_profile = 10 * np.log10(Z_median)
        #drop_std_profile = 10 * np.log10(Z_std)
        
        #add the median/mean dBZ and height profiles to the dropsonde_medianDBZ_dict dict
        dropsonde_medianDBZ_dict[prof_date + prof_time] = {}  #initiate new subdictionary for the given dropsonde
        dropsonde_medianDBZ_dict[prof_date + prof_time]['median_dbz_profile'] = drop_medianDBZ_profile.values
        dropsonde_medianDBZ_dict[prof_date + prof_time]['median_height_profile'] = height_median_profile.values
        #dropsonde_medianDBZ_dict[prof_date + prof_time]['std_profile'] = drop_std_profile.values
        
    return dropsonde_medianDBZ_dict


#USE THE BELOW CODE WHEN USING median_dbz_profile() FUNCTION
color_list = ['b', 'r', 'k', 'orange', 'purple', 'aqua', 'dimgray', 'g', 'salmon', 'c', 'silver',
              'violet', 'm', 'dodgerblue', 'maroon', 'pink', 'khaki', 'chartreuse', 'hotpink', 'mediumseagreen']    
              #see https://matplotlib.org/3.5.0/gallery/color/named_colors.html for all possible color options

#metric thresholds for color-coding the median/mean dBZ profiles
RH_thresholds = {'95 - 100': [95, 100000], '90 - 95': [90, 95], '85 - 90': [85, 90], '80 - 85': [80, 85], 
                  '75 - 80': [75, 80], '70 - 75': [70, 75], '65 - 70': [65, 70], '60 - 65': [60, 65], 
                  '55 - 60': [55, 60], '50 - 55': [50, 55], '45 - 50': [45, 50], '40 - 45': [40, 45], 
                  '35 - 40': [35, 40], '30 - 35': [30, 35], '25 - 30': [25, 30], '20 - 25': [20, 25], 
                  '15 - 20': [15, 20], '10 - 15': [10, 15], '5 - 10': [5, 10], '0 - 5': [0, 5]}

pbl_speed_shear_thresholds = {'0 - 2.5': [0, 2.5], '2.5 - 5': [2.5, 5], '5 - 7.5': [5, 7.5], 
                              '7.5 - 10': [7.5, 10], '10 - 12.5': [10, 12.5], '12.5 - 15': [12.5, 15], 
                              '15 - 17.5': [15, 17.5], '17.5 - 20': [17.5, 20], '20+': [20, 100000], '< 0': [-1000, 0]}

speed_shear_thresholds = {'0 - 10': [0, 10], '10 - 20': [10, 20], '20 - 30': [20, 30], 
                          '30 - 40': [30, 40], '40 - 50': [40, 50], '50 - 60': [50, 60], 
                          '60 - 70': [60, 70], '70+': [70, 100000], '< 0': [-1000, 0]}

cape_thresholds = {'0 - 100': [0, 100], '100 - 200': [100, 200], '200 - 300': [200, 300], 
                   '300 - 400': [300, 400], '400 - 500': [400, 500], '500 - 600': [500, 600], 
                   '600 - 700': [600, 700], '700 - 800': [700, 800], '800 - 900': [800, 900],
                   '900 - 1000': [900, 1000], '1000 - 1100': [1000, 1100], '1100 - 1200': [1100, 1200],
                   '1200 - 1300': [1200, 1300], '1300 - 1400': [1300, 1400], '1400 - 1500': [1400, 1500],
                   '1500 - 1600': [1500, 1600], '1600 - 1700': [1600, 1700], '1700+': [1700, 100000]}

speed_shear_csv_titles_list = ['SHARPpy Direct Method Deep Layer Speed Shear [kts]', 'SHARPpy Direct Method PBL Speed Shear [kts]',
                               'SHARPpy Direct Method Mid Layer Speed Shear [kts]', 'SHARPpy Direct Method Upper Layer Speed Shear [kts]']
speed_shear_subplot_titles_list = ['Deep Layer Shear', 'PBL Shear', 'Mid Layer Shear', 'Upper Layer Shear']
speed_shear_thresholds_list = [speed_shear_thresholds, pbl_speed_shear_thresholds, speed_shear_thresholds, speed_shear_thresholds]

RH_csv_titles_list = ['Deep Layer RH [%]', 'PBL RH [%]', 'Mid Layer RH [%]', 'Upper Layer RH [%]']
RH_subplot_titles_list = ['Deep Layer RH', 'PBL RH', 'Mid Layer RH', 'Upper Layer RH']
RH_thresholds_list = [RH_thresholds, RH_thresholds, RH_thresholds, RH_thresholds]

CAPE_csv_titles_list = ['Deep Layer MUCAPE [J/kg]', 'Above FZL MUCAPE [J/kg]', 'Deep Layer MLCAPE [J/kg]', 'Above FZL MLCAPE [J/kg]']
CAPE_subplot_titles_list = ['Deep Layer MUCAPE', 'Upper Layer MUCAPE', 'Deep Layer MLCAPE', 'Upper Layer MLCAPE']
CAPE_thresholds_list = [cape_thresholds, cape_thresholds, cape_thresholds, cape_thresholds]

sondes_metric_savename = ['CAPE', 'SS', 'RH']
sondes_metric_legend = ['[J kg^{-1}]', '[kts]', '[\%]']
sondes_metric_csv_titles = [CAPE_csv_titles_list, speed_shear_csv_titles_list, RH_csv_titles_list]
sondes_metric_subplot_titles = [CAPE_subplot_titles_list, speed_shear_subplot_titles_list, RH_subplot_titles_list]
sondes_metric_thresholds = [CAPE_thresholds_list, speed_shear_thresholds_list, RH_thresholds_list]

#base_timedeltas = [750, 600, 450, 300]  #seconds on either side of the dropsonde (25,20,15,10 minutes total)
base_timedeltas = [600]                 #seconds on either side of the dropsonde (25,20,15,10 minutes total)

#exclude TDs, TCs, scattered cases, and Case 15 (which has basically no APR reflectivity data) dropsondes
skip_cases = [9, 10, 11, 12, 15, 17, 18, 19, 20]
dropsonde_filepath = os.path.join(os.getcwd(), 'Dropsonde_Metric_Calculations.csv')
df = pd.read_csv(dropsonde_filepath)
df_IsoOrg = df[~df['Case'].isin(skip_cases)].copy()  #filter out cases in skip_cases
df_use = df_IsoOrg[df_IsoOrg['Environment Falling In'] != 'Clear Far'].copy()

if len(df) == len(df_IsoOrg):
    sys.exit('Pandas did not filter out the skip_cases')

#Call the function to calculate and plot median reflectivity profiles 
    #for each desired dropsonde for each desired timedelta
    
for aa in base_timedeltas:
    print ('Working on {} second timedelta.....\n'.format(aa))
    dropsonde_medianDBZ_dict = median_dbz_profile(df_use, aa)

    for xx in range(len(sondes_metric_savename)):
        print ('Working on {} figure.....'.format(sondes_metric_savename[xx]))
        save_name = sondes_metric_savename[xx] + '_medianDBZ_' + str(aa) + '.png'
        
        metrics_use = sondes_metric_csv_titles[xx]
        subplot_titles_use = sondes_metric_subplot_titles[xx]
        metric_thresholds = sondes_metric_thresholds[xx]
        
        group_fig = plt.figure(figsize = (30,30))
        
        #create plots of dropsonde median Ku-reflectivity profiles (color coded by metric magnitude)
        for ii in range(4):
            ax1 = group_fig.add_subplot(4,2,ii * 2 + 1)  #LHS plots (i.e., Isolated plots)
            ax2 = group_fig.add_subplot(4,2,(ii + 1) * 2)  #RHS plots (i.e., Organized plots)
            for case_time in dropsonde_medianDBZ_dict:
                ku_profile = dropsonde_medianDBZ_dict[case_time]['median_dbz_profile']
                height_profile = dropsonde_medianDBZ_dict[case_time]['median_height_profile']
                
                case_time_data = df_use[(df_use['Date'] == int(case_time[:8])) & (df_use['Time'] == int(case_time[8:]))]
                case_time_convective_type = case_time_data['Primary Convective Type'].values[0]
                case_time_envt = case_time_data['Environment Falling In'].values[0]
                metric_value = case_time_data[metrics_use[ii]].values[0]
                
                #if metric_value is blank (nan) or you are plotting CAPE/RH and the dropsonde is "In Precip",
                    #then omit the profile from the plots
                if (not metric_value > -999) or (sondes_metric_savename[xx] == 'CAPE' and case_time_envt == 'In Precip') or (sondes_metric_savename[xx] == 'RH' and case_time_envt == 'In Precip'):
                    continue

                for kk, threshold in enumerate(metric_thresholds[ii]):  #color code by metric magnitude
                    if metric_value >= metric_thresholds[ii][threshold][0] and metric_value < metric_thresholds[ii][threshold][1]:
                        threshold_label = threshold
                        threshold_color = color_list[kk]
                        break
                    
                if case_time_convective_type == 'Isolated':
                    ax1.plot(ku_profile, height_profile, c = threshold_color, label = threshold_label)
                elif case_time_convective_type == 'Organized':
                    ax2.plot(ku_profile, height_profile, c = threshold_color, label = threshold_label)
                else:
                    sys.exit('The dropsonde is not Isolated or Organized convective type')
            
            ax1.grid(True)
            ax1.set_xlim([-15,40])
            ax1.set_xticks(np.arange(-10,41,10))
            ax1.set_ylim([1500,7622.5])
            ax1.set_yticks(np.arange(2000,7000.5,1000))
            ax1.tick_params(length = 15, width = 5, labelsize = 25)
            ax1.set_title(subplot_titles_use[ii] + ' (Isolated Cases)', fontsize = 33, fontweight = 'bold')
            ax1.set_xlabel('Median Ku-band Reflectivity [dBZ]', fontsize = 30, fontweight = 'bold')
            ax1.set_ylabel('Altitude [m]', fontsize = 30, fontweight = 'bold')
            
            #get rid of duplicate legend labels and order legend alphabetically by label name
            #handles, labels = plt.gca().get_legend_handles_labels()
            handles, labels = ax1.get_legend_handles_labels()
            by_label = dict(zip(labels, handles))  #get rid of duplicate legend labels
            ordered_labels, ordered_handles = zip(*sorted(by_label.items(), key=lambda t: t[0]))  #sort the labels alphabetically
            ax1.legend(ordered_handles, ordered_labels, title = f'$\\bf{{}}$'.format(sondes_metric_legend[xx]), loc = 'lower left')
            
            ax2.grid(True)
            ax2.set_xlim([-15,40])
            ax2.set_xticks(np.arange(-10,41,10))
            ax2.set_ylim([1500,7622.5])
            ax2.set_yticks(np.arange(2000,7000.5,1000))
            ax2.tick_params(length = 15, width = 5, labelsize = 25)
            ax2.set_title(subplot_titles_use[ii] + ' (Organized Cases)', fontsize = 33, fontweight = 'bold')
            ax2.set_xlabel('Median Ku-band Reflectivity [dBZ]', fontsize = 30, fontweight = 'bold')
            ax2.set_ylabel('Altitude [m]', fontsize = 30, fontweight = 'bold')
            
            #get rid of duplicate legend labels and order legend alphabetically by label name
            #handles, labels = plt.gca().get_legend_handles_labels()
            handles, labels = ax2.get_legend_handles_labels()
            by_label = dict(zip(labels, handles))  #get rid of duplicate legend labels
            ordered_labels, ordered_handles = zip(*sorted(by_label.items(), key=lambda t: t[0]))  #sort the labels alphabetically
            ax2.legend(ordered_handles, ordered_labels, title = f'$\\bf{{}}$'.format(sondes_metric_legend[xx]), loc = 'lower left')
            
        #plt.subplots_adjust(hspace=0.45, wspace=0.30)
        #ts = plt.suptitle(convective_type + ' Dropsonde Median Ku-reflectivity Profiles', fontsize = 30, fontweight = 'bold')
        #ts.set_y(0.95)
        plt.subplots_adjust(hspace = 0.50, wspace = 0.30)
        #plt.tight_layout()
        plt.savefig(os.path.join(os.getcwd(),'Dropsonde_Median_dBZ_Profiles_Thesis', save_name), bbox_inches = 'tight')
        plt.close()
        print ('Completed {} figure.....\n'.format(sondes_metric_savename[xx]))
            
    print ('Completed {} second timedelta.....\n'.format(aa))

