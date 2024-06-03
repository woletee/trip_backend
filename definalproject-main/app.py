from flask import Flask, jsonify, request
import pandas as pd
from sklearn.cluster import KMeans
import numpy as np
from flask_cors import CORS
import logging

app = Flask(__name__)
CORS(app)  # Enable CORS

logging.basicConfig(level=logging.INFO)

def convert_to_float(value):
    try:
        return float(value)
    except ValueError:
        return None

# Load data from CSV
logging.info("Loading data from CSV...")
df = pd.read_csv("dataset.csv")

# Filter out rows with missing longitude, latitude, rankingPosition, or image values
logging.info("Filtering out rows with missing coordinates...")
filtered_df = df.dropna(subset=['longitude', 'latitude', 'rankingPosition', 'image'])

# Sort by rankingPosition
logging.info("Sorting by ranking position...")
top = filtered_df.sort_values(by=['rankingPosition'], ascending=True)

# Extract coordinates
logging.info("Extracting coordinates...")
coords = top[['longitude', 'latitude']]

# Fit KMeans with k=3
logging.info("Fitting KMeans model...")
kmeans = KMeans(n_clusters=3, init='k-means++')
kmeans.fit(coords)

# Add cluster labels to the DataFrame
top['cluster'] = kmeans.labels_
logging.info("Data preparation completed.")

def recommend_restaurants(top, longitude, latitude):
    cluster = kmeans.predict(np.array([longitude, latitude]).reshape(1, -1))[0]
    logging.info(f"Predicted cluster: {cluster}")
    cluster_df = top[top['cluster'] == cluster].iloc[:5, [12, 7, 9, 18, 6]]
    return cluster_df

@app.route('/')
def index():
    return "Welcome to the restaurant recommendation API. Use /api/clusters to get cluster information or /api/recommend to get restaurant recommendations."

@app.route('/api/clusters')
def get_clusters():
    logging.info("Preparing clusters data...")
    clusters_data = top[['name', 'rankingPosition', 'address', 'image']]

    logging.info("Converting clusters data to list of dictionaries...")
    clusters_list = clusters_data.to_dict(orient='records')

    logging.info("Clusters data processing completed.")
    return jsonify({'clusters': clusters_list})

@app.route('/api/recommend')
def recommend():
    longitude_str = request.args.get('longitude')
    latitude_str = request.args.get('latitude')

    # Convert longitude and latitude strings to floats
    longitude = convert_to_float(longitude_str)
    latitude = convert_to_float(latitude_str)

    if longitude is not None and latitude is not None:
        recommended_restaurants = recommend_restaurants(top, longitude, latitude)
        return jsonify({'recommended_restaurants': recommended_restaurants.to_dict(orient='records')})
    else:
        return jsonify({'error': 'Invalid longitude or latitude value.'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
