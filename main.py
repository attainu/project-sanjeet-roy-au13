import os
import glob
import sys
from stat import S_ISREG, ST_CTIME, ST_MODE
import glob
import time
import datetime


def createIfNotExist(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)


def move(folderName, files):
    for file in files:
        os.replace(file, f"{folderName}/{file}")


def sort_by_size():
    # The folder containing files.
    directory = os.getcwd()

    # Get all files.
    list = os.listdir(directory)
    list.remove("by_size")
    list.remove("Images")
    list.remove("Docs")
    list.remove("Media")
    list.remove("others")
    list.remove("by_date")

    # Loop and add files to list.
    pairs = []
    for file in list:

        # Use join to get full file path.
        location = os.path.join(directory, file)

        # Get size and add to list of tuples.
        size = os.path.getsize(location)
        pairs.append((size, file))

    # Sort list of tuples by the first element, size.
    pairs.sort(key=lambda s: s[0])
    flist = []
    for i in pairs:
        flist.append(i[1])
    print(flist)
    move("by_size", flist)


def sort_by_Date():
    dir_path = sys.argv[1] if len(sys.argv) == 2 else r"."

    # all entries in the directory w/ stats
    data = (os.path.join(dir_path, fn) for fn in os.listdir(dir_path))
    data = ((os.stat(path), path) for path in data)

    # regular files, insert creation date
    data = ((stat[ST_CTIME], path) for stat, path in data if S_ISREG(stat[ST_MODE]))
    flistD = []
    for j in sorted((data)):
        flistD.append(j[1])
    print(flistD)
    move("by_date", flistD)


if __name__ == "__main__":

    files = os.listdir()
    files.remove("main.py")
    createIfNotExist("Images")
    createIfNotExist("Docs")
    createIfNotExist("Media")
    createIfNotExist("others")
    createIfNotExist("by_size")
    createIfNotExist("by_date")

    imagesExt = [".jpeg", ".jpg", ".png", ".gif", ".raw"]
    images = [file for file in files if os.path.splitext(file)[1].lower() in imagesExt]

    docsExts = [".docx", ".txt", ".doc", ".pdf"]
    docs = [file for file in files if os.path.splitext(file)[1].lower() in docsExts]

    mediasExts = [
        ".mp4",
        ".mp3",
        ".mov",
        ".3gp",
        ".avi",
        ".flv",
        ".h264",
        ".m4v",
        ".mkv",
    ]
    medias = [file for file in files if os.path.splitext(file)[1].lower() in mediasExts]

    others = []
    for file in files:
        ext = os.path.splitext(file)[1].lower()
        if (
            (ext not in imagesExt)
            and (ext not in docsExts)
            and (ext not in mediasExts)
            and os.path.isfile(file)
        ):
            others.append(file)
    
    print("WELCOME TO JUNK FILE ORGANIZER")
    filter = int(input("If You want to sort by \n""1.Extension press 1 \n""2.Size press 2\n""3.Date Press 3\n""Enter Your Choice:"))
    if filter == 1:
        move("Images", images)
        move("Docs", docs)
        move("Media", medias)
        move("others", others)
        print("Done")
    elif filter == 2:
        sort_by_size()
        print("Done")
    elif filter == 3:
        sort_by_Date()
        print("Done")
