import pandas as pd



def dynamic_data(input_file):
    data = pd.read_csv(input_file)
    data['sampledate'] = pd.to_datetime(data['sampledate'])
    data = data[data['heading'] != 0]
    data['heading_change'] = data.groupby('traceid')['heading'].diff().fillna(0)
    data['heading_change'] = data['heading_change'].apply(lambda x: (x + 180) % 360 - 180)

    data['speed_difference'] = data.groupby('traceid')['speed'].diff().fillna(0)
    
    output_file = '/Users/markraskin/Documents/GitHub/roundabout-here-hackathon/test_csvs/adding.csv'

    data.to_csv(output_file,index=False)
    print("New CSV file created successfully.")
    return output_file
    
