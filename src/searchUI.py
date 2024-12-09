import numpy
import pandas as pd
import SpotSearch

import itertools
from rich.progress import Progress
import time


pd.set_option('display.max_rows', 5000)

def searchbyTitle(library_df, titleSearch):
    songResult = library_df.loc[library_df['track_name'].fillna('').str.contains(titleSearch, case=False)]

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


def advanced_search(library_df, library_loc, songTitle, artist, album, songID, danceability, energy, loudness, speechiness, instrumentalness, liveness):
  
    default_field_names = ["Song Title", "Artist", "Album", "Title ID", "Danceability", "Energy", "Loudness", "Speechiness", "Instrumentalness", "Liveness"]
    inputs = [songTitle, artist, album, songID, danceability, energy, loudness, speechiness, instrumentalness, liveness]
    inputs = ['' if value in default_field_names else value for value in inputs]
    songTitle, artist, album, songID, danceability, energy, loudness, speechiness, instrumentalness, liveness = inputs


    # quicker search if only one search field is filled in
    inputs = [songTitle, artist, album, songID, danceability, energy, loudness, speechiness, instrumentalness, liveness]
    if check_only_one_string(inputs):
        if songTitle:
            spotifySongSearch = SpotSearch.get_song_attributes(songTitle)
            library_df = pd.concat([library_df, spotifySongSearch], ignore_index = False)
            library_df = library_df.drop_duplicates().reset_index(drop=True)
            library_df.to_csv(library_loc, index = False)
            results = searchBySongTitle(library_df, songTitle)
        elif artist:
            spotifyArtistSearch = SpotSearch.get_artist_attributes(artist)
            library_df = pd.concat([library_df, spotifyArtistSearch], ignore_index = False)
            library_df = library_df.drop_duplicates().reset_index(drop=True)
            library_df.to_csv(library_loc, index = False)
            results = searchByArtist(library_df, artist)
        elif album:
            spotifyAlbumSearch = SpotSearch.get_album_attribtues(album)
            library_df = pd.concat([library_df, spotifyAlbumSearch], ignore_index = False)
            library_df = library_df.drop_duplicates().reset_index(drop=True)
            library_df.to_csv(library_loc, index = False)
            results = searchByAlbum(library_df, album)
        elif songID:
            results = searchBySongID(library_df, songID)
        elif danceability:
            results = searchByDanceability(library_df, danceability)
        elif energy:
            results = searchByEnergy(library_df, energy)
        elif loudness:
            results = searchByLoudness(library_df, loudness)
        elif speechiness:
            results = searchBySpeechiness(library_df, speechiness)
        elif instrumentalness:
            results = searchByInstrumentalness(library_df, instrumentalness)
        elif liveness:
            results = searchByLiveness(library_df, liveness)
        
        # print(results[["track_name", "artist", "album"]].head(20))
        results = results.head(20) # print only top 20 results
    
    # slower search for 2+ search fields
    else:
        songTitleResult = pd.DataFrame(columns = ["artist","album","track_name",  "track_id","danceability","energy","loudness", "speechiness","instrumentalness","liveness"])
        artistResult = pd.DataFrame(columns = ["artist","album","track_name",  "track_id","danceability","energy","loudness", "speechiness","instrumentalness","liveness"])
        albumResult = pd.DataFrame(columns = ["artist","album","track_name",  "track_id","danceability","energy","loudness", "speechiness","instrumentalness","liveness"])
        songIDResult = pd.DataFrame(columns = ["artist","album","track_name",  "track_id","danceability","energy","loudness", "speechiness","instrumentalness","liveness"])
        danceabilityResult = pd.DataFrame(columns = ["artist","album","track_name",  "track_id","danceability","energy","loudness", "speechiness","instrumentalness","liveness"])
        energyResult = pd.DataFrame(columns = ["artist","album","track_name",  "track_id","danceability","energy","loudness", "speechiness","instrumentalness","liveness"])
        loudnessResult = pd.DataFrame(columns = ["artist","album","track_name",  "track_id","danceability","energy","loudness", "speechiness","instrumentalness","liveness"])
        speechinessResult = pd.DataFrame(columns = ["artist","album","track_name",  "track_id","danceability","energy","loudness", "speechiness","instrumentalness","liveness"])
        instrumentalnessResult = pd.DataFrame(columns = ["artist","album","track_name",  "track_id","danceability","energy","loudness", "speechiness","instrumentalness","liveness"])
        livenessResult = pd.DataFrame(columns = ["artist","album","track_name",  "track_id","danceability","energy","loudness", "speechiness","instrumentalness","liveness"])

        with Progress() as progress:
            task = progress.add_task("[green]Searching...", total=11)

            if songTitle != '':
                spotifySongSearch = SpotSearch.get_song_attributes(songTitle)
                library_df = pd.concat([library_df, spotifySongSearch], ignore_index = False)
                library_df = library_df.drop_duplicates().reset_index(drop=True)
                library_df.to_csv(library_loc, index = False)
                songTitleResult = searchBySongTitle(library_df, songTitle)
            progress.update(task, advance=1)
            time.sleep(0.1)
            
            if artist != '':
                spotifyArtistSearch = SpotSearch.get_artist_attributes(artist)
                library_df = pd.concat([library_df, spotifyArtistSearch], ignore_index = False)
                library_df = library_df.drop_duplicates().reset_index(drop=True)
                library_df.to_csv(library_loc, index = False)
                artistResult = searchByArtist(library_df, artist)
            progress.update(task, advance=1)
            time.sleep(0.1)

            if album != '':
                spotifyAlbumSearch = SpotSearch.get_album_attribtues(album)
                library_df = pd.concat([library_df, spotifyAlbumSearch], ignore_index = False)
                library_df = library_df.drop_duplicates().reset_index(drop=True)
                library_df.to_csv(library_loc, index = False)
                albumResult = searchByAlbum(library_df, album)
            progress.update(task, advance=1)
            time.sleep(0.1)

            if songID != '':
                songIDResult = searchBySongID(library_df, songID)
            progress.update(task, advance=1)
            time.sleep(0.1)

            if danceability != '':
                danceabilityResult = searchByDanceability(library_df, danceability)
            progress.update(task, advance=1)
            time.sleep(0.1)
            
            if energy != '':
                energyResult = searchByEnergy(library_df, energy)
            progress.update(task, advance=1)
            time.sleep(0.1)

            if loudness != '':
                loudnessResult = searchByLoudness(library_df, loudness)
            progress.update(task, advance=1)
            time.sleep(0.1)

            if speechiness != '':
                speechinessResult = searchBySpeechiness(library_df, speechiness)
            progress.update(task, advance=1)
            time.sleep(0.1)

            if instrumentalness != '':
                instrumentalnessResult = searchByInstrumentalness(library_df, instrumentalness)
            progress.update(task, advance=1)
            time.sleep(0.1)

            if liveness != '':
                livenessResult = searchByLiveness(library_df, liveness)
            progress.update(task, advance=1)
            time.sleep(0.1)

            frames = [songTitleResult, artistResult, albumResult, songIDResult, danceabilityResult, energyResult, loudnessResult, speechinessResult, instrumentalnessResult, livenessResult]
            combined = pd.concat(frames) # combined each search table
            progress.update(task, advance=1)
            time.sleep(0.1)

            while not progress.finished:
                progress.update(task, advance=1)
                # Simulate some delay
                time.sleep(0.1)

        output = {}
        with Progress() as progress:
            task = progress.add_task("[green]Sorting...", total=len(combined) + len(combined.drop_duplicates()) + 2)
            
            # count how many times a song appears in combined df
            for song in combined.index:
                if song not in output:
                    output[song] = 1
                else:
                    output[song] += 1
                progress.update(task, advance=1)
                time.sleep(0.001)
            for index in output:
                if library_df.loc[index, "track_name"].lower() == songTitle.lower():
                    output[index] += 1
                if library_df.loc[index, "artist"].lower() == artist.lower():
                    output[index] += 1
                if library_df.loc[index, "album"].lower() == album.lower():
                    output[index] += 1
                progress.update(task, advance=1)
                time.sleep(0.001)
            
            # sort by value (number of times song shows up) in reverse
            sorted_output = sorted(output.items(), key=lambda x:x[1], reverse=True)
            progress.update(task, advance=1)
            time.sleep(0.001)
            converted_dict = dict(sorted_output)
            progress.update(task, advance=1)
            time.sleep(0.001)

            while not progress.finished:
                progress.update(task, advance=1)
                # Simulate some delay
                time.sleep(0.1)
                
        results = pd.DataFrame(columns = ["artist","album","track_name",  "track_id","danceability","energy","loudness", "speechiness","instrumentalness","liveness"])

        with Progress() as progress:
            # task = progress.add_task("[green]Saving as dataframe...", total=20)
            task = progress.add_task("[green]Saving as dataframe...", total=len(converted_dict))

            # for index in itertools.islice(converted_dict, 20):
            for index in converted_dict:
                results = pd.concat([results, library_df.loc[[index]]], ignore_index=False)
                progress.update(task, advance=1)
                time.sleep(0.1)

            while not progress.finished:
                progress.update(task, advance=1)
                # Simulate some delay
                time.sleep(0.1)

    playlist_loc = "../output/searchResults.csv"
    results.to_csv(playlist_loc, index = False)

    

