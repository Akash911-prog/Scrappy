import yt_dlp
import json
from .getDownloadPath import get_default_download_path
import random
import time

DOWNLOAD_PATH = get_default_download_path()

def load_songs(filepath=".\\songs.json"):
    """
    Loads songs from a JSON file.

    Args:
        filepath (str): The path to the JSON file containing the songs. Defaults to ".\\songs.json".

    Returns:
        list: A list of songs if the file is successfully read and decoded, otherwise an empty list.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            # Load the JSON data from the file
            songs = json.load(f)
            return songs
    except FileNotFoundError:
        # Handle the case where the file does not exist
        print(f"Error: File '{filepath}' not found.")
        return []
    except json.JSONDecodeError:
        # Handle the case where the JSON is invalid
        print(f"Error: Failed to decode JSON in '{filepath}'.")
        return []

def download_song(ydl, query):
    """
    Downloads a song using the provided YoutubeDL instance and search query.

    Args:
        ydl (yt_dlp.YoutubeDL): An instance of YoutubeDL configured with options.
        query (str): The search query for the song to be downloaded.

    Returns:
        bool: True if download was successful, False otherwise.
    """
    try:
        # Attempt to extract and download song information from the query
        info = ydl.extract_info(query, download=True)
        print(f"Downloaded: {info.get('title', 'Unknown title')}")
        return True
    except yt_dlp.utils.DownloadError as e:
        # Handle specific download errors
        print(f"Download error for query '{query}': {e}")
    except Exception as e:
        # Handle any other unexpected errors
        print(f"Unexpected error for query '{query}': {e}")
    return True

def download_batch(songs_batch, ytld_options):
    """
    Downloads a batch of songs using the provided YoutubeDL instance and options.

    Args:
        songs_batch (list): A list of dictionaries containing song information.
        ytld_options (dict): A dictionary of options for the YoutubeDL instance.
    """
    with yt_dlp.YoutubeDL(ytld_options) as ydl:
        # Iterate over each song in the batch
        for song in songs_batch:
            # Construct the search query for the song
            query = f"ytsearch1:{song['name']} song by {' '.join(song['artists'])} lyrics"
            # Attempt to download the song
            success = download_song(ydl, query)
            # Random sleep between downloads to avoid rate limits
            time.sleep(random.uniform(3, 6))
    return True

def downloadSongs(format, oneSong=""):
    """
    Downloads a batch of songs or a single song in the specified format.

    Args:
        format (str): The audio format to download the songs in (e.g. "mp3").
        oneSong (str, optional): The name of a single song to download. Defaults to "".
    """
    songs = load_songs()

    ytld_options = {
        "format": "bestaudio/best",
        "outtmpl": fr"{DOWNLOAD_PATH}\\songs\\%(title)s.%(ext)s",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": format,
            "preferredquality": "0"
        }],
        "max_sleep_interval": 15,
        "quiet": True,
    }

    if oneSong:
        print(f"Downloading single song: {oneSong}")
        with yt_dlp.YoutubeDL(ytld_options) as ydl:
            download_song(ydl, f"ytsearch1:{oneSong} song")
        return 0

    if not songs:
        print("No songs found in JSON.")
        return 1
    
    if len(songs) < 10:
        print(f"Downloading {len(songs)} songs sequentially...")
        download_batch(songs, ytld_options)
        return 0
    
    # Process in batches of 10
    batches_of_10 = [songs[i:i+10] for i in range(0, len(songs), 10)]
    print(f"Downloading {len(songs)} songs in {len(batches_of_10)} batches...")

    for i, batch in enumerate(batches_of_10):
        download_batch(batch, ytld_options)
        if i < len(batches_of_10) - 1:
            wait_time = random.randint(180, 300)  # 3 to 5 minutes
            print(f"Batch {i+1} done. Waiting {wait_time} seconds before next batch...")
            time.sleep(wait_time)
    
    return True
    

if __name__ == "__main__":
    downloadSongs("mp3")