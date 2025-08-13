import argparse
import os
import subprocess
import sys
from downloadSongs import downloadSongs
from fetchSongs import fetchSongs

VERSION = "1.0.0"

# ---------- Detect and set FFmpeg + FFprobe path ----------
def get_ffmpeg_and_ffprobe():
    """
    Detects if ffmpeg and ffprobe are bundled with the exe and returns their paths.
    Falls back to system-installed versions if not found.
    """
    base_dir = None
    if hasattr(sys, "_MEIPASS"):  # Running as PyInstaller .exe
        base_dir = sys._MEIPASS
    else:  # Running from source
        base_dir = os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else __file__)

    ffmpeg_path = os.path.join(base_dir, "ffmpeg.exe")
    ffprobe_path = os.path.join(base_dir, "ffprobe.exe")

    if not os.path.exists(ffmpeg_path):
        ffmpeg_path = "ffmpeg"  # fallback
    if not os.path.exists(ffprobe_path):
        ffprobe_path = "ffprobe"  # fallback

    return ffmpeg_path, ffprobe_path

# Patch yt-dlp to use our ffmpeg and ffprobe
def set_ffmpeg_for_yt_dlp():
    ffmpeg_path, ffprobe_path = get_ffmpeg_and_ffprobe()
    os.environ["PATH"] = os.path.dirname(ffmpeg_path) + os.pathsep + os.environ["PATH"]
    os.environ["FFMPEG_PATH"] = ffmpeg_path
    os.environ["FFPROBE_PATH"] = ffprobe_path

#________Auto Add To Path_____________


# ---------- CLI Commands ----------
def playlistdl(args):
    set_ffmpeg_for_yt_dlp()
    fetchSongs(args)
    downloadSongs(args.format, folder=args.folder)

def main():
    parser = argparse.ArgumentParser(prog="scrappy", description="Scrappy Spotify Downloader CLI")
    parser.add_argument('--version', action='version', version=f'scrappy {VERSION}')

    subparsers = parser.add_subparsers(title="Commands", dest="command", required=True)

    # download command
    parser_download = subparsers.add_parser('download', help="Download a single song")
    parser_download.add_argument('songname', help="Name of the song to download")
    parser_download.add_argument('format', help="Format to download (e.g., mp3, flac)")
    parser_download.add_argument('folder', help="Download directory", default="downloaded")
    parser_download.set_defaults(func=lambda args: (set_ffmpeg_for_yt_dlp(), downloadSongs(args.format, args.folder, args.songname)))

    # fetch command
    parser_fetch = subparsers.add_parser('fetch', help="Fetch all tracks from a playlist")
    parser_fetch.add_argument('playlistid', help="Spotify playlist ID")
    parser_fetch.set_defaults(func=lambda args: (set_ffmpeg_for_yt_dlp(), fetchSongs(args)))

    # playlistdl command
    parser_playlistdl = subparsers.add_parser('playlistdl', help="Download all songs from a playlist")
    parser_playlistdl.add_argument('playlistid', help="Spotify playlist ID")
    parser_playlistdl.add_argument('format', help="Format to download (e.g., mp3, flac)")
    parser_playlistdl.add_argument('folder', help="Download directory", default="downloaded")
    parser_playlistdl.set_defaults(func=playlistdl)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    sys.setrecursionlimit(5000)
    main()
