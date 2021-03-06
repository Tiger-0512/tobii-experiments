import sys
import tobii_research as tr
import pandas as pd
import numpy as np
from PIL import Image, ImageDraw
from matplotlib import pyplot as plt
from psychopy import core, visual, gui, data, event
from psychopy.core import getTime, wait
from psychopy.tools.monitorunittools import posToPix

sys.path.append("../")
from tools import features


def gaze_data_callback(gaze_data):
    # Print gaze points of left and right eye
    # print("Left eye: ({gaze_left_eye}) \t Right eye: ({gaze_right_eye})".format(
    #     gaze_left_eye=gaze_data['left_gaze_point_on_display_area'],
    #     gaze_right_eye=gaze_data['right_gaze_point_on_display_area']))

    gaze_left_eye = gaze_data[
        "left_gaze_point_on_display_area"
    ]  # (y_coordinate, x_coordinate)
    gaze_right_eye = gaze_data[
        "right_gaze_point_on_display_area"
    ]  # (y_coordinate, x_coordinate)
    out.append([gaze_left_eye, gaze_right_eye])


# Change working directory
if not os.path.isfile(os.path.basename(__file__)):
    os.chdir("./experiments")

# Settings
found_eyetrackers = tr.find_all_eyetrackers()
my_eyetracker = found_eyetrackers[0]

# Variables
display_size = [1920, 1080]
img_original_path = "./images/oura.jpg"
img_resized_path = "./images/oura_resized.jpg"

# Read Images
img_original = Image.open(img_original_path)
img_size = img_original.size
img_resized = Image.open(img_resized_path).resize(img_size)
# mask_base = Image.new('L', img_size, 0)

# Output file
out = []

# Show eye tracker settings
features.show_eyetracker(my_eyetracker)

# Create and Show introduction
win, message1 = features.introduction(display_size)

# For Test
# cv2.imwrite(img_original_path[:-4] + '_copy' + img_original_path[-4:], img_original)


# Start eye tracking
my_eyetracker.subscribe_to(
    tr.EYETRACKER_GAZE_DATA, gaze_data_callback, as_dictionary=True
)

test_image = visual.ImageStim(
    win,
    image=img_original,
    pos=[0, 0],
)
test_image.draw()

circle = visual.Circle(
    win,
    units="norm",  # [(-1.0, 1.0), (-1.0, 1.0)],
    size=(0.1 / (display_size[0] / display_size[1]), 0.1),
    lineColor=(0, 255, 255),
)

win.flip(clearBuffer=True)

count = 0
x_before = 0
y_before = 0

while len(out) == 0:
    continue

while True:
    x, y = out[-1][0]

    if np.isnan(x) or np.isnan(y):
        x = x_before
        y = y_before

    # Trace subject's eye
    img = img_original
    gaze = (int(x * img_size[0]), int(y * img_size[1]))

    tl, br = (gaze[0] - 300, gaze[1] - 300), (gaze[0] + 300, gaze[1] + 300)

    # Create mask
    mask_base = Image.new("L", img_size, 0)
    mask = ImageDraw.Draw(mask_base)
    mask.ellipse((tl, br), fill=255)
    # mask_base.save('./images/test.jpg')

    # Create modified image
    test = Image.composite(img_original, img_resized, mask_base)
    test_image.image = test

    # Modify x, y that the origin becomes center of the display
    y_circle = -y
    x_circle, y_circle = 2 * (x - 0.5), 2 * (y_circle + 0.5)
    circle.pos = (x_circle, y_circle)

    test_image.draw()
    circle.draw()
    win.flip(clearBuffer=True)
    count += 1

    x_before = x
    y_before = y

    # Escape command
    if "space" in event.getKeys():
        break

# End eye tracking
my_eyetracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, gaze_data_callback)
out = pd.DataFrame(out)

# Save outputs as a csv file
path = "./out.csv"
features.save_csv(out, path)

print(out.tail())
print(count)
print(tl, br, gaze)
print(img_size)

win.close()
core.quit()
