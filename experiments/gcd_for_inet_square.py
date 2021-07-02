import sys, os, glob, textwrap, json
import tobii_research as tr
import pandas as pd
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from psychopy import core, visual, gui, data, event

sys.path.append("../")
from tools import features


def search_domain(x, y, threshold):
    for i in range(len(threshold[0]) - 1):
        for j in range(len(threshold[1]) - 1):
            if (
                threshold[0][i] <= x <= threshold[0][i + 1]
                and threshold[1][j] >= y >= threshold[1][j + 1]
            ):
                return (i, j)
    return (-1, -1)


def domain_to_corner(domain, row, col, display_size):
    len_hor = int(display_size[0] / row)
    len_var = int(display_size[1] / col)
    tl = (len_hor * domain[0], len_var * domain[1])
    br = (len_hor * (domain[0] + 1), len_var * (domain[1] + 1))
    return tl, br


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

# Show eye tracker settings
features.show_eyetracker(my_eyetracker)

# Variables
display_size = [1920, 1080]
threshold = [[-1, -1 / 3, 1 / 3, 1], [1, 0, -1]]
row, col = len(threshold[0]) - 1, len(threshold[1]) - 1
root = {0: ["Carnivore", "n02075296"]}
tree = {
    "n02075296": [
        "n02131653",
        "n02083346",
        "n02120997",
        "n02441326",
        "n02507649",
        "n02134971",
    ]
}
count = 0
x_before = 0
y_before = 0
domains = {
    0: "bear",
    1: "canine",
    2: "feline",
    3: "musteline_mammal",
    4: "procyonid",
    5: "vivernine",
}
img_original_path = (
    "C:\\Users\\Coginf\\repos\\tobii_sdk\\imagenet_tree_renew\\128_128\\128_128.png"
)
img_resized_640_path = (
    "C:\\Users\\CogInf\\repos\\tobii_sdk\\imagenet_tree_renew\\640_640\\640_640.png"
)
# Read Images
img_original = Image.open(img_original_path).resize(display_size)
img_size = img_original.size
img_resized_640 = Image.open(img_resized_640_path).resize(display_size)
# Output file
out = []

# Create and Show introduction
win, message1 = features.introduction(display_size)

# Trace eyes
circle = visual.Circle(
    win,
    units="norm",  # [(-1.0, 1.0), (-1.0, 1.0)],
    size=(0.1 / (display_size[0] / display_size[1]), 0.1),
    lineColor=(0, 255, 255),
)


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
win.flip(clearBuffer=True)

while len(out) == 0:
    continue

while True:
    x, y = out[-1][0]

    if np.isnan(x) or np.isnan(y):
        x = x_before
        y = y_before

    # Trace subject's eye
    gaze = (int(x * img_size[0]), int(y * img_size[1]))

    # Create inner mask
    # tl_inner, br_inner = (gaze[0] - 200, gaze[1] - 200), (gaze[0] + 200, gaze[1] + 200)
    # mask_base = Image.new("L", img_size, 0)
    # mask = ImageDraw.Draw(mask_base)
    # mask.ellipse((tl_inner, br_inner), fill=255)
    # mask_blur = mask_base.filter(ImageFilter.GaussianBlur(10))
    # # Create modified image
    # test = Image.composite(img_original, img_resized_640, mask_blur)

    # Create outer mask
    # tl_outer, br_outer = (gaze[0] - 500, gaze[1] - 500), (gaze[0] + 500, gaze[1] + 500)
    # mask.ellipse((tl_outer, br_outer), fill=255)
    # mask_blur = mask_base.filter(ImageFilter.GaussianBlur(10))
    # # Create modified image
    # test = Image.composite(test, img_resized_640, mask_blur)
    # test_image.image = test

    # Modify x, y that the origin becomes center of the display
    y_circle = -y
    x_circle, y_circle = 2 * (x - 0.5), 2 * (y_circle + 0.5)
    circle.pos = (x_circle, y_circle)

    cur_domain = search_domain(x_circle, y_circle, threshold)
    tl, br = domain_to_corner(cur_domain, row, col, display_size)
    mask_base = Image.new("L", img_size, 0)
    mask = ImageDraw.Draw(mask_base)
    mask.rectangle((tl, br), fill=255)
    test = Image.composite(img_original, img_resized_640, mask_base)
    test_image.image = test

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

print(threshold[0], threshold[1])
print(cur_domain, tl, br)
print(out.tail())
print(count)

win.close()
core.quit()
