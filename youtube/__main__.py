from typer import Typer
from pydub import AudioSegment
from youtube.downloader import get_audio, remove_original_file
from youtube.splitter import split_original_file

app = Typer()


@app.command()
def main(url: str, split_file: bool = True, split_duration: int = 10) -> None:
    """
    Write url from YouTube to download (for example: https://www.youtube.com/watch?v=jqnWhBwfbWE).\n
    Use 'no-split-file' if you don't need to split the file.\n
    If necessary, specify the duration of the files in minutes in 'split-duration'.
    """

    print('YouTube file is downloading...')
    audio = get_audio(url)
    print(f'bitrate: {audio.bitrate} \ncodec: {audio.codec}')
    path_to_file = audio.stream.download()

    if split_file:
        original_file = AudioSegment.from_file(path_to_file, 'mp4')
        split_original_file(original_file, audio.title, split_duration)
        remove_original_file(path_to_file)


if __name__ == "__main__":
    app()
