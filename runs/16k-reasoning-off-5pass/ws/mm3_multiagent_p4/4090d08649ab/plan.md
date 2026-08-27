We need to compute, for every subarray, the minimum number of operations to delete all its elements where each operation deletes all occurrences of a contiguous integer segment [l, r] (by value, not index). 

Key observation: f(L,R) equals the number of "maximal contiguous runs" of distinct values in the sorted set of values appearing in A[L..R]. Equivalent: sort the distinct values in the subarray, and count how many times consecutive distinct values differ by more than 1. This is a classic trick: we can greedily delete as large a value-interval as possible.

So f(L,R) = 1 + (number of pairs (i,j) with L ≤ i < j ≤ R such that the distinct values in A[i..j] are NOT a contiguous range of integers). More precisely, for each adjacent pair of positions, we check if inserting a new element creates a "gap" — if the union of values becomes non-contiguous, we add 1.

We can use a two-pointer (sliding window) technique with frequency array `cnt[]` and track `distinct` (number of distinct values in current window) and `contig_len` (size of the contiguous range covering the current min..max). When `distinct == contig_len`, the values form a contiguous range; otherwise, there's at least one missing integer.

For each left endpoint L, we expand right R from L to N, maintaining these counts. For each R, we determine if the new element creates a "new block" (i.e., increases f(L,R) by 1 compared to f(L,R-1)). We accumulate the sum.

Because N ≤ 3e5, an O(N log N) or amortized O(N) solution is required. A frequency array of size N+1 with add/remove is O(1) per move, and we move right pointer at most N times per left pointer overall — leading to O(N^2) in worst case. However, we can use the classic "for each left, move right as far as possible while property holds" combined with contributions. But the property (contiguous range) is monotone, so we can use two pointers to compute, for each L, the largest R such that the window has contiguous values; the number of operations f(L,R) increases by 1 exactly at the first position where a gap appears. But f(L,R) can increase multiple times as R grows — each new gap adds 1. The gaps are determined by pairs of positions i<j where the two values themselves form a "gap" (i.e., |A[i] - A[j]| > 1) and there is no other value between them in the window.

Alternative approach: The answer is N*(N+1)/2 (each subarray at least 1 operation) plus the number of subarrays where the set of values is NOT a contiguous range. But computing the number of subarrays with non-contiguous value sets is easier via two pointers: for each left, find the maximum right where values are contiguous; all subarrays starting at left and ending beyond that have non-contiguous sets, so each such extension adds 1 to the sum. We can process with two pointers efficiently because the property is monotone: as right increases, once a gap appears, expanding further cannot remove it. Thus we can find for each L the boundary `R_max[L]` — the largest R such that A[L..R] has contiguous values. Then contribution from L is: sum_{R=L}^{R_max} 1 + sum_{R=R_max+1}^{N} (1 + (R - R_max)). This is O(N) per L if we compute R_max via sliding window; total O(N) because right pointer only moves forward.

Implementation details:
- Maintain freq[1..N], min_val, max_val, distinct.
- To efficiently update min/max on removal, we can use a "bucket" approach or maintain two deques. Since values are up to N=3e5, we can maintain arrays `first_occurrence` of size N+2 to locate current min and max. A simpler approach: keep `min_v` and `max_v` and when removing the current min, scan downward until finding a value with freq>0. This could be O(N) in worst case per removal, leading to O(N^2). To avoid this, we can maintain two arrays `next_nonempty` using union-find / DSU to jump to the next present value — like "disjoint set on the line" to find the current min and max efficiently (amortized O(α(N))). Or maintain a doubly linked list of active values.

Simpler: Since we only expand right and shrink left, and values are ≤ N, we can maintain `min_v` and `max_v` and when the current min is removed (freq becomes 0), we increment `min_v` until freq>0. This is amortized O(N) because each value can be skipped at most once when moving left, and min_v only increases. Similarly for max_v decreasing. Since we have two pointers both moving monotonically, total amortized O(N).

Algorithm:
- freq = [0]*(N+2)
- distinct = 0
- min_v, max_v = 0, 0
- right = 0
- For left in 1..N:
    - While right+1 <= N and adding A[right+1] keeps the set contiguous:
        - right += 1
        - v = A[right]
        - if freq[v]==0: distinct += 1
        - freq[v] += 1
        - update min_v, max_v: if distinct==1: min_v=max_v=v
        - else: if v < min_v: min_v = v; if v > max_v: max_v = v
        - Check contiguity: max_v - min_v + 1 == distinct
    - R_max = right
    - Now, subarrays [L, R] for R in [L, R_max] have f=1.
    - For R > R_max, f(L,R) = 1 + (R - R_max).
    - Contribution = (R_max - L + 1) * 1 + sum_{k=1}^{N-R_max} (1 + k)
                   = (R_max - L + 1) + (N - R_max) + sum_{k=1}^{N-R_max} k
                   = (R_max - L + 1) + (N - R_max) + (N-R_max)*(N-R_max+1)/2
    - Then before moving left to L+1, remove A[L] from window:
        - v = A[L]
        - freq[v] -= 1
        - if freq[v]==0: distinct -= 1
        - if distinct==0: min_v, max_v = 0, 0
        - else if v == min_v: increase min_v until freq[min_v]>0
        - else if v == max_v: decrease max_v until freq[max_v]>0

- Sum all contributions to ans.

Time complexity: Each index is added to right pointer at most once, and left pointer moves N times. Adjusting min_v/max_v is amortized O(N) because each value index is visited at most constant times when min or max jumps over empty slots. Total O(N + N) = O(N).

Let's verify with samples:
Sample 1: N=4, A=[1,3,1,4]
- L=1: expand right. 
  right=1 (v=1): distinct=1, min=max=1. contig=1==1 ok.
  right=2 (v=3): distinct=2, min=1, max=3. 3-1+1=3, distinct=2 => not contig. So stop. R_max=1.
  R > 1: 2,3,4 are > R_max.
  Contrib = (1-1+1)=1 + (4-1)=3 + sum_{k=1}^{3} k =6 => 1+3+6=10? Wait, formula: (R_max - L + 1) + (N - R_max) + (N-R_max)*(N-R_max+1)/2
  = 1 + 3 + 3*4/2 = 1+3+6 = 10.
