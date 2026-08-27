
## ideation
We need to decide if we can fill -1 entries with non‑negative integers and permute A so that there exists a constant C with A_i + B_i = C for all i.

Observations:
- Permuting A means we can pair any A value with any B value after filling.
- For each i, after filling, we need a_i + b_i = C.
- If both a_i and b_i are known (non‑-1), then C is forced to a_i + b_i. All such forced values must be equal.
- If only one side is known, say a_i known, then we need b_i = C - a_i ≥ 0, so C ≥ a_i. Similarly for known b_i.
- If both are -1, any non‑negative a,b with sum C works.

Thus:
- Let forced_C be the sum from any index where both are known. If there are multiple such indices, they must all give the same sum.
- If forced_C exists, we need forced_C ≥ every known A_i and forced_C ≥ every known B_i (otherwise the other side would be negative).
- If no forced_C exists (no index has both known), we can pick C arbitrarily large, so answer is always Yes.

Edge cases:
- N ≥ 2, but that doesn't matter.
- Values up to 1e9, sums up to 2e9, fits in 64‑bit.

Algorithm:
1. Read N, arrays A, B.
2. Initialize forced = None.
3. For each i:
   - If A[i] != -1 and B[i] != -1:
       - s = A[i] + B[i]
       - If forced is None, set forced = s.
       - Else if forced != s, answer No.
4. If forced is not None:
   - For each i:
       - If A[i] != -1 and A[i] > forced: No.
       - If B[i] != -1 and B[i] > forced: No.
5. Else (no forced): Yes.
6. Output Yes/No.

Complexities: O(N) time, O(1) extra.

## worker: Implement the solution in Python: create a solve()
The solution follows the reasoning in the plan:  
- If any index has both A_i and B_i known, the common sum C is forced to A_i + B_i. All such forced sums must agree.  
- If a forced sum S exists, every known A_i and B_i must be ≤ S, otherwise the counterpart would need to be negative.  
- If no forced sum exists (no index has both known), we can always pick a sufficiently large C, so the answer is always Yes.  
The algorithm runs in O(N) time and O(1) extra space, handling large integers via Python's arbitrary precision.
