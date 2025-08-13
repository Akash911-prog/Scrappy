# 🎵 Scrappy - Spotify Downloader CLI

Scrappy is a command-line tool for downloading songs and playlists from Spotify in various formats using `yt-dlp` with automatic FFmpeg integration.

---

## 🚀 Features

- Download **single songs** directly from youtube.
- Download **entire playlists** in bulk.
- Supports multiple audio formats (`mp3`, `flac`, etc.).
- Automatically detects and uses bundled or system-installed **FFmpeg** and **FFprobe**.
- No Python installation required — just download and run the `.exe`.

---

## 📦 Installation

1. Download the ([Executable](https://github.com/Akash911-prog/Scrappy/releases/download/v1.0.0/scrappySetup.exe)).
2. Run the executable.

---

## 🛠 Usage

Open your terminal or command prompt and run:

### 1️⃣ Download a Single Song
```bash
scrappy download "Song Name" mp3 music
```
- "Song name" -> name of the song you want to download
- mp3 -> format of the song you want to download (eg. m4a, flack etc)
- music -> folder name for the download songs folder

### 2️⃣ Download bulk playlist
```bash
scrappy playlistdl "playlist id" mp3 music
```
- "playlist id" -> the unique identifier of a spotify playlist.
- mp3 -> format of the song you want to download (eg. m4a, flack etc)
- music -> folder name for the download songs folder


## Note
by default the dowload always happen in your systems default download folder. customs download paths will be available in the future.

## Examples
```bash
scrappy download "shape of you" mp3 "ed sheren"