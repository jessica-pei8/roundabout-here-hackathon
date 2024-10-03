from typing import List
import pandas as pd
import numpy as np
import os
from scipy.interpolate import griddata
from make_more_efficient import *


def roundAboutPerLocation(data:pd.DataFrame)->tuple[float, float]:
    data = data[(data['speed'] >= 25) & (data['speed'] <= 45)]
    data['heading_rad'] = np.radians(data['heading'])
    data['vx'] = np.cos(data['heading_rad'])  
    data['vy'] = np.sin(data['heading_rad'])
    grid_lon = np.linspace(data['longitude'].min(), data['longitude'].max(), 100)
    grid_lat = np.linspace(data['latitude'].min(), data['latitude'].max(), 100)
    grid_lon, grid_lat = np.meshgrid(grid_lon, grid_lat)
    grid_vx = griddata((data['longitude'], data['latitude']), data['vx'], (grid_lon, grid_lat), method='linear')
    grid_vy = griddata((data['longitude'], data['latitude']), data['vy'], (grid_lon, grid_lat), method='linear')

    curl = np.gradient(grid_vy, axis=0) - np.gradient(grid_vx, axis=1)
    max_curl = np.nanmax(curl) 
    print("Maximum Curl Value:", max_curl)
    threshold =  0.9 * max_curl 
    near_max_curl_indices = np.argwhere(curl >= threshold)

    near_max_curl_points = []
    for idx in near_max_curl_indices:
        lon_idx, lat_idx = idx[1], idx[0]  
        lon = grid_lon[lon_idx][lat_idx]
        lat = grid_lat[lon_idx][lat_idx]
        near_max_curl_points.append((lat,lon))

    near_max_curl_df = pd.DataFrame(near_max_curl_points, columns=['Latitude',''])
    near_max_curl_df = pd.DataFrame(near_max_curl_points, columns=['Latitude','Longitude'])

    average_lat = near_max_curl_df['Latitude'].mean()
    average_lon = near_max_curl_df['Longitude'].mean()
    return (average_lat, average_lon)



def findAllRoundAbouts(datapath:str)-> List[tuple[float, float]]:
    allRoundabouts = []
    for i in range(0,15):
        folder_path = datapath + str(i)

        data_frames = []
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            df = pd.read_csv(file_path)
            data_frames.append(df)

        data = pd.concat(data_frames, ignore_index=True)
        allRoundabouts.append(roundAboutPerLocation(data))
    return allRoundabouts