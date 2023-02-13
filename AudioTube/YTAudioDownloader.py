#!/usr/bin/env python 
#-*- coding: utf-8 -*-
# TODO: add a feature for splitting chapters into different files

import os

from typing import Tuple
import pytube
import requests

def get_audio_itags() -> list:
    """
        Loops through all available 'audio' itags in pytube, sorts them by bit depth (quality),
        and returns a list of all available  itags.
    """
    itags = pytube.itags.DASH_AUDIO
    itags = [(tag, itags[tag][1]) for tag in itags]
    itags = [(tag, bitrate.replace("kbps", '')) for tag, bitrate in itags if bitrate]
    itags.sort(key=lambda t: -int(t[1]))
    itags = [tag for tag, _ in itags]
    
    return itags

def file_basename_exists_at_path(filename: str, path: str) -> str:
    """
        Looks for the basename of the file in the given path, ignoring file extensions.
        If the filename exists, returns the first matching file + extension.
        
        Returns an empty string if the basename doesn't exist.
    """
    basename, ext = os.path.splitext(os.path.basename(filename))
    for target_filename in os.listdir(path):
        target_basename, target_ext = os.path.splitext(os.path.basename(target_filename))
        if basename == target_basename:
            return os.path.join(path, target_basename + target_ext)

    return ""

class YTAudioDownloader:
    def __init__(self, url:str, path:str):
        self.yt = pytube.YouTube(url)
        self.url = self.yt.watch_url

        self.path = path
        os.makedirs(self.path, exist_ok=True)

        self._itags = get_audio_itags()

        # try to find the best itag then
        self.itag = next(filter(self.yt.streams.get_by_itag, self._itags), -1)

        # download the file and get the filename
        self.filename, self.file_exists = self.download_audio_to_file(self.path, self.itag)
        self.basename, self.ext = os.path.splitext(self.filename)

        self.metadata_downloaded = False

    def download_metadata(self):
        # download the thumbnail image bytes (to inject it later)
        self.thumbnail = self.download_thumbnail()

        # extract metadata if found
        self.title = self.yt.title
        self.song = self.get_song_name()
        self.artist = self.get_artist_name()
        self.album_title = self.get_album_title()
        self.length = self.yt.length
        self.release_year = self.yt.publish_date.year
        self.metadata_downloaded = True

        if (self.song != ""):
            self.title = self.song

        if (self.artist == ""):
            self.artist = self.yt.author 

    def get_song_name(self):
        for metadata in self.yt.metadata.metadata:
            if "Song" in metadata:
                return metadata["Song"]
        
        return ""

    def get_artist_name(self):
        for metadata in self.yt.metadata.metadata:
            if "Artist" in metadata:
                return metadata["Artist"]
        
        return ""

    def get_album_title(self):
        for metadata in self.yt.metadata.metadata:
            if "Album" in metadata:
                return metadata["Album"]
        
        return ""

    def download_audio_to_file(self, path: str, itag: int) -> Tuple[str, bool]:
        """
            Downloads the audio with the given itag to the given path.
        """
        if (itag == -1):
            raise Exception(f"Couldn't find an audio stream for '{self.url}'!")
        
        stream = self.yt.streams.get_by_itag(itag)
        filename = stream.default_filename
        file_exists = True

        # look for the exact filename
        if not stream.exists_at_path(path):

            # look for the basename, in case the file was converted to another format
            filename = file_basename_exists_at_path(filename, path)

            # the file doesn't exist, download it
            if filename == "":
                file_exists = False
                filename = stream.download(output_path=path)

        return filename, file_exists

    def download_thumbnail(self) -> bytes:
        # try to get the highest resolution thumbnail
        base_thumbnail_url = self.yt.thumbnail_url[:self.yt.thumbnail_url.rfind("/")]

        thumbnail_urls = [base_thumbnail_url + "/maxresdefault.jpg",
                          base_thumbnail_url + "/sddefault.jpg",
                          base_thumbnail_url + "/hqdefault.jpg"]

        img = bytes()

        # get the bytes of the image
        for url in thumbnail_urls:
            res = requests.get(url)

            if (res.status_code != 200):
                continue
            
            img = res.content
            break
        
        return img
