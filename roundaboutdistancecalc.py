import pandas as pd
import numpy as np

def haversine_vectorized(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    r = 6371000  # Radius of Earth in meters
    return r * c  # Distance in meters

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

    output_data = []
    for index, row in data_every_other.iterrows():
        is_within = within_radius[index // 2] 
        description = (f'There is a car at coordinates {row["latitude"]}, {row["longitude"]}, '
                       f'going speed {row["speed"]} and heading {row["heading"]}.') 
        output_data.append([description, is_within])
    output_df = pd.DataFrame(output_data, columns=["Description", "Within_Radius"])
    output_df.to_csv('/Users/markraskin/Documents/GitHub/roundabout-here-hackathon/output.csv', index=False)
    
    print("New CSV file created successfully.")


create_csv_with_threshold('/Users/markraskin/Downloads/data_chicago_hackathon_2024/probe_data/0/probe_2024_07_09_18_00_00.csv', 53.54964508900254, 9.96012198516086, 30)
