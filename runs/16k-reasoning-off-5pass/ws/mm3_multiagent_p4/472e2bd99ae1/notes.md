
## ideation
The problem asks for the K-th largest value among N^3 expressions of the form `A_i*B_j + B_j*C_k + C_k*A_i` for indices i, j, k in [1, N]. Constraints: N up to 2e5, K up to min(N^3, 5e5). Sequences contain positive integers up to 1e9.

Key observations:
- If we sort A, B, C in descending order, the expression value is non-increasing in each index. That is, for any (i,j,k) and any (i' >= i, j' >= j, k' >= k), the value at (i,j,k) is >= the value at (i',j',k').
- This monotonicity allows a best-first search on the lattice of (i,j,k) using a max-heap, starting from (0,0,0) and expanding neighbors (i+1,j,k), (i,j+1,k), (i,j,k+1). A visited set prevents duplicate states.
- Each pop yields the next largest value; we pop K times to get the K-th largest. The total number of pushes is at most 3K, so heap size and visited set are O(K), giving O(K log K) time.

Pitfalls:
- Values can be up to ~3e18, so Python's arbitrary precision integers are needed.
- N^3 can be 8e15, so visited set must use encoded integers (e.g., key = i*N^2 + j*N + k) to save memory.
- Ensure we push only within bounds and track visited correctly to avoid duplicate heap entries.

## worker: Implement the solution: read N, K, arrays A, B, C;
- The algorithm leverages the monotonicity of the expression when sequences are sorted in descending order: increasing any index (i, j, or k) can only decrease or keep the value.
- A max-heap (implemented via `heapq` with negative values) performs a best-first search on the lattice of indices, starting from the maximum at (0,0,0).
- Each popped state yields the next largest value; after K pops, the last popped value is the K-th largest.
- A visited set encoded as a single integer (`i*N^2 + j*N + k`) avoids storing large tuples, reducing memory usage.
- The total number of heap operations is O(K), each taking O(log K) time, so the overall complexity is O(K log K), which fits the constraints (K ≤ 5×10⁵).
- The code handles large values using Python's arbitrary precision integers, and bounds checks ensure we only generate valid neighbors.
