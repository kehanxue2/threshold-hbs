# COMP6453 Threshold Hash-Based Signatures

## Overview

This repository contains a working prototype of a threshold hash-based
signature system built around:

- Lamport one-time signatures
- Merkle authentication trees
- XOR-based share recombination
- a distributed two-round signing simulation for later extensions

The code is best understood as a research or coursework prototype. It is useful
for demonstrating signing flow, verification flow, and performance trade-offs,
but it is not a production cryptography library.

## What Is Implemented

### Minimal baseline

`ThresholdHBSScheme` implements a centralized baseline:

- a dealer generates Lamport one-time secret keys for every Merkle leaf,
- the dealer distributes XOR shares across parties,
- an aggregator collects party responses and reconstructs a threshold signature,
- verification checks both the Lamport reveal set and the Merkle path.

### Extension 1: k-of-n via subset subtrees

`KOfNThresholdHBSScheme` realizes k-of-n signing through a k-of-k subset
construction. Each leaf is assigned to one fixed signer subset, so the code
models threshold access by subtree allocation rather than by a generic
combinatorial threshold combiner.

### Extension 2: distributed threshold signing

`DistributedThresholdHBSScheme` adds:

- helper-string lookup,
- PRF-style local share derivation,
- session agreement,
- explicit round-1 and round-2 party responses,
- CRV-style correction material for reconstructing the final signature.

This extension is only partially distributed. Parties derive shares locally
during signing, but setup remains centrally prepared.

### Extension 3: batched signing

`BatchedThresholdHBSScheme` hashes a batch of messages into a batch Merkle root,
signs that root once, and verifies each message with its batch authentication
path.

### Extension 4: hierarchical batched signing

`HierarchicalBatchedThresholdHBSScheme` adds a subtree-level Merkle layer plus
an upper-tree path, producing hierarchical authentication paths.

### Extension 5: Winternitz optimization

`WinternitzThresholdHBSScheme` replaces Lamport reveals with Winternitz chains
while keeping the distributed two-round threshold flow. This reduces signature
size and communication cost, but increases setup complexity.

## Repository Layout

- `threshold_hbs.py`: core implementation for the baseline and Extensions 1-5
- `demo.py`: runnable end-to-end demonstration for all schemes
- `benchmarks.py`: benchmark harness that writes `benchmark_results.csv`
- `performance_analysis.py`: converts benchmark CSV output into SVG charts and a
  short Markdown summary
- `report.md`: review report for code quality, design alignment, and benchmark
  interpretation

## Requirements

- Python 3.x
- Standard library only

The repository does not require third-party Python packages.

## How To Run

### 1. Run the demo

```bash
python demo.py
```

Expected outcome:

- all single-message schemes print `Verification result: True`
- batched schemes print verification lists such as `[True, True, True]`

### 2. Run benchmarks

```bash
python benchmarks.py
```

Generated file:

- `benchmark_results.csv`

### 3. Generate visual analysis

```bash
python performance_analysis.py
```

Generated files:

- `analysis_outputs/avg_setup_time.svg`
- `analysis_outputs/avg_sign_time_per_message.svg`
- `analysis_outputs/avg_verify_time.svg`
- `analysis_outputs/avg_signature_size.svg`
- `analysis_outputs/avg_total_comm.svg`
- `analysis_outputs/performance_summary.md`

## Verified Behavior

The current code was executed successfully with:

- `demo.py`
- `benchmarks.py`
- Python bytecode compilation for the main scripts

The benchmark run completed and produced valid verification results for all
configured rows.

## Performance Interpretation Notes

The benchmark data supports the following high-level conclusions:

- larger trees increase setup cost,
- Extension 2 is slower than the centralized baseline because of two-round
  distributed coordination and CRV reconstruction,
- Extensions 3 and 4 reduce average signing cost per message when batching is
  used,
- Extension 5 significantly reduces signature size and total communication.

Important caution:

- the benchmark parameter tuples differ across schemes, so comparisons are
  useful for directional trends but are not always strict apples-to-apples
  comparisons.

## Limitations

- This repository does not identify a specific target paper or theorem mapping,
  so claims should be read as implementation claims rather than formal
  proof-level conformance claims.
- Extension 2 is not a full distributed key generation system; setup is still
  centrally prepared.
- The code currently behaves like a prototype and does not yet include a full
  automated test suite for adversarial or malformed inputs.

## Suggested Next Steps

If you want to strengthen this repository for submission or evaluation, the most
useful follow-up improvements are:

1. add focused unit tests for tampering and edge cases,
2. add fair-comparison benchmarks under matched parameter tuples,
3. document the exact paper or construction being approximated.
