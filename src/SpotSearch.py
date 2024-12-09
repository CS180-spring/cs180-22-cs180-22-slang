import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

cid = 'ce0010be0c7946a0b9f926585bc24c62'
secret = 'e0d800c29a704893b6ce87886e3b02b8'
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

def get_song_attributes(song_name):
    results = sp.search(q=song_name, type='track', limit=1)
    attributes_list = ["artist","album","track_name",  "track_id","danceability","energy","loudness", "speechiness","instrumentalness","liveness"]

    if results['tracks']['items']:
        track = results['tracks']['items'][0]
        song_features = {}
        #Get metadata
        song_features["artist"] = track["artists"][0]["name"]
        song_features["album"] = track["album"]["name"]
        song_features["track_name"] = track["name"]
        song_features["track_id"] = track["id"]
        song_id = track['id']

        audio_features = sp.audio_features(tracks=[song_id])[0]

        audio_features = sp.audio_features(song_features["track_id"])[0]
        for feature in attributes_list[4:]:
            song_features[feature] = audio_features[feature]
        
        #Combine all the dfs we made in each iteration
        song_df = pd.DataFrame(song_features, index = [0])

        return song_df
    
def get_artist_attributes(artist_name):
    results = sp.search(q=artist_name, type='artist', limit=1)
    attributes_list = ["artist","album","track_name",  "track_id","danceability","energy","loudness", "speechiness","instrumentalness","liveness"]
    artist_df = pd.DataFrame(columns = ["artist","album","track_name",  "track_id","danceability","energy","loudness", "speechiness","instrumentalness","liveness"])

    if results['artists']['items']:
        artist = results['artists']['items'][0]
        artist_id = artist['id']

        # Get the top tracks of the artist
        top_tracks = sp.artist_top_tracks(artist_id=artist_id)['tracks']

        for track in top_tracks:
            song_features = {}
            song_features["artist"] = track["artists"][0]["name"]
            song_features["album"] = track["album"]["name"]
            song_features["track_name"] = track["name"]
            song_features["track_id"] = track["id"]
            song_id = track['id']

            audio_features = sp.audio_features(tracks=[song_id])[0]

            audio_features = sp.audio_features(song_features["track_id"])[0]
            for feature in attributes_list[4:]:
                song_features[feature] = audio_features[feature]
            song_df = pd.DataFrame(song_features, index = [0])
            artist_df = pd.concat([artist_df, song_df], ignore_index = True)
        return artist_df
    
def get_album_attribtues(album_name):
    results = sp.search(q=album_name, type='album', limit=1)
    attributes_list = ["artist","album","track_name",  "track_id","danceability","energy","loudness", "speechiness","instrumentalness","liveness"]
    album_df = pd.DataFrame(columns = ["artist","album","track_name",  "track_id","danceability","energy","loudness", "speechiness","instrumentalness","liveness"])

    if results['albums']['items']:
        album = results['albums']['items'][0]
        album_id = album['id']

        # Get the tracks of the album
        tracks = sp.album_tracks(album_id=album_id)['items']
        for track in tracks:
            song_features = {}
            song_features["artist"] = track["artists"][0]["name"]
            song_features["album"] = album["name"]
            song_features["track_name"] = track["name"]
            song_features["track_id"] = track["id"]
            song_id = track['id']

            audio_features = sp.audio_features(tracks=[song_id])[0]

            audio_features = sp.audio_features(song_features["track_id"])[0]
            for feature in attributes_list[4:]:
                song_features[feature] = audio_features[feature]
            song_df = pd.DataFrame(song_features, index = [0])
            album_df = pd.concat([album_df, song_df], ignore_index = True)
        return album_df