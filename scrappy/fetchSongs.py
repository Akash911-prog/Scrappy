import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
import json
from pathlib import Path
import sys

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and PyInstaller."""
    if getattr(sys, 'frozen', False):  # Running as .exe
        base_path = sys._MEIPASS
    else:  # Running as script
        base_path = os.path.abspath(".")
    return Path(base_path) / relative_path

def spotifyConnect():
    CLIENT_ID = "592674651b5d4d95ae0081189261f0b7"
    CLIENT_SECRET = "89fd3e51c18e493fa5392232498eeae5"
    clientId = os.getenv("CLIENT_ID", CLIENT_ID)
    clientSecret = os.getenv("CLIENT_SECRET", CLIENT_SECRET)

    auth_manager = SpotifyClientCredentials(client_id=clientId, client_secret=clientSecret)
    return spotipy.Spotify(auth_manager=auth_manager)

def fetchSongs(args):
    """
    Fetches all tracks from a specified Spotify playlist and saves simplified track info to songs.json
    in the user's home directory.
    """
    sp = spotifyConnect()
    playlist = sp.playlist_tracks(args.playlistid)
    tracks = [track["track"] for track in playlist["items"]]

    while playlist["next"]:
        playlist = sp.next(playlist)
        tracks.extend([track["track"] for track in playlist["items"]])

    simplified_tracks = []
    for item in tracks:
        if item:
            artist_names = [artist.get("name") for artist in item.get("artists", [])]
            simplified_tracks.append({
                "artists": artist_names,
                "name": item.get("name"),
                "album_art_url": item["album"]["images"][0]["url"]
            })

    # Save to home directory to avoid write errors in .exe mode
    songs_file = Path.home() / "songs.json"
    with open(songs_file, "w", encoding="utf-8") as f:
        json.dump(simplified_tracks, f, ensure_ascii=False, indent=4)

    print(f"[INFO] Saved {len(simplified_tracks)} tracks to {songs_file}")

if __name__ =="__main__":
    args = {
        "playlistId": "2TQPDqPPnTZZjkx4u4jGRM"
    }
    sp = spotifyConnect()
    tracks = fetchSongs(args)

