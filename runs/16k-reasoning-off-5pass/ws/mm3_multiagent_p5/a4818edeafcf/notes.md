
## ideation
The problem asks for the maximum sum of distinct counts of three contiguous non‑empty subarrays formed by splitting at positions `i < j`.  
Constraints: `N ≤ 3·10^5`, values in `[1, N]`.  
The naive O(N^2) scan of both split points is far too slow.

The classic approach for the 2‑split version uses a left sweep and a right sweep to obtain the prefix distinct counts and a data structure (Fenwick/segment tree) to query the best suffix distinct count for each `i`. That is O(N log N). For three parts, we need to consider both split points simultaneously. A divide‑and‑conquer (D&C) strategy reduces the complexity to O(N log N) while keeping implementation simple.

**Core difficulty:** Maximizing `distinct(1..i) + distinct(i+1..j) + distinct(j+1..N)`.  
The first part depends only on `i`, the third part depends only on `j`, while the middle part depends on both `i` and `j`. Because of the middle part, the problem cannot be decomposed into two independent 2‑split subproblems.

**Candidate approaches**
1. **O(N^2)** – Try all `(i, j)` pairs, too slow.
2. **Two pointers with a sliding window** – The middle part is a range, not just a suffix, so sliding window does not directly give the optimal middle distinct count.
3. **Divide‑and‑conquer** – Standard solution for the “three subarrays” problem (harder version of C).  
   Recur on halves, then handle crosses. For a cross, one split (`i`) is in the left half, the other (`j`) in the right half.  
   To answer the crossing case efficiently we need a data structure that, for each possible start position `j` in the right half, gives the maximum distinct count of a subarray starting at `j` and ending anywhere to the right of `j` (but bounded by the right half). This is exactly the “best suffix distinct count from `j`” problem. It can be precomputed with a right‑to‑left sweep in O(N). Then for the crossing case we can iterate over `i` from the middle leftwards, maintaining the distinct count of the left part, and for each `i` query the precomputed value for all `j > i` (or iterate `j` in the right half using a two‑pointer technique to avoid O(N^2)).  
   The crossing step must be linear in the size of the segment to keep the D&C O(N log N). This is achieved by the well‑known “meet‑in‑the‑middle” trick: sweep `i` from the middle to the left, and for each `i` move `j` from the middle+1 to the right, keeping the distinct count of the middle part in a small set, while querying the precomputed suffix best for the right part. The combined work for one level is O(segment size).

4. **Fenwick tree over suffix distinct counts** – Could also be used, but the D&C approach is more straightforward to implement with just arrays and sets.

## worker: Read input (N and array A) from stdin, then implem
The solution uses an O(N log N) divide-and-conquer approach with a segment tree to handle the three-way split. The key insight is reducing the three-split problem to a two-split problem on suffixes. We precompute prefix distinct counts and suffix distinct counts. Then for each starting position `s`, we compute `best_two_split[s]` = max_{j >= s} (distinct(s, j) + suffix[j+1]) using a segment tree with lazy propagation. We maintain an array `arr[j] = suffix[j+1] + distinct(current_start+1, j)` and update it efficiently by adding 1 to ranges where a newly included left element does not yet appear in the right part. Finally, the answer is max_{i} (prefix[i] + best_two_split[i+1]). The segment tree supports range add, point set, and range max query, giving O(N log N) total time.
