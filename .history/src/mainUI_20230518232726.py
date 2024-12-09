import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from sklearn.cluster import KMeans
from sklearn import preprocessing
import pandas as pd
from numba import njit,jit,prange
import search
import recommend
import os


cid = 'ce0010be0c7946a0b9f926585bc24c62'
secret = 'e0d800c29a704893b6ce87886e3b02b8'
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
@jit(nopython=True)

def extract_playlist_id_from_url(url):

    url_parts = url.split('/')

    last_part = url_parts[-1]

    playlist_id = last_part.split('?')[0]
    return playlist_id

def make_playlist_df1(creator, playlist_id):
    
    #Making empy dataframe
    attributes_list = ["artist","album","track_name",  "track_id","danceability","energy","loudness", "speechiness","instrumentalness","liveness"]
    playlist_df = pd.DataFrame(columns = ["artist","album","track_name",  "track_id","danceability","energy","loudness", "speechiness","instrumentalness","liveness"])
    
    #Loop through playlist
    playlist = sp.user_playlist_tracks(creator, playlist_id)["items"]

    total_tracks = sp.user_playlist_tracks(creator, playlist_id, limit=1)['total']

    for i in range(0, total_tracks, 100):
        playlist = sp.user_playlist_tracks(creator, playlist_id, offset=i, limit=100)["items"]
        
        for song in playlist:
            song_features = {}
            #Get metadata
            song_features["artist"] = song["track"]["album"]["artists"][0]["name"]
            song_features["album"] = song["track"]["album"]["name"]
            song_features["track_name"] = song["track"]["name"]
            song_features["track_id"] = song["track"]["id"]
            
            #Get audio features
            audio_features = sp.audio_features(song_features["track_id"])[0]
            for feature in attributes_list[4:]:
                song_features[feature] = audio_features[feature]
            
            #Combine all the dfs we made in each iteration
            song_df = pd.DataFrame(song_features, index = [0])
            playlist_df = pd.concat([playlist_df, song_df], ignore_index = True)
            
    return playlist_df

def make_playlist_df2(creator, playlist_id):
    
    #Making empy dataframe
    attributes_list = ["artist","album","track_name",  "track_id","danceability","energy","loudness", "speechiness","instrumentalness","liveness"]
    playlist_df = pd.DataFrame(columns = ["artist","album","track_name",  "track_id","danceability","energy","loudness", "speechiness","instrumentalness","liveness"])
    
    #Loop through playlist
    playlist = sp.user_playlist_tracks(creator, playlist_id)["items"]
    for song in playlist:
        song_features = {}
        #Get metadata
        song_features["artist"] = song["track"]["album"]["artists"][0]["name"]
        song_features["album"] = song["track"]["album"]["name"]
        song_features["track_name"] = song["track"]["name"]
        song_features["track_id"] = song["track"]["id"]
        
        #Get audio features
        audio_features = sp.audio_features(song_features["track_id"])[0]
        for feature in attributes_list[4:]:
            song_features[feature] = audio_features[feature]
        
        #Combine all the dfs we made in each iteration
        song_df = pd.DataFrame(song_features, index = [0])
        playlist_df = pd.concat([playlist_df, song_df], ignore_index = True)
        
    return playlist_df

def runKmeans(input_df, input_df2):
    combined_df = pd.concat([input_df, input_df2], ignore_index= True)

    #removing duplicates
    combined_df = combined_df.drop_duplicates(subset = ['track_id'], keep = 'first')
    #normalizing values
    x = combined_df.iloc[:, 4:].values 
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(x)
    scaled_df = pd.DataFrame(x_scaled)

    kmeans = KMeans(init="k-means++", n_clusters=3, random_state=15, max_iter = 100).fit(x_scaled)
    scaled_df['cluster number'] = kmeans.labels_
    scaled_df.columns = ['danceability', 'energy', 'loudness', 'speechiness', 'instrumentalness', 'liveness', 'cluster number']
    cluster_df = scaled_df.iloc[:, -1:]
    return_df = pd.concat([combined_df, cluster_df], axis=1, join='inner')
    return return_df

