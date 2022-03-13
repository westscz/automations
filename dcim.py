import glob
import shutil

import exifread
import pathlib

sd_path = "/media/jarek/5FC6-EB2A"


# VIDEO PRIVATE/AVCHD/BDMV/STREAM/
# IMAGE DCIM/122_PANA/

for src in glob.glob("/home/jarek/Desktop/photo/123_PANA/*.*"):
    src = pathlib.Path(src)
    print(src)
    with open(src, "rb") as f_jpg:
        tags = exifread.process_file(f_jpg, details=True)
        try:
            datetime = (
                str(tags["EXIF DateTimeOriginal"]).replace(":", "-").split(" ")[0]
            )
            dst_directory: pathlib.Path = src.parent / datetime
            if not dst_directory.exists():
                dst_directory.mkdir()
            dst = src.parent / datetime / src.name
            shutil.move(src, dst)
        except KeyError:
            print(tags)
