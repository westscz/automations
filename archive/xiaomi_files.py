"""
Change filenames for Xiaomi 3S files to format 'yyyy-mm-dd hh-mm-ss'
"""
import re
import os


def get_new_filename(filename):
    result = re.search(
        "\w*_(\d{4})(\d{2})(\d{2})_(\d{2})(\d{2})(\d{2})(?:_\w*?)\.(\w*)", filename
    )
    if result:
        year, month, day, hour, minute, second, f = result.groups()
        return "-".join([year, month, day]) + " " + ".".join([hour, minute, second, f])
    else:
        return ""


if __name__ == "__main__":
    directory = "/media/jarek/Work [HDD]/290118/New folder/DCIM/Camera"
    dir_files = os.listdir(directory)
    for file in dir_files:
        new_file = get_new_filename(file)
        if new_file:
            os.rename(os.path.join(directory, file), os.path.join(directory, new_file))
