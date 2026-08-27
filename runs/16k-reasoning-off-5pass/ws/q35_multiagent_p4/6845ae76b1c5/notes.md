
## ideation
The core difficulty is efficiently computing the sum of absolute differences for multiple queries where each query considers prefixes of two sorted arrays. A naive $O(N^2)$ per query is too slow. The key insight is that since we only consider prefixes $A[1..X_k]$ and $B[1..Y_k]$, and these subarrays are sorted (if the original arrays are sorted), we can use a two-pointer approach or binary search with prefix sums.

However, the constraints ($N=10^5, K=10^4$) mean that an $O(N)$ per query solution results in $10^9$ operations, which is too slow for Python. We need a faster approach.

Actually, let's re-evaluate the complexity. If we sort A and B once ($O(N \log N)$), then for each query $(X_k, Y_k)$, we can compute the answer in $O(X_k + Y_k)$ using two pointers. In the worst case, this is $O(K \cdot N) = 10^9$, which is borderline. But note that we can optimize further.

Wait, there's a better way: For each query, we can compute the contribution of each $A_i$ ($1 \le i \le X_k$) by finding how many $B_j$ ($1 \le j \le Y_k$) are less than or equal to $A_i$. Using binary search (`bisect_right`) on the prefix $B[1..Y_k]$, we can find the split point in $O(\log Y_k)$. Then, using precomputed prefix sums of B, we can compute the sum of absolute differences for that $A_i$ in $O(1)$. This gives $O(X_k \log Y_k)$ per query. Total complexity: $O(\sum X_k \log Y_k)$. In the worst case, this is $O(K \cdot N \log N) \approx 10^4 \cdot 10^5 \cdot 17 \approx 1.7 \cdot 10^{10}$, which is too slow.

But here's the catch: we can swap the roles. If $X_k$ is large and $Y_k$ is small, we iterate over B. If $Y_k$ is large and $X_k$ is small, we iterate over A. We can choose to iterate over the smaller dimension. So for each query, we iterate over $\min(X_k, Y_k)$ elements, and for each, do a binary search on the other array's prefix. This gives $O(\min(X_k, Y_k) \cdot \log(\max(X_k, Y_k)))$ per query. In the worst case, if $X_k = Y_k = N/2$, this is $O(N \log N)$ per query, total $O(K \cdot N \log N)$, still too slow.

Actually, there's a known linear-time method for two sorted arrays using two pointers. Let's implement that. For each query, we use two pointers to traverse $A[1..X_k]$ and $B[1..Y_k]$ simultaneously. This is $O(X_k + Y_k)$ per query. Total worst-case $O(K \cdot N) = 10^9$. In Python, this might be too slow, but let's try to optimize with efficient code.

Alternatively, we can precompute for each possible split point. But that's not feasible.

Let's go with the two-pointer approach for each query, as it's the most straightforward and likely the intended solution. We'll sort A and B, precompute prefix sums, and for each query, use two pointers to compute the sum.

## worker: Sort arrays A and B, and compute prefix sums for b
The solution sorts arrays A and B and precomputes prefix sums. For each query (X_k, Y_k), it iterates over the first X_k elements of sorted A and for each element, uses binary search (`bisect_right`) to find how many of the first Y_k elements of sorted B are less than or equal to it. Using the prefix sums of B, it efficiently computes the contribution of each A_i to the total sum of absolute differences. The complexity per query is O(X_k log Y_k), and total complexity is O(N log N + K * N log N) in the worst case. Given the constraints (N=10^5, K=10^4), this might be tight in Python, but it's the best approach without more complex precomputation.
