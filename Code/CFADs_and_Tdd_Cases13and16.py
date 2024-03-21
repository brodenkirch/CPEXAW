import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mplc
import matplotlib
import numpy as np
from datetime import datetime
import h5py

matplotlib.rcParams['font.family'] = 'arial'
# matplotlib.rcParams['axes.labelsize'] = 14
# matplotlib.rcParams['axes.titlesize'] = 14
# matplotlib.rcParams['xtick.labelsize'] = 12
# matplotlib.rcParams['ytick.labelsize'] = 12
matplotlib.rcParams['legend.fontsize'] = 22
#matplotlib.rcParams['legend.facecolor'] = 'w'

#for each Case 13/16 that captures a mid-level jet, calculate dewpoint depression for all levels within the 
#jet's layer (800 - 650 mb) and then calculate the average dewpoint depression for the jet layer

case13_jet_drop_times = ['18:15:34','18:19:50','18:53:32','18:59:25','19:49:57','19:55:58']  #for 800-650mb layer
case16_jet_drop_times = ['18:01:43','19:03:12','19:09:29','20:12:49'] #for 800-650mb layer

print ('Mid-level Jet Region (800-650mb) Average Dewpoint Depression:\n')
for date in ['20170611', '20210824']:
    drop_filepath = os.path.join(os.getcwd(), date, 'final_dropsonde_' + date + '.csv')
    df = pd.read_csv(drop_filepath)
    
    if date == '20170611':
        time_list = case13_jet_drop_times
    elif date == '20210824':
        time_list = case16_jet_drop_times
        
    date_list = []
    for time in time_list:
        date_list.append(date[:4] + '-' + date[4:6] + '-' + date[6:8] + ' ' + time)  #YYYY-MM-DD HH:MM:SS

    for x in date_list:
        df_date_jet_region = df[(df['Time [UTC]'] == x) & (df['Pressure [mb]'] <= 800) & (df['Pressure [mb]'] >= 650)]
        tdd_series = df_date_jet_region['Temperature [C]'] - df_date_jet_region['Dew Point [C]']
        print (x, tdd_series.mean())
        #could also just do the following, which is the same thing:
            #df_date_jet_region['Temperature [C]'].mean() - df_date_jet_region['Dew Point [C]'].mean()
                #^^^ this is the same thing mathematically
        
        # df_date = df[df['Time [UTC]'] == x]
        # plt.scatter(df_date['Wind Speed [m/s]'], df_date['Pressure [mb]'])
        # plt.axhline(y = 650, c ='k', linestyle = '--')
        # plt.axhline(y = 800, c ='k', linestyle = '--')
        # plt.xlim([0,20])
        # plt.ylim([1000,300])
        # plt.savefig('/Users/brodenkirch/Desktop/' + x + '.png', bbox_inches = 'tight')
        # plt.close()
        
      
###############################################################################################
###############################################################################################
###############################################################################################

#Create (difference) CFADs for already mature/weakening (i.e., peaked) and intensifying halves of Cases 13 and 16

#create the dictionary of cases/stages for which you want to plot CFADs
case13_intensify_dict = {13: ['20170611', '180000', '185100']}
case13_matureweak_dict = {13: ['20170611', '190300', '203400']}
case16_intensify_dict = {16: ['20210824', '181545', '185000']}
case16_matureweak_dict = {16: ['20210824', '191930', '195745']}

case1_dict = {1: ['20170610','194655','221900']}
case2_dict = {2: ['20170624','180000','194800']}
case3_dict = {3: ['20170624','201200','220000']}
case4_dict = {4: ['20170615', '184840', '205000']}
case5_dict = {5: ['20170616', '182451', '220600' ]}
case6_dict = {6: ['20170601', '175849', '220700']}
case7_dict = {7: ['20170606', '185211', '215000']}
case8_dict = {8: ['20170617', '184650', '220000']}
case9_dict = {9: ['20170619', '173229', '223000']}
case10_dict = {10: ['20170620', '171600', '220600']}
case11_dict = {11: ['20170602', '174415', '221221']}
case12_dict1 = {12: ['20170611', '170000', '174500']}
case12_dict2 = {12: ['20170611', '210000', '214500']}
case13_dict = {13: ['20170611', '180100', '203400']}
case14_dict = {14: ['20210821', '221800', '234145']}
case16_dict = {16: ['20210824', '181545', '195745']}

height_edges = np.arange(1500, 8001, 500)
dbz_edges = np.arange(-20, 60.1, 5)
vel_edges = np.arange(-13, 15.1, 2)

