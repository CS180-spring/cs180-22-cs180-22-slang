import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from sklearn.cluster import KMeans
from sklearn import preprocessing
import pandas as pd
from numba import njit,jit,prange
import os
import search
import kmeans
import recommend


cid = 'ce0010be0c7946a0b9f926585bc24c62'
secret = 'e0d800c29a704893b6ce87886e3b02b8'
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
@jit(nopython=True)

def extract_playlist_id_from_url(url):
    playlist_id = url.split('/')[-1]
    return playlist_id

def make_playlist_df1(creator, playlist_id):
    
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
    return recs


def getPlaylistFromUser():
    user_spotify_id = 'zeldran05'  # Replace with the user's Spotify ID
    playlists = sp.user_playlists(user_spotify_id, limit=50)

    for i, playlist in enumerate(playlists['items']):
        print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'],  playlist['name']))
    return playlists['items']
    


library_df = pd.read_csv("/Users/riyapatel/github-classroom/CS180-spring/cs180-22-slang/library/library.csv")


print("1. Make a new playlist")
print("2. Edit an existing playlist")
print("3. Import a playlist")
print("4. Merge two playlists")
print("5. Get recommendations for a playlist")
print("6. Print Spotify playlists")
print("7. Quit")
inp1 = input("Which would you like to do? ")

while inp1 != "7":

    if inp1 == "1":
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

    elif inp1 == "2":
        inp2 = input("Please enter the name of the playlist you want to edit: ")
        playlist_loc = "../output/" + inp2 + ".csv"
        playlist_df = pd.read_csv(playlist_loc)
        print("1. Add song")
        print("2. Remove song")
        inp3 = input("What do you want to do? ")
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

    elif inp1 == "3":
        playlistLink = input("Please enter link to playlist: ")
        id = extract_playlist_id_from_url(playlistLink)
        playlistName = input("Please name your imported playlist: ")

        df = make_playlist_df1("spotify", id)
        csvName = "../output/" + playlistName + ".csv"
        df.to_csv(csvName, index = False)

    elif inp1 == "4":
        playlist1 = input("Please enter the first playlist's name: ")
        playlist2 = input("Please enter the second playlist's name: ")
        mergedName = input("Please name your new merged playlist: ")

        playlist1_loc = "../output/" + playlist1 + ".csv"
        playlist2_loc = "../output/" + playlist2 + ".csv"
        merged_loc = "../output/" + mergedName + ".csv"
        playlist_df1 = pd.read_csv(playlist1_loc)
        playlist_df2 = pd.read_csv(playlist2_loc)

        combinedPlaylist_df = runKmeans(playlist_df1, playlist_df2)
        combinedPlaylist_df.to_csv(merged_loc)

    elif inp1 == "5":
        rec_playlist = input("Enter the name of the playlist you want songs recommended for: ")
        playlist_loc = "../output/" + rec_playlist + ".csv"
        playlist_df = pd.read_csv(playlist_loc)
        recommended_songs = runRecommend(playlist_df, library_df)
        playlist_df = pd.concat([playlist_df, recommended_songs], ignore_index=True)
        playlist_df.to_csv(playlist_loc, index=False)

    elif inp1 == "6":
        getPlaylistFromUser()
            

    elif inp1 not in ["1", "2", "3", "4", "5", "6", "7"]: 
        print("Not a valid selection")

    print("1. Make a new playlist")
    print("2. Edit an existing playlist")
    print("3. Import a playlist")
    print("4. Merge two playlists")
    print("5. Get recommendations for a playlist")
    print("6. Print Spotify playlists")
    print("7. Quit")
    inp1 = input("Which do you want to do? ")