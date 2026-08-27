
## ideation
Core difficulty: `N` can be `2e5` and values are 60-bit, so general “max XOR of exactly K items” looks hard, but the guarantee `C(N,K) <= 1e6` makes subset enumeration feasible if we enumerate the smaller side `r = min(K, N-K)`. Key identity: if `K > N/2`, enumerate complements of size `N-K`; `xor(chosen) = total_xor ^ xor(complement)` because XOR is self-inverse and chosen/complement partition the array.

Candidate approach: iterative lexicographic combination generation over indices of size `r`, compute each subset XOR, track max. If `r == K`, answer is max subset XOR directly; else answer is max `total_xor ^ subset_xor`. Python integers handle `<2^60` natively. Duplicates are fine because combinations are over indices, not values.

Pitfalls: don’t enumerate the larger side; don’t accidentally maximize complement XOR when using complements; avoid recursion depth/stack and storing all combinations; handle `r=0` (`K=0` or `K=N`) where subset XOR is `0`; ensure combination update terminates correctly; keep per-combination work near `O(r)` or better, since `C(N,r) <= 1e6` but constant factors matter in Python.

## worker: Implement the complete Python program: fast stdin 
- Let `r = min(K, N-K)`. Since `C(N,K) = C(N,N-K) <= 1e6`, enumerating all `r`-subsets is feasible.
- If `K <= N/2`, directly maximize the XOR of each enumerated `K`-subset.
- If `K > N/2`, enumerate complements `S` of size `N-K`; the chosen XOR is `total_xor ^ xor(S)`, because chosen and complement partition the array.
- Combinations are generated iteratively in lexicographic order over indices, so duplicates in values are handled correctly.
- Complexity: `O(N + C(N,r) * r)` time, `O(N + r)` memory. The binomial constraint keeps this easily within limits.
