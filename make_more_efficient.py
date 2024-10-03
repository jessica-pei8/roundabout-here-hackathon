import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.interpolate import griddata

def haversine_vectorized(lat1, lon1, lat2, lon2):
    
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    r = 6371000  
    return r * c 

def create_df_with_threshold(data, round_lat, round_long, radius):
    distances = haversine_vectorized(
        data['latitude'].values,
        data['longitude'].values,
        round_lat,
        round_long
    )
    data.loc[:, 'within_radius'] = distances <= radius

    filtered_data = data[data['within_radius'] == True]

    print("Filtered DataFrame created successfully.")
    return filtered_data


def optimize(lat,long, data_frame, radius):
    data = create_df_with_threshold(data_frame,lat,long,radius)
    data['heading_rad'] = np.radians(data['heading'])
    data['vx'] = np.cos(data['heading_rad'])  
    data['vy'] = np.sin(data['heading_rad']) 

    grid_lon = np.linspace(data['longitude'].min(), data['longitude'].max(), 500)
    grid_lat = np.linspace(data['latitude'].min(), data['latitude'].max(), 500)
    grid_lon, grid_lat = np.meshgrid(grid_lon, grid_lat)

    grid_vx = griddata((data['longitude'], data['latitude']), data['vx'], (grid_lon, grid_lat), method='linear')
    grid_vy = griddata((data['longitude'], data['latitude']), data['vy'], (grid_lon, grid_lat), method='linear')

    curl = np.gradient(grid_vy, axis=0) - np.gradient(grid_vx, axis=1)

    curl = np.gradient(grid_vy, axis=0) - np.gradient(grid_vx, axis=1)

    max_curl = np.nanmax(curl) 
    print("Maximum Curl Value:", max_curl)

    threshold =  0.9* max_curl 

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

    print( average_lat, average_lon)