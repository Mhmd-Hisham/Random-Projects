
## Description

A simple module that uses [pytube](https://github.com/pytube/pytube) to download audio files and their metadata (such as thumbnails, artist title, album name, etc..) from Youtube. All the metadata are injected into the files using [mutagen](https://github.com/quodlibet/mutagen). [FFMPEG-Python](https://github.com/kkroening/ffmpeg-python) is used to re-encode the files and converting them into MP3 format.

## Requirements

```
pip install -r requirements.txt
```

## Usage

```
python youtube_audio_downloader.py -h

usage: youtube_audio_downloader.py [-h] [-u URL] [-f URLS_FILE] [-d DIRECTORY] [--title TITLE] [--album-title ALBUM_TITLE] [--artist ARTIST]
                                   [-p PLAYLIST_URL] [-o OVERRIDE]

Download audio from youtube videos. Tries to extract & inject metadata from youtube.

optional arguments:
  -h, --help            show this help message and exit
  -u URL, --url URL     URL to the YouTube video.
  -f URLS_FILE, --file URLS_FILE
                        File that contains a YouTube URL per line.
  -d DIRECTORY, --directory DIRECTORY
                        Destination directory to download the file in.
  --title TITLE         Set the title in the MP3 metadata.
  --album-title ALBUM_TITLE
                        Set the album title in the MP3 metadata
  --artist ARTIST       Set the artist of the song in the MP3 metdata
  -p PLAYLIST_URL, --playlist PLAYLIST_URL
                        Download songs from a youtube playlist.
  -o OVERRIDE, --override OVERRIDE
                        Override if a file already exists.

```

## Meta

Mohamed Hisham – [Gmail](mailto:Mohamed00Hisham@Gmail.com) | [GitHub](https://github.com/Mhmd-Hisham) | [LinkedIn](https://www.linkedin.com/in/Mhmd-Hisham/)

## License

This project is licensed under the GNU GPLv3 License - check [LICENSE](../LICENSE) for more details.
