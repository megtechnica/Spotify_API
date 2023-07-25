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
    pprint(results)
    for i, item in enumerate(results['items']):
        pprint(item)
        if 'US' in item['available_markets']:
            albums[item['name'].title()] = item['uri']
    """{album name : uri}"""
    return albums

def get_full_tracklist(artist_albums, sp):
    tracklist_by_album = {}
    for album in artist_albums.keys():
        tracklist = []
        album_contents = sp.album(artist_albums[album])
        for track in album_contents['tracks']['items']:
            tracklist.append(track['uri'])
        tracklist_by_album[album] = tracklist
    """{album name:[list of uris]}"""
    return tracklist_by_album

# def calculate_brutality(song_data):
#     sb = ((1 - song_data['valence']) + song_data['energy']) / 2
#     return sb

def get_audio_features_dict(tracklist_by_album, sp):
    audio_features_dict = {}
    for album_name in tracklist_by_album.keys():
        track_uris = tracklist_by_album[album_name]
        track_audio_features = []
        for uri in track_uris:
            features = sp.audio_features(uri)
            track_audio_features_dict = {'energy': features[0]['energy'],
                                    'valence': features[0]['valence'],
                                    'danceability': features[0]['danceability'],
                                    'tempo': features[0]['tempo'],
                                    'liveness': features[0]['liveness'],
                                    }
            track_audio_features.append(track_audio_features_dict)
        audio_features_dict[album_name] = track_audio_features

    """{album title : [{danceability: int}]"""
    return audio_features_dict

