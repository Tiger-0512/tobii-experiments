import sys, os, json, sys, math
import tobii_research as tr
import pandas as pd
import numpy as np
from PIL import Image, ImageDraw
from psychopy import core, visual, event
from psychopy.core import getTime, wait

sys.path.append("../")
from tools import features


# arguments: A(0, 0), B(x, y), d_ca(=AB=CA), d_bc(=BC)
# return: C(x, y)
def calc_coordinate(B, d_ca, d_bc, cur_deg, deg):
    alpha = math.atan2(B[1], B[0])

    x = (2 * (d_ca ** 2) - d_bc ** 2) / (2 * d_ca)
    s = (2 * d_ca + d_bc) / 2
    y = 2 * math.sqrt(s * (s - d_ca) * (s - d_ca) * (s - d_bc)) / d_ca
    C = [
        (
            int(x * math.cos(alpha) - y * math.sin(alpha)),
            int(x * math.sin(alpha) + y * math.cos(alpha)),
        ),
        (
            int(x * math.cos(alpha) + y * math.sin(alpha)),
            int(x * math.sin(alpha) - y * math.cos(alpha)),
        ),
    ]

    if 0 <= cur_deg < 90 or cur_deg == 360:
        if C[0][0] > 0 and C[0][1] >= 0:
            C = C[0]
        else:
            C = C[1]
    elif 90 <= cur_deg < 180:
        if C[0][0] <= 0 and C[0][1] > 0:
            C = C[0]
        else:
            C = C[1]
    elif 180 <= cur_deg < 270:
        if C[0][0] < 0 and C[0][1] <= 0:
            C = C[0]
        else:
            C = C[1]
    else:
        if C[0][0] >= 0 and C[0][1] < 0:
            C = C[0]
        else:
            C = C[1]

    return C


def create_peripheral_stim(win, stim_list, display_size):
    # Calculate stimilus coordinates
    # ref: https://memo.sugyan.com/entry/20090408/1239148436
    deg = 360 / len(stim_list)
    d_ab = display_size[1] * 0.7 / 2
    d_bc = math.sqrt(2 * (d_ab ** 2) * (1 - math.cos(math.radians(deg))))
    coordinates = []

    B = [d_ab, 0]
    cur_deg = deg
    for s in stim_list:
        C = calc_coordinate(B, d_ab, d_bc, cur_deg, deg)
        coordinates.append(C)
        B = C
        cur_deg += deg

        stim = visual.TextStim(
            win,
            text="{}".format(s),
            units="pix",
            pos=C,
            height=32,
        )
        stim.draw()
    return coordinates


def judge_eyes_fixing(
    prev_gaze, cur_gaze, prev_time, cur_time, pix_thr, time_thr, coordinates, back_pos
):
    if (
        prev_gaze[0] - pix_thr < cur_gaze[0] < prev_gaze[0] + pix_thr
        and prev_gaze[1] - pix_thr < cur_gaze[1] < prev_gaze[1] + pix_thr
    ):
        # print("phase 1 clear")
        if cur_time - prev_time > time_thr:
            # print("phase 2 clear")
            for i, c in enumerate(coordinates):
                print(coordinates[i], i, c)
                if (
                    c[0] - pix_thr < cur_gaze[0] < c[0] + pix_thr
                    and c[1] - pix_thr < cur_gaze[1] < c[1] + pix_thr
                ):
                    return i  # Change stimilus
            if (
                back_pos[0] - pix_thr < cur_gaze[0] < back_pos[0] + pix_thr
                and back_pos[1] - pix_thr < cur_gaze[1] < back_pos[1] + pix_thr
            ):
                return -3  # Change stimilus and back to home

            return -1
        else:
            return -1  # Hold states
    else:
        return -2  # Restart fixing


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

coordinates = create_peripheral_stim(win, stim_list, display_size)
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

    judge = judge_eyes_fixing(
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

    coordinates = create_peripheral_stim(win, stim_list, display_size)
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
