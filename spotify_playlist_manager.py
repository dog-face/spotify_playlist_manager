#!/usr/bin/python

import sys
import spotipy
import spotipy.util as util

def get_playlist_tracks(current_user_id, playlist_id):
    playlist_tracks = []
    offset = 0
    more_tracks = True
    while more_tracks:
        playlist = sp.user_playlist_tracks(current_user_id, playlist_id, limit=100, offset=offset)
        print(str(offset) + ", " + str(len(playlist['items'])))
        for item in playlist['items']:
            track_id = item['track']['id']
            if track_id is not None:
                playlist_tracks.append(track_id)
        offset += 100
        if len(playlist['items']) != 100:
            more_tracks = False
    return playlist_tracks

def get_library_tracks(current_user_id):
    library_tracks = []
    offset = 0
    more_tracks = True
    while more_tracks:
        library = sp.current_user_saved_tracks(limit=50, offset=offset)
        print(str(offset) + ", " + str(len(library['items'])))
        for item in library['items']:
            track_id = item['track']['id']
            if track_id is not None:
                library_tracks.append(track_id)
        offset += 50
        if len(library['items']) != 50:
            more_tracks = False
    return library_tracks
            


scope = 'user-library-modify playlist-modify-public'

if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    print "Usage: %s username" % (sys.argv[0],)
    sys.exit()
    
credentials_ini = open('credentials.ini', 'r')
credentials = {}
for line in credentials_ini:
    line = line.strip().split('=')
    credentials[line[0]] = line[1]
    

token = util.prompt_for_user_token(username, scope, client_id=credentials['client_id'],
	client_secret=credentials['client_secret'], redirect_uri=credentials['redirect_uri'])

if token:
    sp = spotipy.Spotify(auth=token)
    current_user_id = sp.current_user()['id']
    playlists = sp.current_user_playlists()
    for item in playlists['items']:
        if item['name'] == 'Current Favorites':
            current_favorites_id = item['id']
        elif item['name'] == 'Starred':
            playlist_id = item['id']
        
    print("Getting current favorites tracks")
    current_favorites_tracks = get_playlist_tracks(current_user_id, current_favorites_id)
            
    print("Getting starred tracks")
    starred_tracks = get_playlist_tracks(current_user_id, playlist_id)
    
        
    print("Getting library tracks")
    library_tracks = get_library_tracks(current_user_id)
    
        
    for track in current_favorites_tracks:
        if track not in starred_tracks:
            sp.user_playlist_add_tracks(current_user_id, playlist_id, [track])
        if track not in library_tracks:
            sp.current_user_saved_tracks_add([track])
        
    



else:
    print "Can't get token for", username