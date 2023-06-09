import os
import shutil
import sys


def main():
    filename = sys.argv[1]

    dst = "Прочее"
    for branch in next(os.walk("."))[1]:
        if branch in filename:
            dst = branch
            break

    filetype = filename.rsplit(".", 1)[-1]

    dst += "/" + filetype

    os.makedirs(dst, exist_ok=True)

    shutil.move(filename, dst)


if __name__ == "__main__":
    main()
