import os, argparse
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict


def calc_acc(df):
    df_ok = df.query("state == ans")
    return len(df_ok) / len(df)


def calc_dt(df):
    return df["durationTime"].sum() / len(df)


# Set arguments
# parser = argparse.ArgumentParser(description="Analyze the peripheral search experiment")
# parser.add_argument("result_path")
# args = parser.parse_args()
# result_path = args.result_path

# Change working directory
if not os.path.isfile(os.path.basename(__file__)):
    os.chdir("./tools")

    # eyefixed
    # result_path_list = [
    #     "../results/eye_fixed/miyoshi_1_2021_Jul_06_1551.csv",
    #     "../results/eye_fixed/sn_2_2021_Jul_05_1759.csv",
    #     "../results/eye_fixed/sou_1_2021_Jul_06_1522.csv",
    #     "../results/eye_fixed/yh_2_2021_Jul_05_1714.csv",
    # ]

    # eye movement
    result_path_list = [
        "../results/eye_movement/miyoshi_1_2021_Jul_07_1840.csv",
        "../results/eye_movement/taiga_1_2021_Jul_07_1511.csv",
        "../results/eye_movement/yh_1_2021_Jul_07_1700.csv",
        "../results/eye_movement/jason_1_2021_Jul_08_1438.csv",
        "../results/eye_movement/sou_1_2021_Jul_08_1500.csv",
        "../results/eye_movement/taiga_2_2021_Jul_08_1539.csv",
        "../results/eye_movement/yh_2_2021_Jul_09_1326.csv",
        "../results/eye_movement/miyoshi_2_2021_Jul_12_1417.csv",
    ]

analyzed_data = defaultdict(list)
for i, result_path in enumerate(result_path_list):
    # Import csv file
    df = pd.read_csv(result_path, index_col=0)

    if "eye_fixed" in result_path:
        analyzed_data["total"].append(calc_acc(df))
        # df_c = df.query("pos == 0 and state == 1")
        # print(calc_acc(df_c))
        # df_1 = df.query("pos == 1 and state == 1")
        # print(calc_acc(df_1))
        # df_2 = df.query("pos == 2 and state == 1")
        # print(calc_acc(df_2))
        # print("\n")

        # size = 1, rate = 1
        df_11 = df.query("size == 1 and rate == 1")
        analyzed_data["11"].append(calc_acc(df_11))
        analyzed_data["11_0"].append(calc_acc(df_11[df_11["pos"] == 0]))
        analyzed_data["11_1"].append(calc_acc(df_11[df_11["pos"] == 1]))
        analyzed_data["11_2"].append(calc_acc(df_11[df_11["pos"] == 2]))

        # size = 1, rate = 2
        df_12 = df.query("size == 1 and rate == 2")
        analyzed_data["12"].append(calc_acc(df_12))
        analyzed_data["12_0"].append(calc_acc(df_12[df_12["pos"] == 0]))
        analyzed_data["12_1"].append(calc_acc(df_12[df_12["pos"] == 1]))
        analyzed_data["12_2"].append(calc_acc(df_12[df_12["pos"] == 2]))

        # size = 2, rate = 1
        df_21 = df.query("size == 2 and rate == 1")
        analyzed_data["21"].append(calc_acc(df_21))
        analyzed_data["21_0"].append(calc_acc(df_21[df_21["pos"] == 0]))
        analyzed_data["21_1"].append(calc_acc(df_21[df_21["pos"] == 1]))
        analyzed_data["21_2"].append(calc_acc(df_21[df_21["pos"] == 2]))

        # size = 2, rate = 2
        df_22 = df.query("size == 2 and rate == 2")
        analyzed_data["22"].append(calc_acc(df_22))
        analyzed_data["22_0"].append(calc_acc(df_22[df_22["pos"] == 0]))
        analyzed_data["22_1"].append(calc_acc(df_22[df_22["pos"] == 1]))
        analyzed_data["22_2"].append(calc_acc(df_22[df_22["pos"] == 2]))

    elif "eye_movement" in result_path:
        df_new = pd.DataFrame(df.iloc[0]).T
        for i, d in df.iterrows():
            if int(d["ans"][1]) == int(d["pos"]) and int(d["ans"][4]) == int(d["ori"]):
                df_new = df_new.append(d)
        print(calc_dt(df_new))
        analyzed_data["total"].append(calc_dt(df_new))

        # size = 1, rate = 1
        df_11 = df_new.query("size == 1 and rate == 1")
        analyzed_data["11"].append(calc_dt(df_11))
        analyzed_data["11_0"].append(calc_dt(df_11[df_11["pos"] == 0]))
        analyzed_data["11_1"].append(calc_dt(df_11[df_11["pos"] == 1]))
        analyzed_data["11_2"].append(calc_dt(df_11[df_11["pos"] == 2]))

        # size = 1, rate = 2
        df_12 = df_new.query("size == 1 and rate == 2")
        analyzed_data["12"].append(calc_dt(df_12))
        analyzed_data["12_0"].append(calc_dt(df_12[df_12["pos"] == 0]))
        analyzed_data["12_1"].append(calc_dt(df_12[df_12["pos"] == 1]))
        analyzed_data["12_2"].append(calc_dt(df_12[df_12["pos"] == 2]))

        # size = 2, rate = 1
        df_21 = df_new.query("size == 2 and rate == 1")
        analyzed_data["21"].append(calc_dt(df_21))
        analyzed_data["21_0"].append(calc_dt(df_21[df_21["pos"] == 0]))
        analyzed_data["21_1"].append(calc_dt(df_21[df_21["pos"] == 1]))
        analyzed_data["21_2"].append(calc_dt(df_21[df_21["pos"] == 2]))

        # size = 2, rate = 2
        df_22 = df_new.query("size == 2 and rate == 2")
        analyzed_data["22"].append(calc_dt(df_22))
        analyzed_data["22_0"].append(calc_dt(df_22[df_22["pos"] == 0]))
        analyzed_data["22_1"].append(calc_dt(df_22[df_22["pos"] == 1]))
        analyzed_data["22_2"].append(calc_dt(df_22[df_22["pos"] == 2]))

    else:
        print("'result_path' is not invalid")

average = {}
for i, key in enumerate(analyzed_data):
    average[key] = sum(analyzed_data[key]) / len(analyzed_data[key])
print(average)


# Visualize RT when eye moving
x = [1, 2, 3]
y_1 = [average["11_0"], average["11_1"], average["11_2"]]
y_2 = [average["12_0"], average["12_1"], average["12_2"]]
y_3 = [average["21_0"], average["21_1"], average["21_2"]]
y_4 = [average["22_0"], average["22_1"], average["22_2"]]

plt.plot(x, y_1, color="red", label="[1, 1, 1]")
plt.plot(x, y_2, color="blue", label="[1, 2, 4]")
plt.plot(x, y_3, color="yellow", label="[2, 2, 2]")
plt.plot(x, y_4, color="green", label="[2, 4, 8]")
plt.xlabel("Position")
# plt.ylabel("Accuracy")
plt.ylabel("Duration Time")
plt.legend()
plt.show()