def searchBySongTitle(library_df, songTitle):
    songTitleResult = library_df.loc[library_df["track_name"].str.lower() == songTitle]
    songTitleResult = pd.concat([songTitleResult, library_df.loc[library_df["track_name"].str.contains(songTitle, case=False).fillna(False)]], ignore_index=False)
    return songTitleResult.drop_duplicates()

def searchByArtist(library_df, artist):
    artistResult = library_df.loc[library_df["artist"].str.lower() == artist]
    artistResult = pd.concat([artistResult, library_df.loc[library_df["artist"].str.contains(artist, case=False).fillna(False)]], ignore_index=False)
    return artistResult.drop_duplicates()

def searchByAlbum(library_df, album):
    albumResult = library_df.loc[library_df["album"].str.lower() == album]
    albumResult = pd.concat([albumResult, library_df.loc[library_df["album"].str.contains(album, case=False).fillna(False)]], ignore_index=False)
    return albumResult.drop_duplicates()

def searchBySongID(library_df, songID):
    songIDResult = library_df.loc[library_df["track_id"].str.lower() == songID]
    songIDResult = pd.concat([songIDResult, library_df.loc[library_df["track_id"].str.contains(songID, case=False).fillna(False)]], ignore_index=False)
    return songIDResult.drop_duplicates()

