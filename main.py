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

name = 'Sepultura'

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
        if 'US' in item['available_markets']:
            albums[item['name'].title()] = item['uri']

    return albums

def get_full_tracklist_dict(artist_albums_uri):
    tracklist = {}
    for album_uri in artist_albums_uri:
        album = sp.album(album_uri)
        for track in album['tracks']['items']:
            tracklist[track['name'].title()] = track['uri']
    return tracklist

def get_clean_album_uri_list(artist_albums, albums_to_delete):
    if albums_to_delete is not None:
        for key in albums_to_delete:
            artist_albums.pop(key)
    artist_albums_uri = [uri for uri in artist_albums.values()]
    return artist_albums_uri



artist_uri = get_artist_uri(name)
artist_albums = get_artist_albums(artist_uri)

albums_to_delete =[]
artist_albums_uri = get_clean_album_uri_list(artist_albums, albums_to_delete)
full_tracklist = get_full_tracklist_dict(artist_albums_uri)
print(list(full_tracklist.items()))
print("Total tracks:", len(full_tracklist))
