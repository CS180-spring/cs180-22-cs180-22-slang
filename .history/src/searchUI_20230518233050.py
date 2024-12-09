import numpy
import pandas as pd

library_df = pd.read_csv("../library/big_library.csv",low_memory=False)
pd.set_option('display.max_rows', 5000)

def searchbyTitle(library_df, titleSearch):
library_df = pd.read_csv("/Users/riyapatel/github-classroom/CS180-spring/cs180-22-slang/library/big_library.csv", low_memory=False)

    if not songResult.empty:
        print("Related Songs:")
        print(songResult[["artist", "album", "track_name", "track_id", "danceability", "energy", "loudness", "speechiness", "instrumentalness", "liveness"]]) 
        songs = songResult[["track_name"]].to_numpy()
        csvName = "../output/" + "cacheSearch" + ".csv"
        songResult.to_csv(csvName, index = False)
    else:
        print("No matching songs found")

def searchbyArtist(library_df, artistSearch):
    artistResult = library_df.loc[library_df['artist'].fillna('').str.contains(artistSearch, case=False)]
    if not artistResult.empty:
        artists = artistResult[["artist"]].drop_duplicates().to_numpy()
        csvName = "../output/" + "cacheSearch" + ".csv"
        artistResult.to_csv(csvName, index = False)

    else: 
        print("No matching artists found")          

