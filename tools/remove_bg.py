"""
Requirements
- python 3.8 or newer
- torch and torchvision stable version
more information: https://github.com/danielgatis/rembg
"""

from rembg.bg import remove
import numpy as np
import io, os, argparse, pathlib
from PIL import Image, ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True

parser = argparse.ArgumentParser(description="Remove background of images")
parser.add_argument("target_path", help="Target folder path")
parser.add_argument("destination_path", help="Destination folder path")
args = parser.parse_args()

target = args.target_path
destination = args.destination_path

p = pathlib.Path(target)
p_list = list(p.glob("*"))

os.makedirs(destination, exist_ok=True)

count = 0
print("******* Start removing background... *******")
for p in p_list:
    count += 1

    f = np.fromfile(p)
    result = remove(f)
    img = Image.open(io.BytesIO(result)).convert("RGBA")
    img.save("{}/removed_{}.png".format(destination, pathlib.Path(p.name).stem))

    if count % 10 == 0:
        print("Removing {}th image's background...\n".format(count))
print("\n******* Finish removing background! *******")
