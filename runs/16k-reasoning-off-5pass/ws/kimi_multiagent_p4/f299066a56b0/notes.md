
## ideation
The core difficulty is pairing mochi such that each top is at most half the size of its bottom, maximizing the number of pairs. Since the array is sorted ascending, the optimal strategy is greedy: use the smallest mochi as tops and find the smallest valid bottoms for them.

Key insight: In an optimal solution, if we make K pairs, we should use the K smallest mochi as tops and pair them with the K smallest valid bottoms from the remaining mochi. This is because smaller tops are easier to satisfy (need smaller bottoms), and using larger mochi as tops would only make constraints harder.

Candidate approaches:
1. **Direct greedy (two pointers)**: Split conceptually into "top half" (first N/2 elements) and "bottom half" (remaining). Use two pointers: i for tops (starting at 0), j for bottoms (starting at N/2). For each top A[i], advance j until A[j] >= 2*A[i], then pair them and advance both. Count pairs.
2. **Binary search on K**: Check if K pairs possible by greedily matching A[0..K-1] as tops with A[N-K..N-1] as bottoms (or similar). O(N log N) total.
3. **Single pass greedy**: More general two-pointer where we try to match smallest available top with smallest available valid bottom.

Pitfalls:
- The condition is `a <= b/2`, i.e., `2*a <= b` (integer arithmetic, careful with overflow in other languages but fine in Python).
- Need to ensure we don't reuse mochi.
- The greedy must match smallest tops with smallest valid bottoms to leave larger bottoms for larger tops.
- N can be up to 5×10^5, so O(N log N) or O(N) needed.

The direct greedy with i starting at 0 and j starting at N/2 works because we never need more than N/2 tops, and the optimal tops are always the smallest ones.

## worker: Implement the complete solution: read input, run t
- **Algorithm**: Two-pointer greedy. Since the array is sorted ascending, the optimal tops are always the smallest mochi (smaller tops are easier to satisfy). We never need more than `N//2` tops (each pair uses 2 mochi). So we use indices `i` in `[0, N//2)` as candidate tops and `j` in `[N//2, N)` as candidate bottoms.
- For each top `a[i]`, we advance `j` until we find a bottom with `a[j] >= 2*a[i]`. If found, we pair them (count++, advance both pointers). Otherwise we advance `j` to look for a bigger bottom.
- **Correctness sketch**: Suppose an optimal solution makes K pairs. Its tops, sorted, are `t_1 <= ... <= t_K` and bottoms `b_1 <= ... <= b_K` with `2*t_m <= b_m` (rearrangement: sort both and match in order — if `2*t_i <= b_j` and `2*t_k <= b_l` with `t_i <= t_k`, `b_j <= b_l`, matching in sorted order never hurts). Since `a[0..K-1] <= t_1..t_K` componentwise (they're the K smallest overall), and the greedy picks the smallest valid bottom for each successive top, greedy succeeds whenever any K-pairing exists. Also K ≤ N//2 always, so restricting tops to the first half is safe: the greedy finds the maximum.
- **Complexity**: O(N) time, O(N) memory for the array. N ≤ 5×10^5, easily fast enough.
- **Sample verification**:
  - Sample 1: `a = [2,3,4,4,7,10]`, tops region `[2,3,4]`, bottoms from index 3: `2→4` (2*2≤4 ✓), `3→7` (6≤7 ✓), `4→10` (8≤10 ✓) → 3. ✓
  - Sample 2: `[387,388,389]`, top `387`, bottom candidates from index 1: 2*387=774 > 388, 389 → 0. ✓
  - Sample 3: greedy pairs 307→614, 321→660, 330→669, 339→678, 349→712, 392→785 → 6. ✓
