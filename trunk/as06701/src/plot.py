import csv
import sys
import argparse
from collections import defaultdict

import matplotlib
import matplotlib.pyplot as plt


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--csv", default="output.csv")
    p.add_argument("--png", default="result.png")
    p.add_argument("--no-show", action="store_true",
                   help="не открывать окно (headless-режим)")
    return p.parse_args()


def load(csv_path):
    """data[model][input] = [(tau, u, y), ...]"""
    data = defaultdict(lambda: defaultdict(list))
    with open(csv_path, newline="") as f:
        for row in csv.DictReader(f):
            data[row["model"]][row["input"]].append(
                (int(row["tau"]), float(row["u"]), float(row["y"]))
            )
    for m in data:
        for inp in data[m]:
            data[m][inp].sort(key=lambda t: t[0])
    return data


def print_table(model, inp, rows):
    print(f"\n=== {model} | input={inp} ===")
    print(f"{'tau':>5} | {'u':>10} | {'y':>12}")
    print("-" * 32)
    for tau, u, y in rows:
        print(f"{tau:>5} | {u:>10.4f} | {y:>12.4f}")


def main():
    args = parse_args()
    data = load(args.csv)

    if not data:
        print(f"No data in {args.csv}")
        sys.exit(1)

    models = sorted(data.keys())
    inputs_order = ["step", "impulse", "harmonic"]

    # печать таблиц
    for m in models:
        for inp in inputs_order:
            if inp in data[m]:
                print_table(m, inp, data[m][inp])

    # график
    fig, axes = plt.subplots(1, len(models),
                             figsize=(4.5 * len(models), 4),
                             squeeze=False)
    axes = axes[0]

    for ax, m in zip(axes, models):
        for inp in inputs_order:
            if inp not in data[m]:
                continue
            rows = data[m][inp]
            ax.plot([r[0] for r in rows],
                    [r[2] for r in rows],
                    label=inp, linewidth=1.2)
        ax.set_title(m)
        ax.set_xlabel("tau")
        ax.set_ylabel("y")
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=8)

    plt.tight_layout()
    plt.savefig(args.png, dpi=120)
    print(f"\nSaved {args.png}")

    if not args.no_show:
        try:
            plt.show()
        except Exception as e:
            print(f"Could not open window: {e}. See {args.png}")


if __name__ == "__main__":
    main()
