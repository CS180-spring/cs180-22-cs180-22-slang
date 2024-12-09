import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
# from sklearn.cluster import KMeans
# from sklearn import preprocessing
from rich.console import Console, Group
from rich.layout import Layout
from rich.panel import Panel
from rich.align import Align
from rich.markdown import Markdown
from rich.text import Text
from rich.progress import Progress
from rich import box
from rich.table import Table
from rich.prompt import Prompt, Confirm
import time
import pandas as pd
from numba import njit,jit,prange
import os
import os.path
import search
import kmeans
import recommend
import df_to_rich

console = Console(height = 11)
layout = Layout()
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

def runKmeans(input_df, input_df2, merged_loc):
    combined_df = kmeans.Classify.run_classification(input_df, input_df2, merged_loc)
    combined_df.to_csv(merged_loc, index = False)

def runRecommend(input_df, lib_df):
    recs = recommend.recommend(input_df, lib_df)
    recs.to_csv("../output/recommendations.csv", index = False)
    return recs


def getPlaylistFromUser(user_spotify_id):
    playlists = sp.user_playlists(user_spotify_id, limit=50)
    playlists_df = pd.DataFrame(columns=['index', 'Spotify ID', 'Playlist name'])
    for i, playlist in enumerate(playlists['items']):
        # print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'],  playlist['name']))
        playlists_df.loc[len(playlists_df)] = [i + 1 + playlists['offset'], playlist['uri'],  playlist['name']]
    
    return playlists, playlists_df
    

library_loc = "../library/library.csv"
library_df = pd.read_csv(library_loc)
library_df['track_name'] = library_df['track_name'].astype(str)
library_df['artist'] = library_df['artist'].astype(str)
library_df['album'] = library_df['album'].astype(str)

# header_text = Text("SpotiDB Terminal", style="bold white")

with Progress() as progress:
    task = progress.add_task("[green]Loading up Terminal Menu...", total=100)
    while not progress.finished:
        progress.update(task, advance=1)
        # Simulate some delay
        time.sleep(0.1)

MARKDOWN = """
# SpotiDB Terminal
"""
md = Markdown(MARKDOWN)
console.print(md) 

title_text = Text("Menu Options", style = "green")

body_content = """
1. Make a new playlist
2. Edit an existing playlist
3. Import a Spotify playlist
4. Merge two playlists
5. Get recommendations for a playlist
6. Import Spotify User playlists
7. Quit
"""

panel_width = 40
panel_height = 10

body_text = Text(body_content)
body_text.truncate(panel_width * panel_height)

body_panel = Panel(body_content, title=title_text, expand=False, height=11)

layout.split(
    Layout(body_panel)
)

console.print(layout)

inp1 = input("Which would you like to do? ")

