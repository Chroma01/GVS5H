
## ideation
The problem requires splitting an array into three contiguous non-empty parts to maximize the sum of distinct element counts in each part. With N up to 3e5, a naive O(N^2) enumeration of cut points is too slow. 

The key idea is to fix the right end of the middle subarray (index j) and efficiently find the best left cut i. We can precompute prefix distinct counts (pref) and suffix distinct counts (suf). For a fixed j, the right part's distinct count is fixed as suf[j+1]. We need to maximize pref[i] + distinct(i+1, j) over i < j.

We can maintain a segment tree over positions i (left cut candidates). Initially, each position i stores pref[i] (the distinct count of the left part when the middle segment is empty). As we advance j from 2 to N-1, we update the middle segment's distinct count. When adding element A[j] to the middle segment, it increases the distinct count for all left cuts i where A[j] hasn't appeared in the current middle segment. This happens exactly when i ≥ prev (where prev is the last occurrence of A[j] before j). So we perform a range add of 1 to the interval [max(prev, 0), j-1] in the segment tree. After each update, we query the maximum value over i=0..j-1 and add suf[j+1] to compute the candidate answer.

This approach runs in O(N log N) time, suitable for N=3e5.

Pitfalls:
- Ensure 0-indexing consistency.
- Handle the case when prev = -1 (element not seen before).
- Be careful with segment tree indices and lazy propagation.
- suf array needs to be computed for indices up to N (with suf[N]=0).

## worker: Implement the segment tree with lazy propagation s
The algorithm uses a segment tree to maintain for each possible left cut `i` the value `pref[i] + distinct(i+1, current_middle_end)`. As we iterate the middle cut `m` from 1 to N-2, we update the distinct count of the middle segment by adding 1 to all left cuts `i` where the new element `A[m]` was not already present in the middle segment. This condition is equivalent to `i ≥ prev` where `prev` is the last occurrence of `A[m]` before index `m`. We perform a range add on `[max(prev, 0), m-1]`. After each update, we query the maximum over all valid left cuts and add the precomputed suffix distinct count `suf[m+1]` to obtain the total distinct count for the current split. The maximum over all splits is the answer. The complexity is O(N log N) due to the segment tree operations.
