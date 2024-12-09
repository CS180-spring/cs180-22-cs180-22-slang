##just run this file to start the UI
import tkinter as tk
from tkinter import ttk
import csv
import os
from mainUI import *
from searchUI import *
import spotipy
import pandas as pd
from spotipy.oauth2 import SpotifyClientCredentials
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

def searchDatabaseUI():
    library_loc = "../library/library.csv"
    library_df = pd.read_csv(library_loc,low_memory=False)
    advanced_search(library_df, library_loc,entries[0].get(),entries[1].get(),entries[2].get(),entries[3].get(),entries[4].get(),entries[5].get(),entries[6].get(),entries[7].get(),entries[8].get(),entries[9].get())

    searchResultsCSV = "../output/searchResults.csv"
    with open(searchResultsCSV, 'r') as f:
        reader = csv.reader(f)
        searchResults = list(reader)
        print(searchResults)

        searchTreeView.delete(*searchTreeView.get_children())

        for row in searchResults[1:]:
            searchTreeView.insert("", "end", values=row)

def loadPlaylistUI():

    playlist1Link = playlist1_entry.get()
    playlist2Link = playlist2_entry.get()

    

    file_path1 = '../output/Playlist.csv'
    file_path2 = '../output/Playlist2.csv'


    if playlist1Link != 'Playlist 1':
        importSpotifyPlaylist(playlist1Link, "Playlist")
        with open(file_path1, 'r') as f1:
            reader1 = csv.reader(f1)
            playlist1 = list(reader1)
            print(playlist1)
    
            treeview1.delete(*treeview1.get_children())

            for row in playlist1[1:]:
                treeview1.insert("", "end", values=row)
    
    if playlist2Link != 'Playlist 2':
        importSpotifyPlaylist(playlist2Link, "Playlist2")
        with open(file_path2, 'r') as f2:
            reader2 = csv.reader(f2)
            playlist2 = list(reader2)
            print(playlist2)

            treeview2.delete(*treeview2.get_children())

            for row in playlist2[1:]:
                treeview2.insert("", "end", values=row)

def mergePlaylistsUI():
    file_path3 = '../output/MergedPlaylist.csv'
    mergePlaylists()

    with open(file_path3, 'r') as f3:
        reader3 = csv.reader(f3)
        MergedPlaylist = list(reader3)
        print(MergedPlaylist)

        treeview3.delete(*treeview3.get_children())

        for row in MergedPlaylist[1:]:
            treeview3.insert("", "end", values=row)

def runRecommendUI():
    print("Here are your recommendations: ")
    file_path3 = '../output/MergedPlaylist.csv'
    getRecommendations()
    with open(file_path3, 'r') as f3:
        reader3 = csv.reader(f3)
        MergedPlaylist = list(reader3)

        treeview3.delete(*treeview3.get_children())

        for row in MergedPlaylist[1:]:
            treeview3.insert("", "end", values=row)


####################################### event handlers

def on_focus_in(e, entry, default_text):
    if entry.get() == default_text:
        entry.delete('0', 'end')

def on_focus_out(e, entry, default_text):
    if not entry.get():
        entry.insert(0, default_text)


def on_tab_changed(event):
    selected_tab = event.widget.tab('current')['text']
    if selected_tab == 'Local Playlists':
        searchTreeView4.delete(*searchTreeView4.get_children())
    

        all_files = os.listdir("../output/")
        
        csv_files = [file for file in all_files if file.endswith('.csv')]

        csv_files = [file[:-4] for file in csv_files]
        for file in csv_files:
            searchTreeView4.insert('', 'end', values=(file, ' '))

