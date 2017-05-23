#!/usr/bin/python

import sys
import spotipy
import spotipy.util as util

scope = 'user-library-read'

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
    results = sp.current_user_saved_tracks()
    for item in results['items']:
        track = item['track']
        print track['name'] + ' - ' + track['artists'][0]['name']
else:
    print "Can't get token for", username