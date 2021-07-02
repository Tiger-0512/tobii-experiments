import sys, os
import tobii_research as tr
import pandas as pd
import numpy as np
from psychopy import core, visual, event

sys.path.append("../")
from tools import features


def change_message(pos_pix, msg, shown_msg):
    if (
        shown_msg.pos[0] - 100 < pos_pix[0] < shown_msg.pos[0] + 100
        and shown_msg.pos[1] - 100 < pos_pix[1] < shown_msg.pos[1] + 100
    ):
        shown_msg.text = msg
        shown_msg.height = 64
    else:
        shown_msg.text = msg[0]
        shown_msg.height = 192


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
msg_list = ["apple", "banana", "orange", "grape", "pineapple"]

# Output file
out = []

# Show eye tracker settings
features.show_eyetracker(my_eyetracker)

# Create and Show introduction
win, message1 = features.introduction(display_size)

# Start eye tracking
my_eyetracker.subscribe_to(
    tr.EYETRACKER_GAZE_DATA, gaze_data_callback, as_dictionary=True
)

msg_center = visual.TextStim(
    win,
    text=msg_list[0][0],
    units="pix",
    pos=[0, 0],
    height=192,
)
msg_left = visual.TextStim(
    win,
    text=msg_list[1][0],
    units="pix",
    pos=[-0.7 * display_size[0] / 2, 0],
    height=192,
)
msg_right = visual.TextStim(
    win,
    text=msg_list[2][0],
    units="pix",
    pos=[0.7 * display_size[0] / 2, 0],
    height=192,
)
msg_top = visual.TextStim(
    win,
    text=msg_list[3][0],
    units="pix",
    pos=[0, 0.7 * display_size[1] / 2],
    height=192,
)
msg_bottom = visual.TextStim(
    win,
    text=msg_list[4][0],
    units="pix",
    pos=[0, -0.7 * display_size[1] / 2],
    height=192,
)
msg_h, msg_w = msg_center.boundingBox

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

    # Modify x, y that the origin becomes center of the display
    y = -y
    x, y = 2 * (x - 0.5), 2 * (y + 0.5)

    x_pix = x * display_size[0] / 2
    y_pix = y * display_size[1] / 2

    change_message((x_pix, y_pix), msg_list[0], msg_center)
    change_message((x_pix, y_pix), msg_list[1], msg_left)
    change_message((x_pix, y_pix), msg_list[2], msg_right)
    change_message((x_pix, y_pix), msg_list[3], msg_top)
    change_message((x_pix, y_pix), msg_list[4], msg_bottom)

    circle.pos = (x, y)

    msg_center.draw()
    msg_left.draw()
    msg_right.draw()
    msg_top.draw()
    msg_bottom.draw()

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

win.close()
core.quit()
