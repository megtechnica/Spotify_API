import json
from pprint import pprint
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotify import get_artist_uri, get_artist_albums, get_full_tracklist, get_audio_features_dict
import matplotlib.pyplot as plt
import seaborn as sns

credentials = open("credentials.json")
credentials = json.load(credentials)
client_credentials_manager = SpotifyClientCredentials(client_id=credentials['ClientID'],
                                                      client_secret=credentials['ClientSecret'])

sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
band_names = ['Phil Collins', 'Elton John']

for name in band_names:
    artist_uri = get_artist_uri(name, sp)
    artist_albums = get_artist_albums(artist_uri, sp)
    artist_tracks = get_full_tracklist(artist_albums, sp)
    tracklist_by_album = get_full_tracklist(artist_albums, sp)
    tracklist_with_audio_features = get_audio_features_dict(tracklist_by_album, sp)

