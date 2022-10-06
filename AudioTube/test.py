
from MP3MetaDataEditor import MP3MetaDataEditor
from YTAudioDownloader import get_audio_itags
from pytube import YouTube
import pytube

yt = YouTube('http://youtube.com/watch?v=2lAe1cqCOXo')
itags = get_audio_itags()
itag = next(filter(yt.streams.get_by_itag, itags), -1)
stream = yt.streams.get_by_itag(itag)

print(stream.default_filename)

# filepath = "Kaleida - Think (Official Video).mp3"
# editor = MP3MetaDataEditor(filepath)
# # editor.set_artist("Kaleida")
# # editor.set_title("Think")
# editor.set_cover_picture(open("m.png", "rb").read(), "image/png")
# editor.save_metadata_to_file()

# url = "https://www.youtube.com/watch?v=999tf5-ONGw"
# url = "https://www.youtube.com/watch?v=1CurN2Fg-2E"
# yt = YouTube(url)
# yt.vid_info["videoDetails"]["author"]
# yt.author
# yt.title
# yt.channel_url
# yt.channel_id
# yt.description
# yt.publish_date -> publish date on youtube
# yt.length -> length in seconds
# yt.metadata.metadata -> list of metadata (Song, Artist, Album, Writers)
# high_resolution_thumbnail_url = pytube.YouTube(YOUR_youtube_url).thumbnail_url.replace('default.jpg', 'maxresdefault.jpg')

class PictureType(object):
    """Enumeration of image types defined by the ID3 standard for the APIC
    frame, but also reused in WMA/FLAC/VorbisComment.
    """

    OTHER = 0
    """Other"""

    FILE_ICON = 1
    """32x32 pixels 'file icon' (PNG only)"""

    OTHER_FILE_ICON = 2
    """Other file icon"""

    COVER_FRONT = 3
    """Cover (front)"""

    COVER_BACK = 4
    """Cover (back)"""

    LEAFLET_PAGE = 5
    """Leaflet page"""

    MEDIA = 6
    """Media (e.g. label side of CD)"""

    LEAD_ARTIST = 7
    """Lead artist/lead performer/soloist"""

    ARTIST = 8
    """Artist/performer"""

    CONDUCTOR = 9
    """Conductor"""

    BAND = 10
    """Band/Orchestra"""

    COMPOSER = 11
    """Composer"""

    LYRICIST = 12
    """Lyricist/text writer"""

    RECORDING_LOCATION = 13
    """Recording Location"""

    DURING_RECORDING = 14
    """During recording"""

    DURING_PERFORMANCE = 15
    """During performance"""

    SCREEN_CAPTURE = 16
    """Movie/video screen capture"""

    FISH = 17
    """A bright coloured fish"""

    ILLUSTRATION = 18
    """Illustration"""

    BAND_LOGOTYPE = 19
    """Band/artist logotype"""

    PUBLISHER_LOGOTYPE = 20
    """Publisher/Studio logotype"""