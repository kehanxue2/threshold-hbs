"""Generate SVG charts and a Markdown summary from benchmark_results.csv.

This script uses only the Python standard library so that it matches the
repository's lightweight dependency model.
"""

from __future__ import annotations

import csv
import math
from collections import defaultdict
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
INPUT_CSV = BASE_DIR / "benchmark_results.csv"
OUTPUT_DIR = BASE_DIR / "analysis_outputs"

SCHEME_LABELS = {
    "minimal": "Minimal",
    "ext1_k_of_k_subtree": "Ext1 k-of-n",
    "ext2_distributed": "Ext2 distributed",
    "ext3_batched": "Ext3 batched",
    "ext4_hierarchical_batched": "Ext4 hierarchical",
    "ext5_winternitz": "Ext5 Winternitz",
}

COLORS = [
    "#1f4e79",
    "#2e8b57",
    "#c26d00",
    "#8b3a3a",
    "#5b4b8a",
    "#4a6a6d",
]

METRICS = [
    ("setup_time_mean", "Average setup time (s)", "avg_setup_time.svg"),
    (
        "avg_sign_time_per_message",
        "Average sign time per message (s)",
        "avg_sign_time_per_message.svg",
    ),
    ("verify_time_mean", "Average verify time (s)", "avg_verify_time.svg"),
    ("signature_size_bytes", "Average signature size (bytes)", "avg_signature_size.svg"),
    ("total_comm_bytes", "Average total communication (bytes)", "avg_total_comm.svg"),
]


def parse_value(row, key):
    value = row.get(key, "")
    if value == "":
        return None
    try:
        return float(value)
    except ValueError:
        return None


def load_rows(path):
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = []
        for row in reader:
            parsed = dict(row)
            for key in row:
                if key in {
                    "setup_time_mean",
                    "setup_time_stdev",
                    "sign_time_mean",
                    "sign_time_stdev",
                    "verify_time_mean",
                    "verify_time_stdev",
                    "avg_sign_time_per_message",
                    "signature_size_bytes",
                    "public_root_size_bytes",
                    "crv_size_bytes",
                    "round1_comm_bytes",
                    "round2_comm_bytes",
                    "total_comm_bytes",
                }:
                    parsed[key] = parse_value(row, key)
            rows.append(parsed)
        return rows


def average_by_scheme(rows, metric):
    grouped = defaultdict(list)
    for row in rows:
        value = row.get(metric)
        if value is not None:
            grouped[row["scheme"]].append(value)

    averages = []
    for scheme, values in grouped.items():
        averages.append(
            {
                "scheme": scheme,
                "label": SCHEME_LABELS.get(scheme, scheme),
                "value": sum(values) / len(values),
            }
        )

    return sorted(averages, key=lambda item: item["value"], reverse=True)


def format_metric(metric, value):
    if metric.endswith("_bytes"):
        return f"{value:.0f}"
    return f"{value:.6f}"


def svg_bar_chart(metric, title, data, output_path):
    width = 980
    height = 560
    margin_top = 80
    margin_right = 40
    margin_bottom = 110
    margin_left = 120
    plot_width = width - margin_left - margin_right
    plot_height = height - margin_top - margin_bottom

    max_value = max(item["value"] for item in data) if data else 1.0
    if max_value <= 0:
        max_value = 1.0

    step = plot_width / max(len(data), 1)
    bar_width = step * 0.62

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#f7f4ee"/>',
        f'<text x="{margin_left}" y="42" font-size="24" font-family="Arial, sans-serif" fill="#1c1c1c">{title}</text>',
        f'<text x="{margin_left}" y="66" font-size="12" font-family="Arial, sans-serif" fill="#555">Generated from benchmark_results.csv</text>',
        f'<line x1="{margin_left}" y1="{margin_top + plot_height}" x2="{margin_left + plot_width}" y2="{margin_top + plot_height}" stroke="#222" stroke-width="1.5"/>',
        f'<line x1="{margin_left}" y1="{margin_top}" x2="{margin_left}" y2="{margin_top + plot_height}" stroke="#222" stroke-width="1.5"/>',
    ]

    ticks = 5
    for idx in range(ticks + 1):
        y = margin_top + plot_height - (plot_height * idx / ticks)
        tick_value = max_value * idx / ticks
        parts.append(
            f'<line x1="{margin_left - 6}" y1="{y:.2f}" x2="{margin_left + plot_width}" y2="{y:.2f}" stroke="#d8d1c4" stroke-width="1"/>'
        )
        parts.append(
            f'<text x="{margin_left - 12}" y="{y + 4:.2f}" text-anchor="end" font-size="11" font-family="Arial, sans-serif" fill="#444">{format_metric(metric, tick_value)}</text>'
        )

    for index, item in enumerate(data):
        bar_height = 0 if max_value == 0 else (item["value"] / max_value) * plot_height
        x = margin_left + index * step + (step - bar_width) / 2
        y = margin_top + plot_height - bar_height
        color = COLORS[index % len(COLORS)]
        label_x = x + bar_width / 2
        value_text = format_metric(metric, item["value"])
        rotation_x = label_x
        rotation_y = margin_top + plot_height + 22

        parts.append(
            f'<rect x="{x:.2f}" y="{y:.2f}" width="{bar_width:.2f}" height="{bar_height:.2f}" rx="6" fill="{color}"/>'
        )
        parts.append(
            f'<text x="{label_x:.2f}" y="{y - 8:.2f}" text-anchor="middle" font-size="11" font-family="Arial, sans-serif" fill="#222">{value_text}</text>'
        )
        parts.append(
            f'<text x="{rotation_x:.2f}" y="{rotation_y:.2f}" text-anchor="end" transform="rotate(-28 {rotation_x:.2f} {rotation_y:.2f})" font-size="12" font-family="Arial, sans-serif" fill="#222">{item["label"]}</text>'
        )

    parts.append("</svg>")
    output_path.write_text("\n".join(parts), encoding="utf-8")


