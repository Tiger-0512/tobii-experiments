import cv2
from psychopy import visual, event


def show_eyetracker(eyetracker):
    print("Address: " + eyetracker.address)
    print("Model: " + eyetracker.model)
    print("Name(It's OK if this is empty): " + eyetracker.device_name)
    print("Serial number: " + eyetracker.serial_number)

    display_area = eyetracker.get_display_area()
    print("Got display area from tracker with serial number {0}:".format(eyetracker.serial_number))
    print("Bottom Left: {0}".format(display_area.bottom_left))
    print("Bottom Right: {0}".format(display_area.bottom_right))
    print("Height: {0}".format(display_area.height))
    print("Top Left: {0}".format(display_area.top_left))
    print("Top Right: {0}".format(display_area.top_right))
    print("Width: {0}".format(display_area.width))


def introduction():
    win = visual.Window([1920, 1080], allowGUI=True, monitor='testMonitor', units='deg')
    message = visual.TextStim(win, pos=[0, 1], text='Hit a Key when ready')
    message.draw()
    win.flip()

    event.waitKeys()
    return [win, message]


def synthesize_images_with_mask(background_img, objective_img, mask):
    # Make inverse mask
    mask_inv = cv2.bitwise_not(mask)

    # Synthesis
    masked_obj = cv2.bitwise_and(objective_img, objective_img, mask=mask)
    masked_bg = cv2.bitwise_and(background_img, background_img, mask=mask_inv)
    synthesized_img = cv2.bitwise_or(masked_obj, masked_bg)

    return synthesized_img


def save_csv(df, path):
    df.to_csv(path)