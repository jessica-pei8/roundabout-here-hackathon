# from roundaboutdistancecalc import create_csv_with_threshold, haversine_vectorized
import pandas as pd



def dynamic_data(input_file):
    data = pd.read_csv(input_file)
    data['sampledate'] = pd.to_datetime(data['sampledate'])
    # Remove rows where heading is 0
    data = data[data['heading'] != 0]
    # Group by traceid and calculate the change in heading
    data['heading_change'] = data.groupby('traceid')['heading'].diff().fillna(0)
    # Optional: Normalize the change in heading to be within -180 to 180 degrees
    data['heading_change'] = data['heading_change'].apply(lambda x: (x + 180) % 360 - 180)

    data['speed_difference'] = data.groupby('traceid')['speed'].diff().fillna(0)
    
    output_file = '/Users/markraskin/Documents/GitHub/roundabout-here-hackathon/test_csvs/adding.csv'

    data.to_csv(output_file,index=False)
    print("New CSV file created successfully.")
    return output_file
    
# dynamic_data('/Users/markraskin/Downloads/data_chicago_hackathon_2024/probe_data/0/probe_2024_07_09_18_00_00.csv')