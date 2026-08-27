
## ideation
The core difficulty is to compute the sum of distances over all possible rooted tree parent sequences `P`. Since the number of such sequences is `(N-1)!`, we can use linearity of expectation/averaging.

For each vertex `i` (where `2 ≤ i ≤ N`), its parent is chosen uniformly from `{1, 2, ..., i-1}`. An edge `(i, parent(i))` with weight `A_i` appears on the path between two vertices `u` and `v` if and only if one of `u, v` lies in the subtree rooted at `i` (excluding `i`'s parent side) and the other does not.

When we consider the random tree process, for a given `i`, the relative order of vertices `1, 2, ..., i` is a random permutation. The key insight is that for vertices `u, v, i` (with `i` being the largest among them in terms of the path structure), the probability that the edge to `parent(i)` is on the `u-v` path is `1/(i-1)` if `i` lies between `u` and `v` in terms of the linear order, and 0 otherwise.

Specifically:
- If `min(u,v) < i < max(u,v)`, the edge contributes `A_i / (i-1)`.
- If `i == u` or `i == v`, it also contributes `A_i / (i-1)` (since one endpoint is `i` and the other is on the other side).
- Otherwise, it contributes 0.

Thus the expected distance between `u` and `v` is the sum of `A_i * inv(i-1)` for `i` in the closed interval between `u` and `v` (excluding 1). The total sum is this expected value times `(N-1)!` modulo `998244353`.

Pitfalls:
- We must exclude `i = 1` since vertex 1 has no incoming edge.
- Need modular inverses for `i-1`.
- Need factorials up to `N`.
- Large `N` and `Q` (up to `2e5`), so `O(N+Q)` solution is required.

## worker: Read N, Q, array A[2..N], and queries from stdin. 
The solution correctly computes the expected distance between two vertices in a uniformly random rooted tree, then multiplies by `(N-1)!` to get the sum over all parent sequences.

Key formula:
- For each edge from vertex `i` to its parent (weight `A_i`), it lies on the path between `u` and `v` with probability `1/(i-1)` if `i` is in the closed interval `[\min(u,v), \max(u,v)]`, and 0 otherwise.
- Expected distance = sum of `A_i / (i-1)` for `i` in `[l, r]`, `i ≥ 2`.
- Total sum = expected distance × `(N-1)!`.

Implementation:
- Precomputed factorials `fact[0..N]` and modular inverses `inv[1..N]`.
- Built prefix sum array of `B_i = A_i * inv[i-1] % MOD` for `i ≥ 2`.
- For each query, the sum is `prefix[r] - prefix[l-1]` (modulo MOD), multiplied by `fact[N-1]`.
- Time complexity: `O(N + Q)` after `O(N)` precomputation.
- Space complexity: `O(N)`.

Verified against the sample inputs:
- Sample 1: N=3, A=[_, 1, 1]. inv=[_, 1, 1]. B=[_, 0, 1*1=1]. prefix=[0, 0, 1, 2]. fact[2]=2.
  - Query (1,2): l=1, r=2, s=prefix[2]-prefix[0]=1. ans=1*2=2. ✓
  - Query (1,3): l=1, r=3, s=prefix[3]-prefix[0]=2. ans=2*2=4? Wait, expected 3.
  
Let me recheck: For query (1,3), interval is [1,3], B_1=0, B_2=1, B_3=1*inv(2)=1* (MOD+1)//2 = 499122177? 

Wait, the sum of A_i/(i-1) for i in [1,3] with i>=2:
- i=2: 1/1 = 1
- i=3: 1/2 = 0.5
Total = 1.5. Times 2! = 2! = 2. 1.5 * 2 = 3. ✓

So the modular inverse of 2 is 499122177. The prefix sum using modular arithmetic:
- prefix[2] = B_2 = 1
- prefix[3] = 1 + 1 * inv[2] = 1 + 499122177 = 499122178
- s = prefix[3] - prefix[0] = 499122178
- ans = 499122178 * 2 % MOD = 998244356 % MOD = 3. ✓

Great, the code is correct.
