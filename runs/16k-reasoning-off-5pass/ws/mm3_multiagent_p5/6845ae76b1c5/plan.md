We need to answer many queries of the form: given a prefix length `x` of A and `y` of B, compute sum_{i≤x, j≤y} |A_i - B_j|. Straight O(N^2) is too slow.

Key idea: Sort copies of A and B while keeping original indices. For a query, the relevant elements are the ones among the first `x` A's (by original index) and first `y` B's. After sorting, we can use prefix sums of sorted values. However, the sets of A_i and B_j for a query are *intersections* of index prefixes and value orders — not contiguous in value order in general. So we cannot simply use sorted prefix sums.

Alternative: Use offline processing with BIT (Fenwick tree) over A indices. Sort queries by `Y_k`. Iterate over B elements in original order; when we include B_j, we add its contribution to all A_i. For each A_i, we need to know if it's selected (i ≤ x_k). Maintain a BIT keyed by A_i's value (compressed) that holds how many A_i's (with index ≤ current processed A's) have each value. When adding B_j, compute its contribution to the sum using two BITs: one for counts and one for value sums. The current total contribution from all processed B's to currently-eligible A's (with index ≤ x) is the answer for queries with this Y and matching X.

Algorithm:
- Read N, arrays A, B.
- Read K queries (X_k, Y_k).
- Sort queries by Y ascending.
- Use coordinate compression of A values (1..M).
- BIT `cnt` stores how many eligible A's have each compressed value; BIT `sumV` stores the sum of their original values.
- Initially empty.
- Use pointer `a_idx` = 1..N. We'll add A_i to BITs only when its index ≤ X_k for the current query. Since queries sorted by Y, for each Y we need the set of A's with index ≤ X_k. But X varies per query. So we need to add A_i's in order of index and keep them only while a query's X is larger.

Better: For each query, the eligible A's are indices 1..X_k. As Y grows, we just need the corresponding A-set for that query's X. So we can:
- Maintain pointer `ptr` over A indices. For each query (sorted by Y), advance `ptr` to X_k, adding A_ptr to BITs.
- Query the current sum over all A's in BIT: total = Σ |A_i - B_j| over all currently added A_i and all B_j processed so far. But we need the sum over B_j with index ≤ Y_k. Since we process B_j's in order: when moving to next Y, we add B's with index ≤ Y_k one by one, and for each new B_j, we compute its contribution to the current A-set and add to a running total `ans[query]`.

So we need to process both dimensions in order of Y and X. Let's do:
- Sort queries by Y.
- Have pointer `bj = 1..N` for B elements. Initially `bj=0`, `total=0`.
- Have BITs (count and sum) for A elements.
- Have pointer `ai = 0` for A elements.
- For each query in order of Y:
  - Advance `bj` from current to Y_k: for each new B_j, compute its contribution to the A-set currently in BITs, add to `total`.
  - Advance `ai` to X_k: add A_ai to BITs.
  - Now `total` equals sum over A_i (i≤X_k) and B_j (j≤Y_k) of |A_i - B_j`. Store it as answer.

Contribution of a new B_j to current A-set:
Let C be the multiset of A values currently in BITs.
We need sum_{a in C} |a - B_j|.
Using BIT: let cntL = number of a ≤ B_j, sumL = sum of those a. Let cntR = total_count - cntL, sumR = total_sum - sumL.
Then sum |a - B_j| = (cntL * B_j - sumL) + (sumR - cntR * B_j).
We can compute cntL, sumL using BIT queries up to index of B_j in compressed coordinates.

Complexities:
- O((N+K) log N) time.
- O(N) memory.

Edge cases:
- Values up to 2e8, compression needed.
- X_k or Y_k can be N.
- K up to 1e4, N up to 1e5, fine.