#This script converts dropsonde metric pressure values to their associated height values and 
#adds the height values to Dropsonde_Metric_Calculations.csv

import os
import sys
import pandas as pd
import numpy as np

sfc_heights = []
upper_lvl_cap_heights = []
PBL_heights = []
FZL_heights = []
dropsonde_filepath = os.path.join(os.getcwd(), 'Dropsonde_Metric_Calculations.csv')
dropsonde_df = pd.read_csv(dropsonde_filepath)

#loop through each dropsonde profile in the dropsonde metrics CSV and find its 'Sfc', PBL, FZL, and Upper Level Cap heights
for ip in range(len(dropsonde_df)):
    prof_day = str(dropsonde_df['Date'].iloc[ip])
    prof_time = str(dropsonde_df['Time'].iloc[ip])
    prof_sfc_pres = dropsonde_df['Sfc Pressure [mb]'].iloc[ip]
    prof_PBL_pres = dropsonde_df['PBL Top [mb]'].iloc[ip]
    prof_FZL_pres = dropsonde_df['Freezing Level [mb]'].iloc[ip]
    prof_upper_cap_pres = dropsonde_df['Upper Level Cap [mb]'].iloc[ip]
    
    #make a datetime string in the format that's in the final dropsonde CSVs (YYYY-mm-dd HH:MM:SS) and 
    #locate that datetime's dropsonde data in the final_dropsonde CSV
    prof_datetime = prof_day[:4] + '-' + prof_day[4:6] + '-' + prof_day[6:8] + ' ' + prof_time[:2] + ':' + prof_time[2:4] + ':' + prof_time[4:6]
    drop_csv_path = os.path.join(os.getcwd(), prof_day, 'final_dropsonde_' + prof_day + '.csv')
    drop_day_df = pd.read_csv(drop_csv_path)
    df_at_time = drop_day_df[drop_day_df['Time [UTC]'] == prof_datetime]
    heights = df_at_time['Height [m]']        #index of the data stays the same, but the integer positions are reset
    pressures = df_at_time['Pressure [mb]']   #index of the data stays the same, but the integer positions are reset
    
    #find height corresponding to the 'Sfc Pressure [mb]' in the dropsonde metrics CSV
    sfc_height_index = abs(pressures - prof_sfc_pres).idxmin()   #.idxmin() returns the index, NOT the integer position
    sfc_height = heights.loc[sfc_height_index]
    sfc_heights.append(sfc_height)
    
    #find height corresponding to the 'PBL Top [mb]' in the dropsonde metrics CSV
    PBL_height_index = abs(pressures - prof_PBL_pres).idxmin()   #.idxmin() returns the index, NOT the integer position
    PBL_height = heights.loc[PBL_height_index]
    PBL_heights.append(PBL_height)

    #find height corresponding to the 'Freezing Level [mb]' in the dropsonde metrics CSV
    FZL_height_index = abs(pressures - prof_FZL_pres).idxmin()   #.idxmin() returns the index, NOT the integer position
    FZL_height = heights.loc[FZL_height_index]
    FZL_heights.append(FZL_height)
    
    #find height corresponding to the 'Upper Level Cap [mb]' in the dropsonde metrics CSV
    cap_height_index = abs(pressures - prof_upper_cap_pres).idxmin()   #.idxmin() returns the index, NOT the integer position
    cap_height = heights.loc[cap_height_index]
    upper_lvl_cap_heights.append(cap_height)

#add the new sfc/upper level cap height fields to the dropsonde metrics CSV
dropsonde_df['Sfc Height [m]'] = sfc_heights
dropsonde_df['PBL Top Height [m]'] = PBL_heights
dropsonde_df['Freezing Level Height [m]'] = FZL_heights
dropsonde_df['Upper Level Cap Height [m]'] = upper_lvl_cap_heights
dropsonde_df.to_csv(dropsonde_filepath, index = False)


