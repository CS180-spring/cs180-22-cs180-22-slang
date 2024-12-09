import pandas as pd

def generalize(input_df):
    generalized = input_df.copy()
    danceability_avg = generalized["danceability"].mean()
    energy_avg = generalized["energy"].mean()
    loudness_avg = generalized["loudness"].mean()
    speechiness_avg = generalized["speechiness"].mean()
    instrumentalness_avg = generalized["instrumentalness"].mean()
    liveness_avg = generalized["liveness"].mean()
    average = [danceability_avg, energy_avg, loudness_avg, speechiness_avg, instrumentalness_avg, liveness_avg]
    return average
def recommend(input, library_df):
    general = generalize(input)
    rounded = []
    for decimal in general:
        rounding = round(decimal, 1)
        rounded.append(rounding)

    #temp search until we get search.py finished
    recs = library_df.loc[(round(library_df["danceability"], 1) == rounded[0]) & (round(library_df["energy"], 1) == rounded[1])
                          & (round(library_df["loudness"], 1) == rounded[2]) & (round(library_df["speechiness"], 1) == rounded[3])
                          & (round(library_df["instrumentalness"], 1) == rounded[4]) & (round(library_df["liveness"], 1) == rounded[5])]
    return recs
