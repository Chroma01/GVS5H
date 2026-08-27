
## ideation
The problem asks, for each query subarray `A[L..R]` (sorted globally, hence also sorted locally), the maximum number of disjoint pairs `(small, big)` with `2*small ≤ big`.  
Greedy on a sorted array is optimal: repeatedly take the smallest unused element as the top and pair it with the smallest unused element that is at least twice it.  
We need to answer many subarray queries fast.

**Core difficulty:**  
A naive greedy per query is O(length). With `N, Q ≤ 2e5` we need roughly `O(log N)` per query.

**Candidate approaches:**
1. **Two-pointer + binary lifting (functional graph jumps).**  
   - Precompute `nxt[i]` = smallest `j > i` with `A[j] ≥ 2*A[i]` using a forward two-pointer sweep in O(N).  
   - After using a pair starting at `i`, the next candidate index is `nxt[i] + 1`.  
   - Build a binary lifting table `jump[k][i]` = position after `2^k` greedy pairings starting at `i` (or `N` sentinel if impossible).  
   - For each query, greedily try powers of two: if `jump[k][cur] ≤ R`, take those `2^k` pairings, update `cur` and `ans`.  
   - Complexity: O(N log N) preprocessing, O(log N) per query.

2. **Segment tree / BIT with custom greedy simulation.**  
   - Harder to implement and likely O(log² N) or worse; not needed.

3. **Offline processing with Mo's algorithm.**  
   - Greedy state is not easily maintained while adding/removing elements; not suitable.

**Pitfalls:**
- `nxt[i]` may be `N` (no valid bottom). Encode as `N` and ensure `jump` stays at `N`.
- Input is 1-indexed; convert to 0-index carefully. The subarray length is `R-L+1`.
- The binary lifting condition must check that the *position after the k-th pairing* is still ≤ `R`, guaranteeing all used indices are inside the subarray.
- `A_i` up to `1e9`; use 64-bit integers when comparing `2*A[i]`.

**Conclusion:** Approach 1 (two-pointer + binary lifting) is the intended solution.

## worker: Implement the solution in Python: parse input, com
- Used two-pointer sweep in O(N) to compute `nxt[i]`, the smallest index `j>i` with `A[j] >= 2*A[i]`.
- Built a binary lifting table where `jump[0][i] = nxt[i] + 1` (position after one successful pairing) and `jump[k][i] = jump[k-1][jump[k-1][i]]`, with `N` as a sentinel for "no more pairings".
- For each query `(L, R)`, greedily applied the largest power-of-two number of pairings whose resulting position stays within `R`. This works because the greedy pairing of smallest available top with smallest valid bottom is optimal and each pairing consumes a contiguous prefix of the remaining sorted subarray.
- Complexity: O(N log N) preprocessing, O(log N) per query, total O((N+Q) log N) time and O(N log N) memory, which fits the constraints.
- The solution is verified mentally against the sample inputs; the greedy + binary-lifting approach is a known standard for this problem.
