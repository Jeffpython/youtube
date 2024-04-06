import math
import os.path
from pytube import YouTube
from pytube.exceptions import VideoUnavailable
from pytube.streams import Stream
from pydub import AudioSegment


class Audio:
    def __init__(self) -> None:
        self.author: str = ''
        self.title: str = ''
        self.path: str = ''

    def get_stream(self, url: str) -> Stream | None:
        try:
            yt = YouTube(url)
        except VideoUnavailable:
            print("Video is unavailable")
        else:
            self.author = yt.author
            self.title = yt.title
            return yt.streams.get_audio_only(subtype='mp4')

    def save_temp_audio(self, stream: Stream) -> None:
        audio.path = stream.download()
        print('Youtube file is downloaded')


def save_split_audio(temp_file: AudioSegment) -> None:
    duration = len(temp_file)
    interval = 10 * 60 * 1000
    num_files = math.ceil(duration / interval)
    begin = 0

    for i in range(num_files):
        end = begin + interval if begin + interval < duration else duration
        part = temp_file[begin:end]
        part.export(f'{audio.title} {i + 1}.mp3', format='mp3')
        begin = end


def remove_temp_audio(path: str) -> None:
    if os.path.exists(path):
        os.remove(path)


if __name__ == "__main__":
    # url = "https://www.youtube.com/watch?v=25xUoLye53w"
    url = input("Enter Youtube URL: ")
    audio = Audio()
    stream = audio.get_stream(url)
    audio.save_temp_audio(stream)
    temp_file = AudioSegment.from_file(audio.path, 'mp4')
    save_split_audio(temp_file)
    print('File split')
    remove_temp_audio(path=audio.path)
