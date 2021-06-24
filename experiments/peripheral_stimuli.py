"""Measure coherence threshold of motion direction
using Staircase procedure, dot direction: 0 (LTR)"""

from __future__ import absolute_import, division, print_function
from psychopy import core, visual, gui, data, event
from psychopy.tools.filetools import fromFile, toFile
import numpy as np
from numpy import matlib, inf
from builtins import range
from random import random
from PIL import Image
import math, os, textwrap

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

stim_classs = [
    "cat",
    "dog",
    "cow",
    "tiger",
    "rabbit",
    "horse",
    "sheep",
    "monkey",
    "lion",
    "bear",
    "fox",
    "raccoon",
    "squirrel",
    "elephant",
    "dear",
    "boar",
    "kangaroo",
    "koala",
    "rhino",
    "pig",
]
# making Stimlist
stim_list = []
for ori in range(0, 360, 90):  # 4 directions
    for pos in [1, 2]:  # 2 positions
        for size in [1, 2, 3]:  # 3 stimuli size
            for state in [1, 2]:
                # append a python 'dictionary' to the list
                stim_list.append({"ori": ori, "pos": pos, "size": size, "state": state})


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
display_size = [3360, 1890]
VA = features.calc_VA(57.0, 33.5)
an2ra = 1 / VA
an2px = round(display_size[1] / VA, 1)
win = visual.Window(
    [1920, 1080],
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

# Place dummy images
img_name = [
    "removed_n02107908_9.png",
    "removed_n02107908_24.png",
    "removed_n02107908_47.png",
    "removed_n02107908_80.png",
    "removed_n02107908_91.png",
    "removed_n02107908_94.png",
    "removed_n02107908_180.png",
    "removed_n02107908_298.png",
]
template = textwrap.dedent(
    """
    img_{INDEX} = visual.ImageStim(
        win,
        image=Image.open("{CWD}/data/removed/{NAME}"),
    )
    """
)
for i in range(9):
    items = template.format(INDEX=i + 1, CWD=os.getcwd(), NAME=img_name[i])


""" Initialize dot stimuli  %we used visual angel as units and assume looking from 57cm, so 1cm =1 visual angle
the paramerter is followed Scase, etal (1996)"""
dotPatch = visual.DotStim(
    win,
    color=(1.0, 1.0, 1.0),
    dir=0,
    nDots=330,
    fieldShape="circle",
    fieldPos=(0.0 * display_size[1], 0.2 * display_size[1]),
    fieldSize=10 * an2px,
    dotSize=3 / 60 * an2px,  # dotsize(pixels), 3 arc min.
    dotLife=30,  # number of frames for each dot to be drawn [-1 is infi]
    signalDots="same",  # are signal dots 'same' on each frame? (see Scase et al)
    noiseDots="direction",  # do the noise dots follow random- 'walk', 'direction', or 'position'
    speed=(3 * an2px) / 60,
    coherence=0.7,
)  # speed: units per frame, 60 hz

# This is for the feedback white noise
noiseangle = 7  # degree
noisesize = noiseangle * an2px  # pixels
# Setting for pink noise
noisesize = [350, 350]  # pixels ~=3VA
# this is from spatialPattern.m by Jon Yearsley to generate pink noise
Beta = -2
x = np.arange(0, int(math.floor(noisesize[0]) / 2 + 1))
y = -(np.arange(int(math.ceil(noisesize[0] / 2) - 1), 0, -1))
u = np.concatenate((x, y)) / noisesize[0]
u = np.matlib.repmat(u, noisesize[1], 1)
u = u.T
x = np.arange(0, int(math.floor(noisesize[1]) / 2 + 1))
y = -(np.arange(int(math.ceil(noisesize[1] / 2) - 1), 0, -1))
v = np.concatenate((x, y)) / noisesize[1]
v = np.matlib.repmat(v, noisesize[0], 1)
S_f = (u ** 2 + v ** 2) ** (Beta / 2)
S_f[S_f == inf] = 0
phi = np.random.rand(noisesize[0], noisesize[1])
x = np.fft.ifft2(
    S_f ** 0.5 * (np.cos(2 * math.pi * phi) + ((np.sin(2 * math.pi * phi)) * 1j))
)
x = x.real
ranx = np.max(x) - np.min(x)
x = (((x - np.min(x)) / ranx) * 2) - 1
noiseTexture = x
# noiseTexture = np.random.rand(noisesize, noisesize) * 2.0 - 1
noise = visual.GratingStim(
    win,
    tex=noiseTexture,
    mask="circle",
    size=(noiseangle * an2px, noiseangle * an2px),
    pos=(0.3 * display_size[1], -0.1 * display_size[1]),  # 360,225 pixel
    interpolate=False,
    autoLog=False,
)

myMouse = event.Mouse()  #  will use win by default
# and some handy clocks to keep track of time
globalClock = core.Clock()


# display instructions and wait
message1.draw()
message2.draw()
message3.draw()
fixation.draw()
win.flip()  # to show our newly drawn 'stimuli'
# pause until there's a keypress
event.waitKeys()

count = 0
for thisTrial in trials:  # handler can act like a for loop
    # define motion direction ans speed
    trialClock = core.Clock()
    dotPatch.dir = thisTrial["ori"]
    dotPatch.dir += np.random.uniform(-1, 1) * 45
    dotPatch.speed = (
        (thisTrial["sp"] + np.random.uniform(-1, 1)) * an2px
    ) / 60  # should be VA/sec, but speed is defined by units/frame so /60Hz
    MouseSpot.mask = "gauss"
    MouseSpot.size = 35
    MouseSpot.color = (1, 1, 0)
    # mouse calibration
    mousehit = 0
    MouseSpot.color = (1, 0, 0)
    while mousehit == 0:
        message1.draw()
        fixation.draw()
        MouseSpot.draw()
        output.draw()
        win.flip()  # to show our newly drawn 'stimuli'
        mouse_dX, mouse_dY = myMouse.getPos()
        MouseSpot.setPos([mouse_dX, mouse_dY])
        output.text = f"mouse@ [%.3f, %.3f]" % (mouse_dX, mouse_dY)

        if (
            abs(mouse_dX) < 0.005 * display_size[1]
            and abs(mouse_dY - 0.2 * display_size[1]) < 0.005 * display_size[1]
        ):  # less than 5 pixels
            MouseSpot.color = (1, 1, 0)
            mousehit = 1

    core.wait(0.2)
    # motion start
    Trialonset = trialClock.getTime()
    for frameN in range(60):
        dotPatch.draw()
        fixation.draw()
        MouseSpot.draw()
        output.draw()
        win.flip()
        mouse_dX, mouse_dY = myMouse.getPos()
        MouseSpot.setPos([mouse_dX, mouse_dY])
        output.text = f"mouse@ [%.3f, %.3f]" % (mouse_dX, mouse_dY)
    Trialoffset = trialClock.getTime()

    ## move the mouse to the center of bottom [ 0, 0.25]
    mouseclick = 0
    mouse_dX, mouse_dY = 0, ConC[1]
    myMouse.setPos(newPos=(0, ConC[1]))

    MouseSpot.mask = "circle"
    MouseSpot.size = 5
    MouseSpot.color = (0, -1, 0)
    while not mouseclick:
        while myMouse.mouseMoved():
            mouse_dX, mouse_dY = myMouse.getPos()
            while (
                np.sqrt((mouse_dX - ConC[0]) ** 2 + (mouse_dY - ConC[1]) ** 2)
                < 4.2 * an2px
            ):  # control panel is 8.4VA if hit then change noise
                mouse_dX, mouse_dY = myMouse.getPos()
                MouseSpot.setPos([mouse_dX, mouse_dY])
                delta = (mouse_dX - ConC[0]), (mouse_dY - ConC[1])
                ang = np.arctan2(delta[1], delta[0]) * 180 / math.pi
                if (
                    delta[1] < 0
                ):  # if y is negative, then polar will become negative so +360
                    ang = ang + 360
                vel = (
                    np.sqrt(delta[0] ** 2 + delta[1] ** 2) / 17.5
                )  # 175pixel is 10VA/Sec
                output.text = f"mouse@ [%.3f, %.3f]" % (mouse_dX, mouse_dY)
                output2.text = "Noise had direction %.3f with speed %.3f VA/Sec" % (
                    ang,
                    vel,
                )
                response_dX = (
                    (mouse_dX - ConC[0]) / 0.35 / 60
                )  # control panel use radius 210pixels to refer 12VA/sec, since 12VA=600pixels, so 1 pixels in panel = 1/0.35 in speed
                response_dY = (
                    (mouse_dY - ConC[1]) / 0.35 / 60
                )  # should be VA/sec, but speed is defined by units/frame so /60Hz
                noise.phase += (
                    response_dX / noisesize[0],
                    response_dY / noisesize[1],
                )  # should control the speed and direction, need to caculate
                mouse1, mouse2, mouse3 = myMouse.getPressed()
                for poly in polyrange:  # this two draw control panel
                    poly.draw()
                for line in linerange:
                    line.draw()
                noise.draw()
                MouseSpot.draw()
                output.draw()
                output2.draw()
                win.flip()
                if mouse1:
                    mouseclick = 1
                    mouse_dX, mouse_dY = 0, ConC[1]
            if (
                abs(mouse_dX) < 0.005 * display_size[1]
                and abs(mouse_dY - 0.2 * display_size[1]) < 0.005 * display_size[1]
            ):
                # mouse_dX, mouse_dY=ConC[0],ConC[1]
                myMouse.setPos(newPos=(0, ConC[1]))
                for frameN in range(60):
                    dotPatch.draw()
                    win.flip()

        MouseSpot.setPos([mouse_dX, mouse_dY])
        output.text = f"mouse@ [%.3f, %.3f]" % (mouse_dX, mouse_dY)
        for poly in polyrange:  # this two draw control panel
            poly.draw()
        for line in linerange:
            line.draw()
        fixation.draw()
        noise.draw()
        MouseSpot.draw()
        output.draw()
        win.flip()
    # presenting feedback frame
    if thisTrial["ori"] == 0:
        if 0 <= ang <= 22.5 or 337.5 <= ang <= 360:
            res = "Correct"
            col = (0, 1, 0)
        else:
            res = "wrong"
            col = (1, 0, 0)
    else:
        if abs(ang - thisTrial["ori"]) <= 22.5:
            res = "Correct"
            col = (0, 1, 0)
        else:
            res = "Wrong"
            col = (1, 0, 0)
    count += 1
    Feedback1.text = "Trial%i had direction %.3f with speed %.3f deg/sec" % (
        count,
        dotPatch.dir,
        dotPatch.speed,
    )
    Feedback2.text = "Mouse response had direction %.3f with speed %.3f VA/Sec" % (
        ang,
        vel,
    )
    Feedback3.text = res
    Feedback3.color = col
    Feedback1.draw()
    Feedback2.draw()
    # Feedback3.draw()
    fixation.draw()
    win.flip()
    trials.data.add("Angle", ang)
    trials.data.add("velocity", vel)
    trials.data.add("CorrResponse", res)
    trials.data.add("OriJi", dotPatch.dir)
    trials.data.add("SpeJi", dotPatch.speed)
    feedbackend = None
    while feedbackend is None:
        allKeys = event.waitKeys()
        for thisKey in allKeys:
            if thisKey == "space":
                feedbackend = 1
            elif thisKey in ["q", "escape"]:
                # win.close()
                core.quit()
    # event.clearEvents()

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
