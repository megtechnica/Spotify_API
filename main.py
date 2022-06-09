from pprint import pprint
import json
import numpy as np
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotify import get_artist_uri, get_artist_albums, remove_live_and_remastered_albums, get_full_tracklist, get_audio_features_dict, merge_song_data

import matplotlib.pyplot as plt

import seaborn as sns

credentials = open("credentials.json")

credentials = json.load(credentials)

client_credentials_manager = SpotifyClientCredentials(client_id=credentials['ClientID'],
                                                      client_secret=credentials['ClientSecret'])
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

band_names = ['Metallica', 'Megadeth']

for name in band_names:
    artist_uri = get_artist_uri(name, sp)
    artist_albums = get_artist_albums(artist_uri, sp)
    artist_albums_uri = remove_live_and_remastered_albums(artist_albums, sp)
    full_tracklist = get_full_tracklist(artist_albums_uri, sp)
    audio_features = get_audio_features_dict(full_tracklist, sp)

    audio_features_dict = get_audio_features_dict(full_tracklist, sp)

    df1 = pd.DataFrame(full_tracklist.items(), columns=['title', 'uri'])
    df2 = pd.DataFrame(audio_features_dict.items(), columns=['uri', 'features'])
    assert len(df1) == len(df2)
    song_data = pd.merge(df1, df2, on=['uri'])

    song_data = merge_song_data(song_data, audio_features_dict, sp)

    song_data_statistics = song_data.describe()

    song_data_statistics.to_csv('data/' + name + ' - Summary Statistics.csv')

    fig, axes = plt.subplots(nrows=1, ncols=3, sharex=True, figsize=(16,4))

    sns.displot(song_data['valence'])
    plt.savefig('figures/' + name + ' - Valence Figure')
    plt.clf()


    sns.displot(song_data['energy'])
    plt.savefig('figures/' + name + ' - Energy Figure')
    plt.clf()

    sns.displot(song_data['danceability'])
    plt.savefig('figures/' + name + ' - Danceability Figure')
    plt.clf()

    sns.displot(song_data['tempo'])
    plt.savefig('figures/' + name + ' - Tempo Figure')
    plt.clf()
