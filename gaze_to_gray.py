#####################################################
# Notice
# Run this experiment with sampling rate : 150 ~ 600
#####################################################


import cv2
import tobii_research as tr
import pandas as pd
import numpy as np
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
img_path = 'C:\\Users\\CogInf\\Desktop\\cyan.png'

# Output file
out = []

# Show eye tracker settings
features.show_eyetracker(my_eyetracker)

# Create and Show introduction
win, message1 = features.introduction(display_size)

# For Test
test = cv2.imread(img_path)
cv2.imwrite(img_path[:-4] + '_copy' + img_path[-4:], test)


# Start eye tracking
my_eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, gaze_data_callback, as_dictionary=True)

test_image = visual.ImageStim(
    win,
    image=img_path,
    pos=[0, 0],
    )
test_image.draw()

circle = visual.Circle(
    win,
    units='norm',  # [(-1.0, 1.0), (-1.0, 1.0)],
    size = (0.1 / (display_size[0] / display_size[1]), 0.1),
    lineColor=(0, 255, 255)
    )

win.flip(clearBuffer=True)

while True:
    if len(out) != 0:
        x, y = out[-1][0]
        if not np.isnan(x) and not np.isnan(y):
            # Trace subject's eye
            img = cv2.imread(img_path)
            img_shape = img.shape[:2]
            gaze = (int(x * img_shape[1]), int(y * img_shape[0]))

            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img_gray = np.stack((img_gray,)*3, axis=-1)

            # Make mask
            mask = np.zeros(img_shape, dtype="uint8")
            cv2.circle(mask, gaze, 30, 255, -1)

            # Synthesize images
            synthesized_img = features.synthesize_images_with_mask(img, img_gray, mask)

            # Save modified image
            cv2.imwrite(img_path, synthesized_img)
            test_image.image = img_path
            test_image.draw()

            # Modify x, y that the origin becomes center of the display
            y = -y
            x, y = 2 * (x - 0.5), 2 * (y + 0.5)
            circle.pos = (x, y)

            test_image.draw()
            circle.draw()
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