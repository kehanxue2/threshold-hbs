from threshold_hbs import ThresholdHBSScheme, KOfNThresholdHBSScheme

def main():
    print("-- Benchmark: Minimal Threshold HBS --")

    mini_settings = [(2, 2), (2, 3), (3, 2), (3, 3), (4, 3),]

    for parties, tree_height in mini_settings:
        scheme = ThresholdHBSScheme(parties=parties, tree_height=tree_height)
        result = scheme.benchmark(rounds=5)
        print(result.to_dict())

    print()
    print("-- Benchmark: Extension 1 k-of-n Threshold HBS --")

    ext_settings1 = [(4, 3, 3), (5, 3, 3), (5, 4, 2), ]

    for parties, threshold_k, tree_height in ext_settings1:
        scheme = KOfNThresholdHBSScheme(parties=parties, threshold_k=threshold_k, tree_height=tree_height)
        result = scheme.benchmark(rounds=5)
        print(result)

if __name__ == "__main__":
    main()

