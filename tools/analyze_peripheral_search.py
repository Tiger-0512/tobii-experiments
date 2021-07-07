import os, argparse
import pandas as pd


def calc_acc(df):
    df_ok = df.query("state == ans")
    return len(df_ok) / len(df)


def calc_dt(df):
    return df["durationTime"].sum() / len(df)


# Set arguments
parser = argparse.ArgumentParser(description="Analyze the peripheral search experiment")
parser.add_argument("result_path")
args = parser.parse_args()
result_path = args.result_path

# Change working directory
if not os.path.isfile(os.path.basename(__file__)):
    os.chdir("./tools")

# Import csv file
df = pd.read_csv(result_path, index_col=0)

if "eye_fixed" in result_path:
    print(calc_acc(df))
    df_c = df.query("pos == 0 and state == 1")
    print(calc_acc(df_c))
    df_1 = df.query("pos == 1 and state == 1")
    print(calc_acc(df_1))
    df_2 = df.query("pos == 2 and state == 1")
    print(calc_acc(df_2))
    print("\n")

    # size = 1, rate = 1
    df_11 = df.query("size == 1 and rate == 1")
    print(calc_acc(df_11))
    df_11_c = df_11.query("pos == 0 and state == 1")
    print(calc_acc(df_11_c))
    df_11_1 = df_11.query("pos == 1 and state == 1")
    print(calc_acc(df_11_1))
    df_11_2 = df_11.query("pos == 2 and state == 1")
    print(calc_acc(df_11_2))
    print("\n")

    # size = 1, rate = 2
    df_12 = df.query("size == 1 and rate == 2")
    print(calc_acc(df_12))
    df_12_c = df_12.query("pos == 0 and state == 1")
    print(calc_acc(df_12_c))
    df_12_1 = df_12.query("pos == 1 and state == 1")
    print(calc_acc(df_12_1))
    df_12_2 = df_12.query("pos == 2 and state == 1")
    print(calc_acc(df_12_2))
    print("\n")

    # size = 2, rate = 1
    df_21 = df.query("size == 2 and rate == 1")
    print(calc_acc(df_21))
    df_21_c = df_21.query("pos == 0 and state == 1")
    print(calc_acc(df_21_c))
    df_21_1 = df_21.query("pos == 1 and state == 1")
    print(calc_acc(df_21_1))
    df_21_2 = df_21.query("pos == 2 and state == 1")
    print(calc_acc(df_21_2))
    print("\n")

    # size = 2, rate = 2
    df_22 = df.query("size == 2 and rate == 2")
    print(calc_acc(df_22))
    df_22_c = df_22.query("pos == 0 and state == 1")
    print(calc_acc(df_22_c))
    df_22_1 = df_22.query("pos == 1 and state == 1")
    print(calc_acc(df_22_1))
    df_22_2 = df_22.query("pos == 2 and state == 1")
    print(calc_acc(df_22_2))
    print("\n")


elif "eye_movement" in result_path:
    df_new = pd.DataFrame(df.iloc[0]).T
    for i, d in df.iterrows():
        if int(d["ans"][1]) == int(d["pos"]) and int(d["ans"][4]) == int(d["ori"]):
            df_new = df_new.append(d)
    print(calc_dt(df_new))
    print("\n")

    # size = 1, rate = 1
    df_11 = df_new.query("size == 1 and rate == 1")
    print(calc_dt(df_11))

    # size = 1, rate = 2
    df_12 = df_new.query("size == 1 and rate == 2")
    print(calc_dt(df_12))

    # size = 2, rate = 1
    df_21 = df_new.query("size == 2 and rate == 1")
    print(calc_dt(df_21))

    # size = 2, rate = 2
    df_22 = df_new.query("size == 2 and rate == 2")
    print(calc_dt(df_22))


else:
    print("'result_path' is not invalid")
