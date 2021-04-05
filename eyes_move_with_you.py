import tobii_research as tr
import pandas as pd
import time
from matplotlib import pyplot as plt
from psychopy import core, visual, gui, data, event
from psychopy.core import getTime, wait

import features


def gaze_data_callback(gaze_data):
    # Print gaze points of left and right eye
    # print("Left eye: ({gaze_left_eye}) \t Right eye: ({gaze_right_eye})".format(
    #     gaze_left_eye=gaze_data['left_gaze_point_on_display_area'],
    #     gaze_right_eye=gaze_data['right_gaze_point_on_display_area']))
    
    gaze_left_eye = gaze_data['left_gaze_point_on_display_area']  # (y_coordinate, x_coordinate)
    gaze_right_eye = gaze_data['right_gaze_point_on_display_area']  # (y_coordinate, x_coordinate)
    out.append([gaze_left_eye, gaze_right_eye])


# Settings
found_eyetrackers = tr.find_all_eyetrackers()
my_eyetracker = found_eyetrackers[0]

# Variables
display_size = [1920, 1080]
flag_l = False
flag_r = False

# Output file
out = []

# Show eye tracker settings
features.show_eyetracker(my_eyetracker)

# Create and Show introduction
win = features.introduction(display_size)[0]


# Start eye tracking
my_eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, gaze_data_callback, as_dictionary=True)

while True:
    if len(out) != 0 and len(out) % 300 == 0:
        # When a subject is looking at Left side in 1 seconds
        if flag_l and out[-1][0][0] < 0.5:
            test_image = visual.ImageStim(win, image='./images/eye_direction_right.jpg', pos=[0, 0])
            test_image.draw()
            win.flip(clearBuffer=True)

        # When a subject is looking at Right side in 1 seconds
        if flag_r and out[-1][0][0] > 0.5:
            test_image = visual.ImageStim(win, image='./images/eye_direction_left.jpg', pos=[0, 0])
            test_image.draw()
            win.flip(clearBuffer=True)

        # When a subject is looking at Left side just now
        if out[-1][0][0] < 0.5:
            flag_l = True
            flag_r = False

        # When a subject is looking at Right side just now
        if out[-1][0][0] > 0.5:
            flag_l = False
            flag_r = True

    # Escape command
    if 'space' in event.getKeys():
        break


# End eye tracking
my_eyetracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, gaze_data_callback)
out = pd.DataFrame(out)

# Save outputs as a csv file
path = './out.csv'
features.save_csv(out, path)

print(out.tail())

core.quit()
win.close()