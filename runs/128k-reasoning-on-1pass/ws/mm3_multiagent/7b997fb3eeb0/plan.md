We need to answer for each query interval `[L,R]` the maximum number of disjoint pairs `(a,b)` with `a ≤ b/2`.  
Because the array is sorted, the optimal greedy matching pairs each element (as a “small”) with the earliest later element (as a “large”) that is at least twice as large.  

For each index `i`, let `nxt[i]` be the smallest `j>i` with `A[j] ≥ 2·A[i]` (or `N+1` if none).  
Define `d[i] = nxt[i] - i`.  

For a query `[L,R]` with length `M = R-L+1`, a matching of size `K` exists iff  
`max_{x∈[L, L+K-1]} d[x] ≤ M - K`.  
This condition is monotone in `K`, so we can binary search the largest feasible `K`.  

We preprocess `d[i]` and build a sparse table for range maximum queries on `d`.  
Each query is answered in `O(log N)` time (binary search with `O(1)` RMQ).