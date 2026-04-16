from threshold_hbs import ThresholdHBSScheme

def main():
    scheme = ThresholdHBSScheme(parties=3, tree_height=3)

    message = b"threshold hash-based signatures demo"
    signature = scheme.sign(message)

    print("-- Demo: Minimal Threshold HBS --")
    print("Merkle root:", scheme.public_bundle.merkle_root.hex())
    print("Max signatures:", scheme.public_bundle.max_signatures)
    print("Leaf index used:", signature.leaf_index)
    print("Revealed elements:", len(signature.revealed))
    print("Verification result:", scheme.verify(signature))

if __name__ == "__main__":
    main()

