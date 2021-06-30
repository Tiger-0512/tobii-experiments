from PIL import Image
import os, argparse, pathlib

parser = argparse.ArgumentParser(description="Remove background of images")
parser.add_argument("target_path", help="Target folder path")
parser.add_argument("destination_path", help="Destination folder path")
args = parser.parse_args()

target = args.target_path
destination = args.destination_path

p = pathlib.Path(target)
p_list = list(p.glob("*.png"))

os.makedirs(destination, exist_ok=True)


count = 0
print("******* Start cutting out blank space... *******")
for p in p_list:
    count += 1

    im = Image.open(p)
    cropped = im.crop(im.getbbox())
    w, h = cropped.size
    if (h >= w and h <= w * 2) or (h <= w and h * 2 >= w):
        cropped.save("{}/cutout_{}.png".format(destination, pathlib.Path(p.name).stem))

    if count % 100 == 0:
        print("Cutting out blank space of {}th image...\n".format(count))
print("\n******* Finish cutting out blank space! *******")
