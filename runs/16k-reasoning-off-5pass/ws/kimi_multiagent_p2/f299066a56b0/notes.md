
## ideation
The core problem: maximum matching in a "comparability" graph where mochi i can sit on mochi j iff 2*a_i ≤ a_j. Since sizes are sorted, this has a special structure — it's a bipartite-like matching with an interval property, which admits a greedy / Hall's-condition solution.

Key insight: For K pairs to be feasible, a necessary and sufficient condition (by a rearrangement/Hall argument) is that the K smallest mochi can each be paired with the K largest: A[i] * 2 ≤ A[N-K+i] for all 0 ≤ i < K. Proof sketch: any feasible solution uses K tops and K bottoms; the K tops must be pairable against K distinct bottoms each at least double. The smallest K tops are the "easiest" to satisfy, and the largest K bottoms are the "most capable"; if the K-th smallest top can't match the K-th largest bottom in this aligned pairing, no other assignment works either (exchange argument). Conversely if the aligned pairing works, it's a valid construction.

Monotonicity: if K is feasible, any K' < K is feasible (drop some pairs). So binary search over K ∈ [0, N//2], each check O(K), total O(N log N) — fine for N = 5×10^5.

Alternative: a single greedy two-pointer pass (match smallest unmatched top with smallest sufficient bottom, but only using the second half as bottom candidates) is O(N). Actually the clean greedy: split at midpoint, i over first half (tops), j over second half (bottoms), advance both when A[i]*2 ≤ A[j], else advance j only. Count matches. This is O(N) and also correct, but requires care with the split point when N is odd. Binary search avoids that subtlety.

Pitfalls:
- Overflow isn't an issue in Python, but in other languages 2*A_i could overflow 32-bit.
- K can be 0 (sample 2).
- The check must use the K largest, i.e., index N-K+i, not just any K elements.
- Don't overthink: a common wrong greedy is pairing adjacent elements or using a top that's too large.

## worker: Write the complete Python solution: parse N and li
- Feasibility of K pairs reduces (by an exchange/Hall argument on the sorted array) to checking the aligned pairing of the K smallest tops against the K largest bottoms: `A[i]*2 <= A[N-K+i]` for all `i < K`. If the easiest tops can't match the most capable bottoms in this aligned way, no assignment exists; if they can, this is a valid construction.
- Feasibility is monotone in K, so binary search over `[0, N//2]`. Each check is O(K), total O(N log N), well within limits for N = 5×10^5. Python ints avoid overflow of `2*A_i`.
- Edge cases: K=0 works automatically (empty check passes); odd N handled since K ≤ N//2.
