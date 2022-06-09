from pprint import pprint
import json
import numpy as np
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotify import get_artist_uri, get_artist_albums, remove_live_and_remastered_albums, get_full_tracklist

credentials = open("credentials.json")

credentials = json.load(credentials)

client_credentials_manager = SpotifyClientCredentials(client_id=credentials['ClientID'],
                                                      client_secret=credentials['ClientSecret'])
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

name = 'Bolt Thrower'

# def get_artist_uri(name):
#     results = sp.search(q='artist:' + name, type='artist')
#     items = results['artists']['items']
#     artist_uri = items[0]['uri']
#     return artist_uri

# results = sp.search(q=artist, limit=50, type='track')
# for i, t in enumerate(results['tracks']['items']):
#     print(' ', i, t['name'])

# def get_artist_albums(artist_uri):
#     albums = {}
#     results = sp.artist_albums(artist_uri, album_type='album', limit=25)
#
#     for i, item in enumerate(results['items']):
#         if 'US' in item['available_markets']:
#             albums[item['name'].title()] = item['uri']
#
#     return albums

# def get_full_tracklist_dict(artist_albums_uri):
#     tracklist = {}
#     for album_uri in artist_albums_uri:
#         album = sp.album(album_uri)
#         for track in album['tracks']['items']:
#             tracklist[track['name'].title()] = track['uri']
#     return tracklist




artist_uri = get_artist_uri(name, sp)
artist_albums = get_artist_albums(artist_uri, sp)

artist_albums_uri = remove_live_and_remastered_albums(artist_albums, sp)

full_tracklist = get_full_tracklist(artist_albums_uri, sp)

print("Total tracks:", len(full_tracklist))
