The pattern `p` has exactly two `*`s, so we can split it into three parts: `p1` (before first `*`), `p2` (between `*`s), `p3` (after second `*`). The substring must start with `p1`, then later contain `p2`, then later contain `p3`, with arbitrary characters between these fixed parts (including empty).

Strategy:
1. Preprocess `s` to find all occurrences of each fixed part using **KMP** (or rolling hash, but KMP is exact and clean).
2. For each occurrence of `p3` ending at position `i`, find the latest occurrence of `p2` that ends before or at `i`. For each occurrence of `p2` ending at position `j`, find the latest occurrence of `p1` that ends before or at `j`. Use **two-pointer sweeps** over precomputed start/end indices for efficiency.
3. Track the minimum total span. The empty substring case (`"**"`) yields `0`. If no valid triple exists, return `-1`.

This runs in `O(|s| + |p|)` time.