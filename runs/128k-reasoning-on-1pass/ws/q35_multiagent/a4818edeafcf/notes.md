
## ideation
The problem requires finding the maximum sum of distinct elements in three subarrays formed by splitting the array at two positions. This can be modeled as maximizing $Pre[i] + D(i+1, j) + Suf[j+1]$ for $1 \le i < j \le N-1$.
We can iterate over the split point $j$ (end of the middle subarray) and maintain the value $Val(i) = Pre[i] + D(i+1, j)$ for all valid $i < j$.
As $j$ increases to $j+1$, the middle subarray extends to include $A[j+1]$. The distinct count $D(i+1, j+1)$ increases by 1 if $A[j+1]$ is not present in $A[i+1..j]$, which corresponds to indices $i \ge Last[A[j+1]]$.
This allows us to use a Segment Tree to maintain $Val(i)$ values, supporting range addition (when $A[j+1]$ is new for a range of $i$) and point updates (when a new $i$ becomes valid), along with range maximum queries.
The algorithm runs in $O(N \log N)$ time, which fits within the constraints. Optimizations include using arrays instead of sets for distinct counting and fast I/O.

## worker: (none)
The problem requires maximizing the sum of distinct elements in three subarrays formed by two split points. We iterate over the end of the middle subarray $y$ and maintain the maximum value of $Pre[x] + D(x+1, y)$ for all valid $x < y$ using a segment tree. As $y$ increases, the middle subarray extends, and the distinct count increases by 1 for ranges of $x$ where the new element $A[y]$ is not already present. This corresponds to a range add operation on the segment tree. We also add new valid split points $x=y-1$ with their initial values. The algorithm runs in $O(N \log N)$ time due to segment tree operations, which fits within the constraints.
