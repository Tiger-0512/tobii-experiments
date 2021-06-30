import argparse, pathlib, os
from PIL import Image


def resize(target, destination, size):
    p = pathlib.Path(target)
    p_list = list(p.glob("*"))

    os.makedirs(destination, exist_ok=True)

    count = 0
    print("******* Start resizing... *******\n\n")
    for p in p_list:
        count += 1

        im = Image.open(p)
        im_resized = im.resize(size=size)
        im_resized.save("{}/resized_{}".format(destination, p.name))

        if count % 100 == 0:
            print("Resizing {}th image...\n".format(count))
    print("\n******* Finish resizing! *******")


parser = argparse.ArgumentParser(description="Resize images to square in one folder")

parser.add_argument("target_path", help="Target folder path")
parser.add_argument("destination_path", help="Destination folder path")
parser.add_argument("size", help="Length of images side to resize")

args = parser.parse_args()

target = args.target_path
destination = args.destination_path
size = (int(args.size), int(args.size))

resize(target, destination, size)
