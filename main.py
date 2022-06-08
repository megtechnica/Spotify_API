from pprint import pprint
import json
import numpy as np
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import credentials


import matplotlib.pyplot as plt

SPOTIPY_CLIENT_ID = credentials.client_id
SPOTIPY_CLIENT_SECRET = credentials.client_secret

client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID,
                                                      client_secret=SPOTIPY_CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_artist_uri(name):
    results = sp.search(q='artist:' + name, type='artist')
    items = results['artists']['items']
    artist_uri = items[0]['uri']
    return artist_uri

artist_uri = get_artist_uri(name)

results = sp.search(q=artist, limit=50, type='track')
for i, t in enumerate(results['tracks']['items']):
    print(' ', i, t['name'])


def get_artist_albums(artist_uri):
    albums = {}
    results = sp.artist_albums(artist_uri, album_type='album', limit=25)
    for i, item in enumerate(results['items']):
        albums[item['name'].title()] = item['uri']
    return albums