# Reference : https://github.com/nficano/pytube
from pytube import YouTube
import os, sys


def get_youtube_vid(url, file_loc, file_name=None):
    yt = YouTube(url)
    yt_filename = yt.filename.replace(" ", "_")
    if not file_name:
        filepath = os.path.join(file_loc, yt_filename+'.mp4')
    else:
        filepath = os.path.join(file_loc, file_name)

    filepath = os.path.abspath(filepath)

    # Download the highest resolution in mp4
    try:
        video = yt.filter('mp4')[-1]
        video.download(filepath, force_overwrite=True)
    except:
        e = sys.exc_info()[0]
        print('get_youtube_vid failed for url' + url + 'with error: ' + str(e))
        filepath = None
    return filepath



if __name__ == "__main__":
    test_link = "https://www.youtube.com/watch?v=Gmaww5-vHFo&feature=youtu.be"
    get_youtube_vid(test_link, 'tmp')