def combobox_callback1(event):
    selected_tab = NotebookPlaylist.tab(NotebookPlaylist.select(), "text")
    selected_option = combobox.get()
    
    if selected_option == "Sort By":
        # If "Sort By" is selected, do nothing.
        pass
    else:
        # Get the data from the searchTreeView
        if selected_tab == 'Playlist 1':
            data = []
            for item in treeview1.get_children():
                values = [treeview1.set(item, column) for column in treeview1["columns"]]
                data.append(values)

            # Sort the data based on the selected column
            column_index = treeview1["columns"].index(selected_option)
            sorted_data = sorted(data, key=lambda x: x[column_index])

            # Clear the existing rows in the searchTreeView
            treeview1.delete(*treeview1.get_children())

            # Insert the sorted data into the searchTreeView
            for values in sorted_data:
                treeview1.insert("", tk.END, values = values)
        elif selected_tab == 'Playlist 2':
            data = []
            for item in treeview2.get_children():
                values = [treeview2.set(item, column) for column in treeview2["columns"]]
                data.append(values)
            
            # Sort the data based on the selected column
            column_index = treeview2["columns"].index(selected_option)
            sorted_data = sorted(data, key=lambda x: x[column_index])

            # Clear the existing rows in the searchTreeView
            treeview2.delete(*treeview2.get_children())

            # Insert the sorted data into the searchTreeView
            for values in sorted_data:
                treeview2.insert("", tk.END, values = values)
        elif selected_tab == 'New Playlist':
            data = []
            for item in treeview3.get_children():
                values = [treeview3.set(item, column) for column in treeview3["columns"]]
                data.append(values)
            
            # Sort the data based on the selected column
            column_index = treeview3["columns"].index(selected_option)
            sorted_data = sorted(data, key=lambda x: x[column_index])

            # Clear the existing rows in the searchTreeView
            treeview3.delete(*treeview3.get_children())

            # Insert the sorted data into the searchTreeView
            for values in sorted_data:
                treeview3.insert("", tk.END, values = values)

                


def combobox_callback2(event):
    selected_option = combobox2.get()

    if selected_option == "Sort By":
        # If "Sort By" is selected, do nothing.
        pass
    else:
        # Get the data from the searchTreeView
        data = []
        for item in searchTreeView.get_children():
            values = [searchTreeView.set(item, column) for column in searchTreeView["columns"]]
            data.append(values)

        # Sort the data based on the selected column
        column_index = searchTreeView["columns"].index(selected_option)
        sorted_data = sorted(data, key=lambda x: x[column_index])

        # Clear the existing rows in the searchTreeView
        searchTreeView.delete(*searchTreeView.get_children())

        # Insert the sorted data into the searchTreeView
        for values in sorted_data:
            searchTreeView.insert("", tk.END, values = values)
    

####################################### end of event handlers


def importLocalPlaylist1():
    selected = searchTreeView4.selection()
    filename = searchTreeView4.item(selected)['values'][0]
    print(filename)
    file_path1 = f'../output/{filename}.csv'
    playlist1df = pd.read_csv(file_path1,low_memory=False)
    playlist1df.to_csv('../output/Playlist.csv', index=False)
    with open(file_path1, 'r') as f1:
        reader1 = csv.reader(f1)
        playlist1 = list(reader1)
        print(playlist1)
        
        treeview1.delete(*treeview1.get_children())

        for row in playlist1[1:]:
            treeview1.insert("", "end", values=row)


def importLocalPlaylist2():
    selected = searchTreeView4.selection()
    filename = searchTreeView4.item(selected)['values'][0]
    print(filename)
    file_path2 = f'../output/{filename}.csv'
    playlist2df = pd.read_csv(file_path2,low_memory=False)
    playlist2df.to_csv('../output/Playlist2.csv', index=False)
    with open(file_path2, 'r') as f2:
        reader2 = csv.reader(f2)
        playlist2 = list(reader2)
        print(playlist2)

        treeview2.delete(*treeview2.get_children())

        for row in playlist2[1:]:
            treeview2.insert("", "end", values=row)

def importFromPlaylistID(playlistNumber):
    selected = searchTreeView3.selection()
    playlistSelection = searchTreeView3.item(selected)['values'][0]
    getPlaylistIDFromPlaylists(playlists,playlistSelection, playlistNumber)

    if playlistNumber == 1:
        file_path1 = '../output/Playlist.csv'
        with open(file_path1, 'r') as f1:
            reader1 = csv.reader(f1)
            playlist1 = list(reader1)
            print(playlist1)
    
            treeview1.delete(*treeview1.get_children())

            for row in playlist1[1:]:
                treeview1.insert("", "end", values=row)
    elif playlistNumber == 2:
        file_path2 = '../output/Playlist2.csv'
        with open(file_path2, 'r') as f2:
            reader2 = csv.reader(f2)
            playlist2 = list(reader2)
            print(playlist2)

            treeview2.delete(*treeview2.get_children())

            for row in playlist2[1:]:
                treeview2.insert("", "end", values=row)


