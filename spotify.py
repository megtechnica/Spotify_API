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

def remove_live_and_remastered_albums(artist_albums, sp):
    key_words = ['Live', 'Edition', 'Sessions']
    all_album_names = list(artist_albums.keys())
    for album in all_album_names:
        for key in key_words:
            if key in album:
                artist_albums.pop(album)

    artist_albums_uri = [uri for uri in artist_albums.values()]
    return artist_albums_uri

def get_full_tracklist(artist_albums_uri, sp):
    tracklist = {}
    for album_uri in artist_albums_uri:
        album = sp.album(album_uri)
        for track in album['tracks']['items']:
            tracklist[track['name'].title()] = track['uri']
    return tracklist
