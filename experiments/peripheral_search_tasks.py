from __future__ import absolute_import, division, print_function
import sys, random, glob
import numpy as np
from collections import defaultdict
from psychopy import core, visual, gui, data, event
from psychopy.tools.filetools import fromFile, toFile
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

# making condition list
condition_list = []
for size in [1, 2, 3]:  # 3 stimuli size
    for rate in [1, 2, 3]:  # 3 magnification rates to periphery
        for state in [0, 1]:  # 2 state (whether the target exists or not)
            for pos in [0, 1, 2]:  # 3 positions (0: center)
                if pos == 0:
                    ori = 3
                    # append a python 'dictionary' to the list
                    condition_list.append(
                        {
                            "size": size,
                            "rate": rate,
                            "state": state,
                            "pos": pos,
                            "ori": ori,
                        }
                    )
                else:
                    for ori in [0, 1, 2, 3]:  # 4 directions
                        condition_list.append(
                            {
                                "size": size,
                                "rate": rate,
                                "state": state,
                                "pos": pos,
                                "ori": ori,
                            }
                        )

# organize them with the trial handler  repeated 10 times
trials = data.TrialHandler(
    condition_list,
    10,
    method="random",
    extraInfo={
        "participant": expInfo["Observer"],
        "session": expInfo["Session"],
        "MotionType": expInfo["Type[1: RDK; 2: Grating]"],
    },
)


# Store images path in dictionary
image_path_dict = defaultdict(list)
image_path_dict[target_class] = glob.glob("../data/{}/*".format(target_class))
for c in non_target_classes:
    image_path_dict[c] = glob.glob("../data/{}/*".format(c))


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
# print(display_size)
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
)

# presenting Concentric circles and lines for control panel
ConC = np.array([-0.3, -0.1]) * display_size[1]
ConS = np.array([6, 5, 4, 3, 2, 1]) * 1.4 * an2px  # 8.4, 7,5.6,4.2,2.8,1.4 VA

stim_list = []
default_size = [an2px, an2px]
# Place dummy images
for i in range(9):
    if i == 0:
        stim_list.append(
            features.place_dummy(
                win, "../data/dummy.png", 0, 0, default_size, display_size
            )
        )
    if 0 < i <= 4:
        stim_list.append(
            features.place_dummy(
                win, "../data/dummy.png", 0.2, i % 4 * 90, default_size, display_size
            )
        )
    if 4 < i < 9:
        stim_list.append(
            features.place_dummy(
                win, "../data/dummy.png", 0.4, i % 4 * 90, default_size, display_size
            )
        )
# for stim in stim_list:
#     stim.draw()


# Show introduction messages
message_1 = visual.TextStim(
    win,
    pos=[0, 0.15 * display_size[1]],
    text="Please answer the question whether cats exist in the stimuli.",
)
message_2 = visual.TextStim(
    win,
    pos=[0, 0.10 * display_size[1]],
    text="Hit a Key when ready.",
)
message_1.draw()
message_2.draw()
win.flip()
# pause until there's a keypress
event.waitKeys()

globalClock = core.Clock()

count = 0
results = []
for cur_trial in trials:  # handler can act like a for loop
    # define motion direction ans speed
    trialClock = core.Clock()

    # Change non-target stimuli
    _non_target_classes = random.sample(non_target_classes, len(non_target_classes))
    for i, stim in enumerate(stim_list):
        stim.image = Image.open(random.choice(image_path_dict[_non_target_classes[i]]))

    # Change target stimulus
    for i, stim in enumerate(stim_list):
        stim.size = list(map(lambda x: cur_trial["size"] * x, default_size))
        if 0 < i <= 4:
            stim.size = list(map(lambda x: cur_trial["rate"] * x, stim.size))
        if 4 < i < 9:
            stim.size = list(
                map(lambda x: cur_trial["rate"] * cur_trial["rate"] * x, stim.size)
            )
    if cur_trial["state"] == 1:
        stim_list[4 * cur_trial["pos"] + cur_trial["ori"] - 3].image = Image.open(
            random.choice(image_path_dict[target_class])
        )

    # Draw stimuli
    for stim in stim_list:
        stim.draw()
    win.flip()

    core.wait(1)
    features.ask_question(win, display_size)

    flag = True
    while flag == 1:
        allKeys = event.waitKeys()
        for key in allKeys:
            if key in ["0", "1"]:
                results.append(key)
                flag = False
            elif key in ["q", "escape"]:
                print(results)
                core.quit()

    count += 1

# give some on-screen feedback
endthank = visual.TextStim(win, pos=[0, 0.15], color=(1, 1, 1), text="Thank you!")
endthank.draw()
win.flip()
event.waitKeys()  # wait for participant to respond

print(results)

# trials.saveAsPickle(fileName='testData')

# Wide format is useful for analysis with R or SPSS.
# df = trials.saveAsWideText("testDataWide.txt")

win.close()
core.quit()
