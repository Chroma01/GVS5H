We split the pattern `p` at the two `*` characters into three parts: prefix `A`, middle `B`, and suffix `C`. A substring `s[i..j]` matches `p` iff it starts with `A`, ends with `C`, and contains `B` somewhere in between (the `*`s can match zero characters). We need the shortest such substring.

Approach:
1. Use Z-algorithm (or prefix-function) to compute, for each position in `s`, the longest prefix of `A` that matches starting there, and the longest suffix of `C` that matches ending there.
2. Similarly compute, for each position in `s`, the longest prefix of `B` that matches starting there.
3. For each possible start index `i` where `A` matches (i.e., `prefA[i] == |A|`), find the earliest end index `j` such that `s[j..]` ends with `C` (`sufC[j] == |C|`) and there exists some `k` in `[i+|A|, j-|C|]` where `B` matches starting at `k` (`prefB[k] >= |B|` and `k+|B|-1 <= j-|C|`). Use a precomputed array of the earliest valid `k` for each `j` (or a segment tree / prefix minimum) to answer this in O(1) per `i`.
4. Take the minimum length `j - i + 1` over all valid pairs. If none, return -1. Edge cases: empty parts (e.g., `**`) are handled naturally.

This runs in O(|s| + |p|) time and O(|s|) memory.