def plot_CFAD(cfad_array, contours, colorbar_label, save_label, var_label, var_centers_meshgrid, height_centers_meshgrid, var_edges, case_dict, median_height_profile_above1500m, medianDBZ_profile_above1500m, Q1DBZ_profile_above1500m, Q3DBZ_profile_above1500m, dbz_plot = True):
    
    """Plot a contourf CFAD given a CFAD 2-D array, contour levels, plot/image labels, and variable/height meshgrids"""
    
    #plot the CFAD
    fig, ax = plt.subplots(1,1, figsize=(21,21))
    cmap = mplc.ListedColormap(['#ffffff', '#d8fcfa', '#bef5f6', '#aaedf1', '#98e4ec', '#89dae7', '#7cd0e2', 
                                '#70c6dd', '#65bcd9', '#5cb2d4', '#53a8cf', '#4b9dca', '#4393c5', '#3c89c0', 
                                '#357ebb', '#2f74b6', '#286ab1', '#2160ac', '#1956a7', '#0f4ca2', '#00429d'])
    
    #the cmap below omits the white fill at the beginnning
    # cmap = mplc.ListedColormap(['#d8fcfa', '#bef5f6', '#aaedf1', '#98e4ec', '#89dae7', '#7cd0e2', 
    #                             '#70c6dd', '#65bcd9', '#5cb2d4', '#53a8cf', '#4b9dca', '#4393c5', '#3c89c0', 
    #                             '#357ebb', '#2f74b6', '#286ab1', '#2160ac', '#1956a7', '#0f4ca2', '#00429d'])
    
    #cs = ax.pcolormesh(dbz_meshgrid, height_meshgrid, cfad_array, cmap = cmap)
    #cs = ax.contour(dbz_centers_meshgrid, height_centers_meshgrid, cfad_array, levels = contours, cmap = cmap, linewidths = 1)
    cs = ax.contourf(var_centers_meshgrid, height_centers_meshgrid, cfad_array, levels = contours, cmap = cmap)
    if dbz_plot:
        ax.plot(medianDBZ_profile_above1500m, median_height_profile_above1500m, color = 'k', linestyle = '-', linewidth = 5, label = 'Case ' + ','.join(map(str, list(case_dict.keys()))) + ' Median Profile') 
        ax.plot(Q1DBZ_profile_above1500m, median_height_profile_above1500m, color = 'k', linestyle = '--', linewidth = 5, label = 'Case ' + ','.join(map(str, list(case_dict.keys()))) + ' Q1 and Q3 Profiles')
        ax.plot(Q3DBZ_profile_above1500m, median_height_profile_above1500m, color = 'k', linestyle = '--', linewidth = 5)
        ax.legend(loc = 'upper right')
    ax.set_ylabel('Altitude [m]', fontsize=30, fontweight = 'bold')
    ax.set_xlabel(var_label, fontsize=30, fontweight = 'bold')
    ax.tick_params(length = 15, width = 5, labelsize = 25)
    #ax.set_title('Total CFAD for Case ' + ','.join(map(str, list(case_dict.keys()))), fontsize=35, fontweight = 'bold')
    ax.set_title('Case ' + ','.join(map(str, list(case_dict.keys()))) + ' Normalized CFAD', fontsize=35, fontweight = 'bold')
    ax.set_ylim([height_edges[0] + 250, height_edges[-1] - 250])
    ax.set_xlim([var_edges[0],var_edges[-1]])
    ax.set_xlim([-5,50])
    
    #set the colorbar axis
    cax = fig.add_axes([ax.get_position().x0, ax.get_position().y0 - 0.08,
                       ax.get_position().x1-ax.get_position().x0, 0.02])    #Left, bottom, width, height (all [0,1])

    #create the colorbar
    cbar = plt.colorbar(cs, cax = cax, orientation = 'horizontal')
    cbar.ax.tick_params(length = 10, width = 3, labelsize = 23)
    cbar.set_label(label = colorbar_label, fontsize = 30, fontweight = 'bold')
    
    #save the figure
    plt.savefig(''.join(['/Users/brodenkirch/Desktop/', save_label]), bbox_inches = 'tight')
    plt.close()


