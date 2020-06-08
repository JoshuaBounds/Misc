
from typing import AnyStr, Iterable, List
import os
import shutil


def copy_files_by_extension(
        source: AnyStr,
        destination: AnyStr,
        extensions: Iterable[AnyStr],
) -> List[AnyStr]:
    """
    Copies a directory tree whilst masking files by extension.
    :param source:
        Source directory.
    :param destination:
        Destination for the copied directory tree.
    :param extensions:
        Whitelisted file extensions.
    :return:
        All copied files.
    """

    result = []
    for dirpath, dirname, filenames in os.walk(source):
        for filename in filenames:

            _, extension = os.path.splitext(filename)
            if extension not in extensions:
                continue

            newdir = dirpath.replace(source, destination)
            if not os.path.isdir(newdir):
                os.makedirs(newdir)

            filepath = os.path.join(dirpath, filename)
            new_filepath = filepath.replace(source, destination)
            shutil.copyfile(filepath, new_filepath)

            result.append(new_filepath)

    return result


if __name__ == '__main__':

    DIR = r"F:\Music"
    DESTINATION = os.path.join(os.environ['USERPROFILE'], 'Desktop', 'Music')
    VALID_EXTENSIONS = '.mp3', '.m4a'

    copy_files_by_extension(DIR, DESTINATION, VALID_EXTENSIONS)
