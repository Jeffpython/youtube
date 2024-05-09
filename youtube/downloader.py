import os.path
from pytube import YouTube
from pytube.exceptions import VideoUnavailable
from pytube.streams import Stream
from pytube.cli import on_progress

from dataclasses import dataclass


@dataclass
class Audio:
    author: str
    title: str
    stream: Stream
    bitrate: str
    codec: str


class AppError(Exception):
    def __init__(self, reason: str) -> None:
        super().__init__(reason)
        self.reason = reason


class VideoUnavailableError(AppError):
    def __init__(self, url: str) -> None:
        super().__init__(f'Video is not available: [{url}]')
        self.url = url


def get_audio(url: str) -> Audio | None:
    try:
        yt = YouTube(url, on_progress_callback=on_progress)
        author = yt.author
        title = yt.title.replace(' ', '_')
        stream = yt.streams.get_audio_only(subtype='mp4')
        bitrate = stream.abr
        codec = stream.audio_codec
    except VideoUnavailable as err:
        raise VideoUnavailableError(url=url) from err

    return Audio(author=author, title=title, stream=stream, bitrate=bitrate, codec=codec)


def remove_original_file(path: str) -> None:
    if not path:
        return

    if not os.path.exists(path):
        return

    os.remove(path)
