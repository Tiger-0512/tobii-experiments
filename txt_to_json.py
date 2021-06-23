from collections import defaultdict
import json

with open("../info-for-robustness/wordnet.is_a.txt", "r") as f1:
    data_list = f1.readlines()

d = defaultdict(list)

for l in data_list:
    key, val = list(l.split())
    d[key].append(val)

out_path = "./my_imgnet.json"
with open(out_path, "w") as f2:
    json.dump(d, f2, indent=4)