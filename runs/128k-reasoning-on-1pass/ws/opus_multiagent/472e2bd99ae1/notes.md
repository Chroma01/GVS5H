
## ideation
**Core structure.** f(i,j,k)=A_iB_j+B_jC_k+C_kA_i = A_iB_j + C_k(A_i+B_j). Since all values are ≥1 (strictly positive), f is strictly increasing in each of A_i, B_j, C_k separately (∂/∂A = B+C > 0, etc.). Hence after sorting A, B, C in **descending** order, f is non-increasing along each index coordinate: (i,j,k) ⪰ (i',j',k') componentwise ⇒ f(i,j,k) ≤ f(i',j',k'). This is exactly the classic "K largest sums over a monotone 3-D grid" setting, so a best-first heap search from (0,0,0) works.

**Why truncation to m = min(N,K) is safe.** If i ≥ K (0-indexed), then the K triples (0,j,k),(1,j,k),…,(K−1,j,k) all have value ≥ f(i,j,k), so f(i,j,k) can be excluded without changing the K-th largest *value* (ties are fine: we only need the value, and the multiset of the top K values is realizable inside the truncated grid). Same for j, k. With N ≤ 2·10⁵ and K ≤ 5·10⁵, usually m = N anyway, so truncation mostly matters when N ≫ K (impossible here) — it's harmless either way.

**Duplicate-avoidance rule (no visited set).** From (i,j,k):
- push (i+1,j,k) always (if in range),
- push (i,j+1,k) only if i == 0,
- push (i,j,k+1) only if i == 0 and j == 0.

Uniqueness argument: the canonical path to (i,j,k) is (0,0,0) → raise k to k → raise j to j → raise i to i; each state has exactly one legal parent, so each node is generated exactly once. Each parent dominates the child componentwise so parent value ≥ child value ⇒ pop order is non-increasing ⇒ K-th pop is the answer. This keeps heap size ≤ ~2K+1 entries and avoids a set of 1.5M tuples.

**Alternatives considered / rejected.**
- Binary search on answer + counting #{f ≥ X}: for fixed i, f is monotone in j and k so a staircase two-pointer counts in O(N) → O(N²) per check → 4·10¹⁰, too slow.
- Two-stage: top-K of pairs (i,j) then combine with C. Invalid in general because the ranking of pairs depends on C_k (value = p + C_k·s with p=A_iB_j, s=A_i+B_j); different k give different orders. Could still be done via a 2-D heap nested inside a 1-D merge, but the direct 3-D heap is simpler and equivalent.
- Sorting all N³ values: obviously impossible.

**Pitfalls / implementation cautions.**
1. Python heapq is a min-heap ⇒ push (−value, i, j, k).
2. Values up to 3·10¹⁸ — fine in Python, but note the sample answer ~6.9·10¹⁷ (needs 64-bit in other languages).
3. Performance: ≤5·10⁵ pops and ≤1.5·10⁶ pushes of 4-tuples. Should run in a few seconds; optimize with `from heapq import heappush, heappop` bound to locals, avoid function-call overhead, precompute A/B/C as local lists, possibly pack (i,j,k) into a single integer i*m*m+j*m+k (m ≤ 2·10⁵ ⇒ fits comfortably) to make tuples 2-long and comparisons cheap — but then need divmod on pop; measure/trade-off. Alternatively store `(-val, i, j, k)` and rely on the fact that ties compare ints (never errors).
4. Fast input: `sys.stdin.buffer.read().split()`.
5. Edge cases: N=1 (K must be 1), K=1, all equal values (ties, sample 2 → 30000), bounds checks i+1<m, j+1<m, k+1<m.
6. Don't forget descending sort (`sort(reverse=True)`).
7. Careful: pushing children only when in range; the canonical rule must still be applied *before* the range check (i.e., condition on i==0 / j==0 is on the *parent*).

## worker: Write the complete Python solution: fast input via
Implemented exactly the planned algorithm:

- **Monotonicity**: with all values ≥ 1, f(i,j,k)=A_iB_j+B_jC_k+C_kA_i is increasing in each of A_i, B_j, C_k. After descending sorts, f is non-increasing along each index coordinate, so a best-first search from (0,0,0) enumerates values in non-increasing order.
- **Truncation** to m = min(N,K) is safe: if an index exceeds K−1 in some coordinate, there are already ≥ K triples with value ≥ it. Also m³ ≥ K always holds (if m=N, N³ ≥ K by constraints; if m=K, K³ ≥ K), so K pops are always possible.
- **Canonical-parent expansion** avoids a visited set: from (i,j,k) push (i+1,j,k) always; (i,j+1,k) only if i==0; (i,j,k+1) only if i==0 and j==0. Each node (i,j,k) has exactly one legal parent (decrement i if i>0, else j if j>0, else k), so every node is generated exactly once; the parent dominates componentwise so its value is ≥ the child's, preserving the non-increasing pop order.
- **Performance**: indices are packed into a single integer idx = (i·m + j)·m + k (≤ ~8·10¹⁵, fine for Python ints) so heap items are 2-tuples with cheap comparisons; heap holds ≤ ~1.5·10⁶ entries for K = 5·10⁵. Input read in one shot; heappush/heappop bound to locals inside `main()`.
- Edge cases handled: N=1 (m=1, mm=1, no children pushed, K must be 1), K=1, all-equal values (ties compare ints, never errors).
