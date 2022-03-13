from converter import Converter  # https://github.com/senko/python-video-converter
import re
import pprint
import shutil
import exifread
import glob
import os
import pathlib

"""
 MAKE PHOTOS IN FIRST PLACE WITH IPHONE PHOTO, not instagram / snapchat / facebook / etc. for best performance

 LOGI przy przemieszczaniu z informacją o timestampach. Może pomóc przy uprzątnięciu tego co zostało :)
 dodawanie samej daty + różnica na jakiej się możę to znaleźć ze znacznikiem niepewności

 datetime do odpowiedniego formatu, będzie łatwiej na nim operować
"""

moved_files = {"photo": 0, "video": 0, "image": 0, "photo-mov": 0, "none": 0}
index_datetime = {}


class FilesCounter:
    def __init__(self):
        self.photo = 0
        self.video = 0
        self.image = 0
        self.photo_mov = 0
        self.none = 0

    def all(self):
        return self.photo + self.video + self.image + self.none

    def moved(self):
        return self.photo + self.video + self.image


def move_file(dst, src, type, datetime):
    result = re.search("\w*_(\d*)", str(src.name))
    if result:
        index_datetime[result.groups()[0]] = datetime
    if not os.path.exists(dst):
        moved_files[type] = moved_files[type] + 1
        shutil.move(src, dst)
    else:
        print(src, dst)


def change_files_names(directory_path):
    for d in glob.glob(directory_path + "/*.JPG"):

        path = pathlib.Path(d)

        with open(path, "rb") as f_jpg:
            tags = exifread.process_file(f_jpg, details=True)
            try:
                datetime = (
                    str(tags["EXIF DateTimeOriginal"])
                    .replace(":", "-")
                    .replace(" ", "_")
                )
                dst = path.parents[1] / "{}.jpg".format(datetime)
                move_file(dst, path, "photo", datetime)

                if path.with_suffix(".MOV").exists():
                    src = path.with_suffix(".MOV")
                    dst = path.parents[1] / "{}.mov".format(datetime)
                    move_file(dst, src, "photo-mov", datetime)

            except KeyError:
                tags["JPEGThumbnail"] = None
                print(path, tags)
                if tags.get("Image Software", ""):
                    soft = str(tags.get("Image Software", ""))
                    name = str(path.name)
                    print(soft, name)
                    directory = path.parents[1] / soft
                    if not os.path.exists(directory):
                        os.makedirs(directory)
                    dst = path.parents[1] / soft / name
                    print(dst)
                    move_file(dst, path, "image", None)

    c = Converter()
    for d in glob.glob(directory_path + "/*.MOV"):
        path = pathlib.Path(d)
        # print(path)
        datetime: str = c.probe(d).streams[0].metadata.get("creation_time")
        datetime = datetime.split(".")[0].replace("T", "_").replace(":", "-")
        dst = path.parents[1] / "{}.mov".format(datetime)
        move_file(dst, path, "video", datetime)

    for d in glob.glob(directory_path + "/*.MP4"):
        path = pathlib.Path(d)
        # print(path)
        try:
            datetime: str = c.probe(d).streams[0].metadata.get("creation_time")
            datetime = datetime.split(".")[0].replace("T", "_").replace(":", "-")
        except AttributeError:
            print(c.probe(d))
        else:
            dst = path.parents[1] / "{}.mp4".format(datetime)
            move_file(dst, path, "video", datetime)

    for d in glob.glob(directory_path + "/*.AAE"):
        os.remove(d)

    moved_files["none"] = moved_files["none"] + len(glob.glob(directory_path + "/*"))


hd = "/home/jarek/Desktop/DCIM"


for apple_directory in glob.glob(hd + "/*"):
    change_files_names(apple_directory)

print(moved_files)
print(
    "all files: ",
    moved_files["photo"]
    + moved_files["video"]
    + moved_files["image"]
    + moved_files["none"],
)


with open(hd + "/apple.log", "w") as f:
    pprint.pprint(index_datetime, f)
