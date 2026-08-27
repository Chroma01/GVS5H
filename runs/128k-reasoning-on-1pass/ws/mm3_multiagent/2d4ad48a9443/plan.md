We need to count subarrays that can be made non‑decreasing with at most `k` total increment operations (each operation adds 1 to any element).  
For a subarray `nums[l..r]`, the minimal number of operations required is the sum of deficits when raising each element to the maximum of the prefix up to that element:

\[
\text{cost}(l,r)=\sum_{i=l}^{r}\bigl(\max(l..i)-\text{nums}[i]\bigr).
\]

We must count pairs \((l,r)\) with \(\text{cost}(l,r)\le k\).

A divide‑and‑conquer approach handles subarrays that cross a middle index `m` efficiently.  
For the right part we precompute the suffix maximums and decompose them into constant‑value segments. For any threshold `A` and right endpoint `j` we can compute

\[
g(A,j)=\sum_{t=m+1}^{j}\max\bigl(A,\text{suffix\_max}[t]\bigr)-\sum_{t=m+1}^{j}\text{nums}[t]
\]

in \(O(\log n)\) using binary search on the segment values.  
For the left part we similarly precompute, in reverse, the data needed to obtain `left_max[i]` and `left_cost[i]` (the cost of the subarray \([i,m]\)) for all `i` in the left half.

While processing the left endpoints from `m` down to `l` we maintain a pointer `j` (the furthest right index still satisfying the condition). Because `g(A,j)` is monotone in `j` and the allowed `K=k-left_cost[i]` decreases as `i` moves left, `j` only moves leftwards, giving an overall `O(n\log^2 n)` algorithm.