def CFAD(case_dict, height_bin_edges, dbz_bin_edges, vel_bin_edges, normalize = True):
    
    """"Calculate and plot Ku-band and Doppler Velocity CFAD 2-D arrays for 
        the given cases and their respective time ranges
    
    Parameters
    ----------
    case_dict:  dictionary of cases for which to calculate the total CFAD; 
                keys should be case numbers;
                values should be 3-element lists of case date and start/end times, 
                with date strings formatted as YYYYMMDD and time strings formatted as HHMMSS
    
    height_bin_edges:  a 1-D array of height [m] bin edges used to create the 2-D CFAD array/histogram    

    dbz_bin_edges:  a 1-D array of reflectivity [dBZ] bin edges used to create the 2-D CFAD array/histogram 

    vel_bin_edges:  a 1-D array of Doppler velocity [m/s] bin edges used to create the 2-D CFAD array/histogram       
                        
    normalized:  True/False; determines whether to normalize the CFAD array by maximum bin at any level 
                 (method from Zagrodnik et al., 2019) and create an additional, normalized CFAD plot
                        
    return:  2-D (normalized) CFAD arrays and plots """

    assert type(case_dict) == dict, "case_dict must be a dictionary"
    
    total_apr_profiles = 0 
    apr_profile_roll10 = 0

    new_vel_array = True
    
    for key in case_dict:
        print ('Processing Case {}...'.format(key))
        
        #grab the case's date and start/end times from the dictionary
        assert type(case_dict[key]) == list, "a key's values must be a list of date, start time, and end time" 
        desired_date = case_dict[key][0]
        start_time = case_dict[key][1]
        end_time = case_dict[key][2]
        assert start_time < end_time, "start time must precede end time in a key's list"
        
        #find the APR files of interest (for the desired date and time ranges)
        apr_folder = os.path.join(desired_date, 'APR_files')
        apr_file_list = sorted(os.listdir(apr_folder))
        
        #angles for each of the 24 rays in a given scan (used for ray adjustment; index order goes from left to right in the scan when looking ahead in the direction that the aircraft is headed)
        if desired_date[:4] == '2017':
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
                
        elif desired_date[:4] == '2021':
            ray_angles = np.linspace(-25,25,25)
            
            #create a list of all the given day's desired range's APR files:    #for APR_plots.py
            start_time1 = datetime.strptime(desired_date + start_time, '%Y%m%d%H%M%S')
            end_time1 = datetime.strptime(desired_date + end_time, '%Y%m%d%H%M%S')
            
            for x in os.listdir(apr_folder):
                if x[0:3] == '.DS':         #delete hidden .DS_Store files if they come up (will show up if you delete a file)
                    os.remove(os.path.join(apr_folder, x))
            
            #find the starting APR file in apr_folder
            first_file_index = None       
            for i, x in enumerate(apr_file_list):
                file_start_time = datetime.strptime(x[13:21] + x[22:28], '%Y%m%d%H%M%S')
                file_end_time = datetime.strptime(x[29:37] + x[38:44], '%Y%m%d%H%M%S')
            
                if start_time1 <= file_start_time:  #if start_time1 is before the APR file start time and not within any previous APR file's time ranges
                    first_file_index = i
                    break
                elif (start_time1 >= file_start_time) and (start_time1 < file_end_time):
                    first_file_index = i
                    break
                else:
                    continue
            if first_file_index == None:
                sys.exit('Requested start_time is beyond all available APR files')
                
            #find the ending APR file in apr_folder
            last_file_index = None       
            for i, x in enumerate(apr_file_list):  
                file_start_time = datetime.strptime(x[13:21] + x[22:28], '%Y%m%d%H%M%S')
                file_end_time = datetime.strptime(x[29:37] + x[38:44], '%Y%m%d%H%M%S')
            
                if end_time1 <= file_start_time:  #if end_time1 is before the APR file start time and not within any previous APR file's time ranges
                    last_file_index = i - 1
                    break
                elif (end_time1 > file_start_time) and (end_time1 <= file_end_time):
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
    
        print (apr_files_use)  #sanity check to make sure you grabbed the right files
        
        #Low resolution ('lores') radar variables in APR hdf files
        ku_band = 'zhh14' #Ku-band reflectivity
        vel = 'vel14c' #mean Doppler Velocity dealiased and from Ku&Ka band    

        for apr_filepath in apr_files_use:
            apr_file = h5py.File(os.path.join(apr_folder, apr_filepath), 'r')
            
            if ('lores' in apr_file.keys()) and (ku_band in apr_file['lores'].keys()):
                
                try:   #some CPEX-AW APR files have corrupted Ku-band data; if so, skip the Ku-band for 
                       #that file (corrupted: "OSError: Can't read data (inflate() failed)")
                    ku_data = apr_file['lores'][ku_band][:]
                except:
                    continue  #both Ku-band and velocity CFADs rely on Ku-band data availability

                try:   #some CPEX-AW APR files have corrupted velocity data; if so, skip the Ku-band for 
                       #that file (corrupted: "OSError: Can't read data (inflate() failed)")
                    vel_data = apr_file['lores'][vel][:]
                    vel_good = True
                except:
                    vel_good = False                    
            
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
                            tmp = datetime.utcfromtimestamp(time[i,j])
                            time_dates[i,j] = tmp
                    
                    unique_apr_times = time_dates[12,:]  #all the times in the given APR file
                    
                    if len(apr_files_use) == 1:  #i.e. apr_filepath == apr_files_use[0] and apr_filepath == apr_files_use[-1]
                    
                        #find the closest time (and its corresponding index) to the desired start_time
                        desired_start_time = datetime.strptime(desired_date + start_time, '%Y%m%d%H%M%S')
                        start_time_idx = np.argmin(abs(unique_apr_times - desired_start_time))
                    
                        #find the closest time (and its corresponding index) to the desired end_time
                        desired_end_time = datetime.strptime(desired_date + end_time, '%Y%m%d%H%M%S')
                        end_time_idx = np.argmin(abs(unique_apr_times - desired_end_time))
                                
                    elif apr_filepath == apr_files_use[0]:  #i.e. the first APR file in the apr_files_use list
                        end_time_idx = time.shape[1] - 1
                        
                        #find the closest time (and its corresponding index) to the desired start_time
                        desired_start_time = datetime.strptime(desired_date + start_time, '%Y%m%d%H%M%S')
                        start_time_idx = np.argmin(abs(unique_apr_times - desired_start_time))
                                
                    else:  #apr_filepath == apr_files_use[-1]  #i.e. the last APR file in the apr_files_use list
                        start_time_idx = 0
                        
                        #find the closest time (and its corresponding index) to the desired end_time
                        desired_end_time = datetime.strptime(desired_date + end_time, '%Y%m%d%H%M%S')
                        end_time_idx = np.argmin(abs(unique_apr_times - desired_end_time))                
                        
                else:  #the entire APR file is within the desired time range, so set the start/end indices to the first/last indices of the APR file
                    start_time_idx = 0
                    end_time_idx = time.shape[1] - 1
                        
                #numpy.histogram2d(dBZ, z) (Zagrodnik et al., 2019) CFAD method:
                
                #loop through the given APR file’s valid times/scans/profiles
                for time_idx in range(start_time_idx, end_time_idx + 1):
                    
                    total_apr_profiles += 1
                    
                    #choose the "nadir" ray factoring in aircraft roll
                    ac_roll = np.nanmean(roll[:,time_idx])  #roll varies slightly w/ray, so take the average roll value for a given scan and use that for ray adjustment
                    ray_use = np.argmin(np.abs(ray_angles - ac_roll))  #the index of the ray whose angle is closest to that of ac_roll
                    
                    if abs(ac_roll) >= 10:
                        apr_profile_roll10 += 1
                    
                    prof_height = alt3d[:,ray_use,time_idx]
                    prof_dbz = ku_data[:,ray_use,time_idx]
                    
                    #grab the height/dbz data above 1.5km
                    idx_1500m = np.argmin(np.abs(prof_height - 1500))
                    prof_height_above1500m = np.flip(prof_height[:idx_1500m + 1])  #height profile above 1.5km, in ascending order
                    prof_dbz_above1500m = np.flip(prof_dbz[:idx_1500m + 1])  #Ku-band profile above 1.5km, in ascending order
                    
                    #store all the profile's height/dbz data in long 1-D concatenated arrays
                    if key == list(case_dict.keys())[0] and apr_filepath == apr_files_use[0] and time_idx == start_time_idx:
                        #if this is the first qualifying time of the first APR file of the first case in case_dict
                        height_concat = prof_height.copy()
                        dbz_concat = prof_dbz.copy()
                        
                        #create a DataFrame of values above 1.5km, in order to calculate median/quartile reflectivity profile for the given case
                            #NOTE: WE ARE ASSUMING THAT EACH ROW CORRESPONDS TO A NEAR IDENTICAL HEIGHT LEVEL
                                #this is the best we can do, and should be fine given that each profile is starting from ~1500m and the height resolution is the same for each profile     
                        height_profiles_above1500m_df = pd.DataFrame(prof_height_above1500m)  #height profile from 1500m to top of profile
                        dbz_profiles_above1500m_df = pd.DataFrame(prof_dbz_above1500m)        #dbz profile from 1500m to top of profile
                    else:
                        height_concat = np.concatenate((height_concat, prof_height))
                        dbz_concat = np.concatenate((dbz_concat, prof_dbz))
                        
                        #NOTE: WE ARE ASSUMING THAT EACH ROW CORRESPONDS TO A NEAR IDENTICAL HEIGHT LEVEL
                            #this is the best we can do, and should be fine given that each profile is starting from ~1500m and the height resolution is the same for each profile
                        height_profiles_above1500m_df = pd.concat((height_profiles_above1500m_df, pd.Series(prof_height_above1500m)), axis = 1, ignore_index = True)  #add profile as a new column to the df; differences in profile lengths are filled in with NaNs
                        dbz_profiles_above1500m_df = pd.concat((dbz_profiles_above1500m_df, pd.Series(prof_dbz_above1500m)), axis = 1, ignore_index = True)  #add profile as a new column to the df; differences in profile lengths are filled in with NaNs
                    
                    if vel_good:
                        prof_vel = vel_data[:,ray_use,time_idx]
                        
                        #store all the profile's velocity data in long 1-D concatenated arrays if 
                        #the profile has Ku data > 0 dBZ above 1.5km (i.e. omits clear profiles)
                        idx_1500m = np.argmin(np.abs(prof_height - 1500))
                        prof_dbz_above1500m = prof_dbz[:idx_1500m + 1]  #Ku-band profile above 1.5km
                        
                        if np.nanmax(prof_dbz_above1500m) > 0:
                            if new_vel_array:
                                vel_concat = prof_vel.copy()
                                height_vel_concat = prof_height.copy()
                                new_vel_array = False
                            else:
                                vel_concat = np.concatenate((vel_concat, prof_vel))
                                height_vel_concat = np.concatenate((height_vel_concat, prof_height))
                        else:  #clear profiles (which may have noisy velocity data) are omitted from the velocity CFAD
                            pass
                    else:
                        pass
            else:
                pass
                
            apr_file.close()
        print ('Case {} complete'.format(key))
        
    #calculate median/quantile dBZ profiles for the given case
    
    #replace blank data (-99.99) with NaNs
    dbz_profiles_above1500m_df[dbz_profiles_above1500m_df <= -99] = np.nan
    height_profiles_above1500m_df[height_profiles_above1500m_df < 0] = np.nan
    
    #convert all the dropsonde's Ku-band data from dBZ to mm^6 m^-3
    Z_df = 10**(dbz_profiles_above1500m_df / 10)
    
    #calculate the dropsonde's median/quantile heights and reflectivity (in mm^6 m^-3) and standard deviation at each height level
    #NOTE: WE ARE ASSUMING THAT EACH ROW CORRESPONDS TO A NEAR IDENTICAL HEIGHT LEVEL
        #this is the best we can do, and should be fine given that each profile is starting from ~1500m and the height resolution is the same for each profile
        
    median_height_profile_above1500m = height_profiles_above1500m_df.median(axis = 1)  #axis of 1 = across all columns (so for each row); NaNs are ignored by default in Pandas
    Z_median = Z_df.median(axis = 1)  #axis of 1 = across all columns (so for each row); NaNs are ignored by default in Pandas
    Z_Q1 = Z_df.quantile(q = 0.25, axis = 1)
    Z_Q3 = Z_df.quantile(q = 0.75, axis = 1)
    #Z_std = Z_df.std(axis = 1)
    
    #convert the dropsonde's median/quartile reflectivity and standard deviation profile back to dBZ
    medianDBZ_profile_above1500m = 10 * np.log10(Z_median)
    Q1DBZ_profile_above1500m = 10 * np.log10(Z_Q1)
    Q3DBZ_profile_above1500m = 10 * np.log10(Z_Q3)
    #stdDBZ_profile_above1500m = 10 * np.log10(Z_std)      
        
    
        
        
    #setting the height, reflectivity, and velocity bin edges, along with their associated meshgrids
    height_edges = height_bin_edges
    dbz_edges = dbz_bin_edges
    #dbz_meshgrid, height_meshgrid = np.meshgrid(dbz_edges, height_edges)
    
    vel_edges = vel_bin_edges
    #vel_meshgrid, height_vel_meshgrid = np.meshgrid(vel_edges, height_edges)
    
    #setting the height, reflectivity, and velocity bin centers and their associated meshgrids for contourf plotting
    height_centers = (height_edges[:-1] + height_edges[1:]) / 2    
    dbz_centers = (dbz_edges[:-1] + dbz_edges[1:]) / 2
    dbz_centers_meshgrid, height_centers_meshgrid = np.meshgrid(dbz_centers, height_centers)
    
    vel_centers = (vel_edges[:-1] + vel_edges[1:]) / 2
    vel_centers_meshgrid, height_vel_centers_meshgrid = np.meshgrid(vel_centers, height_centers)
  
    #create the 2D histogram of values/frequencies for Ku-band data
    cfad_array, xedges, yedges = np.histogram2d(dbz_concat, height_concat, bins = (dbz_edges,height_edges))
    
    #transpose cfad_array shape (rows, columns) to be (height, dbz) instead of (dbz, height)
    cfad_array = cfad_array.T
    #cfad_array = np.log10(cfad_array)  #creates log-weighted CFADs
    contours = np.linspace(0, np.nanmax(cfad_array), 21)
    colorbar_label = 'Total Frequency [#]'
    var_label = 'Ku-band Reflectivity [dBZ]'
    save_label = 'CFAD_Cases' + '-'.join(map(str, list(case_dict.keys()))) + '_Ku.png'
    plot_CFAD(cfad_array, contours, colorbar_label, save_label, var_label, dbz_centers_meshgrid, height_centers_meshgrid, dbz_edges, case_dict, median_height_profile_above1500m, medianDBZ_profile_above1500m, Q1DBZ_profile_above1500m, Q3DBZ_profile_above1500m, dbz_plot = True)
    
    #normalize the CFAD and make a normalized CFAD plot if that is also desired
    if normalize:
        #cfad_array = cfad_array / np.nanmax(cfad_array) * 100
        height_bin_maxs = np.nanmax(cfad_array, axis = 1)   #normalize the CFAD by max count in each height bin
        cfad_array = cfad_array / height_bin_maxs[:, np.newaxis] * 100
        contours = np.arange(0,101,5)
        colorbar_label = 'Normalized Frequency [%]'
        save_label = 'CFADnorm_Cases' + '-'.join(map(str, list(case_dict.keys()))) + '_Ku.png'
        plot_CFAD(cfad_array, contours, colorbar_label, save_label, var_label, dbz_centers_meshgrid, height_centers_meshgrid, dbz_edges, case_dict, median_height_profile_above1500m, medianDBZ_profile_above1500m, Q1DBZ_profile_above1500m, Q3DBZ_profile_above1500m, dbz_plot = True)
        
        
    #create the 2D histogram of values/frequencies for Doppler Velocity data
    cfad_array_vel, xedges, yedges = np.histogram2d(vel_concat, height_vel_concat, bins = (vel_edges,height_edges))
    
    #transpose cfad_array shape (rows, columns) to be (height, vel) instead of (vel, height)
    cfad_array_vel = cfad_array_vel.T
    #cfad_array_vel = np.log10(cfad_array_vel)  #creates log-weighted CFADs
    contours = np.linspace(0, np.nanmax(cfad_array_vel), 21)
    colorbar_label = 'Total Frequency [#]'
    var_label = 'Mean Doppler Velocity [m/s]'
    save_label = 'CFAD_Cases' + '-'.join(map(str, list(case_dict.keys()))) + '_Vel.png'
    plot_CFAD(cfad_array_vel, contours, colorbar_label, save_label, var_label, vel_centers_meshgrid, height_vel_centers_meshgrid, vel_edges, case_dict, median_height_profile_above1500m, medianDBZ_profile_above1500m, Q1DBZ_profile_above1500m, Q3DBZ_profile_above1500m, dbz_plot = False)
    
    #normalize the CFAD and make a normalized CFAD plot if that is also desired
    if normalize:
        #cfad_array_vel = cfad_array_vel / np.nanmax(cfad_array_vel) * 100
        height_bin_maxs = np.nanmax(cfad_array_vel, axis = 1)   #normalize the CFAD by max count in each height bin
        cfad_array_vel = cfad_array_vel / height_bin_maxs[:, np.newaxis] * 100
        contours = np.arange(0,101,5)
        colorbar_label = 'Normalized Frequency [%]'
        save_label = 'CFADnorm_Cases' + '-'.join(map(str, list(case_dict.keys()))) + '_Vel.png'
        plot_CFAD(cfad_array_vel, contours, colorbar_label, save_label, var_label, vel_centers_meshgrid, height_vel_centers_meshgrid, vel_edges, case_dict, median_height_profile_above1500m, medianDBZ_profile_above1500m, Q1DBZ_profile_above1500m, Q3DBZ_profile_above1500m, dbz_plot = False)
        
    print ('Percent of profiles with A/C roll >= 10 degrees:', apr_profile_roll10 / total_apr_profiles * 100)
    
    return cfad_array, cfad_array_vel, dbz_centers_meshgrid, height_centers_meshgrid, vel_centers_meshgrid, height_vel_centers_meshgrid, median_height_profile_above1500m, medianDBZ_profile_above1500m, Q1DBZ_profile_above1500m, Q3DBZ_profile_above1500m
    

