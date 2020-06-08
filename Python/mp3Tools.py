
import eyed3
import re
import os
from typing import AnyStr


def add_track_number_to_file(file_path: AnyStr, track_num: int = 0):
    """
    Adds track number metadata to the given file.
    :param file_path:
        Target directory.
    :param track_num:
        Track number to insert into the metadata.
    """
    mp3_file = eyed3.load(file_path)
    mp3_file.tag.track_num = track_num
    mp3_file.tag.save()


def add_title_from_file_name(file_path: AnyStr, pattern: AnyStr):
    """
    Uses the .mp3's file name to set it's title tag. 
    :param file_path: 
        Path to the target .mp3 file.
    :param pattern:
        Regex pattern used to match the title of the track from the
        file name.
    """
    _, file_name = os.path.split(file_path)
    name, _ = os.path.splitext(file_name)
    track = re.search(pattern, name).group(0)
    audio_file = eyed3.load(file_path)
    audio_file.tag.title = track
    audio_file.tag.save()
