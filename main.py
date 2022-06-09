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


artist_uri = get_artist_uri(name, sp)
artist_albums = get_artist_albums(artist_uri, sp)

artist_albums_uri = remove_live_and_remastered_albums(artist_albums, sp)

full_tracklist = get_full_tracklist(artist_albums_uri, sp)

print("Total tracks:", len(full_tracklist))
