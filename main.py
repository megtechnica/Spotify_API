import json
from pprint import pprint
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotify import get_artist_uri, get_artist_albums, get_full_tracklist_uris, get_audio_features_dict, get_clean_album_uri_list, merge_song_data
import matplotlib.pyplot as plt
import seaborn as sns

credentials = open("credentials.json")
credentials = json.load(credentials)
client_credentials_manager = SpotifyClientCredentials(client_id=credentials['ClientID'],
                                                      client_secret=credentials['ClientSecret'])

sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
band_names = ['Phil Collins']

for name in band_names:
    artist_uri = get_artist_uri(name, sp)
    artist_albums, artist_albums_uris = get_artist_albums(artist_uri, sp)
    full_tracklist = get_full_tracklist_uris(artist_albums, sp)
    audio_features = get_audio_features_dict(full_tracklist, sp)
    # df1 = pd.DataFrame(full_tracklist.items(), columns=['title', 'uri'])
    # df2 = pd.DataFrame(audio_features.items(), columns=['title', 'features'])
    # print(df1.head())
    # print(df2.head())
    # # assert len(df1) == len(df2)
    # song_data = pd.merge(df1, df2, on=['uri'])
    # song_data = merge_song_data(song_data, audio_features)

