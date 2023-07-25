import json
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotify import get_artist_uri, get_artist_albums, get_full_tracklist, get_audio_features_dict, merge_song_data, get_clean_album_uri_list, calculate_brutality
import matplotlib.pyplot as plt
import seaborn as sns

credentials = open("credentials.json")
credentials = json.load(credentials)
client_credentials_manager = SpotifyClientCredentials(client_id=credentials['ClientID'],
                                                      client_secret=credentials['ClientSecret'])

sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
band_names = ['Cannibal Corpse']

for name in band_names:
    artist_uri = get_artist_uri(name, sp)
    artist_albums = get_artist_albums(artist_uri, sp)

    artist_albums_uri = get_clean_album_uri_list(artist_albums)
    full_tracklist = get_full_tracklist(artist_albums_uri, sp)
    audio_features = get_audio_features_dict(full_tracklist, sp)

    df1 = pd.DataFrame(full_tracklist.items(), columns=['title', 'uri'])
    df2 = pd.DataFrame(audio_features.items(), columns=['uri', 'features'])
    assert len(df1) == len(df2)
    song_data = pd.merge(df1, df2, on=['uri'])
    song_data = merge_song_data(song_data, audio_features)

    # drop live songs
    song_data = song_data.drop(song_data[song_data.liveness > .8].index)
    song_data.to_csv('data/' + name + ' - Song Data.csv')
    song_data_statistics = song_data.describe()
    song_data_statistics.to_csv('data/' + name + ' - Summary Statistics.csv')
    song_data['sonic brutality'] = song_data.apply(lambda x: calculate_brutality(x), axis=1)

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

    sns.displot(song_data['sonic brutality'])
    plt.savefig('figures/' + name + ' - Sonic Brutality Figure')
    plt.clf()