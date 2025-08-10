import argparse
from .downloadSongs import downloadSongs
from .fetchSongs import fetchSongs

VERSION = "1.0.0"

def playlistdl(args):
    fetchSongs(args)
    downloadSongs(args.format)

def main():
    parser = argparse.ArgumentParser(prog="scrappy", description="Scrappy Spotify Downloader CLI")
    
    parser.add_argument('--version', action='version', version=f'scrappy {VERSION}')
    
    subparsers = parser.add_subparsers(title="Commands", dest="command", required=True)
    
    # download command
    parser_download = subparsers.add_parser('download', help="Download a single song")
    parser_download.add_argument('songname', help="Name of the song to download")
    parser_download.add_argument('format', help="Format to download (e.g., mp3, flac)")
    parser_download.set_defaults(func=lambda args: downloadSongs(args.format, args.songname))
    
    
    # fetch command
    parser_fetch = subparsers.add_parser('fetch', help="Fetch all tracks from a playlist")
    parser_fetch.add_argument('playlistid', help="Spotify playlist ID")
    parser_fetch.set_defaults(func=fetchSongs)
    
    # playlistdl command
    parser_playlistdl = subparsers.add_parser('playlistdl', help="Download all songs from a playlist")
    parser_playlistdl.add_argument('playlistid', help="Spotify playlist ID")
    parser_playlistdl.add_argument('format', help="Format to download (e.g., mp3, flac)")
    parser_playlistdl.set_defaults(func=playlistdl)
    
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
