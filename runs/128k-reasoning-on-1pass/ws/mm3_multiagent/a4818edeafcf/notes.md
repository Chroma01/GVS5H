
## ideation


## worker: **Prefix & suffix distinct counts:** scan the arra
The algorithm uses two auxiliary arrays:
* `pref[i]` – number of distinct values in the prefix `A[0..i]`.
* `suff[i]` – number of distinct values in the suffix `A[i..N‑1]`.

For a fixed second split position `j` we need  
`max_{i<j} ( pref[i] + distinct(i+1..j) )`.  
Define `V[i] = pref[i] + distinct(i+1..j)`.  
When the middle subarray grows from `j-1` to `j` by appending `A[j]`,
`V[i]` increases by 1 exactly for those `i` with `i ≥ prev`,
where `prev` is the previous occurrence of `A[j]` (or `prev = -1` if none).

Thus we maintain `V[i]` with a segment tree that supports
*range addition* and *range maximum*.  
For each `j` we:
1. add +1 to the range `[prev, j-1]` (or `[0, j-1]` if `prev = -1`);
2. query the maximum on `[0, j-1]`;
3. combine it with `suff[j+1]` and keep the best answer.

The segment tree is built on the next power of two `size ≥ N`,
so updates and queries are `O(log N)`.  
Overall complexity is `O(N log N)` with `N ≤ 3·10⁵`, well within limits.
Memory usage is `O(N)` for the arrays and the segment tree.
