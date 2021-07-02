import cv2, math
from PIL import Image
from psychopy import visual, event


def calc_VA(distance, size):
    return round(360 / math.pi * math.atan2(size, 2 * distance), 1)


def show_eyetracker(eyetracker):
    print("Address: " + eyetracker.address)
    print("Model: " + eyetracker.model)
    print("Name(It's OK if this is empty): " + eyetracker.device_name)
    print("Serial number: " + eyetracker.serial_number)

    display_area = eyetracker.get_display_area()
    print(
        "Got display area from tracker with serial number {0}:".format(
            eyetracker.serial_number
        )
    )
    print("Bottom Left: {0}".format(display_area.bottom_left))
    print("Bottom Right: {0}".format(display_area.bottom_right))
    print("Height: {0}".format(display_area.height))
    print("Top Left: {0}".format(display_area.top_left))
    print("Top Right: {0}".format(display_area.top_right))
    print("Width: {0}".format(display_area.width))


def introduction(display_size, units="norm"):
    win = visual.Window(
        display_size, allowGUI=True, monitor="testMonitor", units="norm"
    )
    message = visual.TextStim(win, pos=[0, 0], text="Hit a Key when ready", height=0.05)
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


def change_message(pos_pix, msg, shown_msg):
    if (
        shown_msg.pos[0] - 100 < pos_pix[0] < shown_msg.pos[0] + 100
        and shown_msg.pos[1] - 100 < pos_pix[1] < shown_msg.pos[1] + 100
    ):
        shown_msg.text = msg
        shown_msg.height = 64
    else:
        shown_msg.text = msg[0]
        shown_msg.height = 192


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


def search_domain(x, y, threshold):
    for i in range(len(threshold[0]) - 1):
        for j in range(len(threshold[1]) - 1):
            if (
                threshold[0][i] <= x <= threshold[0][i + 1]
                and threshold[1][j] >= y >= threshold[1][j + 1]
            ):
                return (i, j)
    return (-1, -1)


def list_to_domain(x, y, X):
    for i in range(y):
        if x == i:
            return x + y * X


def domain_to_corner(domain, row, col, display_size):
    len_hor = int(display_size[0] / row)
    len_var = int(display_size[1] / col)
    tl = (len_hor * domain[0], len_var * domain[1])
    br = (len_hor * (domain[0] + 1), len_var * (domain[1] + 1))
    return tl, br


def place_dummy(win, image_path, an2px, eccentricity, ori, size):
    stim = visual.ImageStim(
        win,
        image=Image.open(image_path),
        pos=(
            an2px * eccentricity * math.sin(math.radians(ori)),
            an2px * eccentricity * math.cos(math.radians(ori)),
        ),
        size=size,
    )
    return stim


def save_csv(df, path):
    df.to_csv(path)
