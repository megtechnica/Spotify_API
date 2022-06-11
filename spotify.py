from pprint import pprint

def get_artist_uri(name, sp):
    results = sp.search(q='artist:' + name, type='artist')
    items = results['artists']['items']
    artist_uri = items[0]['uri']
    return artist_uri

def get_artist_albums(artist_uri, sp):
    albums = {}
    results = sp.artist_albums(artist_uri, album_type='album', limit=25)

    for i, item in enumerate(results['items']):
        if 'US' in item['available_markets']:
            albums[item['name'].title()] = item['uri']

    return albums

def get_clean_album_uri_list(artist_albums):
    artist_albums_uri = [uri for uri in artist_albums.values()]
    return artist_albums_uri

def get_full_tracklist(artist_albums_uri, sp):
    tracklist = {}
    for album_uri in artist_albums_uri:
        album = sp.album(album_uri)
        for track in album['tracks']['items']:
            tracklist[track['name'].title()] = track['uri']
    return tracklist

def get_audio_features_dict(full_tracklist, sp):
    audio_features_dict = {}
    for uri in list(full_tracklist.values()):
        features = sp.audio_features(uri)
        audio_features_dict[uri] = {'energy': features[0]['energy'],
                                    'valence': features[0]['valence'],
                                    'danceability': features[0]['danceability'],
                                    'tempo': features[0]['tempo'],
                                    'liveness': features[0]['liveness']
                                    }
    return audio_features_dict

def merge_song_data(song_data: dict, audio_features_dict: dict) -> dict:

    song_data['energy'] = song_data['uri'].apply(lambda x: audio_features_dict[x]['energy'])
    song_data['valence'] = song_data['uri'].apply(lambda x: audio_features_dict[x]['valence'])
    song_data['danceability'] = song_data['uri'].apply(lambda x: audio_features_dict[x]['danceability'])
    song_data['tempo'] = song_data['uri'].apply(lambda x: audio_features_dict[x]['tempo'])
    song_data['liveness'] = song_data['uri'].apply(lambda x: audio_features_dict[x]['liveness'])
    song_data.drop('features', axis=1, inplace=True)
    return song_data

def calculate_brutality(song_data):
    sb = ((1 - song_data['valence']) + song_data['energy']) / 2
    return sb