def savePlaylistName():
    playlistName = playlistName_entry.get()
    print(playlistName)
    if playlistName == 'Name Playlist':
        playlistName = 'MergedPlaylist'
   
    playlistName = playlistName.replace(' ', '_')
    mergedPlaylist = pd.read_csv('../output/MergedPlaylist.csv')
    mergedPlaylist.to_csv(f'../output/{playlistName}.csv', index=False)


def deletePlaylist():
    selected = searchTreeView4.selection()
    filename = searchTreeView4.item(selected)['values'][0]
    print(filename)
    file_path = f'../output/{filename}.csv'
    os.remove(file_path)
    searchTreeView4.delete(selected)

def deleteSong():
    selected_tab = NotebookPlaylist.tab(NotebookPlaylist.select(), "text")
    
    if selected_tab == 'Playlist 1':
        selected_items = treeview1.selection()
        for item in selected_items:
            song_id = treeview1.item(item)['values'][3]
            print(song_id)
            treeview1.delete(item)
            remove_song_from_csv(song_id,'Playlist')
    
    elif selected_tab == 'Playlist 2':
        selected_items = treeview2.selection()
        for item in selected_items:
            song_id = treeview2.item(item)['values'][3]
            treeview2.delete(item)
            remove_song_from_csv(song_id,'Playlist2')
    
    elif selected_tab == 'New Playlist':
        selected_items = treeview3.selection()
        for item in selected_items:
            song_id = treeview3.item(item)['values'][3]
            treeview3.delete(item)
            remove_song_from_csv(song_id,'MergedPlaylist')

def remove_song_from_csv(song_id, playlist_name):
    file_path = f'../output/{playlist_name}.csv'
    
    rows_to_keep = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[3] != song_id:
                rows_to_keep.append(row)
    print(rows_to_keep)
    
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows_to_keep)


def addSong():
    selected_tab = NotebookPlaylist.tab(NotebookPlaylist.select(), "text")

    if selected_tab == 'Playlist 1':
        selected_items = treeview1.selection()
        for item in selected_items:
            song_id = treeview1.item(item)['values'][3]
            add_song_to_csv(song_id,'Playlist')
    
    elif selected_tab == 'Playlist 2':
        selected_items = treeview2.selection()
        for item in selected_items:
            song_id = treeview2.item(item)['values'][3]
            add_song_to_csv(song_id,'Playlist2')
        

    load_updated_merged_playlist()

def add_song_from_search():
    selected_tab = NotebookPlaylist.tab(NotebookPlaylist.select(), "text")
    
    if selected_tab == 'Playlist 1':
        tree_view = treeview1
        playlist_path = 'Playlist'
        selected_items = searchTreeView.selection()
        for item in selected_items:
            # song_id = searchTreeView.item(item)['values'][3]
            add_song_to_csv_from_search(searchTreeView.item(item)['values'],'Playlist')
    
    elif selected_tab == 'Playlist 2':
        tree_view = treeview2
        playlist_path = 'Playlist2'
        selected_items = searchTreeView.selection()
        for item in selected_items:
            # song_id = searchTreeView.item(item)['values'][3]
            add_song_to_csv_from_search(searchTreeView.item(item)['values'],'Playlist2')
    
    elif selected_tab == 'New Playlist':
        tree_view = treeview3
        playlist_path = 'MergedPlaylist'
        selected_items = searchTreeView.selection()
        for item in selected_items:
            # song_id = searchTreeView.item(item)['values'][3]
            add_song_to_csv_from_search(searchTreeView.item(item)['values'],'MergedPlaylist')

    update_playlists(tree_view, f'../output/{playlist_path}.csv')
            
    
    
