from pprint import pprint
import json
import numpy as np
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

credentials = open("credentials.json")

credentials = json.load(credentials)

client_credentials_manager = SpotifyClientCredentials(client_id=credentials['ClientID'],
                                                      client_secret=credentials['ClientSecret'])
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

name = 'Cannibal Corpse'

def get_artist_uri(name):
    results = sp.search(q='artist:' + name, type='artist')
    items = results['artists']['items']
    artist_uri = items[0]['uri']
    return artist_uri

# results = sp.search(q=artist, limit=50, type='track')
# for i, t in enumerate(results['tracks']['items']):
#     print(' ', i, t['name'])

def get_artist_albums(artist_uri):
    albums = {}
    results = sp.artist_albums(artist_uri, album_type='album', limit=25)
    for i, item in enumerate(results['items']):
        albums[item['name'].title()] = item['uri']
    return albums

artist_uri = get_artist_uri(name)
artist_albums = get_artist_albums(artist_uri)