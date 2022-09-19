
# import subprocess
# from pprint import pprint

# import ffmpeg

import m3u8
import requests

list_url = input("Enter .m3u8 list url: ")
res = requests.get(list_url)

print("Status code:", res.status_code)
m3u8_master = m3u8.loads(res.text)

playlists = m3u8_master.data['playlists']

print("Playlists found: ")
for i, playlist in enumerate(playlists):
    print(f"\t{i}: '{playlist['uri']}' [{playlist['stream_info']['resolution']}]")

choice = int(input("Enter your choice: "))

playlist_url = "/".join(list_url.split("/")[:-1] + [playlists[choice]['uri']])
res = requests.get(playlist_url)
m3u8_master_playlist = m3u8.loads(res.text)

m3_data = (m3u8_master_playlist.data)
prefix = '/'.join(playlist_url.split("/")[:-1]) + "/"

total_segments = len(m3_data['segments'])
update_percentage = total_segments//10
print(f"Total segments: {total_segments}")
with open('video.mp4','wb') as fp:
    for i, segments in enumerate(m3_data['segments']):
        uri = segments['uri']
        uri = prefix+uri

        print(f"\rDownloading... {(i/total_segments)*100:0.2f}%", end="")

        r = requests.get(uri)
        fp.write(r.content)

print(" Done!")

# subprocess.run(['ffmpeg','-i','video.ts','-c', 'copy', 'video.mp4']) 
# ffmpeg.input('video.ts').output('video.mp4', c='copy').run(quiet=False, overwrite_output=True)

