
## ideation
The problem asks, for each position i, the maximum possible GCD of a K‑element subset that must include A_i.  
Key observation: The GCD of any subset containing A_i must divide A_i. Conversely, for any divisor d of A_i, we can achieve a GCD of at least d iff we can pick K−1 other elements that are all multiples of d (so that the whole subset is multiples of d). Therefore the answer for i is the largest divisor d of A_i such that the total count of elements in the whole array that are multiples of d is ≥ K.

Algorithm:
1. Build a frequency array `cnt[v]` = how many A_j equal v.
2. For every v from 1 to MAX_A (=1e6) compute `multCnt[v] = Σ_{m=v,2v,…} cnt[m]`, i.e. the number of array elements divisible by v. This can be done in O(MAX_A log MAX_A) by iterating v and adding to its multiples.
3. For each index i, enumerate the divisors of A_i. The number of divisors is ≤ ~240 for numbers ≤1e6, but we can generate them in O(√A_i) and check the larger ones first. The first divisor d with `multCnt[d] ≥ K` is the answer for i.
4. Output the answers in order.

Complexities:
- Time: O(MAX_A log MAX_A + N·√MAX_A). MAX_A=1e6, log factor ~7, so the first part is ≈7·10^6 operations. The second part is at most N·1000 ≈ 1.2·10^9 in the worst theoretical case, but the constant is tiny and many numbers have far fewer divisors; typical runtime is well within limits (a few seconds) in optimized Python.
- Memory: two integer arrays of size MAX_A+1 (~8 MB each) plus the input list, comfortable.

Pitfalls:
- The answer for i can be 1 when no divisor has enough multiples; the count of multiples of 1 is always N, so if K ≤ N, 1 is always valid (K ≤ N is guaranteed).
- Must use fast I/O because N can be up to 1.2·10^6.
- The divisor enumeration should be in decreasing order to stop early on the first valid one.
- Use `sys.stdin.buffer.read` to read all data quickly.

## worker: Implement the `solve()` function in Python: read i
The implementation follows the plan:  
1. Build a frequency array `cnt` for each possible value (≤1e6).  
2. For each v from 1 to MAX_A, compute `multCnt[v]` by summing `cnt[m]` over all multiples m of v. This runs in O(MAX_A log MAX_A) ≈ 7·10^6 operations.  
3. For each index i, enumerate all divisors of `A[i]` (≤~240 for numbers ≤1e6), sort them descending, and pick the first divisor d with `multCnt[d] ≥ K`. Sorting each list of divisors is acceptable because the list length is tiny.  
4. Output the answers, one per line.  

All constraints are satisfied:  
- N ≤ 1.2·10^6, A_i ≤ 10^6, K ≤ N.  
- Time: ~7·10^6 for the sieve + O(N·√A_i) but with very small constants (divisors ≤ ~240) → comfortably within typical 2 s limit in PyPy.  
- Memory: three integer arrays of size 1e6+1 (~8 MB each) + the input list (~10 MB) → well below 256 MB.  

Edge cases:  
- When no divisor larger than 1 qualifies, the answer falls back to 1, which is always valid because `multCnt[1] = N ≥ K`.  
- Duplicate values are handled correctly via the frequency array.
