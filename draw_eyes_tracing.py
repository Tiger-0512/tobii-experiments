import tobii_research as tr
import pandas as pd
import time
from matplotlib import pyplot as plt
from psychopy import core, visual, gui, data, event
from psychopy.core import getTime, wait
from psychopy.tools.monitorunittools import posToPix

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

# Output file
out = []

# Show eye tracker settings
features.show_eyetracker(my_eyetracker)

# Create and Show introduction
win, message1 = features.introduction()
magnification = posToPix(message1)[1]


# Start eye tracking
my_eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, gaze_data_callback, as_dictionary=True)

while True:
    if len(out) != 0:
        x, y = out[-1][0]
        if x != 'nan' and y != 'nan':
            # Modify x, y that the origin becomes center of the display
            y = -y
            x, y = 2 * (x - 0.5), 2 * (y + 0.5)

            # Trace subject's eye
            test_image = visual.ImageStim(
                win,
                image='C:\\Users\\CogInf\\Desktop\\youtuber.jpg',
                pos=[(display_size[0] / magnification / 2) * x, (display_size[1] / magnification / 2) * y],
                size=[3, 3]
                )
            test_image.draw()
            win.flip(clearBuffer=True)

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