"""
Change filenames for Xiaomi 3S files to format 'yyyy-mm-dd hh-mm-ss'
"""
import re
import os


def get_new_filename(filename):
    result = re.search(
        "\w*_(\d{4})(\d{2})(\d{2})_(\d{2})(\d{2})(\d{2})(\w*?)?\.(\w*)", filename
    )
    if result:
        year, month, day, hour, minute, second, postfix, f = result.groups()
        return (
            "-".join([year, month, day])
            + "_"
            + "-".join([hour, minute, second, postfix])
            + "."
            + f
        )
    else:
        return ""


if __name__ == "__main__":
    directory = "/home/jarek/Desktop/2018"
    dir_files = os.listdir(directory)
    for file in dir_files:
        print(file)
        new_file = get_new_filename(file)
        print(new_file)
        if new_file and not os.path.exists(os.path.join(directory, new_file)):
            import shutil

            shutil.move(
                os.path.join(directory, file), os.path.join(directory, new_file)
            )
        else:
            print(file, "+++++")