def searchByDanceability(library_df, danceability):
    danceabilityResult = library_df.loc[library_df["danceability"].astype(str) == danceability]
    danceabilityResult = pd.concat([danceabilityResult, library_df.loc[library_df["danceability"].astype(str).str.contains(danceability, case=False).fillna(False)]], ignore_index=False)
    return danceabilityResult.drop_duplicates()

def searchByEnergy(library_df, energy):
    energyResult = library_df.loc[library_df["energy"].astype(str) == energy]
    energyResult = pd.concat([energyResult, library_df.loc[library_df["energy"].astype(str).str.contains(energy, case=False).fillna(False)]], ignore_index=False)
    return energyResult.drop_duplicates()

def searchByLoudness(library_df, loudness):
    loudnessResult = library_df.loc[library_df["loudness"].astype(str) == loudness]
    loudnessResult = pd.concat([loudnessResult, library_df.loc[library_df["loudness"].astype(str).str.contains(loudness, case=False).fillna(False)]], ignore_index=False)
    return loudnessResult.drop_duplicates()

def searchBySpeechiness(library_df, speechiness):
    speechinessResult = library_df.loc[library_df["speechiness"].astype(str) == speechiness]
    speechinessResult = pd.concat([speechinessResult, library_df.loc[library_df["speechiness"].astype(str).str.contains(speechiness, case=False).fillna(False)]], ignore_index=False)
    return speechinessResult.drop_duplicates()

def searchByInstrumentalness(library_df, instrumentalness):
    instrumentalnessResult = library_df.loc[library_df["instrumentalness"].astype(str) == instrumentalness]
    instrumentalnessResult = pd.concat([instrumentalnessResult, library_df.loc[library_df["instrumentalness"].astype(str).str.contains(instrumentalness, case=False).fillna(False)]], ignore_index=False)
    return instrumentalnessResult.drop_duplicates()

def searchByLiveness(library_df, liveness):
    livenessResult = library_df.loc[library_df["liveness"].astype(str) == liveness]
    livenessResult = pd.concat([livenessResult, library_df.loc[library_df["liveness"].astype(str).str.contains(liveness, case=False).fillna(False)]], ignore_index=False)
    return livenessResult.drop_duplicates()

def check_only_one_string(arr):
    empty_count = 0
    
    for string in arr:
        if string == "":
            empty_count += 1

    if empty_count == 9:
        return True
    else:
        return False