- Remove A[1]=1. freq[1] becomes 0, distinct=1, min_v=3, max_v=3.
- L=2: right currently=1. Try expand:
  right=2 is already at end? Actually right is at 1, next is 2 (A[2]=3) but wait we are at L=2, the window is [2..1]? That's empty. freq has only A[2]=3? Actually we removed A[1]=1, and right was 1, so window is [2..1] empty. distinct=0. We need to ensure right >= L-1. Actually right pointer is 1, L is 2, so window is empty. We try to expand right to 2: v=3, freq[3] from 0 to 1, distinct=1, min=max=3, contig=1==1 ok.
  right=3: v=1, freq[1] from 0 to 1, distinct=2, min=1, max=3, 3-1+1=3, distinct=2 => not contig. Stop. R_max=2.
  Contrib = (2-2+1)=1 + (4-2)=2 + 2*3/2=3 => 1+2+3=6.
  Remove A[2]=3. freq[3] becomes 0, distinct=1, v was max, so max_v becomes 1, min_v=1.
- L=3: right=2. Expand:
  right=3: v=1, already freq[1]=1, distinct=1, min=max=1 ok. right=3.
  right=4: v=4, freq[4]=1, distinct=2, min=1, max=4, 4-1+1=4, distinct=2 => not contig. Stop. R_max=3.
  Contrib = (3-3+1)=1 + (4-3)=1 + 1*2/2=1 => 1+1+1=3.
  Remove A[3]=1. freq[1]=0, distinct=1, min_v=4, max_v=4.
- L=4: right=3. Expand:
  right=4: v=4, freq[4]=1, distinct=1, min=max=4 ok. right=4.
  Can't expand further.
  R_max=4.
  Contrib = (4-4+1)=1 + 0 + 0 = 1.
  Total = 10+6+3+1 = 20? But expected is 16. Let's recount f(L,R) manually:
  (1,1):1, (1,2): values {1,3} not contig -> 2, (1,3): {1,3} -> 2, (1,4): {1,3,4} -> 2 (example says 2).
  (2,2):1, (2,3): {3,1} -> 2, (2,4): {3,1,4} -> 2.
  (3,3):1, (3,4): {1,4} not contig -> 2.
  (4,4):1.
  Sum = 1+2+2+2 + 1+2+2 + 1+2 + 1 = 16. My calculation gave 20 because my contribution formula overcounted.
  Let's check: For L=1, R_max=1 means subarrays [1,1] have f=1 (correct). For R=2,3,4, f should be 2,2,2. My formula gave: for R=2: 1 + (2-1) = 2; for R=3: 1 + (3-1) = 3? That's wrong. The increase is not simply 1 per step beyond R_max. Because once a gap appears, the number of operations may increase by more than 1 when a new value is added that doesn't fill the gap but extends the range? Actually, if the current set is not contiguous, adding a new element could either keep f same or increase it by 1 (if the new element is also not adjacent to existing values, creating a new gap? Or if it fills a gap, f decreases? But we can't fill gaps because we are only adding elements). 

  Let's think again. f(L,R) = number of connected components of the value graph where edges connect values that differ by 1? No, the operation can delete any contiguous range [l,r] of values. If the values in the window form a set S, the minimum number of operations to delete all values (with possible repeats) is the number of maximal contiguous segments in S. Because we can delete each segment in one operation. 

  So f(L,R) = number of contiguous segments in the set of values in A[L..R].
  For L=1, R=1: {1} -> 1 segment.
  R=2: {1,3} -> segments {1}, {3} -> 2 segments.
  R=3: {1,3} -> 2 segments.
  R=4: {1,3,4} -> segments {1}, {3,4} -> 2 segments. So f is 2 for all R>=2. So it increased by 1 at R=2 and stayed 2.
  My formula assumed f(L,R) = 1 + (R - R_max) for R > R_max, but that's wrong. The number of segments doesn't increase linearly; it increases only when a new value is added that is not adjacent to the current union of values' segments. 

  However, the property "values are contiguous" (i.e., f=1) is monotone: if for a given L, the largest R with f(L,R)=1 is R_max, then for any R > R_max, f(L,R) >= 2. But f(L,R) can be 2, 3, etc. So we need a better way to compute f(L,R) efficiently.

Alternative viewpoint: f(L,R) = 1 + number of "gaps" in the value set, where a gap is a missing integer between min and max. But the set of values is not a simple interval; it can have multiple gaps. Actually, the number of segments = number of connected components in the graph where values are connected if they are adjacent integers present in the subarray. This is exactly: number of distinct values minus the number of adjacent pairs (v, v+1) both present. So f(L,R) = distinct(L,R) - adj(L,R), where adj is number of pairs (v, v+1) such that both v and v+1 appear in A[L..R].

This might be easier to compute using inclusion-exclusion or contributions. But let's think about the two-pointer approach again. We can maintain for each left L, the values in the window and the number of segments. When we expand right, we add a new value v. If v is new, distinct increases by 1. Also, if v-1 is present, adj increases by 1; if v+1 is present, adj increases by 1. Then f = distinct - adj. This is O(1) per expansion. However, as we shrink left (move L forward), we remove values. Removing a value v: if v was present (freq decreases from 1 to 0), distinct decreases by 1. If v-1 is present, adj decreases by 1; if v+1 is present, adj decreases by 1. This is also O(1) per removal.

So we can use a sliding window with left and right pointers, but we need to sum f(L,R) for all L,R. This is a classic problem: sum over all subarrays of some function that can be updated in O(1) with two pointers? Actually, if we fix left and expand right, we can compute f(L,R) for all R >= L in O(N) time per left, total O(N^2). But we can use the fact that the function f(L,R) as a function of R for fixed L is non-decreasing? Let's check: adding an element can only increase or keep same the number of segments. Because new value either forms a new segment (distinct+1, adj unchanged) -> f increases by 1; or it connects to an existing segment (distinct+1, adj+1) -> f unchanged; or it duplicates existing value (distinct unchanged, adj unchanged) -> f unchanged. So f(L,R) is non-decreasing as R increases! This is crucial.

Wait, is it non-decreasing? If we add a value that is exactly between two existing segments? For example, values {1,3}, f=2. Add value 2: set becomes {1,2,3}, f=1. That decreases! So f is not monotone in R. Because adding a value can merge two segments into one. So the two-pointer approach that relies on monotonicity of the condition (like "window is good") won't work directly if we want to compute f for all R.

But we can use the formula: f(L,R) = distinct(L,R) - adj(L,R). The number of distinct values and number of adjacent pairs are both "additive" in a sense. We can use the "contribution of each pair" technique. 

Observation: The total sum of f(L,R) over all subarrays = sum_{L,R} (distinct(L,R) - adj(L,R)) = sum_{L,R} distinct(L,R) - sum_{L,R} adj(L,R).

