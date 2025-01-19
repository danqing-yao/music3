import pandas as pd
import os

# Ensure cleaned_data directory exists
if not os.path.exists('cleaned_data'):
    os.makedirs('cleaned_data')

# Load datasets
tracks = pd.read_csv('data/tracks.csv')
artists = pd.read_csv('data/artists.csv')
chart_performance = pd.read_csv('data/chart_positions.csv')
audio_features = pd.read_csv('data/audio_features.csv')
mapping = pd.read_csv('data/tracks_artists_mapping.csv')

# Data cleaning functions
def clean_tracks(data):
    # Clean tracks dataset by removing duplicates, extracting year and renaming columns. 
    data.drop_duplicates(inplace=True)
    data['release_date'] = pd.to_datetime(data['release_date'], errors='coerce')
    data['release_year'] = data['release_date'].dt.year
    data.rename(columns={'name': 'track_name'}, inplace=True)
    data.to_csv('cleaned_data/tracks_cleaned.csv', index=False)
    print("Tracks cleaned and saved.")

def clean_artists(data):
    # Clean artists dataset by renaming and removing duplicate artists based on highest followers. 
    data.rename(columns={'name': 'artist_name'}, inplace=True)
    data.sort_values(by=['artist_name', 'followers'], ascending=[True, False], inplace=True)
    data.drop_duplicates(subset=['artist_name'], keep='first', inplace=True)
    data.to_csv('cleaned_data/artists_cleaned.csv', index=False)
    print("Artists cleaned and saved.")

def clean_chart_performance(data):
    # Clean chart performance dataset by extracting year and quarter. 
    data['chart_week'] = pd.to_datetime(data['chart_week'], errors='coerce')
    data['chart_year'] = data['chart_week'].dt.year
    data['quarter'] = data['chart_week'].dt.quarter
    data.to_csv('cleaned_data/chart_performance_cleaned.csv', index=False)
    print("Chart performance cleaned and saved.")

def clean_audio_features(data):
    # Clean audio features dataset by dropping null values. 
    data.dropna(inplace=True)
    data.to_csv('cleaned_data/audio_features_cleaned.csv', index=False)
    print("Audio features cleaned and saved.")

def clean_mapping(data):
    # Clean mapping dataset by removing duplicates. 
    data.drop_duplicates(inplace=True)
    data.to_csv('cleaned_data/mapping_cleaned.csv', index=False)
    print("Mapping cleaned and saved.")

if __name__ == "__main__":
    clean_tracks(tracks)
    clean_artists(artists)
    clean_chart_performance(chart_performance)
    clean_audio_features(audio_features)
    clean_mapping(mapping)
    print("Data cleaning completed successfully.")