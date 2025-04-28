import os
import json

import neurosym as ns

without_apps = "processed/without-apps/"
with_apps = "processed/with-apps/"


def rewrite_to_use_apps(node):
    if isinstance(node, str):
        return node
    assert isinstance(node, ns.SExpression)
    if node.symbol in {"lam"}:
        return ns.SExpression(
            node.symbol, [rewrite_to_use_apps(child) for child in node.children]
        )
    if node.symbol not in {
        "prev_dc_inv_0",
        "1x3",
        "3x1",
        "moveHand",
        "prev_dc_inv_1",
        "reverseHand",
        "tower_embed",
        "tower_loopM",
    }:
        raise RuntimeError(f"Invalid symbol: {node.symbol}")
    head = node.symbol
    for child in node.children:
        child = rewrite_to_use_apps(child)
        head = ns.SExpression("app", [head, child])
    return head


result = {}
for file_name in os.listdir(without_apps):
    with open(os.path.join(without_apps, file_name)) as f:
        result[file_name] = json.load(f)

os.makedirs(with_apps, exist_ok=True)

for file_name, data in result.items():
    for i, item in enumerate(data):
        if isinstance(item, str):
            continue
        assert isinstance(item, ns.SExpression)
        data[i] = rewrite_to_use_apps(item)

    with open(os.path.join(with_apps, file_name), "w") as f:
        json.dump(data, f, indent=4)
