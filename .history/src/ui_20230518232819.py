##just run this file to start the UI
import tkinter as tk
from tkinter import ttk
import csv
import os
from mainUI import *
from searchUI import *
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
from spotipy.oauth2 import SpotifyOAuth


def searchTitleUI():
    titleSearch = entries[0].get()
    searchbyTitle(library_df, titleSearch)
    cacheSearchCSV = "../output/cacheSearch.csv"
    with open(cacheSearchCSV, 'r') as f:
        reader = csv.reader(f)
        cacheRead = list(reader)
        print(cacheRead)

        searchTreeView.delete(*searchTreeView.get_children())

        for row in cacheRead[1:]:
            searchTreeView.insert("", "end", values=row)

def searchArtistUI():
    artistSearch = entries[1].get()
    searchbyArtist(library_df, artistSearch)
    cacheSearchCSV = "../output/cacheSearch.csv"
    with open(cacheSearchCSV, 'r') as f:
        reader = csv.reader(f)
        cacheRead = list(reader)
        print(cacheRead)
        searchTreeView.delete(*searchTreeView.get_children())
        for row in cacheRead[1:]:
            searchTreeView.insert("", "end", values=row)



def loadPlaylistUI():

    playlist1Link = playlist1_entry.get()
    playlist2Link = playlist2_entry.get()

    importSpotifyPlaylist(playlist1Link, "Playlist")
    

    file_path1 = '../output/Playlist.csv'
    file_path2 = '../output/Playlist2.csv'

    with open(file_path1, 'r') as f1:
        reader1 = csv.reader(f1)
        playlist1 = list(reader1)
        print(playlist1)

        treeview1.delete(*treeview1.get_children())

        for row in playlist1:
            treeview1.insert("", "end", values=row)


    importSpotifyPlaylist(playlist2Link, "Playlist2")
    with open(file_path2, 'r') as f2:
        reader2 = csv.reader(f2)
        playlist2 = list(reader2)
        print(playlist2)

        treeview2.delete(*treeview2.get_children())

        for row in playlist2:
            treeview2.insert("", "end", values=row)

def mergePlaylistsUI():
    file_path3 = '../output/MergedPlaylist.csv'
    mergePlaylists()

    with open(file_path3, 'r') as f3:
        reader3 = csv.reader(f3)
        MergedPlaylist = list(reader3)
        print(MergedPlaylist)

        treeview3.delete(*treeview3.get_children())

        for row in MergedPlaylist:
            treeview3.insert("", "end", values=row)

def runRecommendUI():
    print("Here are your recommendations: ")
    file_path3 = '../output/MergedPlaylist.csv'
    getRecommendations()
    with open(file_path3, 'r') as f3:
        reader3 = csv.reader(f3)
        MergedPlaylist = list(reader3)

        treeview3.delete(*treeview3.get_children())

        for row in MergedPlaylist:
            treeview3.insert("", "end", values=row)

def on_focus_in(e, entry, default_text):
    if entry.get() == default_text:
        entry.delete('0', 'end')

def on_focus_out(e, entry, default_text):
    if not entry.get():
        entry.insert(0, default_text)


root = tk.Tk()
root.title("SpotiDB")
root.resizable(width=False, height=False)


style = ttk.Style(root)
script_dir = os.path.dirname(os.path.abspath(__file__))
forest_light_tcl = os.path.join(script_dir, "../UI/forest-light.tcl")
forest_dark_tcl = os.path.join(script_dir, "../UI/forest-dark.tcl")

root.tk.call("source", forest_light_tcl)
root.tk.call("source", forest_dark_tcl)
style.theme_use("forest-dark")

frame = ttk.Frame(root)
frame.pack()

windowFrameNotebook = ttk.Notebook(frame)
windowFrameNotebook.grid(row=0, column=0)

tab1 = ttk.Frame(windowFrameNotebook)
windowFrameNotebook.add(tab1, text="Simple View")

leftFrame = ttk.Frame(tab1)
leftFrame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

#############################
widgets_frame = ttk.LabelFrame(leftFrame, text="Search Database",padding=(20, 10))
widgets_frame.grid(row=1, column=0, padx=20, pady=20, sticky="new")


