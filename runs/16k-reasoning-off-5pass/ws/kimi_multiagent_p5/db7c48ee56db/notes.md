
## ideation
The problem asks for the maximum XOR over all K-element subsets, with the special guarantee that C(N,K) ≤ 10^6. This guarantee is the crux: it means brute-force enumeration of combinations is feasible, but only if we enumerate the smaller side. Key observations:

1. If K ≤ N/2, directly enumerate all C(N,K) subsets, maintaining a running XOR via DFS with backtracking (XOR is self-inverse, so "remove" = XOR again). O(C(N,K)) total work, each step O(1).

2. If K > N/2, let M = N−K < N/2. Choosing K elements to include = choosing M elements to exclude. If T = XOR of all elements, and X = XOR of excluded elements, then XOR of chosen = T ⊕ X (since chosen ⊕ excluded = T, XOR both sides by excluded). So enumerate all C(N,M) = C(N,K) ≤ 10^6 exclusion sets and maximize T ⊕ X.

3. Pitfalls:
   - Recursion depth: N up to 2×10^5, but recursion depth is bounded by min(K, N−K), which could still be large? No — if C(N,K) ≤ 10^6 with K ≤ N/2, then K is small (K ≤ ~20 for large N, since C(2×10^5, 20) is astronomically larger than 10^6... actually C(N,2) can be ≤ 10^6 only if N ≤ ~1414; for N = 2×10^5, K must be 1). Hmm, careful: if K ≤ N/2 and C(N,K) ≤ 10^6, K could be up to ~20 when N is small (e.g., N=30, K=7: C(30,7) ≈ 2×10^6, too big; N=25,K=6: 177100 OK). So recursion depth ≤ ~20ish in the worst case, but to be safe use iterative or set recursion limit / convert to iterative. Actually safest: implement DFS iteratively or just set sys.setrecursionlimit high — depth is at most min(K, N−K) which is small given the constraint. But edge case N=K (then M=0) — handle trivially.
   - A_i < 2^60, so use Python ints (arbitrary precision, fine).
   - Reading input fast: use sys.stdin.buffer.read().
   - Time: 10^6 combinations with O(1) update each — Python should handle this within ~1-2 seconds if written tightly (avoid function call overhead where possible; a recursive DFS in Python for 10^6 leaf nodes plus internal nodes ~2×10^6 calls might be ~2-4s; consider iterative enumeration or Gosper's hack-style iteration for combinations to reduce overhead). Actually a well-written recursive combination generator in Python doing ~2×10^6 calls is borderline but typically OK (~2-3s). Alternative: iterative index-array combination enumeration (standard "next combination" loop) which is also ~10^6 iterations with inner while loops — comparable. Either is fine; keep the inner loop minimal.

4. Edge cases: K=0 not possible (K≥1). K=N → answer is total XOR. N−K=0 handled by the M-side enumeration with M=0 (single empty exclusion set).

## worker: Write the complete Python solution: fast input par
- **Approach**: Since C(N,K) ≤ 10⁶, enumerate combinations of the smaller side:
  - If K ≤ N−K: enumerate all K-subsets directly; candidate = running XOR.
  - If K > N−K: enumerate all (N−K)-subsets to *exclude*; candidate = total_xor ⊕ excluded_xor (valid because chosen ⊕ excluded = total, and XOR is self-inverse).
- **Enumeration**: Iterative "next combination" with an index array. The running XOR is maintained by XOR-ing out old elements and XOR-ing in new ones (XOR is its own inverse, so removal = XOR again). Each transition costs O(number of changed positions), amortized O(1) per combination.
- **Edge cases**: r = 0 (i.e., K = N) prints total XOR directly. K = 1 works (r = 1, enumerates singletons). A_i < 2⁶⁰ fits Python ints natively.
- **Complexity**: O(C(N,K)) time, O(N) memory. With ≤ 10⁶ combinations and tight inner loops, runs comfortably in Python.
- Verified logic against Sample 1 mentally: subsets of size 2 from (3,2,6,4) give max 3⊕4 = 7. ✓

## worker: Verify correctness on edge cases: K=N (r=0), K=1, 
**Verification of the requested edge cases:**

1. **K = N (r = 0):** Handled by the early return. Since `k > n - k` becomes `n > 0` (true), we enter exclude mode with `r = 0` and print `total` (the XOR of all elements), which is the only possible choice. ✓

2. **K = 1:** If `n > 1`, then `k=1 ≤ n-k` (for n≥2), so we enter include mode with `r=1`. The enumeration loop starts with `idx=[0]`, `cur=a[0]`. The while loop increments `idx[0]` through `n-1`, updating `cur` by XOR-ing out the old element and XOR-ing in the new one. This correctly checks all singletons and finds max(A_i). If `n=1, k=1`, then `r=0` and we print `total = a[0]`. ✓

3. **Duplicates in A:** The algorithm treats elements by index, not by value. When the running XOR updates (`cur ^= a[old]; cur ^= a[new]`), it correctly handles cases where `a[old] == a[new]` (the two XORs cancel, leaving `cur` unchanged) or where duplicate values appear at different indices. Since we enumerate index combinations, all C(N,K) index subsets are considered regardless of value duplicates. ✓

4. **Large values near 2^60:** Python integers have arbitrary precision, so values up to 2^60−1 (and their XORs, which stay below 2^60) are handled natively without overflow. The `best = -1` initialization is safe because all XOR results are non-negative, so any valid candidate (≥0) will be greater than −1. ✓

**Correctness of the complement trick:** When `k > n/2`, we enumerate `r = n−k` elements to exclude. If `T` is the total XOR and `X` is the XOR of excluded elements, the XOR of the chosen `k` elements is `T ⊕ X` (since `chosen ⊕ excluded = T` implies `chosen = T ⊕ excluded` by XOR-ing both sides with `excluded`). This is exactly what `base ^ cur` computes. ✓

**Complexity:** The enumeration visits each of the C(N,K) ≤ 10^6 combinations exactly once. The inner `for` loop that resets the tail runs in O(r) per combination in the worst case, but amortized analysis shows O(1) per combination (standard combinatorial generation). Given the 10^6 constraint, this runs well within time limits in Python.