def plot_diffCFAD(cfad_array, contours, colorbar_label, save_label, var_label, var_centers_meshgrid, height_centers_meshgrid, var_edges, height_edges, case1_num, case2_num, first_median_height_profile_above1500m, first_medianDBZ_profile_above1500m, first_Q1DBZ_profile_above1500m, first_Q3DBZ_profile_above1500m, second_median_height_profile_above1500m, second_medianDBZ_profile_above1500m, second_Q1DBZ_profile_above1500m, second_Q3DBZ_profile_above1500m, dbz_plot = True):
    
    """Plot a contourf difference CFAD given a difference CFAD 2-D array, contour levels, plot/image labels, and variable/height meshgrids"""
    
    #plot the CFAD
    fig, ax = plt.subplots(1,1, figsize=(21,21))
    # cmap = mplc.ListedColormap(['#00429d', '#2855a6', '#3e68af', '#507bb8', '#618fc1', '#73a3ca', '#85b8d3', 
    #                             '#99ccdc', '#b0e0e6', '#cef2f1', '#ffffff', '#ffe5e7', '#ffcbcf', '#ffafb7', 
    #                             '#ff929e', '#f57789', '#e95d76', '#d94364', '#c62a54', '#af1046', '#93003a'])
    
    cmap = mplc.ListedColormap(['#00429d', '#074ca2', '#0e57a8', '#1561ad', '#1d6bb2', '#2475b8', '#2b7fbd', 
                                '#3289c2', '#3994c8', '#409ecd', '#48a8d2', '#4fb3d8', '#56bddd', '#5ec8e3', 
                                '#65d3e8', '#6dddee', '#74e8f4', '#7cf3f9', '#83feff', '#cbffff', '#ffffff', 
                                '#fef3f0', '#fce7e0', '#fbdad0', '#facec1', '#f8c2b1', '#f7b5a1', '#f5a890', 
                                '#f49b7f', '#f28d6e', '#f17f5c', '#ef6f48', '#ed5f33', '#eb4c1b', '#e13f18', 
                                '#d5351e', '#c82b23', '#bc2128', '#af162e', '#a10b34', '#93003a'])
    
    #cs = ax.pcolormesh(dbz_meshgrid, height_meshgrid, cfad_array, cmap = cmap)
    #cs = ax.contour(dbz_centers_meshgrid, height_centers_meshgrid, cfad_array, levels = contours, cmap = cmap, linewidths = 1)
    cs = ax.contourf(var_centers_meshgrid, height_centers_meshgrid, cfad_array, levels = contours, cmap = cmap)
    if dbz_plot:
        ax.plot(second_medianDBZ_profile_above1500m, second_median_height_profile_above1500m, color = 'k', linestyle = '-', linewidth = 5, label = 'Case ' + case2_num + ' Median Profile') 
        ax.plot(second_Q1DBZ_profile_above1500m, second_median_height_profile_above1500m, color = 'k', linestyle = '--', linewidth = 5, label = 'Case ' + case2_num + ' Q1 and Q3 Profiles')
        ax.plot(second_Q3DBZ_profile_above1500m, second_median_height_profile_above1500m, color = 'k', linestyle = '--', linewidth = 5)
        
        ax.plot(first_medianDBZ_profile_above1500m, first_median_height_profile_above1500m, color = 'darkgoldenrod', linestyle = '-', linewidth = 5, label = 'Case ' + case1_num + ' Median Profile') 
        ax.plot(first_Q1DBZ_profile_above1500m, first_median_height_profile_above1500m, color = 'darkgoldenrod', linestyle = '--', linewidth = 5, label = 'Case ' + case1_num + ' Q1 and Q3 Profiles')
        ax.plot(first_Q3DBZ_profile_above1500m, first_median_height_profile_above1500m, color = 'darkgoldenrod', linestyle = '--', linewidth = 5)
        
        ax.legend(loc = 'upper right')
        
    ax.set_ylabel('Altitude [m]', fontsize=30, fontweight = 'bold')
    ax.set_xlabel(var_label, fontsize=30, fontweight = 'bold')
    ax.tick_params(length = 15, width = 5, labelsize = 25)
    ax.set_title('Difference CFAD (Case ' + case2_num + ' minus ' + 'Case ' + case1_num + ')', fontsize=35, fontweight = 'bold')
    ax.set_ylim([height_edges[0] + 250, height_edges[-1] - 250])
    ax.set_xlim([var_edges[0],var_edges[-1]])
    ax.set_xlim([-5,50])
    
    #set the colorbar axis
    cax = fig.add_axes([ax.get_position().x0, ax.get_position().y0 - 0.08,
                       ax.get_position().x1-ax.get_position().x0, 0.02])    #Left, bottom, width, height (all [0,1])

    #create the colorbar
    cbar = plt.colorbar(cs, cax = cax, orientation = 'horizontal')
    cbar.ax.tick_params(length = 10, width = 3, labelsize = 23)
    cbar.set_label(label = colorbar_label, fontsize = 30, fontweight = 'bold')
    
    #save the figure
    #plt.savefig(''.join(['/Users/brodenkirch/Desktop/CPEX-AW/Coding/CFAD_plots/Case', case1_num, 'and', case2_num, '_Comparison/', save_label]), bbox_inches = 'tight')
    #plt.savefig(''.join(['/Users/brodenkirch/Desktop/CPEX-AW/Coding/CFAD_plots/0_Group_Comparison/Cases', case2_num, '_vs_Case', case1_num, '/', save_label]), bbox_inches = 'tight')
    plt.savefig(''.join(['/Users/brodenkirch/Desktop/', save_label]), bbox_inches = 'tight')    
    plt.close()