The sum of distinct(L,R) over all subarrays is a known problem: for each value v, it contributes to subarrays where v is present. The number of subarrays containing a specific position i is i*(N-i+1). But distinct counts each value at most once per subarray. Standard approach: for each value v, find the positions where it occurs. The number of subarrays where v appears is (total subarrays) - (subarrays where v is absent). Subarrays where v is absent can be counted by gaps between occurrences. But maybe there's an O(N) formula.

Actually, sum of distinct over all subarrays: there is a known O(N) solution using the "last occurrence" trick. For each position i, we can think of A[i] as the "newest" occurrence of its value in the subarray. For each i, the number of subarrays where A[i] is the first occurrence of its value (from the right) or something. Let's recall: For each i, the number of subarrays ending at i where A[i] is the first occurrence of value A[i] (i.e., the leftmost occurrence in the subarray) is i - last_occurrence[A[i]] (where last_occurrence is the previous index where this value appeared). So sum over i of (i - last_occ) gives the number of subarrays where each distinct value is counted exactly once as the "leftmost" in the subarray? Wait, standard result: sum_{L=1}^N sum_{R=L}^N distinct(L,R) = sum_{i=1}^N (i - prev_occ[i]), where prev_occ[i] is the previous index where A[i] appeared. Because for each subarray, the first occurrence of each distinct value from the left is unique. More precisely, for each subarray [L,R], the distinct values are exactly the set of indices i in [L,R] such that A[i] is the first occurrence of its value in [L,R]. The number of such indices is the distinct count. So if we sum over all subarrays the number of first occurrences, we get the total distinct count. And for each position i, the number of subarrays where i is the first occurrence of A[i] is exactly the number of L such that L <= i and for all j in [L, i-1], A[j] != A[i]. That is L can be from prev_occ[i]+1 to i. So count = i - prev_occ[i]. Summing over i gives the total sum of distinct over all subarrays. This is O(N) with the prev_occ array.

Similarly, sum of adj(L,R) over all subarrays: adj is the number of pairs (v, v+1) both present. We can rewrite adj as sum_{v} I(v present and v+1 present). Then sum_{L,R} adj(L,R) = sum_v (number of subarrays where both v and v+1 are present). This is a classic problem: number of subarrays containing a set of two values. We can handle it by for each pair of values (v, v+1), find the positions where either appears, and count subarrays that contain at least one of each? Actually, we need subarrays that contain at least one v and at least one v+1. 

Alternatively, we can use a different decomposition. adj is the number of edges in the adjacency graph of values present. We can count contributions of each edge (v, v+1). For each edge e = (v, v+1), we need to count subarrays that contain at least one occurrence of v and at least one of v+1. Let's denote the positions of v and v+1. A subarray contains both if and only if its left endpoint L <= min(pos_v, pos_{v+1})? No, it must contain at least one of each, so the subarray must cover at least one occurrence of v and at least one of v+1. The number of subarrays containing both can be computed as: total subarrays - subarrays missing v - subarrays missing v+1 + subarrays missing both. But that might be complicated to sum over all v.

But we can use a similar "first occurrence" trick for pairs. For each position i, we can think of the subarray [L,R] and the pair (A[i], A[i]+1) or (A[i]-1, A[i]). Actually, each occurrence of a value can be the "first occurrence" of a pair edge in the subarray. Let's think: In a subarray, an edge (v, v+1) is present if there is some occurrence of v and some occurrence of v+1. The "first" such edge from the left? Not straightforward.

Alternative: Use inclusion-exclusion with positions. For a fixed v, let the positions of v be p1 < p2 < ... < pk, and positions of v+1 be q1 < q2 < ... < qm. A subarray contains both if and only if it starts at or before the first occurrence of one of them, and ends at or after the last occurrence of the other? Not exactly. A subarray [L,R] contains both if max(L, first_occurrence_of_v, first_occurrence_of_{v+1}) <= min(R, last_occurrence...) but we need at least one of each, so L must be <= the first occurrence of v or v+1? Actually, the condition is: there exists i in [L,R] with A[i]=v, and there exists j in [L,R] with A[j]=v+1. This is equivalent to: the subarray's left endpoint L is <= the last occurrence of v or v+1? No, it's easier to use the complement: subarrays that miss v or miss v+1. But summing over all v might be O(N^2) if we do it naively.

We can compute the sum of adj over all subarrays using a two-pointer or stack method. Since we only need adj for adjacent values, we can process the array and for each position, consider it as the "rightmost" occurrence of some value. But maybe we can compute the answer directly using a stack or divide and conquer? 

Wait, the constraints are N up to 3e5. O(N log N) is fine. Can we compute f(L,R) directly for all L,R in O(N log N) using divide and conquer? There is a known algorithm for "sum of number of distinct elements in all subarrays" and "sum of number of adjacent pairs" using divide and conquer. For example, we can recursively split the array, compute subarrays entirely in left, entirely in right, and crossing. For crossing subarrays, we can expand from the middle to left and right, maintaining the value set and number of segments. Since the crossing part is O(N log N) overall, this works.

Let's design a divide and conquer (CDQ) approach:
- Function solve(l, r):
    - if l == r: return f(l,l) = 1.
    - mid = (l+r)//2
    - ans = solve(l, mid) + solve(mid+1, r)
    - Now consider subarrays with L in [l, mid] and R in [mid+1, r].
    - We process left side and right side expansions.
    - For L from mid down to l:
        - maintain a set of values in A[L..mid] (with frequencies, min, max? But we need the number of segments f for the union of left part and right part).
    - For R from mid+1 to r:
        - maintain set of values in A[mid+1..R].
    - We can precompute prefix and suffix info to efficiently merge? Actually, a standard technique: 
        - First, iterate R from mid+1 to r, and for each R, compute the "state" of the right part: its set of values, min, max, distinct, and number of segments in the right part alone. Store these in arrays indexed by R.
        - Then iterate L from mid down to l, maintaining the state of the left part. For each L, we need to compute the number of segments in the union of left part and right part for all R >= mid+1. As we expand L to the left, we add values to the left set. We need to combine with the precomputed right states. But combining two arbitrary sets to get the number of segments in the union is not trivial unless we can quickly compute the number of segments in the union given the two sets' info. 

    - We can do it incrementally: for each L, we can extend R from mid+1 to r, but that would be O(N^2) per level. 
    - Better: For each L, as we go leftwards, we maintain a data structure for the left set. Then we can iterate R from mid+1 to r and update the union? Still O(N^2).

    - Another approach: For each L, we can find the range of R where the union of left and right has certain properties. But maybe we can use the fact that we only need the sum, not each f individually. We can process all crossing subarrays by iterating over the left side and using a "merge" with the right side's precomputed values.

    Actually, there is a known solution for this problem: f(L,R) is the number of "maximal contiguous value segments" in the subarray. The sum over all subarrays can be computed using a stack or by considering contributions of each "gap" between adjacent values. 

