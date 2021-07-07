from __future__ import absolute_import, division, print_function
import random, glob, math, os, argparse
import numpy as np
import pandas as pd
from collections import defaultdict
from psychopy import core, visual, gui, data, event
from psychopy.tools.filetools import fromFile, toFile
from PIL import Image
from screeninfo import get_monitors


def calc_VA(distance, size):
    return round(360 / math.pi * math.atan2(size, 2 * distance), 1)


def place_image(win, image_path, an2px, eccentricity, ori, size):
    stim = visual.ImageStim(
        win,
        image=Image.open(image_path),
        pos=(
            an2px * eccentricity * math.cos(math.radians(ori)),
            an2px * eccentricity * math.sin(math.radians(ori)),
        ),
        size=size,
    )
    return stim


class PeripheralSearchTask:
    # 13 Classes
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
        "fox",
        "pig",
        "otter",
    ]

    keys = [["b", "a", "c", "d"], ["f", "e", "g", "h"], ["j", "i", "k", "l"]]
    key_to_pos = defaultdict(list)
    for i, k_list in enumerate(keys):
        for j, k in enumerate(k_list):
            key_to_pos[k] = [i, j]
    print(key_to_pos)

    def __init__(
        self,
        win,
        an2px,
        default_size,
        eccentricities,
        condition_list,
        stim_list,
        n_reps,
        fixation,
        question,
        feedbacks,
        rest,
    ):
        self.win = win
        self.an2px = an2px
        self.default_size = default_size
        self.eccentricities = eccentricities
        self.condition_list = condition_list
        self.stim_list = stim_list
        self.n_reps = n_reps
        self.fixation = fixation
        self.question = question
        self.feedbacks = feedbacks
        self.rest = rest

        # Store images path in dictionary
        self.image_path_dict = defaultdict(list)
        self.image_path_dict[PeripheralSearchTask.target_class] = glob.glob(
            "../data/{}/*".format(PeripheralSearchTask.target_class)
        )
        for c in PeripheralSearchTask.non_target_classes:
            self.image_path_dict[c] = glob.glob("../data/{}/*".format(c))

    def ask_question(self):
        visual.ImageStim(
            self.win,
            image="../data/stimuli_arrangement.png",
            pos=(0, 0),
            size=(
                (2 * self.eccentricities[2] / math.sqrt(2) + 8) * self.an2px,
                (2 * self.eccentricities[2] / math.sqrt(2) + 8) * self.an2px,
            ),
        ).draw()
        for i, k_list in enumerate(PeripheralSearchTask.keys):
            for j, k in enumerate(k_list):
                visual.TextStim(
                    self.win,
                    text=k,
                    pos=(
                        self.an2px
                        * self.eccentricities[i]
                        * math.cos(math.radians(j % 4 * 90 + ((i + 1) % 2) * 45)),
                        self.an2px
                        * self.eccentricities[i]
                        * math.sin(math.radians(j % 4 * 90 + ((i + 1) % 2) * 45)),
                    ),
                    height=self.an2px * 1.5,
                    color=(0, 0, 0),
                ).draw()
        self.question.draw()

    def change_stim(self, cur_trial):
        # Change non-target stimuli
        _non_target_classes = random.sample(
            PeripheralSearchTask.non_target_classes,
            len(PeripheralSearchTask.non_target_classes),
        )
        for i, stim in enumerate(self.stim_list):
            image_path = random.choice(self.image_path_dict[_non_target_classes[i]])
            stim.image = Image.open(image_path)
            cur_trial[_non_target_classes[i]] = image_path

        # Change stimuli size
        for i, stim in enumerate(self.stim_list):
            stim.size = list(map(lambda x: cur_trial["size"] * x, self.default_size))
            if 4 <= i < 8:
                stim.size = list(map(lambda x: cur_trial["rate"] * x, stim.size))
            elif i >= 8:
                stim.size = list(
                    map(
                        lambda x: cur_trial["rate"] * cur_trial["rate"] * x,
                        stim.size,
                    )
                )

        # Change target stimulus
        image_path = random.choice(
            self.image_path_dict[PeripheralSearchTask.target_class]
        )
        self.stim_list[4 * cur_trial["pos"] + cur_trial["ori"]].image = Image.open(
            image_path
        )
        cur_trial[PeripheralSearchTask.target_class] = image_path

        # Draw stimuli
        for stim in self.stim_list:
            stim.draw()

        # Show fixation point
        self.fixation.fillColor = (192, 192, 192)
        self.fixation.draw()
        return cur_trial

    def create_trial(self):
        trials = data.TrialHandler(
            self.condition_list,
            self.n_reps,
            method="random",
            extraInfo={
                "participant": exp_info["Observer"],
                "session": exp_info["Session"],
                "MotionType": exp_info["Type[1: RDK; 2: Grating]"],
            },
        )
        return trials

    def excute_trial(self, trials):
        count = 0

        # Create data store
        result = pd.DataFrame(
            index=[],
            columns=list(self.condition_list[0].keys())
            + [PeripheralSearchTask.target_class]
            + PeripheralSearchTask.non_target_classes,
        )

        # Start trials
        for cur_trial in trials:
            trial_clock = core.Clock()

            # Show fixation point
            self.fixation.fillColor = (64, 64, 64)
            self.fixation.draw()
            self.win.flip()
            event.waitKeys()

            # Change fixation point's color
            self.fixation.fillColor = (192, 192, 192)
            self.fixation.draw()
            self.win.flip()
            # Gitter
            core.wait(0.5)

            # Change stimuli
            self.change_stim(cur_trial)
            self.win.flip()
            trial_onset = trial_clock.getTime()
            event.waitKeys()

            # When the subject find the target
            trial_offset = trial_clock.getTime()
            cur_trial["durationTime"] = trial_offset - trial_onset

            # Show the question
            self.ask_question()
            win.flip()

            # Answer the question or Exit
            flag = True
            while flag == 1:
                allKeys = event.waitKeys()
                for key in allKeys:
                    if key in sum(PeripheralSearchTask.keys, []):
                        cur_trial["ans"] = PeripheralSearchTask.key_to_pos[key]
                        flag = False
                    elif key in ["q", "escape"]:
                        print(result)
                        result.to_csv("../results/eye_movement/tmp_result.csv")
                        core.quit()

            print(cur_trial["ans"], cur_trial["pos"], cur_trial["ori"])

            # Show feedback
            if (
                cur_trial["ans"][0] == cur_trial["pos"]
                and cur_trial["ans"][1] == cur_trial["ori"]
            ):
                self.feedbacks[0].draw()
                cur_trial["correct"] = 1
            else:
                self.feedbacks[1].draw()
                cur_trial["correct"] = 0
            self.win.flip()
            event.waitKeys(maxWait=1, keyList=["space", "enter"])

            # Store current trial data in df
            result = result.append(cur_trial, ignore_index=True)

            count += 1
            if (
                count % (len(self.condition_list)) == 0
                and count != len(self.condition_list) * self.n_reps
            ):
                # Take a short break
                self.rest.draw()
                self.win.flip()
                core.wait(60)
        return result


