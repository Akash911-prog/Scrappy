import spotipy
import requests
import json


def fetchSongs(playlistId):
    response = requests.get(f"http://127.0.0.1:8000/playlist/{playlistId}")
    response.raise_for_status()
    with open("songs.json", "w") as f:
        json.dump(response.json(), f, indent=4, ensure_ascii=False)
    return response


if __name__ =="__main__":
    fetchSongs("0YIXjREzmTKmQHYU2gEOkQ")

