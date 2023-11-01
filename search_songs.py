import argparse
from dotenv import load_dotenv,find_dotenv

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials


import file_json as fj


# create a playlist in spotify with the songs specified in the songs list
def create_playlist(spotify,name, songs)->None:
    print("creating playlist...")
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="playlist-modify-public"))
    user = spotify.current_user()['id']

    print(user)
    listid = spotify.user_playlist_create(user=user, name=name, public=True, collaborative=False, description="playlist del vídeo "+name)
    print(listid)
    print("adding songs to playlist...")
    for song in songs:
        spotify.user_playlist_add_tracks(user=user, playlist_id=listid["id"], tracks=[song["id"]], position=None)




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


    spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=sp_client_id, client_secret=sp_client_secret))
    # search in spotify for the album specified in the songs list
    all_songs = []
    for song in songs:
        print("searching song...")
        print(song["album"])
        results = spotify.search(q='album:'+song["album"]+' artist:'+song['artist'], limit=1, offset=0, type='track,album,artist', market=None)
        all_songs.append(results)
    print(all_songs)
    fj.write_json( all_songs ,"songs/"+file+".json")
    create_playlist(spotify,"Las mejores obras de Miles Davis",all_songs)


    



if __name__ == "__main__":
    main()