#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import argparse
from datetime import timedelta
import warnings
warnings.filterwarnings('ignore')

import ffmpeg
from pytube import Playlist

from YTAudioDownloader import YTAudioDownloader
from MP3MetaDataEditor import MP3MetaDataEditor


def get_opt_parser() -> argparse.ArgumentParser:
    """Parse command-line options."""

    parser = argparse.ArgumentParser(
        description="Download audio from youtube videos. Tries to extract & inject metadata from youtube.")
    parser.add_argument(
        "-u", "--url", help="URL to the YouTube video.", default="", dest="url")
    parser.add_argument(
        "-f", "--file", help="File that contains a YouTube URL per line.", default="", dest="urls_file")
    parser.add_argument("-d", "--directory", help="Destination directory to download the file in.",
                        default=os.path.abspath(os.curdir), dest="directory")
    parser.add_argument(
        "--title", help="Set the title in the MP3 metadata.", default="", dest="title")
    parser.add_argument(
        "--album-title", help="Set the album title in the MP3 metadata", default="", dest="album_title")
    parser.add_argument(
        "--artist", help="Set the artist of the song in the MP3 metdata", dest="artist", default="")
    parser.add_argument(
        "-p", "--playlist", help="Download songs from a youtube playlist.", dest='playlist_url', default="")
    parser.add_argument(
        "-o", "--override", help="Override if a file already exists.", dest='override', default=False, type=bool)

    return parser.parse_args()

def convert_to_mp3(input_filename: str, delete_original: bool = True) -> str:
    # input_filename =  f"'{input_filename}'"
    # output_filename = f"'{output_filename}'"

    # os.rename(input_filename, input_filename.replace(" ", "_"))
    # os.rename(output_filename, output_filename.replace(" ", "_"))
    # input_filename  = input_filename.replace(" ", "_")
    # output_filename = output_filename.replace(" ", "_")

    filename, old_ext = input_filename.split(".")
    temp_file = f"input_file.{old_ext}"
    os.rename(input_filename, temp_file)

    output_filename = "output_file.mp3"
    ffmpeg.input(temp_file).output(output_filename).run(
        quiet=True, overwrite_output=True)

    if delete_original:
        os.remove(temp_file)

    else:
        os.rename(temp_file, input_filename)

    os.rename(output_filename, filename+".mp3")

    # old way, requires ffmpeg to be installed on the operating system
    # os.system(f"ffmpeg -v quiet -y -i \"{filename}\" \"{mp3_filename}\"")
    # os.system(f"del \"{filename}\"")
    return filename+".mp3"

def get_metadata_from_downloader(downloader: YTAudioDownloader) -> dict:
    if not downloader.metadata_downloaded:
        downloader.download_metadata()

    metadata = dict()
    metadata["title"] = downloader.title
    metadata["artist"] = downloader.artist
    metadata["album_title"] = downloader.album_title
    metadata["length"] = downloader.length
    metadata["release_year"] = downloader.release_year
    metadata["thumbnail"] = downloader.thumbnail
    metadata["url"] = downloader.url

    return metadata

def inject_metadata(filename: str, metadata: dict, save: bool = True) -> None:
    editor = MP3MetaDataEditor(filename)
    editor.set_length(metadata["length"])
    editor.set_release_year(metadata["release_year"])

    editor.set_title(metadata["title"])
    editor.set_song_artist(metadata["artist"])

    editor.set_album_title(metadata["album_title"])
    editor.set_album_artist(metadata["artist"])
    editor.set_album_picture(metadata["thumbnail"], "image/png")

    editor.set_author_url(metadata["url"])
    editor.set_comment("Downloaded from AudioTube.")

    if save:
        # save the metadata to the file
        editor.save_metadata_to_file()

def get_url_list(options):
    urls = []
    if options.url != "":
        urls.append(options.url)

    elif options.urls_file!="":
        with open(options.urls_file, "r") as fh:
            urls = fh.read().strip().splitlines()
    
    elif options.playlist_url != "":
        playlist = Playlist(options.playlist_url)
        urls = playlist.video_urls

    return urls

def main():
    options = get_opt_parser()

    urls = get_url_list(options)
    if not urls:
        print("Please specify any url using the command line arguments!")
        return

    for url in urls:
        # download the audio file
        t0 = time.time()
        print(f"Parsing '{url}'")
        print(f"Downloading audio..  ", end='', flush=True)
        downloader = YTAudioDownloader(url, options.directory)
        filename = downloader.filename
        if downloader.file_exists and not options.override:
            print(f"File '{filename}' already exists! Skipping!")
            continue

        elapsed = timedelta(seconds=round(time.time() - t0))
        print(f"Done! [{elapsed}]", flush=True)
        print(f"File: '{filename}'", flush=True)

        mp3_filename = downloader.basename + ".mp3"
        # convert to MP3 as the metadata injector only supports MP3 files
        if (downloader.ext != ".mp3"):
            print("Converting to *.mp3.. ", flush=True, end='')
            mp3_filename = convert_to_mp3(filename, delete_original=True)
            print("Done!")

        # inject metadata
        print("Injecting metadata.. ", end="", flush=True)
        metadata = get_metadata_from_downloader(downloader)
        metadata["title"] = options.title if options.title != "" else metadata["title"]
        metadata["artist"] = options.artist if options.artist != "" else metadata["artist"]
        metadata["album_title"] = options.album_title if options.album_title != "" else metadata["album_title"]

        inject_metadata(mp3_filename, metadata)

        print("Done!")


if __name__ == "__main__":
    main()
    sys.exit()
