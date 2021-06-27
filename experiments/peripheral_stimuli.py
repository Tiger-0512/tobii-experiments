"""Measure coherence threshold of motion direction
using Staircase procedure, dot direction: 0 (LTR)"""

import math, os, sys, random, textwrap
import numpy as np
from __future__ import absolute_import, division, print_function
from psychopy import core, visual, gui, data, event
from psychopy.tools.filetools import fromFile, toFile
from numpy import matlib, inf
from builtins import range
from PIL import Image
from screeninfo import get_monitors

sys.path.append("../")
from tools import features


try:  # try to get a previous parameters file
    expInfo = fromFile("lastParams.pickle")
except:  # if not there then use a default set
    expInfo = {"Observer": "yh", "Session": "1", "Type[1: RDK; 2: Grating]": "1"}
expInfo["dateStr"] = data.getDateStr()  # add the current time

# present a dialogue to change params
dlg = gui.DlgFromDict(expInfo, title="motion mouse Exp", fixed=["dateStr"])
if dlg.OK:
    toFile("lastParams.pickle", expInfo)  # save params to file for next time
else:
    core.quit()  # the user hit cancel so exit

# 20 Classes
# stim_classs = [
#     "cat",
#     "dog",
#     "cow",
#     "tiger",
#     "rabbit",
#     "horse",
#     "sheep",
#     "monkey",
#     "lion",
#     "bear",
#     "fox",
#     "raccoon",
#     "squirrel",
#     "elephant",
#     "dear",
#     "boar",
#     "kangaroo",
#     "koala",
#     "rhino",
#     "pig",
# ]

# 10 Classes
target_class = "cat"
non_target_classes = [
    "dog",
    "elephant",
    "tiger",
    "rabbit",
    "kangaroo",
    "sheep",
    "monkey",
    "lion",
    "bear",
]

# making Stimlist
stim_list = []
for state in [0, 1]:  # 2 state (whether the target exists or not)
    for size in [1, 2, 3]:  # 3 stimuli size
        for rate in [1, 2, 3]:  # 3 magnification rates to periphery
            for pos in [0, 1, 2]:  # 3 positions (0: center)
                if pos == 0:
                    ori = 0
                    # append a python 'dictionary' to the list
                    stim_list.append(
                        {
                            "state": state,
                            "size": size,
                            "rate": rate,
                            "pos": pos,
                            "ori": ori,
                        }
                    )
                else:
                    for ori in range(0, 360, 90):  # 4 directions
                        stim_list.append(
                            {
                                "state": state,
                                "size": size,
                                "rate": rate,
                                "pos": pos,
                                "ori": ori,
                            }
                        )


# organize them with the trial handler  repeated 10 times
trials = data.TrialHandler(
    stim_list,
    10,
    method="random",
    extraInfo={
        "participant": expInfo["Observer"],
        "session": expInfo["Session"],
        "MotionType": expInfo["Type[1: RDK; 2: Grating]"],
    },
)


# make a text file to save data
fileName = expInfo["Observer"] + "_" + expInfo["Session"] + "_" + expInfo["dateStr"]
# dataFile = open(fileName+'.csv', 'w') # a simple text file with 'comma-separated- values'
# dataFile.write('ori,sp,correct\n')

