import json
from threshold_hbs import (
    ThresholdHBSScheme,
    KOfNThresholdHBSScheme,
    DistributedThresholdHBSScheme,
    BatchedThresholdHBSScheme,
    HierarchicalBatchedThresholdHBSScheme,
    WinternitzThresholdHBSScheme,
)


OUTPUT_FILE = "benchmark_results.json"
ROUNDS = 20


def save_results(results, output_file=OUTPUT_FILE):
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved results to {output_file}")


def print_section(title):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


def normalise_result(result, scheme_name, extra_fields=None):
    """
    Organize the data returned by different benchmarks into a unified dictionary.
    """
    if hasattr(result, "to_dict"):
        row = result.to_dict()
    elif isinstance(result, dict):
        row = dict(result)
    else:
        raise TypeError(f"Unsupported benchmark result type: {type(result)}")

    row["scheme"] = scheme_name

    if extra_fields:
        row.update(extra_fields)

    return row


def run_minimal_benchmarks(rounds=ROUNDS):
    print_section("Benchmark: Minimal Threshold HBS")

    settings = [
        (2, 2),
        (3, 2),
        (4, 2),
        (4, 3),
        (5, 3),
    ]

    results = []

    for parties, tree_height in settings:
        scheme = ThresholdHBSScheme(parties=parties, tree_height=tree_height)
        result = scheme.benchmark(rounds=rounds)

        row = normalise_result(
            result,
            scheme_name="Minimal",
            extra_fields={
                "parties": parties,
                "tree_height": tree_height,
                "rounds": rounds,
            },
        )

        results.append(row)
        print(row)

    return results


def run_extension1_benchmarks(rounds=ROUNDS):
    print_section("Benchmark: Extension 1 k-of-n Threshold HBS")

    settings = [
        (4, 2, 3),
        (4, 3, 3),
        (5, 2, 4),
        (5, 3, 4),
        (6, 3, 5),
    ]

    results = []

    for parties, threshold_k, tree_height in settings:
        scheme = KOfNThresholdHBSScheme(
            parties=parties,
            threshold_k=threshold_k,
            tree_height=tree_height,
        )
        result = scheme.benchmark(rounds=rounds)

        row = normalise_result(
            result,
            scheme_name="Extension1_KOfN",
            extra_fields={
                "parties": parties,
                "threshold_k": threshold_k,
                "tree_height": tree_height,
                "rounds": rounds,
            },
        )

        results.append(row)
        print(row)

    return results


def run_extension2_benchmarks(rounds=ROUNDS):
    print_section("Benchmark: Extension 2 Distributed Threshold HBS")

    settings = [
        (4, 2, 3),
        (4, 3, 3),
        (5, 2, 4),
        (5, 3, 4),
        (6, 3, 5),
    ]

    results = []

    for parties, threshold_k, tree_height in settings:
        scheme = DistributedThresholdHBSScheme(
            parties=parties,
            threshold_k=threshold_k,
            tree_height=tree_height,
        )
        result = scheme.benchmark(rounds=rounds)

        row = normalise_result(
            result,
            scheme_name="Extension2_Distributed",
            extra_fields={
                "parties": parties,
                "threshold_k": threshold_k,
                "tree_height": tree_height,
                "rounds": rounds,
            },
        )

        results.append(row)
        print(row)

    return results


def run_extension3_benchmarks(rounds=ROUNDS):
    print_section("Benchmark: Extension 3 Batched Threshold HBS")

    settings = [
        (4, 2, 3, 2),
        (4, 3, 3, 3),
        (5, 2, 4, 4),
        (5, 3, 4, 4),
        (6, 3, 5, 5),
    ]

    results = []

    for parties, threshold_k, tree_height, batch_size in settings:
        scheme = BatchedThresholdHBSScheme(
            parties=parties,
            threshold_k=threshold_k,
            tree_height=tree_height,
        )
        result = scheme.benchmark_batch(rounds=rounds, batch_size=batch_size)

        row = normalise_result(
            result,
            scheme_name="Extension3_Batched",
            extra_fields={
                "parties": parties,
                "threshold_k": threshold_k,
                "tree_height": tree_height,
                "batch_size": batch_size,
                "rounds": rounds,
            },
        )

        results.append(row)
        print(row)

    return results


def run_extension4_benchmarks(rounds=ROUNDS):
    print_section("Benchmark: Extension 4 Hierarchical Batched Threshold HBS")

    settings = [
        (4, 2, 4, 2, 2),
        (4, 3, 4, 2, 3),
        (5, 2, 4, 2, 4),
        (5, 3, 4, 2, 4),
        (6, 3, 5, 2, 5),
    ]

    results = []

    for parties, threshold_k, tree_height, subtree_height, batch_size in settings:
        scheme = HierarchicalBatchedThresholdHBSScheme(
            parties=parties,
            threshold_k=threshold_k,
            tree_height=tree_height,
            subtree_height=subtree_height,
        )
        result = scheme.benchmark_hierarchical_batch(
            rounds=rounds,
            batch_size=batch_size,
        )

        row = normalise_result(
            result,
            scheme_name="Extension4_Hierarchical",
            extra_fields={
                "parties": parties,
                "threshold_k": threshold_k,
                "tree_height": tree_height,
                "subtree_height": subtree_height,
                "batch_size": batch_size,
                "rounds": rounds,
            },
        )

        results.append(row)
        print(row)

    return results


def run_extension5_benchmarks(rounds=ROUNDS):
    print_section("Benchmark: Extension 5 Winternitz Threshold HBS")

    settings = [
        (4, 2, 3, 4),
        (4, 3, 3, 8),
        (5, 2, 4, 8),
        (5, 3, 4, 16),
        (6, 3, 5, 16),
    ]

    results = []

    for parties, threshold_k, tree_height, w in settings:
        scheme = WinternitzThresholdHBSScheme(
            parties=parties,
            threshold_k=threshold_k,
            tree_height=tree_height,
            w=w,
        )
        result = scheme.benchmark(rounds=rounds)

        row = normalise_result(
            result,
            scheme_name="Extension5_Winternitz",
            extra_fields={
                "parties": parties,
                "threshold_k": threshold_k,
                "tree_height": tree_height,
                "w": w,
                "rounds": rounds,
            },
        )

        results.append(row)
        print(row)

    return results


def main():
    all_results = []

    all_results.extend(run_minimal_benchmarks())
    all_results.extend(run_extension1_benchmarks())
    all_results.extend(run_extension2_benchmarks())
    all_results.extend(run_extension3_benchmarks())
    all_results.extend(run_extension4_benchmarks())
    all_results.extend(run_extension5_benchmarks())

    save_results(all_results)

    print_section("Benchmark Summary")
    print(f"Total benchmark records: {len(all_results)}")


if __name__ == "__main__":
    main()