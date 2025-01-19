import pandas as pd
import os

# Load cleaned datasets
tracks = pd.read_csv('cleaned_data/tracks_cleaned.csv')
artists = pd.read_csv('cleaned_data/artists_cleaned.csv')
chart_performance = pd.read_csv('cleaned_data/chart_performance_cleaned.csv')
audio_features = pd.read_csv('cleaned_data/audio_features_cleaned.csv')
mapping = pd.read_csv('cleaned_data/mapping_cleaned.csv')

# Ensure merged_data file exist
if not os.path.exists('merged_data'):
    os.makedirs('merged_data')

def merge_final_tracks():
    """Merge tracks, audio features, and artist mappings to create a cleaned track dataset."""
    # Merge tracks with audio features
    tracks_with_features = pd.merge(tracks, audio_features, on='track_id', how='left')
    tracks_with_artists = pd.merge(tracks_with_features, mapping, on='track_id', how='left')
    final_tracks = pd.merge(tracks_with_artists, artists, on='artist_id', how='left')

    # Drop rows with missing values in key audio columns
    final_tracks.dropna(subset=['key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'time_signature'], inplace=True)

    # Combine artist names for tracks with multiple artists
    final_tracks['artist_name'] = final_tracks.groupby('track_id')['artist_name'].transform(lambda x: ', '.join(x.dropna().astype(str).unique()))

    # Drop unnecessary columns
    columns_to_drop = ['artist_id', 'popularity', 'followers']
    final_tracks.drop(columns=columns_to_drop, errors='ignore', inplace=True)

    # Keep only unique track_id, retaining the first occurrence
    final_tracks.drop_duplicates(subset='track_id', keep='first', inplace=True)

    # Save to CSV
    final_tracks.to_csv('merged_data/final_tracks.csv', index=False)
    print("Final tracks merged and saved.")

    return final_tracks

def merge_final_artists():
    """Merge artists, mapping, and tracks to create a cleaned artist dataset."""
    artists_with_tracks = pd.merge(artists, mapping, on='artist_id', how='left')
    artists_tracks = pd.merge(artists_with_tracks, tracks, on='track_id', how='left')
    final_artists = pd.merge(artists_tracks, audio_features, on='track_id', how='left')

    # Drop unnecessary columns
    columns_to_drop = ['popularity', 'followers']
    final_artists.drop(columns=columns_to_drop, errors='ignore', inplace=True)

    # Save to CSV
    final_artists.to_csv('merged_data/final_artists.csv', index=False)
    print("Final artists merged and saved.")

    return final_artists

def merge_chart_tracks(final_tracks):
    """Merge chart performance with final tracks to create chart dataset."""
    chart_tracks = pd.merge(chart_performance, final_tracks, on='track_id', how='left')

    # Save to CSV
    chart_tracks.to_csv('merged_data/chart_tracks.csv', index=False)
    print("Chart tracks merged and saved.")

    return chart_tracks

if __name__ == "__main__":
    final_tracks = merge_final_tracks()
    final_artists = merge_final_artists()
    chart_tracks = merge_chart_tracks(final_tracks)
    
    print("All data merging tasks completed successfully.")

