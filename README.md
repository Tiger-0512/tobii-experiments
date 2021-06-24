# Eye Tracking experiments with Tobii Pro Spectrum

## Environments
- Python 3.6
- Psychopy 3.0

## Features of the Experiments
- Switch the image whether you gaze left side or right side of the screen - [eyes_move_with_you.py](https://github.com/Tiger-0512/tobii-experiments/blob/main/experiments/eyes_move_with_you.py)
- Trace your eyes - [trace_eyes.py](https://github.com/Tiger-0512/tobii-experiments/blob/main/experiments/trace_eyes.py)
- Indicate where you are looking on the backgroud image - [show_where_you_look.py](https://github.com/Tiger-0512/tobii-experiments/blob/main/experiments/show_where_you_look.py)
- Turn to the gray scale from RGB where you are looking on the background image - [gaze_to_gray.py](https://github.com/Tiger-0512/tobii-experiments/blob/main/experiments/gaze_to_gray.py)
- Create Gaze-Contingent-Display(GCD) with synthesizing high/low resolution images - [gcd_for_image_blur.py](https://github.com/Tiger-0512/tobii-experiments/blob/main/experiments/gcd_for_image_blur.py)
- Create GCD for text stimilus - [gcd_for_text.py](https://github.com/Tiger-0512/tobii-experiments/blob/main/experiments/gcd_for_text.py)
- Create GCD for tree structure of text - [gcd_for_tree.py](https://github.com/Tiger-0512/tobii-experiments/blob/main/experiments/gcd_for_tree.py)
- Create GCD for ImageNet datasets to search one class from several classes in the display - [gcd_for_inet_ciecle.py](https://github.com/Tiger-0512/tobii-experiments/blob/main/experiments/gcd_for_inet_circle.py), [gcd_for_inet_square.py](https://github.com/Tiger-0512/tobii-experiments/blob/main/experiments/gcd_for_inet_square.py)

## Usage
### 1. Clone this reopsitory
```
$ git clone https://github.com/Tiger-0512/tobii-experiments.git
```

### 2. Create conda environment
```
$ cd tobii-experiments
$ curl https://raw.githubusercontent.com/psychopy/psychopy/master/conda/psychopy-env.yml > psychopy-env.yml
$ conda env create -n psychopy -f psychopy-env.yml
```
Check [this page](https://www.psychopy.org/download.html) for more information.

### 3. Run Psychopy
```
$ conda activate psychopy
$ psychopy
```

### 4. Save Eye Tracker Calibration Data
Use [Tobii Pro Eye Tracker Manager](https://www.tobiipro.com/product-listing/eye-tracker-manager/) to calibrate.<br>
Once you calibrate your eye, the parameter is saved in the eye tracker internally.<br>

### 5. Execute the experiments
In PsychoPy editor, select the experiment in this repo and the run it.

### 6. Analyze the eyes' movements(optional)
Run `analyze.py` to draw eyes' tracing


## Notice
Any sampling rate is OK when you calibrate your eye.
