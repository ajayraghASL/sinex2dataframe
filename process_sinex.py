#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 18 11:09:58 2022

@author: Divya
"""

import numpy as np
import pandas as pd

def corrected_dataframe(slantTD_file):
    with open(slantTD_file,'r') as f:
        lines = f.readlines()

    # separating headings and rows
    heading = lines[0]
    row1 = heading[274:]
    row1 = row1.replace(' ', ',')
    row1_trimmed = row1[:len(row1)-1]
    listed_row1 = row1_trimmed.split(',')
    data = []
    data.append(listed_row1)
    for i in range (1,len(lines)):
        line = lines[i]
        line = line.replace(' ',',')
        trimmed_line = line[:len(line)-1]
        listed_line = trimmed_line.split(',')
        data.append(listed_line)

    #creating indices for dataframe
    indices = []
    for i in range (len(data)):
        indices.append(i)

    dataframe = pd.DataFrame(data,index = indices)
    return dataframe
    

        






def get_satpos(satno, slantTDs):
    satpos = slantTDs.loc[slantTDs[4] == satno]
    satpos_xyz= satpos[:][[5,6,7]]*1000
   # print(satpos_xyz)
    return satpos_xyz

def get_satellite_info(slantTDs):
    satellites = slantTDs[4].unique()
    sat_info =[];
    for satno in satellites:
        sat_details = slantTDs.loc[slantTDs[4] == satno]
        start_acq_time = sat_details.iloc[0][0:3] # Year,day, secs.
        sat_info.append([satno,start_acq_time[0],start_acq_time[1],start_acq_time[2]])
    return sat_info

def get_slantWV(satno,slantTDs):
    slant_wv = slantTDs.loc[slantTDs[4] == satno]
    satpos_wv_delay= slant_wv[:][[3]] 
    return satpos_wv_delay
'''
def main( ):
    acqdate='03012020'
    slantTD_file = './Data/03012020/igs_wuhan/ABPO_SlantTD_2020003_0000_66241.SNX'
    slantTDs =  pd. read_csv(slantTD_file, sep=" ",header = None,skiprows=1)
    satellites = slantTDs[4].unique()
    #print(satellites)
    for sat in satellites:
        #print(sat)
        satpos = get_satpos(sat, slantTD_file)
        satpos.to_csv('Data/igs_wuhan/GPS_pos_{}_{}.txt'.format(sat,acqdate), header=None, index=None, sep=' ', mode='w')

    

    get_satellite_info(slantTD_file)
    return


main()


'''