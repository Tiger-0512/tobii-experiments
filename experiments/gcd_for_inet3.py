import sys, glob, textwrap, json
import tobii_research as tr
import pandas as pd
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from psychopy import core, visual, gui, data, event

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
# Output file
out = []

# Import first images
path = "C:\\Users\\CogInf\\repos\\tobii_sdk\\imagenet_tree_renew\\test"
p_list = glob.glob("{}\*\*.JPEG".format(path))
print(p_list)
template = textwrap.dedent(
    """
    image_{INDEX}_path = p_list[i]
    image_{INDEX} = Image.open(image_{INDEX}_path).resize(
        [display_size[0] // row, display_size[1] // col]
    )
    """
)
for i in range(row * col):
    items = template.format(INDEX=i + 1)
    exec(items)

# Create and Show introduction
win, message1 = features.introduction(display_size)

# Show first images
tmp = [1, -1]
template = textwrap.dedent(
    """
    image_{INDEX} = visual.ImageStim(
        win,
        image=image_{INDEX},
        pos=[2 / row * (i % row - 1), tmp[i // row] / col],
    )
    image_{INDEX}.draw()
    """
)
for i in range(row * col):
    items = template.format(INDEX=i + 1)
    exec(items)

# Trace eyes
circle = visual.Circle(
    win,
    units="norm",  # [(-1.0, 1.0), (-1.0, 1.0)],
    size=(0.1 / (display_size[0] / display_size[1]), 0.1),
    lineColor=(0, 255, 255),
)

win.flip(clearBuffer=True)


# Start eye tracking
my_eyetracker.subscribe_to(
    tr.EYETRACKER_GAZE_DATA, gaze_data_callback, as_dictionary=True
)

while len(out) == 0:
    continue

while True:
    x, y = out[-1][0]

    if np.isnan(x) or np.isnan(y):
        x = x_before
        y = y_before

    # Trace subject's eye
    # gaze = (int(x * img_size[0]), int(y * img_size[1]))

    # Modify x, y that the origin becomes center of the display
    y_circle = -y
    x_circle, y_circle = 2 * (x - 0.5), 2 * (y_circle + 0.5)
    circle.pos = (x_circle, y_circle)

    # circle.draw()
    # win.flip(clearBuffer=True)
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

win.close()
core.quit()
