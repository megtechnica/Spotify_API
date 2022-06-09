from pprint import pprint
import json
import numpy as np
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotify import get_artist_uri, get_artist_albums, remove_live_and_remastered_albums, get_full_tracklist, get_audio_features_dict

import matplotlib.pyplot as plt

import seaborn as sns

credentials = open("credentials.json")

credentials = json.load(credentials)

client_credentials_manager = SpotifyClientCredentials(client_id=credentials['ClientID'],
                                                      client_secret=credentials['ClientSecret'])
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

name = 'Bolt Thrower'


artist_uri = get_artist_uri(name, sp)
artist_albums = get_artist_albums(artist_uri, sp)
artist_albums_uri = remove_live_and_remastered_albums(artist_albums, sp)
full_tracklist = get_full_tracklist(artist_albums_uri, sp)
audio_features = get_audio_features_dict(full_tracklist, sp)

audio_features_dict = get_audio_features_dict(full_tracklist, sp)

temp_df1 = pd.DataFrame(full_tracklist.items(), columns = ['title', 'uri'])
temp_df2 = pd.DataFrame(audio_features_dict.items(), columns = ['uri', 'features'])
assert len(temp_df1) == len(temp_df2)
song_data = pd.merge(temp_df1, temp_df2, on=['uri'])

song_data['energy'] = song_data['uri'].apply(lambda x: audio_features_dict[x]['energy'])
song_data['valence'] = song_data['uri'].apply(lambda x: audio_features_dict[x]['valence'])
song_data['danceability'] = song_data['uri'].apply(lambda x: audio_features_dict[x]['danceability'])
song_data.drop('features', axis=1, inplace=True)


fig, axes = plt.subplots(nrows=1, ncols=3, sharex=True, figsize=(16,4))
sns.displot(song_data['valence'], hist_kws={'edgecolor': 'grey'},ax=axes[0])
sns.displot(song_data['energy'], hist_kws={'edgecolor': 'grey'}, ax=axes[1])
sns.displot(song_data['danceability'],hist_kws={'edgecolor': 'grey'},
             color="grey", ax=axes[2])

axes[0].set_xlabel('Valence', fontsize='large')
axes[1].set_xlabel('Energy', fontsize='large')
axes[2].set_xlabel('Danceability', fontsize='large')
axes[0].set_ylabel('Frequency', fontsize='large')