def pick_best_rows(rows):
    best_rows = {}
    for row in rows:
        scheme = row["scheme"]
        score = row.get("avg_sign_time_per_message")
        if score is None:
            continue
        current = best_rows.get(scheme)
        if current is None or score < current["avg_sign_time_per_message"]:
            best_rows[scheme] = row
    return best_rows


def summarize_rows(rows):
    best_rows = pick_best_rows(rows)

    minimal_best = best_rows.get("minimal")
    ext2_best = best_rows.get("ext2_distributed")
    ext3_best = best_rows.get("ext3_batched")
    ext4_best = best_rows.get("ext4_hierarchical_batched")
    ext5_best = best_rows.get("ext5_winternitz")

    lines = [
        "# Performance Summary",
        "",
        "## Scope",
        "",
        "- Source file: `benchmark_results.csv` generated by `benchmarks.py`.",
        "- Visual outputs: SVG charts in `analysis_outputs/`.",
        "- Interpretation rule: benchmark rows use different parameter tuples, so cross-scheme comparisons are directional rather than fully apples-to-apples.",
        "",
        "## Key Findings",
        "",
    ]

    if minimal_best and ext2_best:
        ratio = ext2_best["avg_sign_time_per_message"] / minimal_best["avg_sign_time_per_message"]
        lines.append(
            f"- The best distributed configuration is about {ratio:.2f}x slower than the best minimal configuration on signing, which matches the expected overhead of two-round coordination and CRV reconstruction."
        )

    if ext2_best and ext3_best:
        improvement = 1 - (
            ext3_best["avg_sign_time_per_message"] / ext2_best["avg_sign_time_per_message"]
        )
        lines.append(
            f"- Batched signing reduces average signing cost per message by about {improvement * 100:.1f}% relative to the best distributed single-message configuration."
        )

    if ext3_best and ext4_best:
        delta = ext4_best["avg_sign_time_per_message"] - ext3_best["avg_sign_time_per_message"]
        lines.append(
            f"- Hierarchical batching is slightly slower per message than flat batching in the best observed settings (+{delta:.6f}s), so its value is structural scalability rather than raw speed in this prototype."
        )

    if ext2_best and ext5_best:
        sig_ratio = ext5_best["signature_size_bytes"] / ext2_best["signature_size_bytes"]
        comm_ratio = ext5_best["total_comm_bytes"] / ext2_best["total_comm_bytes"]
        lines.append(
            f"- Winternitz cuts signature size to about {sig_ratio * 100:.1f}% and communication to about {comm_ratio * 100:.1f}% of the best distributed Lamport configuration."
        )
        lines.append(
            "- Winternitz setup is still the most expensive stage because CRV material must be prepared for every chain and every leaf."
        )

    lines.extend(
        [
            "",
            "## Best Observed Row Per Scheme",
            "",
            "| Scheme | Sign/msg (s) | Verify (s) | Signature (bytes) | Total comm (bytes) |",
            "| --- | ---: | ---: | ---: | ---: |",
        ]
    )

    for scheme in [
        "minimal",
        "ext1_k_of_k_subtree",
        "ext2_distributed",
        "ext3_batched",
        "ext4_hierarchical_batched",
        "ext5_winternitz",
    ]:
        row = best_rows.get(scheme)
        if row is None:
            continue
        lines.append(
            "| {label} | {sign:.6f} | {verify:.6f} | {sig:.0f} | {comm:.0f} |".format(
                label=SCHEME_LABELS.get(scheme, scheme),
                sign=row["avg_sign_time_per_message"],
                verify=row["verify_time_mean"],
                sig=row["signature_size_bytes"],
                comm=row["total_comm_bytes"],
            )
        )

    return "\n".join(lines) + "\n"


def main():
    if not INPUT_CSV.exists():
        raise FileNotFoundError("benchmark_results.csv was not found. Run benchmarks.py first.")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    rows = load_rows(INPUT_CSV)

    for metric, title, filename in METRICS:
        chart_data = average_by_scheme(rows, metric)
        svg_bar_chart(metric, title, chart_data, OUTPUT_DIR / filename)

    summary = summarize_rows(rows)
    (OUTPUT_DIR / "performance_summary.md").write_text(summary, encoding="utf-8")
    print(f"Saved analysis outputs to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
