from flask import Flask, jsonify, request
import os
import pandas as pd
from curl import roundAboutPerLocation, findAllRoundAbouts

app = Flask(__name__)



DATA_PATH = './data/probe_data/'

@app.route('/roundabout/<int:i>', methods=['GET'])
def estimate_roundabout(i):
    folder_path = os.path.join(DATA_PATH, str(i))

    if not os.path.exists(folder_path):
        return jsonify({"error": "Invalid folder path"}), 400

    data_frames = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv'):
            file_path = os.path.join(folder_path, file_name)
            df = pd.read_csv(file_path)
            data_frames.append(df)

    if not data_frames:
        return jsonify({"error": "No CSV files found in the folder"}), 400

    combined_data = pd.concat(data_frames, ignore_index=True)

    estimated_location = roundAboutPerLocation(combined_data)

    return jsonify({"estimated_location": estimated_location})

@app.route('/roundabouts', methods=['GET'])
def get_all_roundabouts():
    all_roundabouts = findAllRoundAbouts(DATA_PATH)
    return jsonify({"roundabouts": all_roundabouts})

if __name__ == '__main__':
    app.run(debug=True)
