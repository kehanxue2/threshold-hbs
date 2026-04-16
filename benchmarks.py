from threshold_hbs import ThresholdHBSScheme

def main():
    print("-- Benchmark: Minimal Threshold HBS --")

    settings = [(2, 2), (2, 3), (3, 2), (3, 3), (4, 3),]

    for parties, tree_height in settings:
        scheme = ThresholdHBSScheme(parties=parties, tree_height=tree_height)
        result = scheme.benchmark(rounds=5)
        print(result.to_dict())

if __name__ == "__main__":
    main()

