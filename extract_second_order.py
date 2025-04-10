from collections import defaultdict
import os
import glob
import json

out_path = "processed/without-apps"
paths = glob.glob("**/out/stitch/**/raw/*.json", recursive=True)

loaded = {}
for path in paths:
    with open(path) as f:
        loaded[path] = json.load(f)["original"]

# keys look like benches/logo_logo_batch_50_1h_ellisk_2019-03-23T14.13.04/out/stitch/2022-10-04_19-35-55/raw/bench000_it0.json
# benches/list_list_hard_test_ellisk_2019-02-15T11.26.41/out/stitch/2022-10-04_19-36-01/raw/bench004_it5.json
# we want to extract an overall name (e.g., logo_logo_batch_50) and the specific name (e.g., 0 or 4)

named = defaultdict(list)
for k, v in loaded.items():
    v = sorted(v)
    _, name_1, *_, name_2 = k.split("/")
    name_1, _ = name_1.split("_ellisk_")
    assert name_2.endswith(".json")
    name_2 = name_2[: len(".json")]
    # name_2 = int(re.match(r"bench(\d+)_it(\d+)", name_2).group(1))
    named[(name_1, name_2)].append(v)

named = {
    (name_1, name_2, it): v
    for (name_1, name_2), vs in named.items()
    for it, v in enumerate(vs)
}

os.makedirs(out_path, exist_ok=True)

for (name_1, name_2, it), v in named.items():
    with open(f"{out_path}/{name_1}_{name_2}_{it}.json", "w") as f:
        json.dump(v, f, indent=4)