def difference_CFAD(case_dict_1, case_dict_2, height_bin_edges, dbz_bin_edges, vel_bin_edges):

    """"Calculate and plot Ku-band and Doppler Velocity difference (normalized) CFAD 2-D arrays for 
        the given pair of dictionaries containing given cases and their respective time ranges
    
    Parameters
    ----------
    case_dict_1:  dictionary of cases for which to calculate the first normalized CFAD; 
                  keys should be case numbers;
                  values should be 3-element lists of case date and start/end times, 
                  with date strings formatted as YYYYMMDD and time strings formatted as HHMMSS
                  
    case_dict_2:  dictionary of cases for which to calculate the second normalized CFAD; 
                  keys should be case numbers;
                  values should be 3-element lists of case date and start/end times, 
                  with date strings formatted as YYYYMMDD and time strings formatted as HHMMSS
    
    height_bin_edges:  a 1-D array of height [m] bin edges used to create the 2-D difference CFAD array/histogram    

    dbz_bin_edges:  a 1-D array of reflectivity [dBZ] bin edges used to create the 2-D difference CFAD array/histogram 

    vel_bin_edges:  a 1-D array of Doppler velocity [m/s] bin edges used to create the 2-D difference CFAD array/histogram
                        
    return:  2-D (normalized) difference CFAD plots (case_dict_2 - case_dict_1)"""

    #calculate the Ku-band and Doppler Velocity 2-D normalized CFADs for each case
    first_dbz_CFAD, first_vel_CFAD, dbz_centers_meshgrid, height_centers_meshgrid, vel_centers_meshgrid, height_vel_centers_meshgrid, first_median_height_profile_above1500m, first_medianDBZ_profile_above1500m, first_Q1DBZ_profile_above1500m, first_Q3DBZ_profile_above1500m = CFAD(case_dict_1, height_bin_edges, dbz_bin_edges, vel_bin_edges, normalize = True)
    second_dbz_CFAD, second_vel_CFAD, dbz_centers_meshgrid, height_centers_meshgrid, vel_centers_meshgrid, height_vel_centers_meshgrid, second_median_height_profile_above1500m, second_medianDBZ_profile_above1500m, second_Q1DBZ_profile_above1500m, second_Q3DBZ_profile_above1500m = CFAD(case_dict_2, height_bin_edges, dbz_bin_edges, vel_bin_edges, normalize = True)
    
    #calculate the Ku-band and Doppler Velocity 2-D difference CFADs
    dbz_diff_CFAD = second_dbz_CFAD - first_dbz_CFAD
    vel_diff_CFAD = second_vel_CFAD - first_vel_CFAD
    
    #calculate the maximum magnitude for each CFAD and create contours for diverging colormaps accordingly
    
    #dbz_highest_mag = np.nanmax(np.abs(dbz_diff_CFAD))  #creates unique colorbar range for each difference CFAD plot
    dbz_highest_mag = 100  #creates uniform colorbar range across all difference CFAD plots
    dbz_contours = np.linspace(-dbz_highest_mag, dbz_highest_mag, 41)  #an odd number of intervals (21) guarantees a contour at 0 for a range from -x to x
    
    #vel_highest_mag = np.nanmax(np.abs(vel_diff_CFAD))  #creates unique colorbar range for each difference CFAD plot
    vel_highest_mag = 100  #creates uniform colorbar range across all difference CFAD plots
    vel_contours = np.linspace(-vel_highest_mag, vel_highest_mag, 41)  #an odd number of intervals (21) guarantees a contour at 0 for a range from -x to x
    
    #grab the case numbers of the 2 cases/case sets being differenced and create appropriate image names
    case1_num = ','.join(map(str, list(case_dict_1.keys())))
    case2_num = ','.join(map(str, list(case_dict_2.keys())))
    cases = case1_num + 'and' + case2_num
    colorbar_label = 'Differential Normalized Frequency [%]'
    dbz_save_label = 'diff_CFADnorm_Cases_' + cases + '_Ku.png'
    vel_save_label = 'diff_CFADnorm_Cases_' + cases + '_Vel.png'

    #plot the Ku-band and Doppler Velocity 2-D difference CFADs
    plot_diffCFAD(dbz_diff_CFAD, dbz_contours, colorbar_label, dbz_save_label, 'Ku-band Reflectivity [dBZ]', dbz_centers_meshgrid, height_centers_meshgrid, dbz_bin_edges, height_bin_edges, case1_num, case2_num, first_median_height_profile_above1500m, first_medianDBZ_profile_above1500m, first_Q1DBZ_profile_above1500m, first_Q3DBZ_profile_above1500m, second_median_height_profile_above1500m, second_medianDBZ_profile_above1500m, second_Q1DBZ_profile_above1500m, second_Q3DBZ_profile_above1500m, dbz_plot = True) 
    plot_diffCFAD(vel_diff_CFAD, vel_contours, colorbar_label, vel_save_label, 'Mean Doppler Velocity [m/s]', vel_centers_meshgrid, height_vel_centers_meshgrid, vel_bin_edges, height_bin_edges, case1_num, case2_num, first_median_height_profile_above1500m, first_medianDBZ_profile_above1500m, first_Q1DBZ_profile_above1500m, first_Q3DBZ_profile_above1500m, second_median_height_profile_above1500m, second_medianDBZ_profile_above1500m, second_Q1DBZ_profile_above1500m, second_Q3DBZ_profile_above1500m, dbz_plot = False)
  

#run the CFAD function to plot the CFADs
#CFAD(case_isolated_dict, height_edges, dbz_edges, vel_edges)

#comparing intensifying halves of Cases 13 and 16
#difference_CFAD(case13_intensify_dict, case16_intensify_dict, height_edges, dbz_edges, vel_edges)

#comparing mature/peaked halves of Cases 13 and 16
#difference_CFAD(case13_matureweak_dict, case16_matureweak_dict, height_edges, dbz_edges, vel_edges)

#difference_CFAD(case7_dict, case16_dict, height_edges, dbz_edges, vel_edges)    
#difference_CFAD(case7_dict, case14_dict, height_edges, dbz_edges, vel_edges)
difference_CFAD(case13_dict, case16_dict, height_edges, dbz_edges, vel_edges)  
    
    

