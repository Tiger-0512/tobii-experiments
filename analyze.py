import pandas as pd
import numpy as np
from matplotlib import pyplot as plt


def str_to_float(array):
    array = array[1:-1]
    array = list(map(float, array.split(',')))
    return array[0], array[1]

def divide_to_axis(df):
    # initialization
    left_x = np.empty(0)
    left_y = np.empty(0)
    right_x = np.empty(0)
    right_y = np.empty(0)

    left = df_csv['0'].to_numpy()
    right = df_csv['1'].to_numpy()

    for i in range(len(left)):
        # left eye
        x, y = str_to_float(left[i])
        left_x = np.append(left_x, x)
        left_y = np.append(left_y, y)

        # right eye
        x, y = str_to_float(right[i])
        right_x = np.append(right_x, x)
        right_y = np.append(right_y, y)

    return left_x, left_y, right_x, right_y


df_csv = pd.read_csv('out.csv')
l_x, l_y, r_x, r_y = divide_to_axis(df_csv)


fig, ax1 = plt.subplots()
ax1.plot(l_x, l_y)
ax1.plot(r_x, r_y)

ax1.set_ylim([1, 0])
ax1.set_xlim([0, 1])

plt.show()
