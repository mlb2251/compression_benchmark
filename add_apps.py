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
        "$0",
        "$2",
        "*",
        "*.",
        "+",
        "+.",
        "-",
        "-.",
        "/.",
        "1x3",
        "3x1",
        "car",
        "cdr",
        "char-eq?",
        "cons",
        "empty?",
        "eq?",
        "fold",
        "gt?",
        "if",
        "index",
        "is-prime",
        "is-square",
        "length",
        "logo_ADDA",
        "logo_DIVA",
        "logo_DIVL",
        "logo_FWRT",
        "logo_GETSET",
        "logo_MULA",
        "logo_MULL",
        "logo_PT",
        "logo_SUBA",
        "logo_forLoop",
        "map",
        "mod",
        "moveHand",
        "power",
        *[f"prev_dc_inv_{i}" for i in range(25)],
        "range",
        "reverseHand",
        "tower_embed",
        "tower_loopM",
        "unfold",
        "zip",
    }:
        # syms.add(node.symbol)
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
        item = ns.parse_s_expression(item)
        item = rewrite_to_use_apps(item)
        item = ns.render_s_expression(item)
        data[i] = item

    with open(os.path.join(with_apps, file_name), "w") as f:
        json.dump(data, f, indent=4)
