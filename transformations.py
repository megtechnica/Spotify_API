import pandas as pd

def track_audio_features_to_df(albums_tracks_audio_features_dict):
    # {'Daemon (Bonus Tracks Version)': {'Aeon Daemonium': {'danceability': 0.309,
    #                                                       'energy': 0.958,
    #                                                       'loudness': -8.47,
    #                                                       'tempo': 156.041,
    #                                                       'valence': 0.0387},
    album_audio_features_flattened = {}
    for album in albums_tracks_audio_features_dict.keys():
        for track in albums_tracks_audio_features_dict[album].keys():
            album_audio_features_flattened = {'track_title': track,
                                                'danceability': albums_tracks_audio_features_dict[album][track]['danceability'],
                                                'energy': albums_tracks_audio_features_dict[album][track]['energy'],
                                                'loudness': albums_tracks_audio_features_dict[album][track]['loudness'],
                                                'tempo': albums_tracks_audio_features_dict[album][track]['tempo'],
                                                'valence': albums_tracks_audio_features_dict[album][track]['valence'],
                                              'album': album}
            print(album_audio_features_flattened)
