import math
from pydub import AudioSegment
from rich.progress import track


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