searchTitle_entry = ttk.Entry(widgets_frame)
searchTitle_entry.insert(0, "Song Title")
searchTitle_entry.bind("<FocusIn>", lambda e: on_focus_in(e, searchTitle_entry, "Song Title"))
searchTitle_entry.bind("<FocusOut>", lambda e: on_focus_out(e, searchTitle_entry, "Song Title"))
searchTitle_entry.grid(row=0, column=0, padx=5, pady=(0, 5), sticky="nsew")


searchArtist_entry = ttk.Entry(widgets_frame)
searchArtist_entry.insert(0, "Artist")
searchArtist_entry.bind("<FocusIn>", lambda e: on_focus_in(e, searchArtist_entry, "Artist"))
searchArtist_entry.bind("<FocusOut>", lambda e: on_focus_out(e, searchArtist_entry, "Artist"))
searchArtist_entry.grid(row=2, column=0, padx=5, pady=(0, 5), sticky="nsew")

loadButton = ttk.Button(widgets_frame, text="Search", style="Accent.TButton")
loadButton.grid(row=3, column=0, padx=5, pady=(0, 5), sticky="nsew")
#############################

separator = ttk.Separator(leftFrame)
separator.grid(row=2, column=0, padx=(20, 10), pady=10, sticky="ew")
#############################

widgets2_frame = ttk.LabelFrame(leftFrame, text="Paste Playlists",padding=(20, 10))
widgets2_frame.grid(row=3, column=0, padx=20, pady=20, sticky="new")

playlist1_entry = ttk.Entry(widgets2_frame)
playlist1_entry.insert(0, "Playlist 1")
playlist1_entry.bind("<FocusIn>", lambda e: on_focus_in(e, playlist1_entry, "Playlist 1"))
playlist1_entry.bind("<FocusOut>", lambda e: on_focus_out(e, playlist1_entry, "Playlist 1"))
playlist1_entry.grid(row=0, column=0, padx=5, pady=(0, 5), sticky="ew")


playlist2_entry = ttk.Entry(widgets2_frame)
playlist2_entry.insert(0, "Playlist 2")
playlist2_entry.bind("<FocusIn>", lambda e: on_focus_in(e, playlist2_entry, "Playlist 2"))
playlist2_entry.bind("<FocusOut>", lambda e: on_focus_out(e, playlist2_entry, "Playlist 2"))
playlist2_entry.grid(row=1, column=0, padx=5, pady=(0, 5), sticky="ew")

loadButton = ttk.Button(widgets2_frame, text="Load Playlists", style="Accent.TButton", command=loadPlaylistUI)
loadButton.grid(row=2, column=0, padx=5, pady=(0, 5), sticky="ew")


#############################
rightFrame = ttk.Frame(tab1)
rightFrame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
buttonsFrame = ttk.Frame(rightFrame)
buttonsFrame.grid(row=0, column=0, sticky="nsew")

mergeButton = ttk.Button(buttonsFrame, text="Merge", style="Accent.TButton", command=mergePlaylistsUI)
mergeButton.grid(row=0, column=0, padx = (0,20),pady=(20,0))

recommendButton = ttk.Button(buttonsFrame, text="Add Recommended", style="Accent.TButton", command=runRecommendUI)
recommendButton.grid(row=0, column=1, padx=20,pady=(20,0))

combo_list = ["Sort By", "Title", "Album", "Artist", "Genre", "Release Date"]
combobox = ttk.Combobox(buttonsFrame, state="readonly", values=combo_list)
combobox.current(0)
combobox.grid(row=0, column=2, padx=20,pady=(20,0), sticky="ew")

#############################

separator1 = ttk.Separator(rightFrame)
separator1.grid(row=1, column=0, pady=(20,0), sticky="ew")

############################# 

NotebookPlaylist = ttk.Notebook(rightFrame)
NotebookPlaylist.grid(row=2, column=0, padx=(0,20), pady=20, sticky="nsew")

playlistFrame1 = ttk.LabelFrame(NotebookPlaylist, width=200, height=200)
playlistFrame2 = ttk.LabelFrame(NotebookPlaylist, width=200, height=200)
playlistFrame3 = ttk.LabelFrame(NotebookPlaylist, width=200, height=200)


cols = ("Artist", "Album", "Title", "SongID")
treeview1 = ttk.Treeview(NotebookPlaylist, show="headings", columns=cols, height=13)
for col in cols:
    treeview1.column(col, width=100)
treeview1.pack(fill="both", expand=True, side="left")
for col in cols:
    treeview1.heading(col, text=col)

