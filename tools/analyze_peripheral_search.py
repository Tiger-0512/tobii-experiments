import os
import pandas as pd


def calculate_acc(df):
    df_ok = df.query("state == ans")
    return len(df_ok) / len(df)


# Change working directory
if not os.path.isfile(os.path.basename(__file__)):
    os.chdir("./tools")

# Import csv file
df = pd.read_csv("../data/sn_2_2021_Jul_05_1759.csv", index_col=0)
print(calculate_acc(df))

# size = 1, rate = 1
df_11 = df.query("size == 1 and rate == 1")
print(calculate_acc(df_11))

# size = 1, rate = 2
df_12 = df.query("size == 1 and rate == 2")
print(calculate_acc(df_12))

# size = 2, rate = 1
df_21 = df.query("size == 2 and rate == 1")
print(calculate_acc(df_21))

# size = 2, rate = 2
df_22 = df.query("size == 2 and rate == 2")
print(calculate_acc(df_22))