# Set arguments
parser = argparse.ArgumentParser(description="Peripheral Search Tasks")
parser.add_argument("device", help="'iMac' or 'Macbook' (Air 2017)")
args = parser.parse_args()
device = args.device

# Check arguments
if device in ["iMac", "imac"]:
    print("This device is iMac")
    va_arg = (57.0, 33.5)
elif device in ["Macbook", "macbook"]:
    va_arg = (57.0, 17.9)
    print("This device is Macbook")
else:
    print("Device is not found.")
    core.quit()


"""
From Yung-Hao San
notes: we used "hight" as units, my macbookpro is 18cm(900pixel), assume 57cm distance,
so 1 degree =50 pixel, 1/18 (.055) in ratio
below all use visual angle to calculate size, so always multiple an2ra

In My iMac,
Display Height: 33.5 cm (1890 pix)
Distance: 57.0 cm
i.e.
VA: 32.8 degree
1 degree: 1890 / 32.8 = 57.6 pix

In My Macbook Air 2017,
Display Height: 17.9 cm (900 pix)
Distance: 30.0 cm
i.e.
VA: 33.2 degree
1 degree: 900 / 33.2 = 27.1 pix
"""
# Calculate the visual angle and the pixel per angle
VA = calc_VA(va_arg[0], va_arg[1])
display_size = [get_monitors()[0].width, get_monitors()[0].height]
an2ra = 1 / VA  # Doesn't use in this experiment
an2px = round(display_size[1] / VA, 1)
print("Visual Angle: {}, degree: {} pix, ".format(VA, an2px))


