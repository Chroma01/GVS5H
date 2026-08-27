
## ideation
- Problem reduces to maximum number of disjoint pairs (i, j) with i < j and A[i] * 2 ≤ A[j] in a sorted array.
- Greedy two-pointer method is optimal: pair each “bottom” (larger) mochi with the smallest possible “top” (smaller) mochi that still satisfies the condition, then move both pointers.
- Need to handle duplicates correctly; the array is already non‑decreasing.
- Edge cases: when A[i] * 2 > A[j] for all j, answer is 0.
- Constraints N up to 5e5 → O(N) or O(N log N) is fine; O(N) two-pointer is ideal.
- Be careful with multiplication: A[i] and A[j] ≤ 1e9, so product ≤ 2e18, fits in 64‑bit integer (Python int is unbounded).

## worker: Implement the two-pointer greedy solution in Pytho
The algorithm uses a classic two-pointer greedy: maintain a pointer `i` for the smallest unused mochi that could serve as a top, and a pointer `j` for the current candidate bottom. For each `j`, we advance `i` (while `i < j`) until `a[i] * 2 > a[j]`. When that happens, `a[i]` cannot pair with `a[j]` nor any larger bottom (since the array is sorted), so we skip this `j` by incrementing `j`. If we find a valid `i` (`a[i] * 2 ≤ a[j]`), we pair them, count one kagamimochi, and advance both pointers. The correctness follows from the exchange argument: pairing the smallest feasible top with each bottom leaves larger tops for larger bottoms, never hurting future pairings. Complexity is O(N) time and O(1) extra space (aside from the input array). All arithmetic safely fits in Python's arbitrary‑precision integers.
