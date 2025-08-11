import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
import json


def spotifyConnect():
    clientId = os.getenv("CLIENT_ID")
    clientSecret = os.getenv("CLIENT_SECRET")

    try:
        with open(r".\src\config.json", "r") as f:
            config = json.load(f)
            clientId = config["CLIENT_ID"] if config["CLIENT_ID"] else clientId
            clientSecret = config["CLIENT_SECRET"] if config["CLIENT_SECRET"] else clientSecret
    except FileNotFoundError:
        print("File not found")

    auth_manager = SpotifyClientCredentials(client_id=clientId, client_secret=clientSecret)
    sp = spotipy.Spotify(auth_manager=auth_manager)
    return sp

def fetchSongs(args):
    sp = spotifyConnect()
    playlist = sp.playlist_tracks(args.playlistId)
    tracks = [track["track"] for track in playlist["items"]]

    while playlist["next"]:
        playlist = sp.next(playlist)
        tracks.extend([track["track"] for track in playlist["items"]])

    # Keep only artist names and track name
    simplified_tracks = []
    for item in tracks:
        if item:
            artist_names = [artist.get("name") for artist in item.get("artists", [])]
            simplified_tracks.append({
                "artists": artist_names,
                "name": item.get("name")
            })

    with open(r".\songs.json", "w", encoding="utf-8") as f:
        json.dump(simplified_tracks, f, ensure_ascii=False, indent=4)


if __name__ =="__main__":
    playlistId = "2TQPDqPPnTZZjkx4u4jGRM"
    sp = spotifyConnect()
    tracks = fetchSongs(playlistId)

