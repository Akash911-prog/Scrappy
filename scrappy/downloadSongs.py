import os
import platform
import sys
import json
import random
import time
import subprocess
from pathlib import Path
import requests
from re import sub
import yt_dlp


# ===============================
# Get default download path (no relative imports for exe)
# ===============================
def get_default_download_path():
    system = platform.system()

    if system == "Windows":
        try:
            import ctypes
            from ctypes import wintypes
            from uuid import UUID

            KF_FLAG_DEFAULT = 0
            FOLDERID_Downloads = UUID('{374DE290-123F-4565-9164-39C4925E467B}')
            HRESULT = ctypes.c_long

            SHGetKnownFolderPath = ctypes.windll.shell32.SHGetKnownFolderPath
            SHGetKnownFolderPath.argtypes = [ctypes.POINTER(ctypes.c_byte * 16), wintypes.DWORD, wintypes.HANDLE, ctypes.POINTER(ctypes.c_wchar_p)]
            SHGetKnownFolderPath.restype = HRESULT

            path_ptr = ctypes.c_wchar_p()
            r = SHGetKnownFolderPath((ctypes.c_byte * 16).from_buffer_copy(FOLDERID_Downloads.bytes_le), KF_FLAG_DEFAULT, 0, ctypes.byref(path_ptr))
            if r != 0:
                raise ctypes.WinError()
            path = path_ptr.value
            ctypes.windll.ole32.CoTaskMemFree(path_ptr)
            return Path(path)
        except Exception as e:
            print(" Error getting default download path, Error:", e)
            # fallback
            return Path.home() / "Downloads"

    elif system == "Darwin":  # macOS
        return Path.home() / "Downloads"

    else:  # Linux and others
        # Use XDG user dirs if available
        try:
            xdg_config_home = os.environ.get("XDG_CONFIG_HOME", os.path.join(Path.home(), ".config"))
            user_dirs_file = os.path.join(xdg_config_home, "user-dirs.dirs")

            if os.path.exists(user_dirs_file):
                with open(user_dirs_file) as f:
                    for line in f:
                        if line.startswith("XDG_DOWNLOAD_DIR"):
                            # Example: XDG_DOWNLOAD_DIR="$HOME/Downloads"
                            path = line.split("=")[1].strip().strip('"').replace("$HOME", str(Path.home()))
                            return Path(path)
        except Exception:
            pass

        # fallback
        return Path.home() / "Downloads"

DOWNLOAD_PATH = get_default_download_path()

# ===============================
# Auto-update yt-dlp
# ===============================
def update_yt_dlp():
    try:
        print("🔄 Updating yt-dlp...")
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-U", "yt-dlp"],
            check=True
        )
    except Exception as e:
        print(f"⚠ Could not update yt-dlp: {e}")

# ===============================
# Load songs.json
# ===============================
def load_songs(filepath="songs.json"):
    try:
        with open((Path.home() / filepath), "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.")
        return []
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON in '{filepath}'.")
        return []
    

# ===============================
# Download single song
# ===============================
def download_song(ydl, query, output_path, song={}):
    try:
        info = ydl.extract_info(query, download=False)
        if song:
            info["entries"][0]["thumbnail"] = song["album_art_url"]
        ydl.download([info["entries"][0]["webpage_url"]])
        # original_filename = ydl.prepare_filename(info["entries"][0])
        print(f"✅ Downloaded: {info.get('title', 'Unknown title')}")

        return True
    except yt_dlp.utils.DownloadError as e:
        if "403" in str(e):
            print(f"🚫 403 Forbidden for '{query}', retrying with fallback format...")
            ydl.params["format"] = "bestaudio/best"
            ydl.extract_info(query, download=True)
            return True
        print(f"Download error for '{query}': {e}")
    # except Exception as e:
    #     print(f"Unexpected error for '{query}': {e}")
    return False

# ===============================
# Batch download
# ===============================
def download_batch(songs_batch, ytld_options):
    with yt_dlp.YoutubeDL(ytld_options) as ydl:
        for song in songs_batch:
            query = f"ytsearch1:{song['name']} song by {' '.join(song['artists'])} lyrics"
            download_song(ydl, query, ytld_options["outtmpl"], song)
            time.sleep(random.uniform(3, 6))
    return True

# ===============================
# Main downloadSongs function
# ===============================
def downloadSongs(format, folder, oneSong=""):
    if not (hasattr(sys, "_MEIPASS")):  # Running as PyInstaller .exe
        update_yt_dlp()

    songs = load_songs()

    ytld_options = {
        "format": "bestaudio[ext=m4a]/bestaudio/best",
        "outtmpl": fr"{DOWNLOAD_PATH}\songs\{folder}\%(title)s.%(ext)s",
        "final_ext": format,  # ensures correct final extension
        "overwrites": True,
        "windowsfilenames": True,  # ✅ Sanitize for Windows
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": format,
            "preferredquality": "0"
        },{
            "key": "EmbedThumbnail"
        },{
            "key": "FFmpegMetadata"
        }],
        "writethumbnail": True,
        "http_headers": {"User-Agent": "Mozilla/5.0"},
        "max_sleep_interval": 15,
        "quiet": True,
    }

    if oneSong:
        print(f"🎵 Downloading single song: {oneSong}")
        with yt_dlp.YoutubeDL(ytld_options) as ydl:
            download_song(ydl, f"ytsearch1:{oneSong} song", ytld_options["outtmpl"])
        return

    if not songs:
        print("❌ No songs found in JSON.")
        return
    
    if len(songs) < 10:
        print(f"📥 Downloading {len(songs)} songs sequentially...")
        download_batch(songs, ytld_options)
        return
    
    batches_of_10 = [songs[i:i+10] for i in range(0, len(songs), 10)]
    print(f"📥 Downloading {len(songs)} songs in {len(batches_of_10)} batches...")

    for i, batch in enumerate(batches_of_10):
        download_batch(batch, ytld_options)
        if i < len(batches_of_10) - 1:
            wait_time = random.randint(180, 300)
            print(f"⏳ Batch {i+1} done. Waiting {wait_time} seconds before next batch...")
            time.sleep(wait_time)

# ===============================
# CLI Entry Point
# ===============================
if __name__ == "__main__":
    choice = input("Enter song name or leave empty to batch download: ").strip()
    downloadSongs("mp3", choice)