# Change working directory
if not os.path.isfile(os.path.basename(__file__)):
    os.chdir("./experiments")


# Try to get a previous parameters file
try:
    exp_info = fromFile("lastParams.pickle")
# If not there then use a default set
except:
    exp_info = {"Observer": "unknown", "Session": "1", "Type[1: RDK; 2: Grating]": "1"}
# Add the current time
exp_info["dateStr"] = data.getDateStr()

# Present a dialogue to change params
dlg = gui.DlgFromDict(
    exp_info, title="Peripheral Vision Search Experiment", fixed=["dateStr"]
)
# Save params to file for next time
if dlg.OK:
    toFile("lastParams.pickle", exp_info)
# The user hit cancel so exit
else:
    core.quit()


# Make a text file to save data
file_name = exp_info["Observer"] + "_" + exp_info["Session"] + "_" + exp_info["dateStr"]
# data_file = open(file_name+'.csv', 'w') # a simple text file with 'comma-separated- values'
# data_file.write('ori,sp,correct\n')


# Calculate eccentricities of stimuli
eccentricity_level_1 = round(np.sqrt(2), 1)
eccentricity_level_2 = round(np.roots([1, -2, -7]).max(), 1)
eccentricity_level_3 = round(
    np.roots([1, -np.sqrt(2) - 4, 4 * np.sqrt(2) - 27]).max(), 1
)

# This is the example to explain the experiment
example_list = [{"size": 1, "rate": 2, "pos": 1, "ori": 2}]
# Practice list: 2 * 2 * 2 = 8 conditions
# Condition list: 2 * 2 * 2 * 3 * 4 = 96 conditions
practice_list = []
experiment_list = []
for size in [1, 2]:  # 2 stimuli size
    for rate in [1, 2]:  # 2 magnification rates to periphery
        practice_list.append(
            {
                "size": size,
                "rate": rate,
                "pos": random.randrange(3),
                "ori": random.randrange(4),
            }
        )
        for pos in [0, 1, 2]:  # 3 positions (0: center)
            for ori in [0, 1, 2, 3]:  # 4 directions
                experiment_list.append(
                    {
                        "size": size,
                        "rate": rate,
                        "pos": pos,
                        "ori": ori,
                    }
                )

# Create window
win = visual.Window(
    display_size,
    allowGUI=True,
    color=(0, 0, 0),
    monitor="testMonitor",
    winType="pyglet",
    units="pix",
)

# Dummy images
stim_list = []
dummy_path = "../data/dummy.png"
default_size = [an2px, an2px]
for i in range(12):
    if i < 4:
        stim_list.append(
            place_image(
                win,
                dummy_path,
                an2px,
                eccentricity_level_1,
                i % 4 * 90 + 45,
                default_size,
            )
        )
    elif 4 <= i < 8:
        stim_list.append(
            place_image(
                win,
                dummy_path,
                an2px,
                eccentricity_level_2,
                i % 4 * 90,
                default_size,
            )
        )
    else:
        stim_list.append(
            place_image(
                win,
                dummy_path,
                an2px,
                eccentricity_level_3,
                i % 4 * 90 + 45,
                default_size,
            )
        )
# for stim in stim_list:
#     stim.draw()

