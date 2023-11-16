from pprint import pprint

def get_artist_uri(name, sp):
    results = sp.search(q='artist:' + name, type='artist')
    items = results['artists']['items']
    artist_uri = items[0]['uri']
    # returns spotify:artist:0yLwGBQiBqhXOvmTfH2A7n
    return artist_uri

def get_artist_albums(artist_uri, sp):
    albums = {}
    results = sp.artist_albums(artist_uri, album_type='album')
    for i, item in enumerate(results['items']):
        if ('deluxe' in item['name'].lower()) or ('live' in item['name'].lower()):
            continue
        if 'US' in item['available_markets']:
            albums[item['name'].title()] = {'uri': item['uri'], 'release_date': item['release_date']}
    """{album name : {uri: <uri>, release_date: <release_date>}"""
    return albums


def get_full_tracklist_uris(artist_albums, sp):
    for album in artist_albums.keys():
        tracklist = {}
        album_contents = sp.album(artist_albums[album]['uri'])
        for track in album_contents['tracks']['items']:
            tracklist[track['name']] = track['uri']
        artist_albums[album]['tracklist'] = tracklist
    """{album name:{uri: <uri>, release_date: <release_date>, tracklist:{<title>: uri, ....}}"""
    return artist_albums

def get_audio_features_dict(tracklist, sp):
    for track in tracklist.keys():
        print(track)
        audio_features = {}
        track_contents = sp.audio_features(tracklist[track])
        pprint(track_contents)
    return


# def calculate_brutality(song_data):
#     sb = ((1 - song_data['valence']) + song_data['energy']) / 2
#     return sb

# def get_audio_features_dict(tracklist_by_album, sp):
#     audio_features_dict = {}
#     for album_name in tracklist_by_album.keys():
#         track_uris = tracklist_by_album[album_name]
#         track_audio_features = []
#         for uri in track_uris:
#
#             features = sp.audio_features(uri)
#             track_audio_features_dict[uri] = {'energy': features[0]['energy'],
#                                     'valence': features[0]['valence'],
#                                     'danceability': features[0]['danceability'],
#                                     'tempo': features[0]['tempo'],
#                                     'liveness': features[0]['liveness']
#                                     }
#             track_audio_features.append(track_audio_features_dict)
#         audio_features_dict[album_name] = track_audio_features
#
#     """{album title : [{danceability: int}]"""
#     return audio_features_dict

def merge_song_data(song_data: dict, audio_features_dict: dict) -> dict:

    song_data['energy'] = song_data['uri'].apply(lambda x: audio_features_dict[x]['energy'])
    song_data['valence'] = song_data['uri'].apply(lambda x: audio_features_dict[x]['valence'])
    song_data['danceability'] = song_data['uri'].apply(lambda x: audio_features_dict[x]['danceability'])
    song_data['tempo'] = song_data['uri'].apply(lambda x: audio_features_dict[x]['tempo'])
    song_data['liveness'] = song_data['uri'].apply(lambda x: audio_features_dict[x]['liveness'])
    song_data.drop('features', axis=1, inplace=True)
    return song_data
