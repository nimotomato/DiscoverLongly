import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
import keys

client_credentials_manager = SpotifyClientCredentials(keys.id, keys.secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
#scope = 'playlist-modify-private', 'playlist-read-private'
#sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
source_playlist_name = "Discover Weekly"


def main():
    #Get id of source playlist.
    source_playlist_id = get_playlist_id(source_playlist_name, sp)
    
    #Get id of target playlist.
    target_playlist_id = get_playlist_id("Discover Longly", sp)

    #Get ids of all tracks in source playlist.
    track_uris = get_unique_uris(target_playlist_id, source_playlist_id, sp)

    #Add tracks to target playlist.
    if len(track_uris) > 0:
        sp.playlist_add_items(playlist_id=target_playlist_id, items=track_uris, position=None)
        print(f"{len(track_uris)} new track(s) added. ")
    else:
        print("No new tracks to add. ")
    
    
def get_uris_long_list(playlist_id, sp) -> list:
    #Get uris of list longer than 100 items
    #Local master list
    target_uris_master = []

    #Uri list of max size
    target_uris = get_tracks_uri(playlist_id, sp, 100)
    
    #Counts iterations
    counter = 1

    #Keeps moving each time a max size list has been spotted
    while len(target_uris) >= 100:
        for uri in target_uris:
            target_uris_master.append(uri)
        target_uris = get_tracks_uri(playlist_id, sp, 100, offset=counter*100)
        counter += 1

    #Appends remaining uris to master list
    for uri in target_uris:
        target_uris_master.append(uri)

    return target_uris_master
    

def get_unique_uris(target_playlist_id, source_playlist_id, sp):
    
    target_uris = get_uris_long_list(target_playlist_id, sp)
    source_uris = get_tracks_uri(source_playlist_id, sp, 30)

    uri_list = []

    for uri in source_uris:
        if uri not in target_uris:
            uri_list.append(uri)

    print("Checking for doubles...")
    return uri_list


def get_tracks_uri(source_playlist_id, sp, limit, offset=0):
    #Get all data from playlist.
    tracks_raw = sp.playlist_tracks(source_playlist_id, limit=limit, offset=offset)
    uri_list = []

    #Store list of track uris.
    for track in tracks_raw['items']:
        uri_list.append(track['track']['uri'])
    print("Uri list created...")

    return uri_list


def get_playlist_id(playlist_name, sp):
    #Get 50 playlists.
    playlists = sp.current_user_playlists(limit=50)
    #Search for playlist name, return its ID.
    for playlist in playlists['items']:
        if playlist['name'] == playlist_name:
            print("Getting list id...")
            return playlist['id']


if __name__ == "__main__":
    main()