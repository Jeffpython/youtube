import math
import os.path
from pytube import YouTube
from pytube.exceptions import VideoUnavailable
from pytube.streams import Stream
from pytube.cli import on_progress
from pydub import AudioSegment
from typer import Typer
from rich.progress import track
from dataclasses import dataclass

app = Typer()


@dataclass
class Audio:
    author: str
    title: str
    stream: Stream


def get_audio(url: str) -> Audio | None:
    try:
        yt = YouTube(url, on_progress_callback=on_progress)
    except VideoUnavailable:
        print("Video is unavailable")
    else:
        author = yt.author
        title = yt.title.replace(' ', '_')
        stream = yt.streams.get_audio_only(subtype='mp4')
        return Audio(author, title, stream)


def save_original_file(stream: Stream) -> str:
    return stream.download()


def split_original_file(temp_file: AudioSegment, title: str, split_duration: int) -> None:
    duration = len(temp_file)
    interval = split_duration * 60 * 1000
    num_files = math.ceil(duration / interval)
    begin = 0

    for i in track(range(num_files), description="File splitting..."):
        end = begin + interval if begin + interval < duration else duration
        part = temp_file[begin:end]
        part.export(f'{title}_{i + 1}.mp3', format='mp3')
        begin = end


def remove_original_file(path: str) -> None:
    if os.path.exists(path):
        os.remove(path)


@app.command()
def main(url: str, split_file: bool = True, split_duration: int = 10) -> None:
    """
    Write url from youtube to download (for example: https://www.youtube.com/watch?v=25xUoLye53w).
    Use 'no-split-file' if you don't need to split the file.
    If necessary, specify the duration of the files in minutes in 'split-duration'.
    """

    print('Download a file from Youtube...')
    audio = get_audio(url)
    path_to_file = save_original_file(audio.stream)
    print('Youtube file is downloaded ')

    if split_file:
        original_file = AudioSegment.from_file(path_to_file, 'mp4')
        split_original_file(original_file, audio.title, split_duration)
        remove_original_file(path_to_file)


if __name__ == "__main__":
    app()