Let's think differently. f(L,R) = 1 + (number of gaps in the value set). A gap is a value v such that v is not in the set, but both v-1 and v+1 are in the set? No, that's not right. The number of segments = 1 + (number of "missing adjacencies" in the set). A missing adjacency is a pair (v, v+1) such that v is present but v+1 is not present, and there is no other present value between them? Actually, the number of segments in a set S is the number of connected components in the graph where edges are between consecutive integers. This is exactly: |S| - (number of edges in the graph). An edge exists if both v and v+1 are in S. So segments = |S| - (number of pairs (v, v+1) with both in S). This is our formula f = distinct - adj.

We already have a formula for sum of distinct over all subarrays: sum_i (i - prev_occ[i]).

Now we need sum of adj over all subarrays. adj(L,R) = sum_v I(v in S and v+1 in S), where S is the set of values in [L,R]. So total sum of adj = sum_v (number of subarrays where both v and v+1 are present). 

Let's compute for a fixed v, the number of subarrays containing at least one v and at least one v+1. Let the positions of v be P = [p1, p2, ..., pk] and positions of v+1 be Q = [q1, q2, ..., qm]. We need the number of intervals [L,R] such that L <= some p_i <= R and L <= some q_j <= R. This is equivalent to: R >= min(last p_i in [L,R]?) No. 

A standard combinatorial way: The total number of subarrays is N*(N+1)/2. Subarrays missing v: these are subarrays contained in the gaps between occurrences of v. Similarly for v+1. By inclusion-exclusion, the number of subarrays containing both = total - (missing v) - (missing v+1) + (missing both). 

Let the positions of all values (including v and v+1) be considered. The array is partitioned by the occurrences of v into blocks: before p1, between p1 and p2, ..., after pk. In each block, there is no v. Similarly for v+1. The subarrays missing v are those entirely within one of these blocks. So sum of lengths of these blocks choose 2? Actually, if the gaps (segments without v) have lengths g1, g2, ..., g_{k+1} (where g1 is length of prefix before p1, g2 is length between p1 and p2, etc.), then the number of subarrays with no v is sum_{i} g_i*(g_i+1)/2. Similarly for v+1. 

The subarrays missing both v and v+1 are those entirely within the gaps where neither v nor v+1 appears. So we can compute the lengths of intervals between occurrences of v or v+1. 

This seems doable per v, but there are up to N values, so doing it for each v separately might be O(N^2) if we iterate over positions. However, we can process all v efficiently if we consider the combined occurrences. But we need the result for each adjacent pair (v, v+1). Since the number of pairs is N-1, and each value appears at some positions, total sum of occurrences over all v is N. So iterating over all pairs and their positions might be O(N) if we handle it carefully. But for each pair, we need the positions of both values. If we iterate over the array and for each position i, we consider the pair (A[i], A[i]+1) and (A[i]-1, A[i]), we can update a data structure. 

Actually, we can compute the number of subarrays missing a specific value v in O(1) per gap if we know the gap lengths. If we precompute for each value v the list of its occurrences, we can compute the sum of g_i*(g_i+1)/2 for that v. But doing this for each v separately would require O(N) time to scan the list, total O(N^2) in worst case (e.g., all values distinct). 

But we can compute the sum of "subarrays missing v" over all v using a single pass? There is a known trick: For each subarray, it is missing some set of values. But that's not easy.

Alternatively, we can compute the sum of adj directly using a "contribution of each occurrence" method. Consider the graph where each subarray's adj is the number of edges (v, v+1) present. We can think of each occurrence of a value as potentially "activating" an edge. For a fixed pair (v, v+1), the edge is present in a subarray if the subarray contains at least one v and at least one v+1. This is equivalent to: the subarray's left endpoint is <= the first occurrence of v or v+1 from the left? Not exactly.

Let's think in terms of intervals. For a fixed v, let prev_v(i) be the previous occurrence of v before i, and next_v(i) be the next occurrence. Then a subarray [L,R] contains v if and only if L <= some occurrence <= R. This is equivalent to: there exists i in [L,R] with A[i]=v. This is not easily expressed as a function of L and R only.

Maybe we can use the "first occurrence from the right" trick for pairs. For a subarray [L,R], consider the rightmost occurrence of v and the rightmost occurrence of v+1. The edge (v, v+1) is present if both rightmost occurrences exist and the max of their positions is <= R? Actually, if we look at the subarray, the condition "contains both v and v+1" is equivalent to: the last occurrence of v in [L,R] and the last occurrence of v+1 in [L,R] both exist. But that's just the condition.

Another approach: Since N is 3e5, an O(N log N) solution is acceptable. We can use a BIT (Fenwick tree) or segment tree to process offline queries. For each R, we want to know the sum of f(L,R) for all L. f(L,R) = distinct(L,R) - adj(L,R). For a fixed R, as L decreases, the set of values in [L,R] only grows. The number of distinct values and number of adjacent pairs can be updated as we add elements. We can iterate L from R down to 1, and for each L, we need to compute the sum of f(L,R) over all R. That's O(N^2) if done naively.

But we can swap the loops: fix L and iterate R? Still O(N^2). 

We need a smarter way. Let's revisit the divide and conquer idea with a twist: we can compute the sum of f(L,R) for all L,R in O(N log N) using the "small to large" or "D&C on values" method. Actually, there is a known problem: "sum of number of distinct elements in all subarrays" is O(N). "Sum of number of adjacent pairs in all subarrays" might also be O(N) or O(N log N) using similar ideas. 

Let's attempt to compute sum of adj using a D&C on the array. Suppose we want to compute for all subarrays the number of adjacent pairs. We can use a divide and conquer: 
- Recursively compute for left half, right half.
- For crossing subarrays [L,R] with L in left, R in right: we can expand from the middle. 
- For each L from mid down to left, we maintain the set of values in A[L..mid]. As we expand L, we add A[L] to the set. 
- For each R from mid+1 to right, we precompute the state of the right part: its set of values, and for each possible "left set", the number of edges? Not straightforward.

