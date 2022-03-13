import pathlib
import pdb
import sys

# https://pypi.org/project/sanitize-filename/ for filenames
# TODO: split logic to make unit tests
# TODO: files duplication https://www.geeksforgeeks.org/finding-duplicate-files-with-python/
# TODO: Cut long filenames


print(sys.argv)

p = pathlib.Path(sys.argv[1])
# pdb.s
# pdb.set_trace()
# out_dir = p.home() / 'output'

# # pdb.set_trace()

not_allowed_chars = [
    " ",
    ",",
    "\\",
    "/",
    ":",
    "*",
    "?",
    '"',
    "<",
    ">",
    "|",
    ".",
    "!",
    '"',
]

for x in p.rglob("*"):
    try:
        if x.is_file():
            filename = x.stem
        else:
            filename = x.name
        for char in not_allowed_chars:
            filename = filename.replace(char, "_")
        filename = filename.lower()
        filename = filename.strip("_")

        if x.is_file():
            x.rename((x.parent / filename).with_suffix(x.suffix))
        else:
            x.rename(x.parent / filename)
    except Exception as e:
        print(e)