treeview2 = ttk.Treeview(NotebookPlaylist, show="headings", columns=cols, height=13)
for col in cols:
    treeview2.column(col, width=100)
treeview2.pack(fill="both", expand=True, side="left")
for col in cols:
    treeview2.heading(col, text=col)

treeview3 = ttk.Treeview(NotebookPlaylist, show="headings", columns=cols, height=13)
for col in cols:
    treeview3.column(col, width=100)
treeview3.pack(fill="both", expand=True, side="left")
for col in cols:
    treeview3.heading(col, text=col)


scrollbar1 = ttk.Scrollbar(treeview1, orient="vertical", command=treeview1.yview)
scrollbar1.pack(side="right", fill="y")
treeview1.configure(yscrollcommand=scrollbar1.set)

scrollbar2 = ttk.Scrollbar(treeview2, orient="vertical", command=treeview2.yview)
scrollbar2.pack(side="right", fill="y")
treeview2.configure(yscrollcommand=scrollbar2.set)

scrollbar1_h = ttk.Scrollbar(treeview1, orient="horizontal", command=treeview1.xview)
scrollbar1_h.pack(side="bottom", fill="x")
treeview1.configure(xscrollcommand=scrollbar1_h.set)

scrollbar2_h = ttk.Scrollbar(treeview2, orient="horizontal", command=treeview2.xview)
scrollbar2_h.pack(side="bottom", fill="x")
treeview2.configure(xscrollcommand=scrollbar2_h.set)

NotebookPlaylist.add(treeview1, text="Playlist 1")
NotebookPlaylist.add(treeview2, text="Playlist 2")
NotebookPlaylist.add(treeview3, text="New Playlist")

NotebookPlaylist.add(treeview1, text="Playlist 1")
NotebookPlaylist.add(treeview2, text="Playlist 2")
NotebookPlaylist.add(treeview3, text="New Playlist")


MiniFrame = ttk.Frame(rightFrame)
MiniFrame.grid(row=3, column=0, padx=5, pady=5, sticky="nsew")

button1 = ttk.Button(MiniFrame, text="Add", style="Accent.TButton")
button1.grid(row=0, column=0, padx = (40,0),pady=(0,0))


button2 = ttk.Button(MiniFrame, text="Delete", style="Accent.TButton")
button2.grid(row=0, column=1, padx = (40,0),pady=(0,0))


button3 = ttk.Button(MiniFrame, text="Deselect", style="Accent.TButton")
button3.grid(row=0, column=2, padx = (40,0),pady=(0,0))


##########################################################################################
tab2 = ttk.Frame(windowFrameNotebook)

windowFrameNotebook.add(tab2, text="Search")
leftFrame2 = ttk.Frame(tab2)
leftFrame2.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

#############################
widgets_frame2 = ttk.LabelFrame(leftFrame2, text="Search Database",padding=(20, 10))
widgets_frame2.grid(row=1, column=0, padx=20, pady=20, sticky="new")

searchFields = ["Song Title", "Artist", "Albumn", "Title ID", "Dancebility", "Energy", 
          "Loudness", "Speechiness", "Instrumentalness", "Liveness"]

entries = []
for i, text in enumerate(searchFields):
    entry = ttk.Entry(widgets_frame2)
    entry.insert(0, text)
    entry.bind("<FocusIn>", lambda e, entry=entry, text=text: on_focus_in(e, entry, text))
    entry.bind("<FocusOut>", lambda e, entry=entry, text=text: on_focus_out(e, entry, text))
    entry.grid(row=i, column=0, padx=5, pady=(0, 5), sticky="nsew")
    entries.append(entry)


searchButton2 = ttk.Button(widgets_frame2, text="Search", style="Accent.TButton",command=searchArtistUI)
searchButton2.grid(row=11, column=0, padx=5, pady=(0, 5), sticky="nsew")

#############################
rightFrame2 = ttk.Frame(tab2)
rightFrame2.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
buttonsFrame2 = ttk.Frame(rightFrame2)
buttonsFrame2.grid(row=0, column=0, sticky="nsew")


combo_list2 = ["Sort By", "Title", "Album", "Artist", "Genre", "Release Date"]
combobox2 = ttk.Combobox(buttonsFrame2, state="readonly", values=combo_list2)
combobox2.current(0)
combobox2.grid(row=2, column=2, padx=20,pady=(20,0), sticky="ew")

#############################

