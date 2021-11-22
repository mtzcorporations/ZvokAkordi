from __future__ import unicode_literals
import pathlib
import youtube_dl


def downloadYT(link):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([link])

def currentDir(_file_, path):
    return str(pathlib.PurePath(_file_).parent.joinpath(path))

downloadYT("https://youtu.be/T8Zj1oLGaQE")