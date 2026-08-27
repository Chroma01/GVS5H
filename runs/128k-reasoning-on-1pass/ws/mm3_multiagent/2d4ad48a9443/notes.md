
## ideation
The problem requires counting subarrays that can be made non‑decreasing with at most `k` total increment operations.  
For a subarray `nums[l..r]`, the minimal number of operations needed is  

\[
\text{cost}(l,r)=\sum_{i=l}^{r}\bigl(\max(l..i)-\text{nums}[i]\bigr),
\]

where `max(l..i)` is the maximum of the original values in the prefix up to `i`.  
We need to count pairs `(l,r)` with `cost(l,r) ≤ k`.

A divide‑and‑conquer (D&C) approach works in `O(n log² n)`:

1. Recursively count subarrays completely in the left half and right half.
2. Count subarrays that cross the middle index `m` (left endpoint in `[L..m]`, right endpoint in `[m+1..R]`).

For the crossing part:
* Precompute for the left half (scanning from `m` down to `L`) the values  
  `left_max[i] = max(nums[i..m])` and `left_cost[i] = cost(i,m)` using a stack of “constant‑max” segments.  
  This is done in `O(m-L+1)` amortized time.
* Precompute for the right half the “prefix‑max” segments (values where the running maximum changes).  
  With these segments and a prefix sum of `nums`, we can compute  

  \[
  g(A,j)=\sum_{t=m+1}^{j}\max(A,\text{prefix\_max}[t])-\sum_{t=m+1}^{j}\text{nums}[t]
  \]

  in `O(log n)` using binary search on the segment values.
* While iterating `i` from `m` down to `L`, maintain a pointer `j` (the farthest right index still satisfying the condition).  
  Because both `left_cost[i]` and `left_max[i]` increase (or stay) as `i` moves left, the feasible `j` never increases, so `j` only moves leftwards.  
  Each `i` triggers at most one `g` evaluation to check the condition; total work per D&C level is `O(n log n)`.

The recursion depth is `O(log n)`, giving overall `O(n log² n)` time and `O(n)` extra memory.

## worker: Build a segment decomposition (constant‑value runs
The solution uses a divide‑and‑conquer approach to count subarrays whose minimal cost to become non‑decreasing does not exceed `k`.  
The cost for a subarray `nums[l..r]` is `∑(max(l..i) - nums[i])`.  
For crossing subarrays (`l` in left half, `r` in right half) we precompute:

* **Left side**: as we extend leftwards, we maintain a stack of “constant‑max” segments. This allows O(1) update of `left_max[i]` and `left_cost[i]`.
* **Right side**: we build a segment decomposition of the suffix‑max array (prefix‑max of the right half). With prefix sums over these segments we can compute  
  `g(A, j) = ∑_{t=m+1}^{j} max(A, suffix_max[t]) - ∑_{t=m+1}^{j} nums[t]`  
  in `O(log n)` using binary search on the segment values.

A two‑pointer technique then iterates `i` from `m` down to `l`, keeping a pointer `j` that never moves right, so the total work per level is `O(n log n)`. With `O(log n)` recursion levels the overall time is `O(n log² n)` and memory `O(n)`.

The algorithm was tested on the provided examples and small edge cases (single elements, decreasing/increasing arrays) and produces the expected results.
