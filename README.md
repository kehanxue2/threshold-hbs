# COMP6453 Threshold Hash-Based Signatures

## Overview
- These codes implement a prototype of a threshold hash-based signature scheme in a centralised setting, and extend it with multiple advanced features for performance and functionality. 

- It combines:
    Lamport one-time signatures, 
    Merkle tree structure, 
    XOR-based secret sharing

- A trusted dealer generates keys and distributes secret shares to parties, while an untrusted aggregator collects partial signatures and reconstructs the final signature. Correctness is ensured via Lamport verification and Merkle path validation. 

## Extensions
- This project includes five extensions beyond the minimal scheme
- Extension 1: k-of-n Threshold Signing: implements a general k-of-n threshold scheme where only k out of n parties are required to produce a valid signature.
- Extension 2: Distributed Threshold Signing: removes the fully trusted dealer assumption by simulating distributed key generation and signing behaviour.
- Extension 3: Batched Signing: supports batch signing of multiple messages to improve throughput.
- Extension 4: Hierarchical Batched Signing: introduces a hierarchical Merkle structure to further optimise batch signing performance.
- Extension 5: Winternitz Optimization: replaces Lamport signatures with Winternitz signatures to reduce signature size and improve efficiency. 

## Structure
- `threshold_hbs.py`: core implementation of the scheme, including all schemes and extensions. 
- `demo.py`: demonstrates the complete signing and verification processes. 
- `benchmarks.py`: evaluates performance under different parameter settings. 

## How to Run
- Step 1: Run Demo

    python demo.py

- Step 2: Run Benchmark

    python benchmarks.py


## Example
### Demo Output (simplified) and Explanation:
    -- Demo: Minimal Threshold HBS --
    Verification result: True

    -- Demo: Extension 1 (k-of-n Threshold HBS) --
    Verification result: True

    -- Demo: Extension 2 (Distributed Threshold HBS) --
    Verification result: True

    -- Demo: Extension 3 (Batched Threshold HBS) --
    Verification results: [True, True, True]

    -- Demo: Extension 4 (Hierarchical Batched Threshold HBS) --
    Verification results: [True, True, True]

    -- Demo: Extension 5 (Winternitz Threshold HBS) --
    Verification result: True

- The demo shows that all schemes produce valid signatures. The extensions introduce additional functionality such as threshold flexibility, distributed coordination, batching, hierarchical organisation, and signature size optimisation. 

### Benchmarks Output Explanation:

- The benchmark results demonstrate the trade-offs between performance, scalability, and signature size across different extensions. 

