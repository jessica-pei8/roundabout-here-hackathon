from data_processing.addingdata import dynamic_data
from data_processing.create_csv_with_threshold import create_csv_with_threshold
new_file = dynamic_data('/Users/markraskin/Downloads/data_chicago_hackathon_2024/probe_data/0/probe_2024_07_09_18_00_00.csv')
create_csv_with_threshold(new_file, 50, 9, 30)