But we can process the crossing part by iterating over the right part and using a data structure that stores the left part's "profile" of values. However, the number of segments in the union of two sets S_left and S_right depends on the gap between the max of S_left and min of S_right, etc. Actually, if we know the set of values in the left part and in the right part, the number of segments in the union is: segments(left) + segments(right) - (number of adjacencies between left and right values) + (number of new adjacencies created when we merge). More precisely, the union's number of segments = segments(L) + segments(R) - (number of v in L and v+1 in R? No, that's not right because v and v+1 could be in the same side.

Wait, the number of segments in a set S is |S| - E(S), where E(S) is the number of edges (v, v+1) with both in S. So for the union of two disjoint sets (in terms of indices, but values can overlap? Values are the same set, but the subarray values are the union of values from left and right parts. The union of values in the crossing subarray is the union of the value sets from the left part and the right part. Let V_L be the set of values in A[L..mid], V_R be the set in A[mid+1..R]. Then V = V_L ∪ V_R. Then segments(V) = |V| - E(V). We can write |V| = |V_L| + |V_R| - |V_L ∩ V_R|. And E(V) = E(V_L) + E(V_R) + E_cross, where E_cross is the number of edges (v, v+1) such that one is in V_L\V_R and the other in V_R\V_L, or one in V_L∩V_R and the other in the other set, etc. Actually, an edge (v, v+1) is in E(V) if both v and v+1 are in V. This is equivalent to: (v in V_L and v+1 in V_R) or (v in V_R and v+1 in V_L) or (both in V_L) or (both in V_R). So E(V) = E(V_L) + E(V_R) + E_LR, where E_LR counts edges with one endpoint in V_L\V_R and the other in V_R\V_L, plus edges with one in V_L∩V_R and the other in the other set? Actually, careful: If both v and v+1 are in V, there are three cases:
1. Both in V_L
2. Both in V_R
3. One in V_L, one in V_R.
Case 3 includes subcases where one of them is in the intersection, but the other is in the other set. So E(V) = E(V_L) + E(V_R) + number of pairs (v, v+1) with v in V_L, v+1 in V_R OR v in V_R, v+1 in V_L.
So segments(V) = (|V_L| + |V_R| - |V_L ∩ V_R|) - (E(V_L) + E(V_R) + E_LR)
= segments(V_L) + segments(V_R) - |V_L ∩ V_R| - E_LR.
But wait, segments(V_L) = |V_L| - E(V_L). So:
|V_L| - E(V_L) + |V_R| - E(V_R) - |V_L ∩ V_R| - E_LR
= segments(V_L) + segments(V_R) - |V_L ∩ V_R| - E_LR.
This is not simply the sum of segments of the two sides minus something constant, because E_LR depends on the overlap and the specific values.

This seems messy. Maybe there's a simpler way.

Let's go back to the formula: f(L,R) = 1 + number of "missing values" between min and max? No, it's 1 + number of gaps. A gap is a pair of consecutive values that are not both present. Actually, if we have a set of integers S, the number of connected components (contiguous segments) is equal to the number of elements in S minus the number of adjacent pairs in S. This is exact.

We already have a way to compute sum of distinct over all subarrays in O(N). Let's verify the formula: sum_{L,R} distinct(L,R) = sum_{i=1}^N (i - prev_occ[i]), where prev_occ[i] is the previous index where A[i] appeared (0 if none). This is standard and correct.

Now we need sum_{L,R} adj(L,R). Let's try to find a similar O(N) or O(N log N) formula for adj. 

Consider each pair of adjacent values (v, v+1). The contribution of this pair to the sum of adj over all subarrays is the number of subarrays that contain at least one v and at least one v+1. Let's denote this as C(v). We need sum_{v=1}^{N-1} C(v).

Now, for a fixed v, how to compute C(v) efficiently? Let the positions of v be p1 < p2 < ... < pk, and positions of v+1 be q1 < q2 < ... < qm. We need the number of intervals [L,R] such that there exists pi in [L,R] and qj in [L,R]. 

This is equivalent to: the subarray is not entirely contained in a gap of v, and not entirely contained in a gap of v+1. But we can use inclusion-exclusion as mentioned. Let the array be partitioned by all occurrences of v and v+1? Actually, to count subarrays missing v, we just look at gaps between occurrences of v (including before first and after last). Let the lengths of these gaps be g1, g2, ..., g_{k+1} (where g1 = p1 - 1, g_{i} = p_{i+1} - p_i - 1 for i=1..k-1, and g_{k+1} = N - p_k). Then the number of subarrays with no v is sum_{i=1}^{k+1} g_i*(g_i+1)/2. Similarly, let the gaps for v+1 have lengths h1, ..., h_{m+1}. Then the number of subarrays with no v+1 is sum h_j*(h_j+1)/2. 

The number of subarrays with neither v nor v+1 is the number of subarrays entirely contained in the intersection of the gap sets. The gaps of both v and v+1 combined form a partition of the array into segments where neither v nor v+1 appears. The lengths of these segments can be found by merging the positions of v and v+1. Let the positions of v and v+1 combined be sorted. The gaps between consecutive positions (and before the first and after the last) are exactly the segments with no v and no v+1. Let these segments have lengths d1, d2, ..., d_{k+m+2}? Actually, the number of such segments is (k+m+1) if we consider the gaps between consecutive occurrences in the combined sorted list. The number of subarrays with neither is sum d_t*(d_t+1)/2.

Then by inclusion-exclusion, C(v) = Total - (missing v) - (missing v+1) + (missing both).

Total = N*(N+1)/2.

So if we can compute the sum of g_i*(g_i+1)/2 for all v efficiently, we can get C(v). But we need to do this for each v. If we do it separately for each v, we need to iterate over the occurrences of v. Since total occurrences over all v is N, if we can compute the missing count for all v in O(N) total time, we are good.

How to compute for each v the sum of g_i*(g_i+1)/2? For a fixed v, the gaps are determined by the positions of v. This is exactly the number of subarrays that do not contain v. This is a known quantity: the number of subarrays not containing a particular value can be computed by scanning the array and maintaining the length of the current gap. For a single value v, we can do it in O(N) by scanning and checking if A[i] == v. But doing this for all v would be O(N^2). 

However, we can use the fact that we only need this for v and v+1 for each adjacent pair. So we need the missing counts for all v, but we can compute them all in one pass? There is a known technique: for each position i, consider it as the "rightmost" of a gap. But we need the sum over all v of (number of subarrays missing v). This is the sum over v of the number of subarrays that do not contain v. This is not the same as our C(v) but related.

Wait, we need C(v) for each v, but we can compute C(v) using the inclusion-exclusion formula. To compute C(v) for all v, we need for each v: total - miss(v) - miss(v+1) + miss_both(v, v+1). Here miss(v) is the number of subarrays missing v, miss(v+1) missing v+1, and miss_both is missing both. 

We can compute miss(v) for all v efficiently? The total number of subarrays missing any particular value v can be computed as: for each v, we look at the positions of v. The gaps between them. The sum of g_i*(g_i+1)/2. To compute this for all v, we can precompute for each v the list of its positions. The total length of all lists is N. If we iterate over the list for each v and compute the gaps, the total time is O(N) because we just traverse the positions in order. But we need to do this for each v separately. If we store the positions in a list of lists, for each v we can compute its gaps in O(occurrences(v)) time. So total O(N) to compute miss(v) for all v! Let's check: For v from 1 to N, we have a list pos[v] of occurrences. We can iterate through pos[v] and compute the gap lengths. The sum of lengths of pos[v] is N. So total time to compute all miss(v) is O(N). 

Similarly, we need miss_both(v, v+1) for each v. miss_both(v, v+1) is the number of subarrays missing both v and v+1. This is the number of subarrays entirely contained in the gaps where neither v nor v+1 appears. To compute this for all v, we need the merged positions of v and v+1. The total number of positions in the union over all v of (pos[v] ∪ pos[v+1]) is at most 2N per v, but summed over all v it's O(N^2) if we do it naively. However, we can compute miss_both for all v using a single pass? 

Consider the array. For each v, miss_both(v, v+1) is computed from the gaps of the set {v, v+1}. The set {v, v+1} has occurrences that are the union of pos[v] and pos[v+1]. The gaps in this combined set are the segments of the array where neither v nor v+1 appears. If we can compute for each adjacent pair (v, v+1) the sum of d_t*(d_t+1)/2 where d_t are the lengths of these gaps, we can do it in O(N) total? Let's think. 

We can process the array once and for each v, we can update a data structure. But maybe there's a simpler way: the sum of adj over all subarrays can be computed directly using a stack or by considering each occurrence of a value as the "last seen" for its value and its neighbor. 

Let's try a different approach: the sum of f(L,R) can be computed using a "contribution of each value" method with a stack. Notice that f(L,R) is the number of segments in the value set. Each time we add a new value, it either creates a new segment or merges two segments. The change in f is +1 if the new value is isolated from existing values (no v-1 or v+1 present), or 0 if it connects to one existing segment, or -1 if it connects two existing segments. Since we only add elements, f can go up and down. 

But we are summing over all subarrays. There is a known problem: "Sum of number of connected components of the value graph in all subarrays" or similar. I recall a problem from AtCoder or Codeforces: "Sum of f(L,R) where f is the number of contiguous segments in the value set". This is likely the problem we have. 

Let's search memory: This problem is from AtCoder ABC 294 F? No. Maybe it's from a recent contest. The constraints N up to 3e5, values up to N. The problem is to compute sum of f(L,R). I think the solution uses a stack and processes the array to find for each position the next position where the value is "isolated" or something. 

Another idea: For each subarray, f(L,R) is the number of times we need to "jump" to cover all values. This is equivalent to: sort the distinct values, and count the number of times consecutive values differ by >1. So f(L,R) = 1 + #{ (x, y) in S such that x and y are consecutive in sorted order of S and y - x > 1 }. 

So f(L,R) = 1 + number of "gaps" in the sorted distinct values. A gap is a pair (v, w) with v < w, both in S, no value between them in S, and w - v > 1. 

So sum_{L,R} f(L,R) = N*(N+1)/2 + sum_{L,R} (number of gaps in S). 

Now, a gap in S is defined by two values v and w that are consecutive in S and w - v > 1. For each pair of values (v, w) with w - v > 1, we can ask: in how many subarrays are v and w consecutive in the set of values? That is, subarrays where v and w are present, and no other value between them is present. 

Let's formalize: For two values a < b with b - a > 1, consider subarrays where a and b are both present, and no value in (a, b) is present. Then in such a subarray, a and b become consecutive in the sorted distinct set, and since b - a > 1, they form a gap. So each such subarray contributes 1 to the number of gaps. Conversely, every gap in a subarray corresponds to such a pair (a, b) with a, b present and no values between. 

So the number of gaps in S is exactly the number of pairs (a, b) with a < b, b - a > 1, such that a, b ∈ S, and for all x with a < x < b, x ∉ S. 

Therefore, sum_{L,R} (number of gaps) = sum_{a < b, b-a>1} (number of subarrays where a and b are present and no value in (a,b) is present). 

Now, this is a sum over pairs of values. The number of such pairs is O(N^2) in the worst case (e.g., values are 1, 2, 3, ... and gaps are between 1 and 3, 1 and 4, etc., but actually only consecutive in S matter, which is at most N-1 per subarray, but over all subarrays it could be large). However, we can sum this by considering each subarray's gaps. But we need an efficient way to sum over all subarrays the number of gaps. 

Notice that a gap is formed by a pair of values that are "adjacent" in the value set with a difference > 1. For a fixed subarray, if we list the distinct values in order, the gaps are exactly the edges between consecutive values where the difference is > 1. So the number of gaps is the number of "missing integers" between the min and max that are not in the set? No, it's the number of intervals between consecutive distinct values that have length > 1. 

Another perspective: f(L,R) = 1 + (number of values in (min(S), max(S)) \ S). That is, the number of missing values between the minimum and maximum. Because the set S is a subset of [min, max], and the number of segments is exactly the number of connected components, which is 1 + (number of holes). A hole is a missing integer between min and max. Indeed, if S is a subset of [min, max], then the number of segments is 1 + (number of x in [min, max] such that x is not in S, but there is some element of S less than x and some greater than x). Actually, it's exactly the number of missing integers in [min, max] that have both a smaller and a larger element in S. But since S is a subset, the number of segments is (max - min + 1) - |S| - (number of missing integers at the ends? No). Let's check: S = {1, 4}. min=1, max=4. The missing integers are 2, 3. The number of segments is 2. Here 2 segments, 2 missing integers. S = {1, 2, 4}. min=1, max=4. missing: 3. segments: {1,2} and {4} = 2. So segments = 1 + number of missing integers in [min, max] that are not in S? But 1 is in S, 2 in S, 4 in S. Missing is 3. So 1 + 1 = 2. Yes! S = {1, 3, 4}. min=1, max=4. missing: 2. segments: {1} and {3,4} = 2. 1+1=2. S = {1, 2, 3, 5}. min=1, max=5. missing: 4. segments: {1,2,3} and {5} = 2. 1+1=2. S = {1, 3, 5}. min=1, max=5. missing: 2,4. segments: 3. 1+2=3. So indeed, for a set S, the number of segments = 1 + number of integers in (min(S), max(S)) that are not in S. Wait, is this always true? Let's test S = {1, 2, 4, 5}. min=1, max=5. missing in (1,5): 3. segments: {1,2} and {4,5} = 2. 1+1=2. S = {1, 4, 6}. min=1, max=6. missing: 2,3,5. But wait, is 5 a missing that creates a segment? S has 1,4,6. The missing integers between 1 and 6 are 2,3,5. But the segments are {1}, {4}, {6} = 3 segments. 1 + 3 = 4? That's wrong. So the formula is not simply missing in (min, max). Because 5 is missing, but 4 and 6 are present, so the gap between 4 and 6 is created by the missing 5. But 2 and 3 are missing, but 1 and 4 are present, so the gap between 1 and 4 is created by both 2 and 3? Actually, the number of segments is the number of connected components. In {1,4,6}, the components are {1}, {4}, {6}. The missing integers are 2,3,5. The number of segments is 3. The number of missing integers is 3. But 1 + 3 = 4, not 3. So the formula "1 + missing in (min, max)" is incorrect. The correct formula is: number of segments = |S| - (number of adjacent pairs in S). And missing in (min, max) is (max - min + 1) - |S|. The number of segments is not simply related to missing in (min, max). 

Let's stick to f = distinct - adj. This is exact and easy to update.

We need to compute sum_{L,R} adj(L,R) efficiently. Let's try to compute sum of adj using a two-pointer approach but on the value space? There is a known algorithm: for each left L, we can find the right R such that the set of values is "contiguous" (f=1). But we need the sum for all R, not just when f=1. 

Wait, maybe we can compute the sum of f(L,R) directly by iterating over the array and using a stack to find the next position where a "gap" appears. Consider the array of values. We can think of the process of expanding the window to the right. The number of segments f changes only when we add a value that is not adjacent to any existing value, or when we add a value that bridges two existing segments. But as R increases, f can change multiple times. However, we can use a "divide and conquer" that processes the array in O(N log N) by splitting at the median and using two pointers with a Fenwick tree or something. 

Actually, there is a simpler solution using a stack. Let's think about the contribution of each position as the "right endpoint". For a fixed R, we want to compute the sum of f(L,R) for all L <= R. As L decreases from R to 1, we add values. The function f(L,R) as L moves is non-increasing? No, as L moves left (adding more values), f can increase or decrease. For example, R=3, A[1..3] = [1,3,4]. For L=3: {4} -> f=1. L=2: {3,4} -> f=1 (since 3,4 adjacent). L=1: {1,3,4} -> f=2 (1 and 3 not adjacent). So f increased. Can f decrease as L moves left? Yes, if adding a value bridges two segments. For example, R=3, A=[1,3,2]. L=3: {2} -> 1. L=2: {3,2} -> 1. L=1: {1,3,2} -> {1,2,3} -> 1. So it stayed 1, not decreased. Can it decrease? Suppose A=[1,3,2], R=3. L=3: f=1. L=2: {3,2} -> f=1. L=1: {1,3,2} -> f=1. No decrease. Try A=[1,3,5,4]. R=4. L=4: {4} ->1. L=3: {5,4} ->1. L=2: {3,5,4} -> {3,4,5} ->1. L=1: {1,3,5,4} -> {1}, {3,4,5} ->2. So f increased. To decrease, we need adding a value to merge segments. But if we add a value, it can only merge segments that are already present. But as L moves left, we are adding values that were previously not in the set. If the new value is between two existing segments, it merges them, reducing f. For example, suppose current set S for L=2, R=4 is {3,5,4} = {3,4,5}, f=1. Now move L to 1, add 1. New set {1,3,4,5}, f=2. That's an increase. What if the current set S has two segments, say {1,4}, f=2. Adding a value 2: new set {1,2,4}, f=2? Actually {1,2} and {4} -> 2 segments. Adding 3: {1,3,4} -> {1} and {3,4} -> 2. Adding 2 and 3: {1,2,3,4} -> 1. So to decrease, we need to add a value that is between two segments and bridges them. For example, current set S = {1,4} (f=2). Add 2: {1,2,4} (f=2). Add 3: {1,3,4} (f=2). Add 2 and 3 (by moving L further left): if we have both 2 and 3 in the left part, then when we include them, f drops to 1. But in the sliding window from L to R, as L decreases, we add one element at a time. So f can decrease when we add an element that is exactly between two segments. For instance, R=5, values: 1, 4, and somewhere in the left we have 2,3. Suppose the array is [2, 1, 4, 3, 5]? Let's construct: R=4: [1,4,3,5] -> values {1,3,4,5} -> f=2 ({1}, {3,4,5}). L=3: [4,3,5] -> {3,4,5} -> f=1. L=2: [1,4,3,5] -> f=2. L=1: [2,1,4,3,5] -> {1,2,3,4,5} -> f=1. So f went 2 -> 1 -> 2 -> 1. It decreased when we added 2 (from 2 to 1? Wait, L=4: {5} f=1. L=3: {3,5} f=2. L=2: {4,3,5} f=1 (decrease!). L=1: {2,4,3,5} f=2 (increase). So f can both increase and decrease as L moves left. So it's not monotone.

Thus, we cannot use a simple two-pointer where left moves and right is fixed, because the property "f is small" is not monotone. However, the sum over all subarrays can be computed by a divide and conquer that is O(N log N). Let's design a D&C that computes the sum for crossing subarrays.

Standard D&C for subarray problems: 
solve(l, r):
  if l == r: return 1 (since f(l,l)=1)
  mid = (l+r)//2
  ans = solve(l, mid) + solve(mid+1, r)
  // Now handle subarrays with L in [l, mid] and R in [mid+1, r]
  // We want to compute sum_{L=l..mid} sum_{R=mid+1..r} f(L,R)
  
  // To compute this efficiently, we can precompute the state of the right part for all R, and then iterate L from mid down to l, maintaining the state of the left part, and for each L, we need to compute the sum over R of f(L,R). 
  // If we can compute f(L,R) for all R in O(r - mid) time per L, total O(N^2). Not good.
  // But we can use the fact that as L moves left, we only add one value to the left set. We can maintain a data structure for the right part that allows us to compute the sum of f(L,R) quickly. 
  // Specifically, for a fixed left set S_L, we want to compute sum_{R} f(S_L ∪ S_R), where S_R is the set for a particular R. This is sum of (segments(S_L ∪ S_R)) over R. 
  // segments(S_L ∪ S_R) = segments(S_L) + segments(S_R) - (number of edges between S_L and S_R) + something? Actually, it's not additive because of overlaps.

Let's use the formula: f(L,R) = distinct(L,R) - adj(L,R). 
For a crossing subarray, distinct(L,R) = distinct(L,mid) + distinct(mid+1,R) - distinct_overlap, where distinct_overlap is the number of values that appear in both the left and right parts. Similarly, adj(L,R) = adj(L,mid) + adj(mid+1,R) + adj_cross, where adj_cross is the number of edges (v, v+1) with one endpoint in left and one in right. 
So f(L,R) = (d_L + d_R - d_overlap) - (e_L + e_R + e_cross) = (d_L - e_L) + (d_R - e_R) - d_overlap - e_cross = f_L + f_R - d_overlap - e_cross.
Here f_L = f(L,mid), f_R = f(mid+1,R). So f(L,R) = f(L,mid) + f(mid+1,R) - overlap(L,R), where overlap(L,R) = d_overlap + e_cross. d_overlap is the number of values that appear in both left and right parts. e_cross is the number of pairs (v, v+1) such that v is in left and v+1 in right, or v in right and v+1 in left. 
Thus, the sum over crossing subarrays: sum_{L,R} f(L,R) = sum_{L} sum_{R} [f(L,mid) + f(mid+1,R) - overlap(L,R)].
We can precompute for each L, the sum of f(mid+1,R) over R, which is just the sum of f_R for the right part. But we already have that from the recursive call? Actually, the recursive call for the right half gives the sum of f over all subarrays entirely in the right half. But we need the sum of f(mid+1,R) for a fixed L? No, f(mid+1,R) depends only on R, not on L. So sum_{L=l..mid} sum_{R=mid+1..r} f(mid+1,R) = (mid - l + 1) * sum_{R=mid+1..r} f(mid+1,R). Similarly, sum_{L} sum_{R} f(L,mid) = (r - mid) * sum_{L=l..mid} f(L,mid). So those parts are easy if we have the prefix sums of f for the left and right halves. 
The hard part is sum_{L,R} overlap(L,R). overlap(L,R) = d_overlap(L,R) + e_cross(L,R). d_overlap is the number of values present in both left and right parts. e_cross is the number of edges (v, v+1) with one in left, one in right. 
So we need to compute, for all L in [l, mid] and R in [mid+1, r], the quantity d_overlap + e_cross. 
Notice that d_overlap + e_cross is exactly the number of "connected components" in the union? Not exactly. But we can compute it efficiently by iterating over the right part and using a data structure for the left part.

Let's process the right part first. For each R from mid+1 to r, we can compute the state of the right part: the set of values present, and the number of segments f_R, but we need more: we need to know, for each value v, whether it is present in the right part. Actually, d_overlap is the size of the intersection of the value sets. e_cross is the number of v such that v in left and v+1 in right, plus v in right and v+1 in left. 
If we can, for a fixed left set, compute the sum over R of (d_overlap + e_cross), we can do it. But the left set changes as L decreases. 
We can process L from mid down to l. Maintain a frequency array for the left set. As we add a new value v = A[L], we update the left set's distinct count and its internal edges. But we also need to know how it interacts with the right sets. For each R, the contribution to overlap is: if v is in right set, then d_overlap increases by 1. Also, if v-1 is in right set, then e_cross increases by 1 (since v in left, v-1 in right => edge (v-1, v)). Similarly, if v+1 is in right set, e_cross increases by 1. So for a fixed L, the overlap(L,R) = (number of values in right set that are in left set) + (number of v in left set such that v-1 in right set) + (number of v in left set such that v+1 in right set). 
Let V_L be the set of values in left, V_R the set in right. Then overlap = |V_L ∩ V_R| + |{v in V_L : v+1 in V_R}| + |{v in V_L : v-1 in V_R}|. 
Note that the second term is the number of edges from V_L to V_R in the "forward" direction, and the third is "backward". 
So for a fixed left set V_L, we need to compute for each R: |V_L ∩ V_R| + (number of edges from V_L to V_R) + (number of edges from V_R to V_L). 
This can be computed if we know for each R, for each value v, whether v in V_R. We can precompute an array right_has[v][R]? No, that's too big. 
But we can process R from mid+1 to r and maintain a frequency array for the right set. As we expand R to the right, we add values. For each R, we can compute the state of the right set. Then for a fixed L, we want to sum over R of this overlap. If we process L from mid down to l, and for each L we want to compute the sum over R, we could iterate over all R? That would be O(N^2). 
We need a way to compute the sum of overlap(L,R) over all L,R efficiently. 
Notice that overlap(L,R) depends on V_L and V_R. It is a sum of indicator functions: 
For each value v, it contributes to overlap if:
- v in V_L and v in V_R (adds 1)
- v in V_L and v+1 in V_R (adds 1)
- v in V_L and v-1 in V_R (adds 1)
So we can write overlap(L,R) = sum_{v} I(v in V_L) * [ I(v in V_R) + I(v+1 in V_R) + I(v-1 in V_R) ].
Then the total sum over L,R is sum_v [ sum_{L} I(v in V_L) * sum_{R} (I(v in V_R) + I(v+1 in V_R) + I(v-1 in V_R)) ].
But this is not separable because the sum over L of I(v in V_L) and the sum over R of I(v in V_R) are independent! Actually, they are independent because the condition for L and R are separate. V_L depends only on the left part [L, mid], and V_R depends only on the right part [mid+1, R]. So for a fixed v, the contribution to the sum over all L,R of the term I(v in V_L) * I(v in V_R) is simply (number of L in [l, mid] such that v in V_L) * (number of R in [mid+1, r] such that v in V_R). This is because the events for L and R are independent given the division. Similarly, the term I(v in V_L) * I(v+1 in V_R) factors as (number of L with v in V_L) * (number of R with v+1 in V_R). And the term I(v in V_L) * I(v-1 in V_R) factors as (number of L with v in V_L) * (number of R with v-1 in V_R). 
This is a huge simplification! Because the sum over all crossing subarrays of overlap(L,R) can be computed by independently counting for each value how many left windows contain it, and for each value how many right windows contain it, and then combining. 
Let's verify: 
overlap(L,R) = sum_{v} [ I(v in V_L) I(v in V_R) + I(v in V_L) I(v+1 in V_R) + I(v in V_L) I(v-1 in V_R) ].
Sum over L in [l,mid], R in [mid+1,r] of overlap(L,R) = 
sum_{v} [ (sum_L I(v in V_L)) (sum_R I(v in V_R)) + (sum_L I(v in V_L)) (sum_R I(v+1 in V_R)) + (sum_L I(v in V_L)) (sum_R I(v-1 in V_R)) ].
This is correct because the sum over L and R of a product of a function of L and a function of R is the product of the sums. 
So we can precompute for the left part [l, mid] for each value v, the number of L in [l, mid] such that v appears in A[L..mid]. Let's denote left_cnt[v] = number of L in [l, mid] with v in V_L. Similarly, right_cnt[v]