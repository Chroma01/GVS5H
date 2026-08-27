
## ideation
We need to compute the sum of `f(L,R)` over all subarrays, where `f(L,R)` is the minimum number of interval‑deletions needed to erase all numbers in the subarray.

**Key observation**  
For a subarray, let `S` be the set of distinct values in it.  
An operation can erase any integer interval `[l,r]` whose every integer appears at least once in the current multiset.  
Thus in one operation we can delete all occurrences of a whole *consecutive* block of integers.  
The optimal strategy is to delete each maximal consecutive block of values in `S` separately, and these blocks are exactly the connected components of the graph where vertices are the values in `S` and edges connect `v` and `v+1` when both are present.

Hence  
`f(L,R) = (#distinct values in [L,R]) - (#pairs (v,v+1) both present in [L,R])`.  

Let `C(L,R) = #distinct values` and `J(L,R) = #adjacent pairs both present`.  
We need `Σ (C - J) = Σ C - Σ J`.

**Counting Σ C**  
For each value `v`, the number of subarrays containing `v` is `total - missing_v`, where `total = N(N+1)/2` and `missing_v` is the number of subarrays that contain no `v`.  
If the positions of `v` are `p1 < p2 < … < pk`, the gaps where `v` is absent are intervals of lengths  
`g0 = p1-1, gj = p_{j+1}-p_j-1, gk = N-p_k`.  
A subarray missing `v` must lie completely inside one gap, so  
`missing_v = Σ C(g+1, 2) = Σ g*(g+1)/2`.  

`Σ C = Σ_v (total - missing_v)`.  
We can compute `missing_v` for all `v` in `O(N)` by scanning each value’s position list once.

**Counting Σ J**  
For each pair `v` and `v+1` (1 ≤ v < N), let `J_v` be the number of subarrays containing both values.  
Using inclusion–exclusion:

```
J_v = total - missing_v - missing_{v+1} + missing_both(v,v+1)
```

`missing_both(v,v+1)` counts subarrays containing neither `v` nor `v+1`.  
If we merge the sorted position lists of `v` and `v+1`, the gaps in the union are exactly the maximal index intervals with no `v` and no `v+1`.  
The same gap formula gives `missing_both = Σ C(g+1,2)` over those gaps.

**Total work**  
Each position `i` belongs to value `A_i`. This value appears in at most two adjacent pairs (`A_i-1, A_i`) and (`A_i, A_i+1`).  
Therefore the total size of all merged position lists over all `v` is `2N`.  
Processing every pair by a two‑pointer merge costs `O(|P|+|Q|)`, so the whole Σ J phase is `O(N)`.

Overall algorithm: `O(N)` time, `O(N)` memory.

**Edge Cases**  
- If a value never appears, `missing_v = total` and its contribution to Σ C is zero.  
- If one of the two lists in a pair is empty, `J_v = 0`.  
- Use 64‑bit integers (Python int is unbounded).  

**Verification on Sample 1** (N=4, A=[1,3,1,4]) gives 16, matching.

## worker: Implement the algorithm in Python: read N and A, b
- Derived `f(L,R) = (#distinct values) - (#adjacent pairs both present)`.
- Counted `Σ C` (distinct sum) using per‑value gaps: `missing[v] = Σ gap*(gap+1)/2`, contribution `total - missing[v]`.
- Counted `Σ J` (adjacent‑pair sum) by merging the two sorted position lists for each pair `(v, v+1)`. The total size of all merged lists is `2N`, giving `O(N)` time.
- Verified the three samples:
  - Sample 1 → 16
  - Sample 2 → 23
  - Sample 3 → 129
- Complexity: `O(N)` time, `O(N)` memory, works for `N ≤ 3·10⁵`.
