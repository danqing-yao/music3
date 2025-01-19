
from google.auth import load_credentials_from_file
from google.cloud.bigquery import Client
import pandas as pd

# Set credentials
credentials, project_id = load_credentials_from_file('service_account.json')
client = Client(project = project_id, credentials=credentials)


def load_data(table):
    query = f"SELECT * FROM `da26-python.music_data.{table}`"
    load_job = client.query(query)
    return load_job.to_dataframe()

# Save the data to local files
if __name__ == "__main__":
    tables = ["audio_features", "tracks", "artists", "tracks_artists_mapping", "chart_positions"]
    for table in tables:
        df = load_data(table)
        df.to_csv(f"data/{table}.csv", index=False)
        print(f"{table} saved locally.")