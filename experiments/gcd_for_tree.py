import cv2, json, sys
from PIL import Image, ImageDraw
import tobii_research as tr
import pandas as pd
import numpy as np
from psychopy import core, visual, event
from psychopy.core import getTime, wait

import features


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

# Variables
display_size = [1920, 1080]

with open("./imagenet_tree.json") as f:
    dic = json.load(f)
stim_list = dic["0"]
num = len(stim_list)
print(num)

# Output file
out = []

# Show eye tracker settings
features.show_eyetracker(my_eyetracker)

# Create and Show introduction
win, message1 = features.introduction(display_size)

# # Start eye tracking
my_eyetracker.subscribe_to(
    tr.EYETRACKER_GAZE_DATA, gaze_data_callback, as_dictionary=True
)

msg_back = visual.TextStim(
    win,
    text="back",
    units="pix",
    pos=[-0.7 * display_size[0] / 2, 0.7 * display_size[1] / 2],
    height=64,
)

circle = visual.Circle(
    win,
    units="pix",  # [(-1.0, 1.0), (-1.0, 1.0)],
    size=(50, 50),
    lineColor=(0, 255, 255),
)

coordinates = features.create_peripheral_stim(win, stim_list, display_size)
win.flip(clearBuffer=True)

count = 0
x_before = 0
y_before = 0

while len(out) == 0:
    continue

prev_time = getTime()

while True:
    cur_time = getTime()
    x, y = out[-1][0]

    if np.isnan(x) or np.isnan(y):
        x = x_before
        y = y_before

    # Modify x, y that the origin comes center of the display
    y = -y
    x, y = 2 * (x - 0.5), 2 * (y + 0.5)
    x_pix = x * display_size[0] / 2
    y_pix = y * display_size[1] / 2

    judge = features.judge_eyes_fixing(
        [x_before, y_before],
        [x_pix, y_pix],
        prev_time,
        cur_time,
        300,
        2,
        coordinates,
        msg_back.pos,
    )

    if judge == -1:
        pass
    elif judge == -2:
        prev_time = cur_time
    elif judge == -3:  # When gaze is fixed "back button"
        stim_list = dic["0"]
        prev_time = cur_time
    else:  # judge == 0, 1, 2, ...
        try:
            print(judge)
            print("{}".format(stim_list[judge]))
            stim_list = dic["{}".format(stim_list[judge])]
            prev_time = cur_time
            print("True")
        except:
            print("stim_list is not exist, check json file")
            print("{}".format(stim_list[judge]))
            sys.exit(1)

    circle.pos = (x_pix, y_pix)
    circle.draw()

    coordinates = features.create_peripheral_stim(win, stim_list, display_size)
    msg_back.draw()

    win.flip()
    count += 1

    x_before = x_pix
    y_before = y_pix

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

# print(msg_center.boundingBox)  # return pixel
# print(msg_right.boundingBox)  # return pixel
# print(msg_left.boundingBox)  # return pixel

win.close()
core.quit()
