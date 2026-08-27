
## ideation
We need the K‑th largest value among all N³ triples
V(i,j,k) = A_i·B_j + B_j·C_k + C_k·A_i
with 1 ≤ N ≤ 2·10⁵ and K ≤ 5·10⁵.

Because K is relatively small we cannot enumerate triples, but we can binary‑search the answer X and, for a given X, count how many triples satisfy V ≥ X. The count routine must be fast (≈ O(K log N) or similar).

Key observation: V(i,j,k) can be rewritten as
(A_i + C_k)·B_j + A_i·C_k.
Fix (i,k); the expression grows with B_j, and fixing (i,j) it grows with C_k (or vice‑versa). So for a fixed B_j we can treat the sum of A_i and A_i·C_k later, but the term A_i·C_k couples i and k.

A standard approach for this problem (known from AtCoder ABC 155 F / similar problems) is:
* Sort B in decreasing order.
* Use a max‑heap to keep the current best pairs (i, j) by the value of A_i·B_j.
* Extract up to K largest values of A_i·B_j – because A_i·C_k is non‑negative (A_i, C_k >0) the final triple value is at least the pair value, thus the K‑th largest triple is among the triples formed from the K largest (i,j) pairs.
* For each such (i,j) we need to know how many C_k satisfy (A_i + C_k)·B_j + A_i·C_k ≥ X.
  Rearranged: A_i·C_k + C_k·B_j ≥ X – A_i·B_j
  → C_k·(A_i + B_j) ≥ X – A_i·B_j
  → C_k ≥ ceil((X – A_i·B_j) / (A_i + B_j))   (if X > A_i·B_j, else any C works)
* Since C is sorted, we can binary‑search (or two‑pointer) to count C_k ≥ threshold in O(log N). Because we only process O(K) pairs, total O(K log N).

Binary search on X:
* X is in range [1, 10^9·10^9 + 10^9·10^9 + 10^9·10^9] ≈ 3·10^18, fits in 64‑bit.
* For a given X, compute cnt = number of triples with value ≥ X.
  * If cnt ≥ K → X is achievable as K‑th largest, move left boundary up.
  * Else → X too big, move right boundary down.
* Stop when left == right; that is the K‑th largest value.

Implementation details:
* Sort A descending, C descending (or keep them sorted for binary search).
* Iterate B in descending order. For each B_j, we need the top A_i·B_j. Using a heap of size at most N:
  - Push (A_i·B_j, i) for all i when B_j changes? Too heavy (O(N²)).
  - Better: keep a pointer over A and a max‑heap of A_i·B_j. Standard technique: for each B_j (decreasing), we add new (i,j) pairs where A_i is the next best unseen A. We maintain a max‑heap of values A_i·B_j for the current B_j and all previously considered B's. But we actually need pairs (i,j) themselves, not just A_i·B_j. The known solution (e.g., ABC 155 F) does the following:
    - Sort B descending.
    - Keep a max‑heap of pairs (value = A_i·B_current, i) while scanning A from large to small.
    - Actually, we only need the K largest values of A_i·B_j. We can generate them as follows:
      - For each B_j (in descending order) do:
        - Insert all A_i (i from 0..N-1) into a max‑heap with key A_i·B_j? That's O(N²).
      - Instead, we can generate the K largest products by iterating B from largest to smallest and maintaining a max‑heap of (A_i·B_j, i, j). A classic method: for each B_j we push the best A_i (i=0) into heap, then repeatedly pop the largest (value, i, j) and push the next A (i+1) with the same B_j. This enumerates the top K (i,j) pairs in O(K log K). This works because the matrix A_i·B_j is monotone decreasing in both i and j, and we treat it as a “matrix multiplication” problem.
    - So we treat arrays A and B (both sorted descending). The largest products A_i·B_j are obtained by the standard “k largest sums/products” technique using a heap:
        heap = [(-A_0·B_0, 0, 0)]   (negate for max‑heap)
        visited = set()
        repeat K times:
            val,i,j = heappop
            store pair (i,j)
            if i+1 < N and (i+1,j) not visited: push (-A_{i+1}·B_j, i+1, j)
            if j+1 < N and (i,j+1) not visited: push (-A_i·B_{j+1}, i, j+1)
    - This enumerates the K largest A_i·B_j values in decreasing order, and we also remember which (i,j) indices produced them.
* Once we have the K best (i,j) pairs (value = A_i·B_j), for each pair we compute the number of C_k that make the triple ≥ X:
  - Let base = A_i·B_j.
  - Need: (A_i + C_k)·B_j + A_i·C_k ≥ X  →  C_k·(A_i + B_j) ≥ X – base.
  - If X ≤ base, then any C works → add N.
  - Else, need C_k ≥ ceil((X – base) / (A_i + B_j)).
  - Since C is sorted ascending, we can binary‑search the lower bound.
* Sum over all K pairs → cnt. O(K log N) per count call.
* Binary search takes about 60 iterations (since values up to 3·10^18). So total O(60·K·log N) ≈ 60·5·10⁵·18 ≈ 5.4·10⁸ operations, borderline but optimized C++ passes. In Python we need a faster constant: 60·5·10⁵·log(N) ≈ 5·10⁷, feasible if we use fast loops and built‑ins.

