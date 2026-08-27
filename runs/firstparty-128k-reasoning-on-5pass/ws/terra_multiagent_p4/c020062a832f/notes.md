- **Algorithm:** Compute the inversion number for shift `k=0` with a Fenwick tree in `O(N log M)`. Process left to right; for element `A[i]=x`, previous greater elements equal `i - count(previous values <= x)`.
- **Shift update:** From shift `k` to `k+1`, only original value `x = M-1-k` wraps from current value `M-1` to `0`. Comparisons not involving this class remain unchanged.
- **Wrap delta:** For an occurrence of `x` at zero-based position `i`, with `s` previous occurrences of `x` and total frequency `c=freq[x]`, the inversion change is:
  `other_before - other_after = (i-s) - (N-i-c+s) = 2*i - 2*s - N + c`.
  Summing this over all occurrences gives `delta[x]`.
- **Duplicates:** Pairs of equal values are never inversions and are excluded by subtracting same-value elements through `s` and `freq[x]`.
- **Output order:** Print current answer for each `k=0..M-1`; after printing shift `k`, add `delta[M-1-k]` for the next shift.
- **Complexity:** `O(N log M + N + M)` time and `O(M)` auxiliary memory, aside from input storage.
- **Integer safety:** Python integers safely hold the maximum inversion count, approximately `N*(N-1)/2`.
