from fastapi import FastAPI, HTTPException
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
import json
import dotenv

dotenv.load_dotenv()

app = FastAPI()

def spotifyConnect():
    clientId = os.getenv("CLIENT_ID")
    clientSecret = os.getenv("CLIENT_SECRET")

    try:
        with open(r".\scrappy\config.json", "r") as f:
            config = json.load(f)
            clientId = config["CLIENT_ID"] if config["CLIENT_ID"] else clientId
            clientSecret = config["CLIENT_SECRET"] if config["CLIENT_SECRET"] else clientSecret
    except FileNotFoundError:
        print("File not found")

    auth_manager = SpotifyClientCredentials(client_id=clientId, client_secret=clientSecret)
    sp = spotipy.Spotify(auth_manager=auth_manager)
    return sp

@app.get("/playlist/{playlist_id}")
def fetchSongs(playlist_id: str):
    try:
        sp = spotifyConnect()
        playlist = sp.playlist_tracks(playlist_id)
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

        return {"tracks": simplified_tracks}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



# You can add /download/song and /download/playlist endpoints similarly