Potential pitfalls:
* Overflows: Use Python's unlimited int.
* Ceil division for large ints: (X - base + (A_i + B_j) - 1) // (A_i + B_j).
* K can be as large as N³, but constraint limits K ≤ 5·10⁵, so the “top K pairs” approach is safe.
* Edge case: X can be larger than any value, count = 0.
* Edge case: X can be smaller than any value, count = N³. But we only need up to K.
* The K best (i,j) pairs enumeration requires memory O(K) and a visited set. Use a set of tuples (i,j) or a dictionary with a key i*N+j. Since K ≤ 5e5, set operations are okay.

Optimization for Python:
* Use heapq, store ( -value, i, j ).
* Pre‑compute A and C as Python lists of ints, sorted descending.
* Sort B descending, keep original B? Not needed, just descending for the matrix.
* In the binary search, we can early‑stop counting once cnt ≥ K (no need to process all K pairs).
* For each X, we need to iterate over the K pairs (i,j) in decreasing order of A_i·B_j. However, the count for a pair depends only on X, not on order. So we can pre‑compute the list of K pairs (their A_i·B_j and A_i, B_j) once before the binary search, and reuse it. Complexity: O(K) memory, O(K) to generate. Then for each X we just loop over this list.

Thus algorithm steps:
1. Read N, K, arrays A, B, C.
2. Sort A descending, B descending, C ascending (for binary search) – keep C sorted ascending.
3. Generate the K best (i,j) pairs:
   - Use heap as described, store (value = A[i]*B[j], i, j).
   - For each popped pair, append (value, A[i], B[j]) to list `pairs`.
4. Binary search:
   - lo = 1 (or 0), hi = max possible (e.g., max(A)*max(B)+max(B)*max(C)+max(C)*max(A)).
   - While lo < hi:
       mid = (lo + hi + 1) // 2   (upper mid to find smallest X with cnt ≥ K)
       cnt = 0
       for each (base, a, bj) in pairs:
           if cnt >= K: break
           if mid <= base: cnt += N
           else:
               need = mid - base
               # C_k * (a + bj) >= need
               t = need // (a + bj)
               if need % (a + bj) != 0: t += 1
               # C is sorted ascending, need C_k >= t
               idx = bisect_left(C, t)
               cnt += N - idx
       if cnt >= K: lo = mid
       else: hi = mid - 1
5. Print lo.

Complexities:
* Generation of K pairs: O(K log K).
* Binary search: O(log V) ≈ 60 iterations, each O(K log N) due to bisect. Total O(60·K·log N) ≤ ~5·10⁷ operations.
* Memory: O(N) for arrays + O(K) for pairs.

Potential improvements:
* Use `bisect` from `bisect` module (binary search on C).
* For the inner loop, we can break early when cnt reaches K.
* Use local variables for speed.

Now the implementation details are clear.

## worker: Write the Python solution implementing the algorit
- The algorithm uses binary search on the answer X and counts how many triples have value ≥ X.
- Because K ≤ 5·10⁵, it suffices to consider only the K largest products A_i·B_j. These are generated efficiently using a max‑heap (standard “k largest products” technique) in O(K log K).
- For each candidate X, for each of the K (i,j) pairs we compute the required lower bound on C_k using `C_k ≥ (X - A_i·B_j) / (A_i + B_j)` and count C values satisfying it via binary search (`bisect_left`). Counting stops as soon as the count reaches K.
- The binary search runs ~60 iterations (values up to ~3·10¹⁸), so the total work is about 60·K·log N ≈ 5·10⁷ operations, which fits comfortably in Python.
- Edge cases: if X ≤ A_i·B_j, all N choices of C_k are valid; if the required threshold is larger than the maximum C, the count for that pair is 0.
- The solution uses 64‑bit integers (Python’s native `int` has arbitrary precision) to avoid overflow.

## worker: Generate the K best (i,j) pairs of A_i·B_j using a
- The expression `A_i·B_j + B_j·C_k + C_k·A_i` can be rearranged as `(A_i + C_k)·B_j + A_i·C_k`. For a fixed pair `(i, j)`, the term `A_i·B_j` is constant, and the remaining part is linear in `C_k` with positive coefficient `(A_i + B_j)`. Thus for a candidate `X`, we can solve for the minimum `C_k` needed.
- Because `K ≤ 5·10⁵`, only the `K` largest products `A_i·B_j` can possibly participate in the top `K` triples. These are enumerated efficiently with a max‑heap using the classic “k largest products of two sorted arrays” technique, maintaining a visited set to avoid duplicates.
- For each candidate `X`, the counting routine iterates over the at most `K` pre‑computed pairs and uses `bisect_left` on the sorted `C` array to count how many `C_k` satisfy the inequality. Early termination occurs as soon as the count reaches `K`.
- Binary search runs ~60 iterations (values up to ≈3·10¹⁸), giving total work about `60·K·log N`, well within limits for Python.
- Edge cases: when `X ≤ A_i·B_j`, all `N` choices of `C_k` are valid; when the required `C_k` exceeds the maximum, the pair contributes 0.