def runRecommend(input_df, lib_df):
    recs = recommend.recommend(input_df, lib_df)
    recs.to_csv("../output/recommendations.csv", index = False)
    print("Here are your recommendations: ")
    print(recs)
    return recs


library_df = pd.read_csv("/Users/riyapatel/github-classroom/CS180-spring/cs180-22-slang/library/library.csv")


def namePlaylist():
    newPlaylistName = input("Please name your playlist: ")
    newPlaylist_loc = "../output/" + newPlaylistName + ".csv"
    temp_song = search.search(library_df)
    playlist = temp_song
    inp3 = input("Keep adding songs? Y/N: ")
    while inp3 == "Y":
        new_temp_song = search.search(library_df)
        playlist = pd.concat([playlist, new_temp_song], ignore_index= True)
        inp3 = input("Keep adding songs? Y/N: ")
    playlist.to_csv(newPlaylist_loc, index = False)

def editPlaylist():
    inp2 = input("Please enter the name of the playlist you want to edit: ")
    playlist_loc = "../output/" + inp2 + ".csv"
    playlist_df = pd.read_csv(playlist_loc)
    print("1. Add song")
    print("2. Remove song")
    inp3 = input("What do you wanna do? ")
    if inp3 == "1":
        temp_song = search.search(library_df)
        playlist_df = pd.concat([playlist_df, temp_song], ignore_index=True)
        inp4 = input("Keep adding songs? Y/N: ")
        while inp4 == "Y":
            new_temp_song = search.search(library_df)
            playlist_df = pd.concat([playlist_df, new_temp_song], ignore_index= True)
            inp4 = input("Keep adding songs? Y/N: ")
        playlist_df.to_csv(playlist_loc, index = False)
    elif inp3 == "2":
        inp4 = input("Enter the name of the song you want to remove: ")
        temp_song = playlist_df.loc[playlist_df["track_name"] == inp4]
        drop_index = temp_song.index
        playlist_df = playlist_df.drop(drop_index)
        playlist_df.to_csv(playlist_loc, index = False)

def importSpotifyPlaylist(playlistLink, playlistName):
    id = extract_playlist_id_from_url(playlistLink)
    df = make_playlist_df1("spotify", id)
    csvName = "../output/" + playlistName + ".csv"
    df.to_csv(csvName, index = False)

def mergePlaylists():
    playlist1 = "Playlist"
    playlist2 = "Playlist2"
    mergedName = "MergedPlaylist"

    playlist1_loc = "../output/" + playlist1 + ".csv"
    playlist2_loc = "../output/" + playlist2 + ".csv"
    merged_loc = "../output/" + mergedName + ".csv"
    playlist_df1 = pd.read_csv(playlist1_loc)
    playlist_df2 = pd.read_csv(playlist2_loc)
    combinedPlaylist_df = runKmeans(playlist_df1, playlist_df2)
    
    cluster_1 = combinedPlaylist_df.loc[combinedPlaylist_df["cluster number"] == 1]
    cluster_1 = cluster_1.drop(["cluster number"], axis = 1)
    cluster_1.to_csv(merged_loc, index = False)

def runRecommend(input_df, lib_df):
    recs = recommend.recommend(input_df, lib_df)
    recs.to_csv("../output/recommendations.csv", index = False)
    return recs

def getRecommendations():
    playlist_loc = "../output/" + "MergedPlaylist.csv"
    playlist_df = pd.read_csv(playlist_loc)
    recommended_songs = runRecommend(playlist_df, library_df)
    playlist_df = pd.concat([playlist_df, recommended_songs], ignore_index=True)
    playlist_df.to_csv(playlist_loc, index=False)

def getPlaylistFromUser():
    user_spotify_id = 'zeldran05'  # Replace with the user's Spotify ID
    playlists = sp.user_playlists(user_spotify_id, limit=50)
    print(playlists['items'])
    # for i, playlist in enumerate(playlists['items']):
    #     print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'],  playlist['name']))
    return playlists['items']
    