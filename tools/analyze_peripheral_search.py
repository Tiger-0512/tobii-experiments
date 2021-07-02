import pandas as pd


def calculate_acc(df):
    return len(df[df["ans"] == 1]) / len(df)


# Import csv file
df = pd.read_csv("../data/yh_1_2021_Jul_02_1736.csv", index_col=0)
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
