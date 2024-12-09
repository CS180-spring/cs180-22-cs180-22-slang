import random
import recommend
from typing import List
import pandas as pd

class Song:
    def __init__(self, songName, albumName, artistName, coords):
        self.name = songName
        self.cluster = 0  # initially doesn't belong to any cluster
        self.coordinates = coords
        self.dimensions = len(coords)
        self.album = albumName
        self.artist = artistName


    def set_cluster(self, cluster_num: int):
        self.cluster = cluster_num

    def get_cluster(self) -> int:
        return self.cluster

    def get_name(self) -> str:
        return self.name

    def get_coords(self):
        return self.coordinates

    def get_coord(self, index: int) -> float:
        return self.coordinates[index]
    
    def get_dimensions(self):
        return self.dimensions


class Cluster:
    def __init__(self, num, cent: Song):
        self.cluster_number = num
        self.center = cent.get_coords()
        self.songs = []

        # we want to add the center to the cluster so we know where the center is for the
        # next round of calculations
        self.add_song(cent)

    def add_song(self, new_song: Song):
        new_song.set_cluster(self.cluster_number)
        self.songs.append(new_song)

    def remove_song(self, song_name: str) -> bool:
        for i, song in enumerate(self.songs):
            if song.get_name() == song_name:
                self.songs.pop(i)
                return True
        return False

    def get_song(self, index: int) -> Song:
        return self.songs[index]

    def get_size(self) -> int:
        return len(self.songs)

    def set_center(self, index: int, value: float):
        self.center[index] = value

    def get_center(self):
        return self.center
    
    def get_cluster_number(self):
        return self.cluster_number
    


class kMeans:
    def __init__(self, K: int, num_of_iterations: int, output_loc: str):
        self.k = int(K)
        self.iterations = num_of_iterations
        self.output_file = output_loc
        self.dimensions = None
        self.total_songs = None
        self.clusters = []

    def get_nearest_cluster(self, song: Song) -> int:
        sum = 0.0
        shortestPath = 0
        nearest = 0
        if self.dimensions == 1:
            shortestPath = abs(self.clusters[0].get_center()[0], - song.get_coord(0))
        else:
            i = 0
            while i < self.dimensions:
                sum += pow(self.clusters[0].get_center()[i] - song.get_coord(i), 2)
                i +=1
            shortestPath = pow(sum, 0.5)
        nearest = self.clusters[0].get_cluster_number()

        i = 1
        while i < self.k:
            sum = 0.0
            if self.dimensions == 1:
                distance = abs(self.clusters[i].get_center[0] - song.get_coord(0))
            else:
                j = 0
                while j < self.dimensions:
                    sum += pow(self.clusters[i].get_center()[j] - song.get_coord(j), 2)
                    j +=1
                distance = pow(sum, 0.5)
            
            if distance < shortestPath:
                shortestPath = distance
                nearest = self.clusters[i].get_cluster_number()
            i += 1

        return nearest
    
    def clear_clusters(self) -> None:
        for i in range(self.k):
            self.clusters[i].songs = []

    def classify(self, all_songs: List[Song], total_playlist):
        self.total_songs = len(all_songs)
        self.dimensions = all_songs[0].get_dimensions()

        used_songs = []

        # make k clusters and pick a random song to put in each. These random songs
        # will act as the cluster centers for now
        for i in range(1, self.k+1):
            while True:
                index = random.randint(0, self.total_songs-1)
                temp_song = all_songs[index].get_name()
                if temp_song not in used_songs:
                    used_songs.append(temp_song)
                    all_songs[index].set_cluster(i)
                    new_cluster = Cluster(i, all_songs[index])
                    self.clusters.append(new_cluster)
                    break

        it_Num = 1
        while True:
            done = True
            for i in range(self.total_songs):
                curr_cluster = all_songs[i].get_cluster()
                nearest_cluster = self.get_nearest_cluster(all_songs[i])
                if curr_cluster != nearest_cluster:
                    all_songs[i].set_cluster(nearest_cluster)
                    done = False

            # clear the clusters and reassign based on what we found above
            self.clear_clusters()
            for i in range(self.total_songs):
                temp_cluster = self.clusters[all_songs[i].get_cluster() - 1]
                temp_cluster.add_song(all_songs[i])

            # recalculate the cluster centers
            for i in range(self.k):
                size = self.clusters[i].get_size()
                for j in range(self.dimensions):
                    sum = 0
                    if size > 0:
                        for l in range(size):
                            sum += self.clusters[i].get_song(l).get_coord(j)
                        self.clusters[i].set_center(j, sum / size)

            if done or it_Num >= self.iterations:
                break
            it_Num += 1

        with_clusters = total_playlist.copy()
        cluster_numbers = [song.get_cluster() for song in all_songs]
        with_clusters.loc[:, 'cluster_number'] = cluster_numbers
        # with_clusters.to_csv(self.output_file, index = False)
        return with_clusters

class Classify:
    def run_classification(playlist1, playlist2, mergedLoc):
        both_playlist = pd.concat([playlist1, playlist2], ignore_index= True)
        songs = []
        for index, row in both_playlist.iterrows():
            temp_cords = [row["danceability"], row["energy"], row["loudness"], row["speechiness"], row["instrumentalness"], row["liveness"]]
            new_Song = Song(row["track_name"], row["album"], row["artist"], temp_cords)
            songs.append(new_Song)

        iterations = 1000
        merge = kMeans(3, iterations, mergedLoc)
        merged = merge.classify(songs, both_playlist)

        clusters = merged["cluster_number"].unique()
        options = []
        for cluster in clusters:
            temp_df = merged.loc[merged["cluster_number"] == cluster]
            options.append(temp_df)
        max_len = len(options[0])
        max_i = 0
        i = 0
        for option in options:
            if len(option) > max_len:
                max_len = len(option)
                max_i = i
            i += 1
        return options[max_i].drop("cluster_number", axis = 1)
