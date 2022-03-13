is_article = False
is_code = True

md = open("test.md", "w")


def write(open_file, line):
    print(line, end="")
    open_file.write(line)


with open("mdpy.py", "r") as f:
    for i, l in enumerate(f.readlines()):
        if l[:3] == '"""':
            is_article = not (is_article)
            is_code = not (is_article)
            if is_code:
                write(md, "```python\n")
            elif i:
                write(md, "```\n")
        else:
            if (is_code and not l == "\n") or is_article:
                write(md, f"{l}\n")
if not is_article:
    write(md, "```\n")
md.close()
