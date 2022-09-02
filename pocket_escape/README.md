# Pocket Escape (🏃✔️)

Move urls from Pocket to Netscape formated html file to import them as
bookmarks to any web browser which supports netscape formated bookmark files.

## Background

TBD

## Getting Started

Install requirements

```bash
python -m pip install -r requirements.txt
```

Run script

```bash
python code/pocket_escape.py --consumer-key POCKET_CONSUMER_KEY
```

Script will ask for authorization to Pocket, and then create file with all
links from Pocket.

## Example

This is how looks file created by `pocket_escape`

```html
<!DOCTYPE NETSCAPE-Bookmark-file-1><?xml version="1.0" ?>
<root>
  <!--This is an automatically generated file.
        It will be read and overwritten.
        DO NOT EDIT! -->
  <head>
    <meta HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8"/>
    <title>Bookmarks</title>
  </head>
  <body>
    <h1>Bookmarks Menu</h1>
    <DT>
      <h3>POCKET_ESCAPE[2022-09-02]</h3>
    </DT>
    <DL>
      <DT>
        <a HREF="http://piszczala.pl/">Jarosław Piszczała - Python Developer</a>
      </DT>
      <DT>
        <a HREF="https://akademiapython.pl/">O Pythonie w inny sposób</a>
      </DT>
      <DT>
        <a HREF="https://docs.python.org/3/">3.10.2 Documentation</a>
      </DT>
    </DL>
  </body>
</root>
```
