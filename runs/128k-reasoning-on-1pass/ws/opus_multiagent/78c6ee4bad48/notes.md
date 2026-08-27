
## ideation
**Core reduction (verified).** Let the sorted positions be p_1<…<p_N and gaps d_k = p_{k+1}−p_k (k = 1..N−1).
For an operation at i: M = (p_i+p_{i+3})/2, and
- p_{i+1} → p_i+p_{i+3}−p_{i+1} = p_i + (b+c)
- p_{i+2} → p_i+p_{i+3}−p_{i+2} = p_i + c

where (a,b,c) = (d_i, d_{i+1}, d_{i+2}). The four points become p_i, p_i+c, p_i+b+c, p_i+a+b+c, i.e. the gap triple (a,b,c) → (c,b,a). So **one operation = swap d_i ↔ d_{i+2}**, everything else fixed. Note p_i and p_{i+3} don't move, positions stay integers (even though M may be half-integer), and gaps stay positive → distinctness automatic.

**Reachable set.** Swapping indices at distance 2 = adjacent transpositions inside the odd-index list (1,3,5,…) and inside the even-index list (2,4,6,…). These generate the full symmetric group on each parity class, and nothing mixes parities (parity of index is invariant). So reachable configurations = arbitrary permutation of the odd-indexed gaps among odd positions and of even-indexed gaps among even positions. X_1 (and X_N) are invariant.

**Objective.** Σ_j p_j = N·X_1 + Σ_{k=1}^{N−1} (N−k)·d_k. Weight w_k = N−k is strictly decreasing in k. Within one parity class, we permute its multiset of gaps against its weight list; by the rearrangement inequality the minimum of the dot product pairs the largest gap with the smallest weight, i.e. **sort each parity class's gaps ascending and place them in increasing index order** (since increasing index ⇒ decreasing weight).

**Answer formula.** ans = N·X_1 + Σ_{parity classes} Σ_t (sorted-ascending gap)_t · (weight at t-th index of that class, indices ascending).

**Sanity checks.**
- Sample 1: N=4, d=(4,2,3), w=(3,2,1). Odd {1,3}: gaps {4,3}→(3,4)·(3,1)=13. Even {2}: 2·2=4. Total 4·1+17=21 ✓.
- Sample 2: N=6, d=(1,5,4,4,2), w=(5,4,3,2,1). Odd {1,3,5}: (1,2,4)·(5,3,1)=15. Even {2,4}: (4,5)·(4,2)=26. Total 0+41=41 ✓.

**Pitfalls.**
- Don't confuse "sort descending" direction: largest gaps must go to the *rightmost* indices of their parity class.
- Parity classes use gap index k (1-based), not the piece index; with 0-based arrays the parity flips — be careful.
- Values: X up to 1e12, weights up to 2e5 ⇒ sum up to ~2e17·… fits in Python int (no overflow issue), but must not use floats anywhere (midpoint is half-integer — never compute it explicitly).
- Need fast input: `sys.stdin.buffer.read().split()`; N up to 2e5 so O(N log N) sorting is trivial.
- Input already guaranteed sorted ascending (X_1<…<X_N), so no pre-sorting needed, but sorting cheaply is harmless.
- Output as integer (no floats, no scientific notation).

## worker: *Implement the solution:** read N and X with `sys.
Implemented exactly the planned formula:
- One operation at index i maps gap triple (d_i, d_{i+1}, d_{i+2}) → (d_{i+2}, d_{i+1}, d_i), i.e. swaps gaps at indices differing by 2, leaving X_1 fixed. These generate all permutations within each parity class of gap indices, and nothing more.
- Sum of coordinates = N·X_1 + Σ_{k=1}^{N-1} (N−k)·d_k, weights strictly decreasing in k. By the rearrangement inequality, minimize each parity class independently by pairing largest gaps with smallest weights ⇒ sort each class ascending and place them in increasing index order.
- Verified against both samples by hand (21 and 41) as noted in the plan.
- Pure integer arithmetic, fast buffered input, O(N log N).
