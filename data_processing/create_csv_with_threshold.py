import pandas as pd
import numpy as np

def haversine_vectorized(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    r = 6371000  
    return r * c 

def create_csv_with_threshold(input_file, round_lat, round_long, radius=30):
    data = pd.read_csv(input_file)
    data_every_other = data.iloc[::2]
    distances = haversine_vectorized(
        data_every_other['latitude'].values,
        data_every_other['longitude'].values,
        round_lat,
        round_long
    )
    within_radius = distances <= radius

    data_every_other['within_radius'] = within_radius
    data_every_other.drop(columns=data_every_other.columns[0], axis=1, inplace=True) 
       
    output_file = '/Users/markraskin/Documents/GitHub/roundabout-here-hackathon/test_csvs/output.csv'

    data_every_other.to_csv(output_file, index=False)
    print("New CSV file created successfully.")

