import pandas as pd
import ast


df = pd.read_csv("../library/tracks_features.csv")


df['artists'] = df['artists'].apply(ast.literal_eval)


df['artist'] = df['artists'].apply(lambda x: x[0] if x else "")


new_columns = ['artist', 'album', 'name', 'id', 'danceability', 'energy', 'loudness', 'speechiness', 'instrumentalness', 'liveness']


df = df[new_columns]

df.columns = ['artist', 'album', 'track_name', 'track_id', 'danceability', 'energy', 'loudness', 'speechiness', 'instrumentalness', 'liveness']

df.to_csv("../library/new_library.csv", index=False)
