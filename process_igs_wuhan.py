#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 14:12:42 2022

@author: divya
"""

import argparse
import georinex as gr
import pandas as pd
import time
import numpy as np
import json
import process_sinex 
import obs

tic = time.time()
'''
parser = argparse.ArgumentParser()
parser.add_argument('-s', '--snx', default = 'No sinex file provided', dest = 'slantTD_file', help = 'Provide slant delay file', type= str)
parser.add_argument('-d', '--acqdate', default = 'No date provided', dest = 'acqdate', help = 'Provide date of acquisition', type= str)
args = parser.parse_args()
'''
acqdate='03012020'
acqloc='igs_wuhan'
slantTD_file = 'ABPO_SlantTD_2020003_0000_66241.SNX'

print("Processing Sinex file...")
slantTDs =  process_sinex.corrected_dataframe(slantTD_file)
satellites = slantTDs[4].unique()

#print(satellites)
for sat in satellites:
    #print(sat)
    satpos = process_sinex.get_satpos(sat, slantTDs)
    satpos.to_csv('Data/igs_wuhan/GPS_pos_{}_{}.txt'.format(sat,acqdate), header=None, index=None, sep=' ', mode='w')
    
    slant_wv = process_sinex.get_slantWV(sat,slantTDs)
    slant_wv.to_csv('Data/igs_wuhan/slant_wv_delay_mm_{}_{}.txt'.format(sat,acqdate), header=None, index=None, sep=' ', mode='w')
   
    
print("Generated GPS position files.")   
 
#write satellite details  - satno, time of first obs
satinfo = process_sinex.get_satellite_info(slantTDs)
satinfo_data = pd.DataFrame(list(zip(satinfo)),columns=['Satno Year Day Secs'])
satinfo_data.to_csv('Data/igs_wuhan/satellite_time_info_{}_{}.txt'.format(acqdate,acqloc),header=None, index=None, sep=' ')


print("Generated satelllite info file.")
print("Successfully processed Sinex file.")


print("\n Processing obs file...")
obs_file ='./Data/03012020/igs_wuhan/test.obs'

rinex_ver = "3.03"
obs_intvl = "sec"
device = "igs_wuhan"
acqdate = "03012022"


if rinex_ver == "2.11":
    band = ['L1','D1','L2','D2']
    rinex_3= False
if rinex_ver == "3.02":
    band = ['C1C','L1C','D1C','C2X','L2X','D2X']
    rinex_3 = True  
if rinex_ver == "3.04":
    band = ['C1C','L1C','D1C','C2W','L2W','D2W']
    rinex_3 = True
if rinex_ver == "3.03": #G   14 C1C L1C S1C C1W S1W C2W L2W S2W C2L L2L S2L C5Q L5Q
    band = ['C1C','L1C','S1C','C2L','L2L','S2L']
    rinex_3 = True

observs = gr.load(obs_file)
observs_hdr = gr.obsheader3(obs_file)

svlist_obs = obs.extract_gps(observs)
svlist_obs.sort()
svlist_obs_temp = svlist_obs
svlist_obs_temp = np.asarray(svlist_obs_temp)
total_obs = []
for i in svlist_obs:
    for bandindx in (0,3):
        phase_l1c,time_l1c,time_interval_phase = obs.extract_doppler_and_time(i,band[bandindx+1],observs,rinex_3,obs_intvl)
        doppler_d1c,time_d1c,time_interval_doppler = obs.extract_doppler_and_time(i,band[bandindx+2],observs,rinex_3,obs_intvl)
        pseudorange,time_pseudo_range,time_interval_pseudorange = obs.extract_doppler_and_time(i,band[bandindx],observs,rinex_3,obs_intvl)
    
        total = len(phase_l1c)
        total_obs.append(total)
        
        phase_data = pd.DataFrame(list(zip(time_l1c,phase_l1c,time_interval_phase)),columns=['Epoch','Carrier_Phase','Time_interval (ms)'])
        doppler_data = pd.DataFrame(list(zip(time_d1c,doppler_d1c,time_interval_doppler)),columns=['Epoch','Doppler','Time_interval (ms)'])
        pseudorange_data = pd.DataFrame(list(zip(time_pseudo_range,pseudorange,time_interval_pseudorange)),columns=['Epoch','Pseudorange','Time_interval (ms)'])
   
        if device=='igs_wuhan':
            phase_data.to_csv('Data/igs_wuhan/carrier_phase_{}_{}_{}.txt'.format(i,acqdate,band[bandindx+1]), header=None, index=None, sep=' ', mode='w')
            doppler_data.to_csv('Data/igs_wuhan/doppler_{}_{}_{}.txt'.format(i,acqdate,band[bandindx+2]), header=None, index=None, sep=' ', mode='w')
            pseudorange_data.to_csv('Data/igs_wuhan/pseudo_range_{}_{}_{}.txt'.format(i,acqdate,band[bandindx]), header=None, index=None, sep=' ', mode='w')

print("\n Successfully processed obs file.")