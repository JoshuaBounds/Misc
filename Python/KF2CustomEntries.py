"""
Rebuilds custom map entries for the KFGame.ini file.
"""


from typing import *
import re


__all__ = (
    'remove_custom_maps',
    'get_custom_maps',
)


def remove_custom_maps(lines: Iterable[AnyStr]) -> List[AnyStr]:
    """
    Removes custom maps from given lines of .ini file data.
    :param lines:
        Iterable of .ini file lines.
    :return:
        Lines with all custom map data removed.
    """

    # Sorts lines into entry blocks (blocks are .ini code separated
    # by blank lines).
    entries = [[]]
    for line in lines:
        entries[-1].append(line)
        if line == '\n':
            entries.append([])

    # Compiles regex to search for custom map entry blocks.
    re_line_1 = re.compile(r"\[.+KFMapSummary\]")
    re_line_2 = re.compile(r"MapName=.+")

    # Returns False if the given entry meets all criteria to be
    # considered a custom entry; returns True otherwise.
    def filter_vanilla_entries(entry):
        if len(entry) not in (2, 3):
            return True
        if not re_line_1.search(entry[0]):
            return True
        if not re_line_2.search(entry[1]):
            return True
        return False

    # Filters out non vanilla entries.
    filtered_entries = filter(filter_vanilla_entries, entries)

    # Returns lines with custom map data removed.
    return sum(filtered_entries, [])


def get_custom_maps(path: AnyStr) -> List[AnyStr]:
    """
    Creates custom map entries by scanning the given directory
    for .kfm files and using the names of any found.
    :param path:
        Path to the custom map directory to gather map names from.
    :return:
        Entries for custom maps, returned as lines of .ini code.
    """

    # Template for custom map entries.
    entry_template = (
        '[%(name)s KFMapSummary]\n',
        'MapName=%(name)s\n',
    )

    # Gets all map names from the given directory.
    custom_lines = []
    for file_name in os.listdir(path):

        # Gets the full file path.
        # Continues if the path is not actually a file.
        file_path = os.path.join(custom_directory, file_name)
        if not os.path.isfile(file_path):
            continue

        # Gets the name and extension.
        # Continues if the extension is not ".kfm".
        name, extension = os.path.splitext(file_name)
        if extension.casefold() != '.kfm':
            continue

        # Creates custom entry lines using name.
        for line in entry_template:
            custom_lines.append(line % {'name': name})
        custom_lines.append('\n')

    # Returns custom map entries as lines of .ini code.
    return custom_lines


if __name__ == '__main__':

    import os

    ini_path = (
        r"D:\steamCMD\steamapps\common\kf2server\KFGame"
        r"\Config\PCServer-KFGame.ini"
    )
    custom_directory = (
        r"D:\steamCMD\steamapps\common\kf2server\KFGame"
        r"\BrewedPC\Maps\Custom"
    )

    with open(ini_path) as f:
        read_lines = f.readlines()

    vanilla_lines = remove_custom_maps(read_lines)
    custom_lines = get_custom_maps(custom_directory)

    with open(ini_path, 'w') as f:
        f.writelines(vanilla_lines + custom_lines)
