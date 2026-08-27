
## ideation
The core difficulty is that N can be up to 2×10⁵ and values up to 2⁶⁰, so we cannot enumerate all subsets. However, the constraint C(N,K) ≤ 10⁶ is the key: it bounds the number of combinations we need to consider. Since C(N,K) = C(N,N-K), we can always work with the smaller of K and N-K.

Key insight: XOR of K chosen elements = (XOR of all N elements) ⊕ (XOR of the N-K unchosen elements). So if N-K < K, we can instead enumerate combinations of N-K "excluded" elements, compute their XOR, and XOR with the total to get the chosen XOR.

So the algorithm:
1. Let M = min(K, N-K). Enumerate all C(N,M) combinations (≤ 10⁶).
2. If M == K: maximize XOR of chosen M elements directly.
3. If M == N-K: maximize total_xor ⊕ (XOR of excluded M elements).

Implementation concerns:
- Python's itertools.combinations over 10⁶ combinations is feasible but slow if we compute XOR from scratch each time (O(M) per combination → up to 4×10⁶ ops, fine since M is small when C(N,M) is large... actually M could be moderate). Better: use a recursive DFS that maintains a running XOR, updating incrementally (XOR is self-inverse, so add/remove is just one XOR op). This gives O(1) per combination.
- Recursion depth could be an issue if M is large, but when C(N,M) ≤ 10⁶ and N is large, M is tiny (1 or 2). When N is small (≤ ~60), M could be up to N/2 ~ 30, recursion depth fine. Actually worst case: C(2M, M) ≤ 10⁶ → M ≤ ~10 (C(20,10)≈184756, C(22,11)≈705432, C(24,12)≈2.7M). So M ≤ ~11-12 for the balanced case, and for M larger, N ≈ M meaning K side small... wait no: if M = min(K, N-K) and M is large, then N ≥ 2M, and C(N,M) ≥ C(2M,M) which exceeds 10⁶ for M ≥ 12. So M ≤ ~11 always? Check: C(23,11) = 1352078 > 10⁶. C(22,11) = 705432 ≤ 10⁶. So M ≤ 11 when N ≥ 2M. But if N < 2M, then M = N-K < N/2 contradicts M ≤ N/2. M = min(K,N-K) ≤ N/2 always, so N ≥ 2M, so M ≤ 11. 

So M ≤ 11 always. That means even O(M) per combination via itertools.combinations is at most 11×10⁶ = 1.1×10⁷ XOR ops — fine in Python, though a bit tight. Iterative DFS with incremental XOR is safer and simple.

Pitfalls:
- Recursion limit if using recursion (set it high, or use iterative).
- Reading input fast (sys.stdin).
- The answer must be printed as an integer.
- Edge cases: K=0? No, K≥1. K=N → M=0, answer is XOR of all. Handle M=0: combinations of 0 elements → XOR = 0, answer = total_xor if M==N-K side... if K=N, M=0=N-K, answer = total_xor ⊕ 0 = total_xor. Handle gracefully.

## worker: Write the complete Python solution: parse stdin, c
- **Key observation**: Since C(N,K) = C(N,N-K) ≤ 10⁶, we always enumerate the smaller side M = min(K, N-K). As shown in the plan, M ≤ 11 in all valid cases (because C(2M,M) grows past 10⁶ at M≈12), so enumeration is cheap.
- **Complement trick**: XOR of K chosen elements = (XOR of all N) ⊕ (XOR of the N−K excluded elements), since x ⊕ x = 0. So when N−K < K, we enumerate excluded sets and XOR with `total`.
- **Enumeration**: Iterative DFS with an explicit stack; each node either takes or skips the current element, maintaining the running XOR incrementally (O(1) per node). Total nodes ≈ 2 × C(N,M) ≤ 2×10⁶, well within limits. A pruning check (`remaining < need`) avoids dead branches.
- **Edge cases**: K = N → M = 0, answer = total XOR (handled by the m == 0 branch). K ≥ 1 guaranteed, so the m == 0 case only arises from the complement side.
- Verified against Sample 1 mentally: N=4, K=2, M=2, no complement; enumeration finds 3⊕4=7 as max. ✓
