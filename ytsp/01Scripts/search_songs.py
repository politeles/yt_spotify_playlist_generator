import argparse
import os
import json
from dotenv import load_dotenv,find_dotenv

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials


import file_json as fj


# create a playlist in spotify with the songs specified in the songs list
def create_playlist(name:str, songs:list)->None:
    print("creating playlist...")
    sp_client_id = os.environ.get("SPOTIPY_CLIENT_ID")
    sp_client_secret = os.environ.get("SPOTIPY_CLIENT_SECRET")
    sp_redirect_uri = os.environ.get("SPOTIPY_REDIRECT_URI")
    print(sp_redirect_uri)
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="playlist-modify-public",client_id=sp_client_id,client_secret=sp_client_secret,redirect_uri=sp_redirect_uri))
    user = sp.current_user()['id']
    listid = sp.user_playlist_create(user=user, name=name, public=True, collaborative=False, description="playlist del vídeo "+name)
    print("adding songs to playlist...")
    for song in songs:
        sp.user_playlist_add_tracks(user=user, playlist_id=listid["id"], tracks=[song], position=None)



def main():
    parser = argparse.ArgumentParser(description='Search song in spotify')
    parser.add_argument('file', help='The file that contains the songs to search')
    args = parser.parse_args()
    file = args.file
    print("loading file info...")
    songs = fj.read_json(file)
    print(type(songs))
    print("loading environment variables...")
    _ = load_dotenv(find_dotenv())
    sp_client_id = os.environ.get("SPOTIPY_CLIENT_ID")
    sp_client_secret = os.environ.get("SPOTIPY_CLIENT_SECRET")
    sp_redirect_uri = os.environ.get("SPOTIPY_REDIRECT_URI")


    spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=sp_client_id, client_secret=sp_client_secret))
    # search in spotify for the album specified in the songs list
    all_tracks = []
    for song in songs:
        print("searching song...")
        results = spotify.search(q='album:'+song["album"]+' artist:'+song['artist'], limit=10, offset=0, type='track', market='ES')
      
        if len(results['tracks']['items']) > 0:
            all_tracks.append(results['tracks']['items'][0]['id'])
    fj.write_json( all_tracks ,"songs/"+file+".json")
    create_playlist(spotify,"Las mejores obras de Miles Davis",all_tracks)


    



if __name__ == "__main__":
    main()