separator1 = ttk.Separator(rightFrame2)
separator1.grid(row=1, column=0, pady=(20,0), sticky="ew")

############################# 

treeview_frame = ttk.Frame(rightFrame2)
treeview_frame.grid(row=2, column=0, padx=(0,20), pady=20, sticky="nsew")

cols = ("Artist", "Album", "Title", "SongID")
searchTreeView = ttk.Treeview(treeview_frame, show="headings", columns=cols, height=13)

for col in cols:
    searchTreeView.heading(col, text=col)
    searchTreeView.column(col, width=100)

scrollbarS = ttk.Scrollbar(treeview_frame, orient="vertical", command=searchTreeView.yview)
searchTreeView.configure(yscrollcommand=scrollbarS.set)
searchTreeView.pack(side="left", fill="both", expand=True)
scrollbarS.pack(side="right", fill="y")


#############################
MiniFrame = ttk.Frame(rightFrame2)
MiniFrame.grid(row=3, column=0, padx=5, pady=5, sticky="nsew")

button1 = ttk.Button(MiniFrame, text="Add", style="Accent.TButton")
button1.grid(row=0, column=0, padx = (40,0),pady=(0,0))

button2 = ttk.Button(MiniFrame, text="Delete", style="Accent.TButton")
button2.grid(row=0, column=1, padx = (40,0),pady=(0,0))

button3 = ttk.Button(MiniFrame, text="Deselect", style="Accent.TButton")
button3.grid(row=0, column=2, padx = (40,0),pady=(0,0))

########################################
tab3 = ttk.Frame(windowFrameNotebook)
windowFrameNotebook.add(tab3, text="View Playlists")


leftFrame3 = ttk.Frame(tab3)
leftFrame3.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

#############################
widgets_frame3 = ttk.LabelFrame(leftFrame3, text="Spotify user ID",padding=(20, 10))
widgets_frame3.grid(row=1, column=0, padx=20, pady=20, sticky="new")

searchFields = ["User ID"]

entries = []
for i, text in enumerate(searchFields):
    entry = ttk.Entry(widgets_frame3)
    entry.insert(0, text)
    entry.bind("<FocusIn>", lambda e, entry=entry, text=text: on_focus_in(e, entry, text))
    entry.bind("<FocusOut>", lambda e, entry=entry, text=text: on_focus_out(e, entry, text))
    entry.grid(row=i, column=0, padx=5, pady=(0, 5), sticky="nsew")
    entries.append(entry)


searchButton3 = ttk.Button(widgets_frame3, text="Search", style="Accent.TButton",command=searchArtistUI)
searchButton3.grid(row=2, column=0, padx=5, pady=(0, 5), sticky="nsew")

#############################
rightFrame3 = ttk.Frame(tab3)
rightFrame3.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
buttonsFrame3 = ttk.Frame(rightFrame3)
buttonsFrame3.grid(row=0, column=0, sticky="nsew")


separator1 = ttk.Separator(rightFrame3)
separator1.grid(row=1, column=0, pady=(20,0), sticky="ew")

############################# 

treeview_frame = ttk.Frame(rightFrame3)
treeview_frame.grid(row=2, column=0, padx=(0,20), pady=20, sticky="nsew")

cols = ("Artist", "Album", "Title", "SongID")
searchTreeView = ttk.Treeview(treeview_frame, show="headings", columns=cols, height=13)

for col in cols:
    searchTreeView.heading(col, text=col)
    searchTreeView.column(col, width=100)

scrollbarS = ttk.Scrollbar(treeview_frame, orient="vertical", command=searchTreeView.yview)
searchTreeView.configure(yscrollcommand=scrollbarS.set)
searchTreeView.pack(side="left", fill="both", expand=True)
scrollbarS.pack(side="right", fill="y")

########################################################


def loadPlaylistUI():
    # Get the Spotify user ID
    user_id = "your_user_id"  # Replace "your_user_id" with the actual Spotify user ID
    
    playlist1Link = playlist1_entry.get()
    playlist2Link = playlist2_entry.get()

    # Initialize the Spotipy client
    client_credentials_manager = SpotifyClientCredentials()
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    # Get the playlist tracks using the Spotify API
    playlist1 = sp.user_playlist_tracks(user_id, playlist_id=playlist1Link)
    playlist2 = sp.user_playlist_tracks(user_id, playlist_id=playlist2Link)

    # Rest of your code...
    # Update the treeview with the playlist data



root.mainloop()



