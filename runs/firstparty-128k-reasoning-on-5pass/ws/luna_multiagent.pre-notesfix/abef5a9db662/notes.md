
## ideation
The core difficulty is that each contest checks the rating reached so far, so the effect of a contest cannot be determined independently from the initial rating. Simulating all contests for every query is too slow.

The useful observation is that the mapping from initial rating to current rating is monotone nondecreasing. If the current mapping is represented as an array \(f(x)\), contest \([L,R]\) increments exactly those entries whose values lie in \([L,R]\). Because \(f\) is monotone, those entries form one contiguous range of initial ratings. Thus each contest becomes a range-add operation on the domain of initial ratings.

A segment tree can maintain the values \(f(x)\), support range addition, and locate the first and last indices whose current values lie within a given interval. Since the values remain monotone, boundary searches are valid. The initial array is \(f(x)=x\), and only initial ratings up to \(5\times 10^5\) are needed for queries. After processing all contests, each query is answered by retrieving the corresponding point value. This gives \(O((N+Q)\log V)\) time and \(O(V)\) memory, where \(V=5\times 10^5\).

Care is needed with inclusive interval endpoints, lazy propagation during boundary searches, and the fact that a contest may affect no initial ratings. The final rating can exceed \(5\times 10^5\), but the segment tree’s stored values should allow for additions up to \(N\).

## worker: Implement and verify a lazy segment tree over init
Maintains the monotone function mapping each initial rating to its current rating. For every contest, the initial ratings whose current values lie in `[L, R]` form a contiguous interval, found using segment-tree searches on minimum and maximum values. That interval is then incremented with lazy propagation.

Complexity is `O((N + Q) log V)` with `V = 500000`, and memory usage is `O(V)`.