"""
From Yung-Hao San
notes: we used "hight" as units, my macbookpro is 18cm(900pixel), assume 57cm distance,
so 1 degree =50 pixel, 1/18 (.055) in ratio
below all use visual angle to caculate size, so always multiple an2ra

In My Case,
Display Height: 33.5 cm (1890 pix)
Distance: 57.0 cm
i.e.
VA: 32.8 degree
1 degree: 1890 / 32.8 = 57.6 pix
"""
# create window and stimuli,
# This version I used "pixel" as units
display_size = [get_monitors()[0].width, get_monitors()[0].height]
print(display_size)
VA = features.calc_VA(57.0, 33.5)
an2ra = 1 / VA
an2px = round(display_size[1] / VA, 1)
win = visual.Window(
    display_size,
    allowGUI=True,
    color=(0, 0, 0),
    monitor="testMonitor",
    winType="pyglet",
    units="pix",
)  # fullscr=True
fixation = visual.GratingStim(
    win,
    color=-1,
    colorSpace="rgb",
    pos=(0.0, 0.2 * display_size[1]),
    tex=None,
    mask="circle",
    size=0.2 * an2px,
)
message1 = visual.TextStim(
    win,
    pos=[0, +0.14 * display_size[1]],
    text="Please move the mouse to the gray point to start trials. ",
)
message2 = visual.TextStim(
    win,
    pos=[0, 0.1 * display_size[1]],
    text="You will see a moving object for a secend",
)
message3 = visual.TextStim(
    win,
    pos=[0, 0.05 * display_size[1]],
    text="Afterwards, please click the mouse to refer direction and speed of the moving object.",
)
Feedback1 = visual.TextStim(
    win, pos=[0, +0.14 * display_size[1]], text="Physical propeties "
)
Feedback2 = visual.TextStim(
    win, pos=[0, +0.1 * display_size[1]], text="Mouse response "
)
Feedback3 = visual.TextStim(win, pos=[0, +0.05 * display_size[1]], text="Feedback ")
output = visual.TextBox2(
    win,
    text="No mouse pressed yet",
    font="Open Sans",
    pos=(-0.3 * display_size[1], -0.4 * display_size[1]),
)
output2 = visual.TextBox2(
    win,
    text="noise direction/speed",
    font="Open Sans",
    pos=(0.3 * display_size[1], -0.4 * display_size[1]),
)
MouseSpot = visual.GratingStim(
    win,
    tex="none",
    mask="gauss",
    pos=(0.2 * display_size[1], 0.2 * display_size[1]),
    size=(0.7 * an2px, 0.7 * an2px),
    color=(1.0, 1.0, 0),
    autoLog=False,
)  # for mouse
# presenting Concentric circles and lines for control panel
ConC = np.array([-0.3, -0.1]) * display_size[1]
ConS = np.array([6, 5, 4, 3, 2, 1]) * 1.4 * an2px  # 8.4, 7,5.6,4.2,2.8,1.4 VA

stim = []
# Place dummy images
template = textwrap.dedent(
    """
    stim_{INDEX} = visual.ImageStim(
        win,
        image=Image.open("../data/dummy.png"),
        pos=({POS_RATE} * display_size[1], {POS_RATE} * display_size[1]),
        size=(0.5 * an2px, 0.5 * an2px),
    )
    stim_{INDEX}.draw()
    """
)
for i in range(9):
    if i == 0:
        items = template.format(INDEX=i + 1, POS_RATE=0)
    if 0 < i <= 4:
        items = template.format(INDEX=i + 1, POS_RATE=0.2)
    if 4 < i < 9:
        items = template.format(INDEX=i + 1, POS_RATE=0.5)
    exec(items)

globalClock = core.Clock()

# display instructions and wait
# message1.draw()
# message2.draw()
# message3.draw()
# fixation.draw()
win.flip()  # to show our newly drawn 'stimuli'
# pause until there's a keypress
event.waitKeys()


count = 0
for thisTrial in trials:  # handler can act like a for loop
    # define motion direction ans speed
    trialClock = core.Clock()

    _non_target_classes = random.sample(non_target_classes, len(non_target_classes))
    """
    stim_
    """

    # for i in range(len(_non_target_classes)):

    count += 1

# give some on-screen feedback
endthank = visual.TextStim(win, pos=[0, +3], color=(1, 1, 1), text="Thank you!")
endthank.draw()
fixation.draw()
win.flip()
event.waitKeys()  # wait for participant to respond


# Write summary data to a text file ...
trials.saveAsText(
    fileName="fileName",
    stimOut=["ori", "sp"],
    dataOut=["Angle_mean", "Angle_std", "velocity_raw"],
)

# Write summary data to a text file ...
trials.saveAsText(
    fileName="fileName",
    stimOut=["ori", "sp"],
    dataOut=["Angle_mean", "Angle_std", "velocity_raw"],
)

# trials.saveAsPickle(fileName='testData')

# Wide format is useful for analysis with R or SPSS.
df = trials.saveAsWideText("testDataWide.txt")

win.close()
core.quit()
