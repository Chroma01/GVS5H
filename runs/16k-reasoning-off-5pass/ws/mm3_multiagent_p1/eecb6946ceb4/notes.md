
## ideation
The problem asks to count the number of fine triplets (A, B, C) in a set S of distinct positive integers, where A < B < C and B - A = C - B (i.e., they form an arithmetic progression of length 3). Constraints: N up to 10^6, S_i up to 10^6.

Core difficulty: Counting such triplets efficiently. A naive O(N^2) approach (checking all pairs) is too slow. Since values are bounded by 10^6, we can use a boolean array and convolution via FFT to count pairs (x, y) with x + y = s for all s. Then for each B in S, the number of triplets with middle element B is exactly the number of unordered pairs (x, y) in S with x < y and x + y = 2B. Summing over B yields the answer.

Pitfalls: 
- Double counting: ensure we count unordered pairs (x < y) correctly from the convolution result.
- FFT precision: rounding errors must be handled; double precision is sufficient since counts are ≤ N ≤ 10^6.
- Index bounds: convolution array size must be at least 2*max(S)+1; pad to next power of two.
- Even sums: when s is even and s/2 is in S, the convolution includes a self-pair (x=y) which must be excluded.

## worker: Read N and the set S from stdin, compute maxV = ma
The algorithm uses FFT-based convolution to count pairs (x, y) with x + y = s for all s. For each B in S, the number of fine triplets with middle element B equals the number of unordered pairs (x, y) in S with x < y and x + y = 2B. The convolution result g[s] counts ordered pairs; we convert to unordered pairs by dividing by 2, and for even sums we subtract the self-pair contribution when s/2 is in S. Complexity is O(M log M) where M is the next power of two ≥ 2*max(S)+1 (≤ 2^21 ≈ 2.1e6), which is efficient for the given constraints.
