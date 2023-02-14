#!/usr/bin/env python 
#-*- coding: utf-8 -*-

import struct
from mutagen.id3 import ID3NoHeaderError
from mutagen.id3 import TCOM, TCON, TDRC, TRCK, APIC
from mutagen.id3 import PictureType, TLEN, WOAR, WXXX
from mutagen.id3 import ID3, TIT2, TALB, TPE1, TPE2, COMM
from mutagen.id3 import CHAP, CTOC, CTOCFlags, Encoding
from mutagen.mp3 import MP3

def fix_mutagen_CHAP_sorting_bug():
    """
        A shitty workaround to fix the CHAP tags sorting issue in mutagen.
        CHAP tags should be sorted by the start time, not the length of the title...
    """
    from mutagen.id3._util import BitPaddedInt, ID3SaveConfig
    from mutagen.id3._frames import TextFrame
    def save_frame(frame, name=None, config=None):
        if config is None:
            config = ID3SaveConfig()

        flags = 0
        if isinstance(frame, TextFrame):
            if len(str(frame)) == 0:
                return b''

        framedata = frame._writeData(config)

        usize = len(framedata)
        if usize > 2048:
            # Disabled as this causes iTunes and other programs
            # to fail to find these frames, which usually includes
            # e.g. APIC.
            # framedata = BitPaddedInt.to_str(usize) + framedata.encode('zlib')
            # flags |= Frame.FLAG24_COMPRESS | Frame.FLAG24_DATALEN
            pass

        if config.v2_version == 4:
            bits = 7
        elif config.v2_version == 3:
            bits = 8
        else:
            raise ValueError

        datasize = BitPaddedInt.to_str(len(framedata), width=4, bits=bits)

        if name is not None:
            assert isinstance(name, bytes)
            frame_name = name
        else:
            frame_name = type(frame).__name__
            frame_name = frame_name.encode("ascii")

        header = struct.pack('>4s4sH', frame_name, datasize, flags)
        return header + framedata

    def _write(self, config):
        # Sort frames by 'importance', then reverse frame size and then frame
        # hash to get a stable result
        order = ["TIT2", "TPE1", "TRCK", "TALB", "TPOS", "TDRC", "TCON"]

        framedata = [
            (f, save_frame(f, config=config)) for f in self.values()]

        def get_prio(frame):
            try:
                return order.index(frame.FrameID)
            except ValueError:
                return len(order)

        def sort_key(items):
            frame, data = items
            frame_key = frame.HashKey
            frame_size = len(data)

            # Let's ensure chapters are always sorted by their 'start_time'
            # and not by size/element_id pair.
            if frame.FrameID == "CHAP":
                frame_key = frame.FrameID
                frame_size = frame.start_time

            return (get_prio(frame), frame_key, frame_size)

        framedata = [d for (f, d) in sorted(framedata, key=sort_key)]

        # only write unknown frames if they were loaded from the version
        # we are saving with. Theoretically we could upgrade frames
        # but some frames can be nested like CHAP, so there is a chance
        # we create a mixed frame mess.
        if self._unknown_v2_version == config.v2_version:
            framedata.extend(data for data in self.unknown_frames
                             if len(data) > 10)

        return bytearray().join(framedata)

    ID3._write = _write
fix_mutagen_CHAP_sorting_bug()

class MP3MetaDataEditor:
    def __init__(self, filepath:str):
        self.filepath = filepath

        # read the ID3 tag or create one if not present
        try: 
            self.tags = ID3(self.filepath)
        
        except ID3NoHeaderError:
            self.tags = ID3()

    def set_author_url(self, url:str) -> None:
        self.tags.add(WOAR(encoding=3, url=url))
        self.tags.add(WXXX(encoding=3, url=url))

    def set_album_artist(self, band:str) -> None:
        self.tags["TPE2"] = TPE2(encoding=3, text=band)

    def set_comment(self, comment:str) -> None:
        self.tags["COMM"] = COMM(encoding=3, lang=u'eng', desc='desc', text=comment)

    def set_track_number(self, track_number:str) -> None:
        self.tags["TRCK"] = TRCK(encoding=3, text=track_number)

    def set_composer(self, composer:str) -> None:
        self.tags["TCOM"] = TCOM(encoding=3, text=composer)

    def set_release_year(self, year:str) -> None:
        self.tags["TDRC"] = TDRC(encoding=3, text=str(year))

    def set_title(self, title:str) -> None:
        self.tags["TIT2"] = TIT2(encoding=3, text=title)

    def set_length(self, length:int) -> None:
        # self.meta['length'] = str(length)
        # self.tags["TLEN"] = str(length)
        self.tags.add(TLEN(encoding=3, text=str(length)))

    def set_album_title(self, album:str) -> None:
        self.tags["TALB"] = TALB(encoding=3, text=album)

    def set_song_artist(self, artist:str) -> None:
        self.tags["TPE1"] = TPE1(encoding=3, text=artist)

    def set_genre(self, genre:str) -> None:
        self.tags["TCON"] = TCON(encoding=3, text=genre)

    def set_album_picture(self, picture:bytes, mime_type:str) -> None:
        self.tags["APIC"] = APIC(encoding=3,
                                 mime=mime_type, 
                                 type=PictureType.MEDIA, 
                                 desc=u'Media', 
                                 data=picture)
        
        # self.tags.add(APIC(encoding=3,
        #                    mime=mime_type, 
        #                    type=PictureType.COVER_BACK, 
        #                    desc=u'Media', 
        #                    data=picture)
        # )
        # self.tags.pprint()
        # self.audio.tags.add(
        #     APIC(
        #         encoding=3, # 3 is for utf-8
        #         mime=mime_type, # image/jpeg or image/png
        #         type=3, # 3 is for the cover image
        #         desc=u'Cover',
        #         data=picture
        #     )
        # )

    def save_metadata_to_file(self) -> None:
        # self.meta.save(self.filepath, v2_version=3)
        # self.audio.save(v2_version=3)
        self.tags.save(self.filepath, v2_version=3)

    def add_chapters(self, chapters: dict):
        """
            Adds chapters to the MP3 file. 
        """
        # https://github.com/quodlibet/mutagen/issues/506
        # https://github.com/quodlibet/mutagen/pull/539

        # open the file
        # audio_book = MP3(self.filepath, ID3=self.tags)
        audio_book = MP3(self.filepath)

        # add the chapters
        for chapter in chapters:
            audio_book.tags.add(
                CHAP(
                    element_id=chapter['id'],
                    start_time=chapter['start_time'],
                    end_time=chapter['end_time'],
                    sub_frames=[TIT2(encoding=Encoding.UTF8, text=[chapter['title']])]
                )
            )

        # create a table of contents
        audio_book.tags.add(
            CTOC(
                element_id='toc', 
                flags=CTOCFlags.TOP_LEVEL | CTOCFlags.ORDERED,
                child_element_ids=[ch['id'] for ch in chapters],
                sub_frames=[TIT2(encoding=Encoding.UTF8, text=['Table of Contents'])]
            )
        )

        # save to file
        audio_book.save()
