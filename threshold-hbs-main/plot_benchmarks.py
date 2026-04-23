# plot_benchmarks.py
import json
import matplotlib.pyplot as plt
from collections import defaultdict

def load_results(path="benchmark_results.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def safe_metric(row, metric):
    return row.get(metric, 0.0)

def plot_scheme_comparison(results):
    schemes = []
    setup = []
    sign = []
    verify = []

    chosen = {}
    for row in results:
        scheme = row["scheme"]
        if scheme not in chosen:
            chosen[scheme] = row

    for scheme, row in chosen.items():
        schemes.append(scheme)
        setup.append(safe_metric(row, "setup_time"))
        sign.append(
            row.get("sign_time",
            row.get("batch_sign_time",
            row.get("hierarchical_batch_sign_time", 0.0)))
        )
        verify.append(safe_metric(row, "verify_time"))

    x = range(len(schemes))

    plt.figure(figsize=(10, 5))
    plt.bar(x, setup)
    plt.xticks(x, schemes, rotation=30, ha="right")
    plt.ylabel("Seconds")
    plt.title("Setup Time Across Schemes")
    plt.tight_layout()
    plt.savefig("plot_setup_comparison.png")
    plt.close()

    plt.figure(figsize=(10, 5))
    plt.bar(x, sign)
    plt.xticks(x, schemes, rotation=30, ha="right")
    plt.ylabel("Seconds")
    plt.title("Signing Time Across Schemes")
    plt.tight_layout()
    plt.savefig("plot_sign_comparison.png")
    plt.close()

    plt.figure(figsize=(10, 5))
    plt.bar(x, verify)
    plt.xticks(x, schemes, rotation=30, ha="right")
    plt.ylabel("Seconds")
    plt.title("Verification Time Across Schemes")
    plt.tight_layout()
    plt.savefig("plot_verify_comparison.png")
    plt.close()

def plot_tree_height_effect(results):
    grouped = defaultdict(list)
    for row in results:
        if "tree_height" in row and row["scheme"] in {
            "Minimal", "Extension1_KOfN", "Extension2_Distributed", "Extension5_Winternitz"
        }:
            grouped[row["scheme"]].append(row)

    for scheme, rows in grouped.items():
        rows = sorted(rows, key=lambda r: r["tree_height"])
        x = [r["tree_height"] for r in rows]
        y = [r.get("setup_time", 0.0) for r in rows]

        plt.figure(figsize=(8, 5))
        plt.plot(x, y, marker="o")
        plt.xlabel("Tree Height")
        plt.ylabel("Setup Time (s)")
        plt.title(f"Tree Height vs Setup Time: {scheme}")
        plt.tight_layout()
        plt.savefig(f"plot_treeheight_{scheme}.png")
        plt.close()

def plot_batch_efficiency(results):
    batch_rows = [
        r for r in results
        if r["scheme"] in {"Extension3_Batched", "Extension4_Hierarchical"}
    ]

    grouped = defaultdict(list)
    for row in batch_rows:
        grouped[row["scheme"]].append(row)

    plt.figure(figsize=(8, 5))
    for scheme, rows in grouped.items():
        rows = sorted(rows, key=lambda r: r["batch_size"])
        x = [r["batch_size"] for r in rows]
        y = [r["avg_sign_time_per_message"] for r in rows]
        plt.plot(x, y, marker="o", label=scheme)

    plt.xlabel("Batch Size")
    plt.ylabel("Average Sign Time per Message (s)")
    plt.title("Batch Efficiency Comparison")
    plt.legend()
    plt.tight_layout()
    plt.savefig("plot_batch_efficiency.png")
    plt.close()

def main():
    results = load_results()
    plot_scheme_comparison(results)
    plot_tree_height_effect(results)
    plot_batch_efficiency(results)
    print("Plots generated.")

if __name__ == "__main__":
    main()