def add_song_to_csv(song_id, playlistPath):
    addFromPath = f'../output/{playlistPath}.csv'
    file_path = f'../output/MergedPlaylist.csv'

    songsInPlaylist = set()
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            songsInPlaylist.add(row[3])

        
    rows_to_add = []
    with open(addFromPath, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            print(row[3])
            if row[3] == song_id and row [3] not in songsInPlaylist:
                rows_to_add.append(row)
    

    with open(file_path, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows_to_add)


def add_song_to_csv_from_search(song, playlistPath):
    addFromPath = f'../output/{playlistPath}.csv'

    songsInPlaylist = set()
    with open(addFromPath, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            songsInPlaylist.add(row[3])
            print(row[3])

    if song[3] not in songsInPlaylist:
        with open(addFromPath, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(song)


def update_playlists(tree_view, playlist_path):
    # Clear the existing rows in the tree view
    tree_view.delete(*tree_view.get_children())

    # Read the updated playlist CSV file
    with open(playlist_path, 'r') as file:
        reader = csv.reader(file)
        loadPlaylistList = list(reader)
        for row in loadPlaylistList[1:]:
            # Insert the row values into the tree view
            tree_view.insert("", tk.END, values=row)

def load_updated_merged_playlist():
    file_path3 = '../output/MergedPlaylist.csv'
    treeview3.delete(*treeview3.get_children())
    with open(file_path3, 'r') as f3:
        reader3 = csv.reader(f3)
        MergedPlaylist = list(reader3)

        for row in MergedPlaylist[1:]:
            treeview3.insert("", "end", values=row)
    

################################################################ start of window

def combobox_callback(event):
    selected_option = combobox2.get()

    if selected_option == "Sort By":
        # If "Sort By" is selected, do nothing.
        pass

    else:
        # Get the data from the searchTreeView
        data = []
        for item in searchTreeView.get_children():
            values = [searchTreeView.set(item, column) for column in searchTreeView["columns"]]
            data.append(values)

        # Sort the data based on the selected column
        column_index = searchTreeView["columns"].index(selected_option)
        sorted_data = sorted(data, key=lambda x: x[column_index])

        # Clear the existing rows in the searchTreeView
        searchTreeView.delete(*searchTreeView.get_children())

        # Insert the sorted data into the searchTreeView
        for values in sorted_data:
            searchTreeView.insert("", tk.END, values=values)


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

widgets2_frame = ttk.LabelFrame(leftFrame, text="Paste Playlists",padding=(20, 10))
widgets2_frame.grid(row=0, column=0, padx=20, pady=20, sticky="new")

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
widgets3_frame = ttk.LabelFrame(leftFrame, text="Save New Playlist",padding=(20, 10))
widgets3_frame.grid(row=1, column=0, padx=20, pady=20, sticky="new")

playlistName_entry = ttk.Entry(widgets3_frame)
playlistName_entry.insert(0, "Name Playlist")
playlistName_entry.bind("<FocusIn>", lambda e: on_focus_in(e, playlistName_entry, "Name Playlist"))
playlistName_entry.bind("<FocusOut>", lambda e: on_focus_out(e, playlistName_entry, "Name Playlist"))
playlistName_entry.grid(row=0, column=0, padx=5, pady=(0, 5), sticky="ew")


SaveButton = ttk.Button(widgets3_frame, text="Save", style="Accent.TButton", command=savePlaylistName)
SaveButton.grid(row=2, column=0, padx=5, pady=(0, 5), sticky="ew")




#############################
rightFrame = ttk.Frame(tab1)
rightFrame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
buttonsFrame = ttk.Frame(rightFrame)
buttonsFrame.grid(row=0, column=0, sticky="nsew")

mergeButton = ttk.Button(buttonsFrame, text="Merge", style="Accent.TButton", command=mergePlaylistsUI)
mergeButton.grid(row=0, column=0, padx = (0,20),pady=(20,0))

recommendButton = ttk.Button(buttonsFrame, text="Add Recommended", style="Accent.TButton", command=runRecommendUI)
recommendButton.grid(row=0, column=1, padx=20,pady=(20,0))

combo_list = ["Sort By", "Title", "Album", "Artist", "SongID"]
combobox = ttk.Combobox(buttonsFrame, state="readonly", values=combo_list)
combobox.current(0)
combobox.grid(row=0, column=2, padx=20,pady=(20,0), sticky="ew")
combobox.bind("<<ComboboxSelected>>", combobox_callback1)

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

MiniFrame = ttk.Frame(rightFrame)
MiniFrame.grid(row=3, column=0, padx=5, pady=5, sticky="nsew")

button1 = ttk.Button(MiniFrame, text="Add", style="Accent.TButton", command=addSong)
button1.grid(row=0, column=0, padx = (40,0),pady=(0,0))


button2 = ttk.Button(MiniFrame, text="Delete", style="Accent.TButton", command=deleteSong)
button2.grid(row=0, column=1, padx = (40,0),pady=(0,0))



##########################################################################################
tab2 = ttk.Frame(windowFrameNotebook)

windowFrameNotebook.add(tab2, text="Search")
leftFrame2 = ttk.Frame(tab2)
leftFrame2.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

#############################
widgets_frame2 = ttk.LabelFrame(leftFrame2, text="Search Database",padding=(20, 10))
widgets_frame2.grid(row=1, column=0, padx=20, pady=20, sticky="new")

searchFields = ["Song Title", "Artist", "Album", "Title ID", "Danceability", "Energy", 
          "Loudness", "Speechiness", "Instrumentalness", "Liveness"]

entries = []
for i, text in enumerate(searchFields):
    dbentry = ttk.Entry(widgets_frame2)
    dbentry.insert(0, text)
    dbentry.bind("<FocusIn>", lambda e, entry=dbentry, text=text: on_focus_in(e, entry, text))
    dbentry.bind("<FocusOut>", lambda e, entry=dbentry, text=text: on_focus_out(e, entry, text))
    dbentry.grid(row=i, column=0, padx=5, pady=(0, 5), sticky="nsew")
    entries.append(dbentry)


searchButton2 = ttk.Button(widgets_frame2, text="Search", style="Accent.TButton",command=searchDatabaseUI)
searchButton2.grid(row=11, column=0, padx=5, pady=(0, 5), sticky="nsew")

#############################
rightFrame2 = ttk.Frame(tab2)
rightFrame2.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
buttonsFrame2 = ttk.Frame(rightFrame2)
buttonsFrame2.grid(row=0, column=0, sticky="nsew")



combo_list2 = ["Sort By", "Artist", "Album", "Title", "SongID"]
combobox2 = ttk.Combobox(buttonsFrame2, state="readonly", values=combo_list2)
combobox2.current(0)
combobox2.grid(row=2, column=2, padx=20,pady=(20,0), sticky="ew")
combobox2.bind("<<ComboboxSelected>>", combobox_callback2)


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

button1 = ttk.Button(MiniFrame, text="Add", style="Accent.TButton", command=add_song_from_search)
button1.grid(row=0, column=0, padx = (40,0),pady=(0,0))

########################################
tab3 = ttk.Frame(windowFrameNotebook)
windowFrameNotebook.add(tab3, text="View Playlists")


leftFrame3 = ttk.Frame(tab3)
leftFrame3.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

#############################
widgets_frame3 = ttk.LabelFrame(leftFrame3, text="Spotify user ID",padding=(20, 10))
widgets_frame3.grid(row=1, column=0, padx=20, pady=20, sticky="new")


searchUserPlaylist_entry = ttk.Entry(widgets_frame3)
searchUserPlaylist_entry.insert(0, "User ID")
searchUserPlaylist_entry.bind("<FocusIn>", lambda e: on_focus_in(e, searchUserPlaylist_entry, "User ID"))
searchUserPlaylist_entry.bind("<FocusOut>", lambda e: on_focus_out(e, searchUserPlaylist_entry, "User ID"))
searchUserPlaylist_entry.grid(row=0, column=0, padx=5, pady=(0, 5), sticky="nsew")


def searchUserPlaylist():
    global playlists
    user_spotify_id = searchUserPlaylist_entry.get()  # Replace with the desired Spotify user ID

    # Clear the searchTreeView
    searchTreeView3.delete(*searchTreeView3.get_children())

    # Call the getPlaylistFromUser function
    playlists = getPlaylistFromUser(user_spotify_id)
    print (playlists)
    # Display the playlists in the searchTreeView
    for playlist in playlists:
        name = playlist['name']
        playlist_id = playlist['id']
        searchTreeView3.insert("", "end", values=(name, " ", playlist_id))


# Modify the searchButton3 command

searchButton3 = ttk.Button(widgets_frame3, text="Search", style="Accent.TButton",command=searchUserPlaylist)
searchButton3.grid(row=2, column=0, padx=5, pady=(0, 5), sticky="nsew")

#############################
rightFrame3 = ttk.Frame(tab3)
rightFrame3.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

separator1 = ttk.Separator(rightFrame3)
separator1.grid(row=0, column=0, pady=(20,0), sticky="ew")





############################# 


NotebookPlaylist3 = ttk.Notebook(rightFrame3)
NotebookPlaylist3.grid(row=1, column=0, padx=(0,20), pady=20, sticky="nsew")

OnlinePlaylistFrame1 = ttk.LabelFrame(NotebookPlaylist3, width=200, height=200,style="Accent.TFrame")
OnlinePlaylistFrame1.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
LocalPlaylistFrame2 = ttk.LabelFrame(NotebookPlaylist3, width=200, height=200,style="Accent.TFrame")
LocalPlaylistFrame2.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

NotebookPlaylist3.add(OnlinePlaylistFrame1, text="Spotify Playlists")
NotebookPlaylist3.add(LocalPlaylistFrame2, text="Local Playlists")
NotebookPlaylist3.bind("<<NotebookTabChanged>>", on_tab_changed)

#############################


cols = ("Name"," ","PlaylistID")
searchTreeView3 = ttk.Treeview(OnlinePlaylistFrame1, show="headings", columns=cols, height=13)


for col in cols:
    searchTreeView3.heading(col, text=col)
    searchTreeView3.column(col, width=100)

scrollbarS = ttk.Scrollbar(OnlinePlaylistFrame1, orient="vertical", command=searchTreeView3.yview)
searchTreeView3.configure(yscrollcommand=scrollbarS.set)
searchTreeView3.grid(row=0, column=0, sticky="nsew")
scrollbarS.grid(row=0, column=1, sticky="ns")  




cols1 = ("Name", " ")
searchTreeView4 = ttk.Treeview(LocalPlaylistFrame2, show="headings", columns=cols, height=13)

for col in cols1:
    searchTreeView4.heading(col, text=col)
    searchTreeView4.column(col, width=100)

scrollbarS = ttk.Scrollbar(LocalPlaylistFrame2, orient="vertical", command=searchTreeView4.yview)
searchTreeView4.configure(yscrollcommand=scrollbarS.set)
searchTreeView4.grid(row=0, column=0, sticky="nsew")
scrollbarS.grid(row=0, column=1, sticky="ns")


#############################
buttonsFrame3 = ttk.Frame(OnlinePlaylistFrame1)
buttonsFrame3.grid(row=1, column=0, sticky="nsew")

buttonsFrame4 = ttk.Frame(LocalPlaylistFrame2)
buttonsFrame4.grid(row=1, column=0, sticky="nsew")

iPlaylist1B = ttk.Button(buttonsFrame3, text="Playlist 1", style="Accent.TButton", command=lambda: importFromPlaylistID(1))
iPlaylist1B.grid(row=0, column=0, padx = (40,0),pady=(0,0))

iPlaylist2B = ttk.Button(buttonsFrame3, text="Playlist 2", style="Accent.TButton", command=lambda: importFromPlaylistID(2))
iPlaylist2B.grid(row=0, column=1, padx = (40,0),pady=(0,0))

LiPlaylist1B = ttk.Button(buttonsFrame4, text="Playlist 1", style="Accent.TButton", command=importLocalPlaylist1)
LiPlaylist1B.grid(row=0, column=0, padx = (40,0),pady=(0,0))

LiPlaylist2B = ttk.Button(buttonsFrame4, text="Playlist 2", style="Accent.TButton", command=importLocalPlaylist2)
LiPlaylist2B.grid(row=0, column=1, padx = (40,0),pady=(0,0))

deletePlaylistB = ttk.Button(buttonsFrame4, text="Delete", style="Accent.TButton", command=deletePlaylist)
deletePlaylistB.grid(row=0, column=2, padx = (40,0),pady=(0,0))


root.mainloop()