while inp1 != "7":

    if inp1 == "1":
        playlistExists = True
        while playlistExists:
            newPlaylistName = input("Please name your playlist: ")
            newPlaylist_loc = "../output/" + newPlaylistName + ".csv"
            playlistExists = os.path.isfile(newPlaylist_loc)
            if playlistExists:
                console.print("[red]Playlist name already exists.[/red]")
        playlist_df = pd.DataFrame(columns = ["artist","album","track_name",  "track_id","danceability","energy","loudness", "speechiness","instrumentalness","liveness"])
        console.print("[bold]Add songs:")
        inp3 = True
        while inp3:
            temp_song, library_df = search.advanced_search(library_df, library_loc)
            if not temp_song.empty: 
                if temp_song['track_id'].to_string(index=False) in playlist_df['track_id'].values:
                    inp4 = Confirm.ask("[red]Song already in playlist.[/red] Would you still like to add?")
                    if inp4:
                        console.print('[bold green3]Song added')
                        playlist_df = pd.concat([playlist_df, temp_song], ignore_index= True)
                        playlist_df.to_csv(newPlaylist_loc, index = False)
                else:
                    playlist_df = pd.concat([playlist_df, temp_song], ignore_index= True)
                    playlist_df.to_csv(newPlaylist_loc, index = False)
            inp3 = Confirm.ask("Keep adding songs?")

    elif inp1 == "2":
        playlistExists = False
        while not playlistExists:
            inp2 = input("Please enter the name of the playlist you want to edit: ")
            playlist_loc = "../output/" + inp2 + ".csv"
            playlistExists = os.path.isfile(playlist_loc)
            if not playlistExists:
                console.print("[red]Playlist does not exist[/red]")
        playlist_df = pd.read_csv(playlist_loc)
        console.print("[bold white]1. Add song")
        console.print("[bold white]2. Remove song")
        inp3 = Prompt.ask("What do you want to do?", choices=['1', '2'])
        if inp3 == "1":
            inp4 = True
            while inp4:
                temp_song, library_df = search.advanced_search(library_df, library_loc)
                if not temp_song.empty:
                    if temp_song['track_id'].to_string(index=False) in playlist_df['track_id'].values:
                        inp5 = Confirm.ask("[red]Song already in playlist.[/red] Would you still like to add?")
                        if inp5:
                            console.print('[bold green3]Song added')
                            playlist_df = pd.concat([playlist_df, temp_song], ignore_index= True)
                            playlist_df.to_csv(playlist_loc, index = False)
                    else:
                        playlist_df = pd.concat([playlist_df, temp_song], ignore_index= True)
                        playlist_df.to_csv(playlist_loc, index = False)
                inp4 = Confirm.ask("Keep adding songs?")
        elif inp3 == "2":
            # Initiate a Table instance to be modified
            table = Table(show_header=True, header_style="green")
            # Modify the table instance to have the data from the DataFrame
            table = df_to_rich.df_to_table(playlist_df[["track_name", "artist", "album"]], table, index_name='index')
            # Update the style of the table
            table.row_styles = ["none", "dim"]
            table.box = box.SIMPLE_HEAD
            console.print(table)
            validInput = True
            while validInput:
                inp4 = input("Enter the index of the song you want to remove: ")
                if int(inp4) in playlist_df.index:
                    playlist_df = playlist_df.drop(int(inp4))
                    playlist_df.to_csv(playlist_loc, index = False)
                    break
                else:
                    validInput = False
                    inp5 = Confirm.ask('[red]Invalid song choice.[/red] Would you like to try again?')
                    if inp5:
                        validInput = True

    elif inp1 == "3":
        playlistLink = input("Please enter link to playlist: ")
        id = extract_playlist_id_from_url(playlistLink)
        playlistName = input("Please name your imported playlist: ")
        if " " in playlistName:
            playlistName = playlistName.replace(" ", "_")

        df = make_playlist_df1("spotify", id)
        csvName = "../output/" + playlistName + ".csv"
        df.to_csv(csvName, index = False)

    elif inp1 == "4":
        playlist1Exists = False
        while not playlist1Exists:
            playlist1 = input("Please enter the first playlist's name: ")
            playlist1_loc = "../output/" + playlist1 + ".csv"
            playlist1Exists = os.path.isfile(playlist1_loc)
            if not playlist1Exists:
                console.print("[red]Playlist does not exist")

        playlist2Exists = False
        while not playlist2Exists:
            playlist2 = input("Please enter the second playlist's name: ")
            playlist2_loc = "../output/" + playlist2 + ".csv"
            playlist2Exists = os.path.isfile(playlist2_loc)
            if not playlist2Exists:
                console.print("[red]Playlist does not exist")

        playlistMergeExists = True
        while playlistMergeExists:
            mergedName = input("Please name your new merged playlist: ")
            merged_loc = "../output/" + mergedName + ".csv"
            playlistMergeExists = os.path.isfile(merged_loc)
            if playlistMergeExists:
                console.print("[red]Playlist name already exist")

        playlist_df1 = pd.read_csv(playlist1_loc)
        playlist_df2 = pd.read_csv(playlist2_loc)

        merged = kmeans.Classify.run_classification(playlist_df1, playlist_df2, merged_loc)
        merged.to_csv(merged_loc, index = False)

    elif inp1 == "5":
        
        playlist1Exists = False
        while not playlist1Exists:
            rec_playlist = input("Enter the name of the playlist you want songs recommended for: ")
            playlist_loc = "../output/" + rec_playlist + ".csv"
            playlist1Exists = os.path.isfile(playlist_loc)
            if not playlist1Exists:
                console.print("[red]Playlist does not exist")
        playlist_df = pd.read_csv(playlist_loc)
        recommended_songs = runRecommend(playlist_df, library_df)
        playlist_df = pd.concat([playlist_df, recommended_songs], ignore_index=True)
        playlist_df.to_csv(playlist_loc, index=False)

    elif inp1 == "6":
        inp2 = input("Please enter the spotify username: ")
        spotify_playlists, df_to_print = getPlaylistFromUser(inp2)
        # Initiate a Table instance to be modified
        table = Table(show_header=True, header_style="green")
        # Modify the table instance to have the data from the DataFrame
        table = df_to_rich.df_to_table(df_to_print, table, show_index=False)
        # Update the style of the table
        table.row_styles = ["none", "dim"]
        table.box = box.SIMPLE_HEAD
        console.print(table)
        inp3 = Confirm.ask("Do you want to import this user's playlists?")
        if inp3:
            original = []
            changed = []

            console.print("[bold white]1. Import all playlists")
            console.print("[bold white]2. Select which playlist to import")
            inp4 = Prompt.ask("What would you like to do", choices = ['1', '2'])
            
            if inp4 == '1':
                with Progress() as progress:
                    task = progress.add_task("[green]Importing playlists...", total=len(list(enumerate(spotify_playlists['items']))))

                    for i, playlist in enumerate(spotify_playlists['items']):
                        id = playlist["uri"].rsplit(":", 1)[-1]
                        new_playlist = make_playlist_df1("spotify", id)
                        new_name = playlist["name"]
                        if " " in new_name:
                            new_name = playlist["name"].replace(" ", "_")
                            original.append(playlist["name"])
                            changed.append(new_name)
                        new_loc = "../output/" + new_name + ".csv"
                        new_playlist.to_csv(new_loc, index=False)

                        progress.update(task, advance=1)
                        time.sleep(0.1)

            elif inp4 == '2':
                validInput = False
                while not validInput:
                    inp5 = input("Type the index of the playlist you would like to import: ")
                    if int(inp5) <= len(list(enumerate(spotify_playlists['items']))):
                        validInput = True
                    else:
                        inp6 = Confirm.ask('[red]Invalid playlist index.[/red] Would you like to try again?')
                        if not inp6:
                            break
                if validInput:
                    playlist = spotify_playlists['items'][int(inp5)-1]
                    id = playlist["uri"].rsplit(":", 1)[-1]
                    new_playlist = make_playlist_df1("spotify", id)
                    new_name = playlist["name"]
                    if " " in new_name:
                        new_name = playlist["name"].replace(" ", "_")
                        original.append(playlist["name"])
                        changed.append(new_name)
                    new_loc = "../output/" + new_name + ".csv"
                    new_playlist.to_csv(new_loc, index=False)

            if original and changed:
                renamed = pd.DataFrame({'original name': original, 'new name': changed})
                print("The following playlist names were changed to fit our naming conventions:")
                # Initiate a Table instance to be modified
                table2 = Table(show_header=True, header_style="green")
                # Modify the table instance to have the data from the DataFrame
                # Modify the table instance to have the data from the DataFrame
                table2 = df_to_rich.df_to_table(renamed, table2, show_index=False)

                # Update the style of the table
                table2.row_styles = ["none", "dim"]
                table2.box = box.SIMPLE_HEAD

                console.print(table2)

    elif inp1 not in ["1", "2", "3", "4", "5", "6", "7"]: 
        console.print("[red]Not a valid selection")

    console.print(layout)
    inp1 = input("Which do you want to do? ")