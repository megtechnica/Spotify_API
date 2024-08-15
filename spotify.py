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

def get_album_popularity(album_uri, sp):
    

def get_full_tracklist_uris(artist_albums, sp):
    for album in artist_albums.keys():
        tracklist = {}
        album_contents = sp.album(artist_albums[album]['uri'])
        
        for track in album_contents['tracks']['items']:
            tracklist[track['name']] = track['uri']
        artist_albums[album]['tracklist'] = tracklist
    """{album name:{uri: <uri>, release_date: <release_date>, tracklist:{<title>: uri, ....}}"""
    return artist_albums

def get_audio_features_dict(album_tracklist_uris, sp):
    for album in album_tracklist_uris:
        for track in album_tracklist_uris[album]['tracklist'].keys():
            track_uri = album_tracklist_uris[album]['tracklist'][track]
            audio_features = sp.audio_features(track_uri)
            pprint(audio_features
                   )
            break
            """Wolf'S Lair Abyss (Bonus Tracks)": {'release_date': '2019-07-19',
                                      'tracklist': {'Ancient Skin': 'spotify:track:3wfohgqEFpkMFO0pZZr9Wc',
                                                    'Ancient Skin - May 1997 Recording': 'spotify:track:6dbQHF8RTc3Bye6hkAZ2S4',
                                                    'Fall of Serephs': 'spotify:track:7H401UpfvghFY3H6StYxfb',
                                                    'I Am the Labyrinth': 'spotify:track:2kxrOSUTm4YRisCQGx3P41',
                                                    'Necrolust - May 1997 Recording': 'spotify:track:0rW14sgzhDrZxGVO1dei1i',
                                                    'Symbols of Bloodswords': 'spotify:track:4Ts1LnfdgAchNbGf1EaFV0',
                                                    'The Vortex Void of Inhumanity (Intro)': 'spotify:track:0GUz0uEidryLUqOBJW1jfb'},
                                      'uri': 'spotify:album:2Iwm3Tru1xGW6rEttU61ca'}}"""
    # for album_name in album_tracklist_uris.keys():
    #     for track in album_name.keys():
    #         pprint()
    #     audio_features = {}
    #     track_contents = sp.audio_features(tracklist[track])
    #     pprint(track_contents)
    # return
