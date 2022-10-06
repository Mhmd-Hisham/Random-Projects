#!/usr/bin/env python 
#-*- coding: utf-8 -*-

from mutagen.id3 import ID3NoHeaderError
from mutagen.id3 import TCOM, TCON, TDRC, TRCK, APIC
from mutagen.id3 import PictureType, TLEN, WOAR, WXXX
from mutagen.id3 import ID3, TIT2, TALB, TPE1, TPE2, COMM

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