# Introduction messages
introduction_1 = visual.TextStim(
    win,
    pos=(0, 0),
    text="Thank you for participating in the experiment. \n\n"
    + "First, look at the example. \n\n"
    + "Hit a Key when ready.",
)
introduction_2 = visual.TextStim(
    win,
    pos=(0.30 * display_size[0], 0),
    text="This is the example of the stimuli. \n\n"
    + "Before the stimuli presented, \n the fixation point is shown. \n\n"
    + "When you hit 'space' Key, \n stimuli are presented. \n\n"
    + "After that, you can move your eye. \n\n"
    + "When you find the 'cat', \n hit a Key and answer the question, \n 'Where was the cat?' \n\n"
    + "You answer with the keyboard. \n\n"
    + "Notice: When the stimuli are presented, \n please focus on the center of the display.",
)
introduction_3 = visual.TextStim(
    win,
    pos=(0, 0),
    text="Let's practice with some stimuli. \n\n" + "Hit a Key when ready.",
)
introduction_4 = visual.TextStim(
    win,
    pos=(0, 0.05 * display_size[1]),
    text="Practice part has finished. \n\n"
    + "Next part is the experiment. \n\n"
    + "Hit 's' Key when ready.",
)
# Fixation point
fixation = visual.Circle(
    win,
    pos=(0, 0),
    size=an2px // 5,
    fillColor=(64, 64, 64),
    colorSpace="rgb255",
)
# Question
question = visual.TextStim(
    win,
    pos=(0.30 * display_size[0], 0),
    text="Where Was the cat? \n Please press the Key \n corresponding to the position",
)
# Feedback
feedback_1 = visual.TextStim(
    win,
    pos=(0, 0),
    text="Your answer is correct!",
)
feedback_2 = visual.TextStim(
    win,
    pos=(0, 0),
    text="Your answer is incorrect.",
)
# Break
rest = visual.TextStim(
    win,
    pos=(0, 0),
    text="Please take a short break. \n\n"
    + "If the experiment is ready, \n the window will change to the fixation point.",
)


# Show introduction messages and the example
introduction_1.draw()
win.flip()
event.waitKeys()
print("Start Example")
Example = PeripheralSearchTask(
    win,
    an2px,
    default_size,
    [eccentricity_level_1, eccentricity_level_2, eccentricity_level_3],
    example_list,
    stim_list,
    1,
    fixation,
    question,
    [feedback_1, feedback_2],
    rest,
)
example_trials = Example.create_trial()
for trial in example_trials:
    Example.change_stim(trial)
    introduction_2.draw()
    win.flip()
    event.waitKeys()


# Start the practice part
introduction_3.draw()
win.flip()
event.waitKeys()

print("Start Practice")
Practice = PeripheralSearchTask(
    win,
    an2px,
    default_size,
    [eccentricity_level_1, eccentricity_level_2, eccentricity_level_3],
    practice_list,
    stim_list,
    1,
    fixation,
    question,
    [feedback_1, feedback_2],
    rest,
)
practice_trials = Practice.create_trial()
result = Practice.excute_trial(practice_trials)
print(result)

introduction_4.draw()
win.flip()
event.waitKeys(keyList=["s"])

globalClock = core.Clock()

# Start the experiment part
print("Start Experiment")
Experiment = PeripheralSearchTask(
    win,
    an2px,
    default_size,
    [eccentricity_level_1, eccentricity_level_2, eccentricity_level_3],
    experiment_list,
    stim_list,
    4,
    fixation,
    question,
    [feedback_1, feedback_2],
    rest,
)
experiment_trials = Experiment.create_trial()
result = Experiment.excute_trial(experiment_trials)
print(result)
result.to_csv("../results/eye_movement/{}.csv".format(file_name))

# trials.saveAsPickle(file_name='testData')

# Wide format is useful for analysis with R or SPSS.
# df = trials.saveAsWideText("testDataWide.txt")

# give some on-screen feedback
endthank = visual.TextStim(win, pos=[0, 0.15], color=(1, 1, 1), text="Thank you!")
endthank.draw()
win.flip()
core.wait(1.0)

win.close()
core.quit()
