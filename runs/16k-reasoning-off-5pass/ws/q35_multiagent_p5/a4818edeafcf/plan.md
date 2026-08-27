1. The problem asks us to split an array into three non-empty contiguous subarrays and maximize the sum of distinct element counts in each.
2. A naive O(N^2) approach checking all pairs (i,j) is too slow for N up to 3*10^5. We need an O(N) or O(N log N) approach.
3. Let the split points be i and j (1 <= i < j <= N-1). The three parts are A[0..i-1], A[i..j-1], A[j..N-1] (using 0-based indexing for implementation).
4. We can precompute prefix distinct counts: `pre[k]` = number of distinct elements in A[0..k-1].
5. We can precompute suffix distinct counts: `suf[k]` = number of distinct elements in A[k..N-1].
6. The middle part is A[i..j-1]. Its distinct count is `total_distinct - distinct_in_prefix + distinct_in_middle_prefix`? No, that's not straightforward.
7. Alternative approach: Iterate over the first split point `i`. For a fixed `i`, we want to choose `j` (i+1 <= j <= N-1) to maximize `pre[i] + distinct(A[i..j-1]) + suf[j]`.
8. Note that `distinct(A[i..j-1]) + suf[j]` is not simply related to `pre` and `suf` of the whole array because of overlaps in counting.
9. However, we can rewrite the total score as: `distinct(A[0..i-1]) + distinct(A[i..j-1]) + distinct(A[j..N-1])`.
10. Let's use the fact that the total distinct elements in the whole array is D. The sum of distinct counts in three parts is at most D + (some overlaps). Actually, it's not bounded by D simply.
11. Better idea: Iterate `i` from 1 to N-2. For each `i`, we need to find `j` in [i+1, N-1] maximizing `distinct(A[i..j-1]) + suf[j]`.
12. Let `f(i, j) = distinct(A[i..j-1]) + suf[j]`. As `j` increases, `distinct(A[i..j-1])` is non-decreasing and `suf[j]` is non-increasing. This suggests we might use a two-pointer or a segment tree approach.
13. Actually, we can precompute for each starting position `i`, the function `g_i(j) = distinct(A[i..j-1]) + suf[j]`. We want max over `i,j`.
14. Let's reverse the iteration. Fix `j` and iterate `i`? No, the middle part depends on both.
15. Standard technique for this problem: 
    - Precompute `pre[k]` for all k.
    - Precompute `suf[k]` for all k.
    - For the middle part, note that `distinct(A[i..j-1]) = pre[j] - pre[i] + (correction for elements that appear in both prefix and middle)`. This correction is hard.
16. Alternative efficient approach: 
    - Iterate `i` from 1 to N-2. Maintain a data structure for the right part.
    - As `i` increases, the middle part starts later. We can maintain the distinct count of the middle part as we expand `j`.
    - Specifically, for a fixed `i`, as `j` goes from `i+1` to `N-1`, we add `A[j-1]` to the middle part. We can maintain the distinct count of the middle part in a variable.
    - But we need `max_j (mid_distinct + suf[j])`. We can precompute an array `max_suf_plus_mid`? No, `mid_distinct` depends on `i`.
17. Let's try this: 
    - Precompute `suf[k]` for all k.
    - Precompute `pre[k]` for all k.
    - Iterate `i` from 1 to N-2. 
    - For each `i`, we want `max_{j=i+1}^{N-1} (distinct(A[i..j-1]) + suf[j])`.
    - Let `mid_dist(j) = distinct(A[i..j-1])`. 
    - We can compute `mid_dist(j)` for all `j` starting from `j=i+1` by incrementally adding elements.
    - But doing this for each `i` is O(N^2).
18. Optimization: 
    - Notice that `distinct(A[i..j-1]) + suf[j]` can be rewritten. 
    - Let's use a segment tree or similar structure. 
    - Actually, a known solution for this problem is to iterate `i` and maintain the best value for the right side.
    - Let's define `val[j] = suf[j]`. When we move `i` to `i+1`, the middle part changes. The element `A[i]` is removed from the middle part (if it was there) and added to the left part.
    - This is complex. Let's use a simpler O(N log N) or O(N) approach.
19. Correct efficient approach:
    - Precompute `pre` and `suf`.
    - Iterate `i` from 1 to N-2.
    - For the current `i`, the middle part is `A[i..j-1]`. 
    - We can precompute for each position `k`, the next occurrence of `A[k]` to the right, say `next_occ[k]`.
    - The distinct count of `A[i..j-1]` is the number of indices `k` in `[i, j-1]` such that `next_occ[k] >= j` (i.e., the first occurrence in the middle part is the one that counts? No, distinct count is the number of unique values. An element `x` contributes to the distinct count of `A[i..j-1]` if its first occurrence in `A[i..N-1]` is before `j`? No.
    - An element `x` is in `A[i..j-1]` if its first occurrence >= i and last occurrence <= j-1? No, it's in the subarray if at least one occurrence is in `[i, j-1]`.
    - Distinct count of `A[i..j-1]` = number of unique values that appear in `A[i..j-1]`.
20. Let's use the following trick:
    - Total answer = `pre[i] + distinct(A[i..j-1]) + suf[j]`.
    - We can iterate `j` from 2 to N-1 (as the start of the third part, so middle part ends at j-1).
    - For a fixed `j`, we want to maximize `pre[i] + distinct(A[i..j-1])` for `i` in `[1, j-1]`.
    - Let `h(j, i) = pre[i] + distinct(A[i..j-1])`.
    - As `j` increases, the middle part `A[i..j-1]` grows by adding `A[j-1]`.
    - We can maintain for each `i` the value `distinct(A[i..j-1])`.
    - When we move from `j` to `j+1`, we add `A[j]` to the middle part for all `i <= j`.
    - Adding `A[j]` to the middle part increases `distinct(A[i..j])` by 1 if `A[j]` does not appear in `A[i..j-1]`.
    - `A[j]` does not appear in `A[i..j-1]` if the last occurrence of `A[j]` before index `j` is before `i`. Let `prev_occ[k]` be the previous occurrence of `A[k]`. Then `A[j]` is new in `A[i..j-1]` if `prev_occ[j] < i`.
    - So for all `i` in `(prev_occ[j], j]`, `distinct(A[i..j])` increases by 1.
    - We can use a segment tree with range add updates and range max queries.
    - Initialize segment tree for `i` from 1 to N-2. Initially, for `j=1` (middle part empty? No, middle part must be non-empty, so `j >= i+1`).
    - Let's set up the segment tree for `i` from 1 to N-2.
    - Start with `j=2`. Middle part is `A[1..1]` (if i=1). 
    - Actually, let's iterate `j` from 2 to N-1. The middle part is `A[i..j-1]`.
    - We maintain an array `D[i] = distinct(A[i..j-1])` for all `i <= j-1`.
    - Initially, for `j=2`, `i` can only be 1. `D[1] = distinct(A[1..1]) = 1`.
    - We want to query `max_{i=1}^{j-1} (pre[i] + D[i])`.
    - Then add `suf[j]` to this max to get a candidate answer for split at `i, j`.
    - When moving from `j` to `j+1`, we add `A[j]` to the middle part.
    - For all `i` such that `prev_occ[j] < i <= j`, `D[i]` increases by 1.
    - We update the segment tree: range add 1 to `[prev_occ[j]+1, j]`.
    - Then query max in `[1, j-1]` (since `i <= j-1` for middle part to be non-empty and third part to be non-empty? No, third part is `A[j..N-1]`, so `j <= N-1`. Middle part `A[i..j-1]` non-empty implies `i <= j-1`. Left part `A[0..i-1]` non-empty implies `i >= 1`.
    - So for each `j` from 2 to N-1:
        1. Update segment tree: range add 1 to `[prev_occ[j]+1, j]`. Note: `prev_occ[j]` is the index of the previous occurrence of `A[j]`. If no previous occurrence, `prev_occ[j] = -1`.
        2. Query max in `[1, j-1]` from the segment tree. Let this be `M`.
        3. Candidate answer: `M + suf[j]`.
        4. Update global maximum.
    - The segment tree stores `pre[i] + D[i]`. Initially, for `j=1`, we haven't started. 
    - Let's initialize the segment tree with `pre[i]` for all `i`. And `D[i]` starts at 0 for all `i`.
    - When `j=2`, we add `A[1]` to the middle part. `prev_occ[1]` is the previous occurrence of `A[1]`. If none, -1. Range add 1 to `[0, 1]`? But `i` starts at 1. So `[max(1, prev_occ[1]+1), 1]`.
    - Actually, we can initialize the segment tree with `pre[i]` for `i` in `[1, N-2]`. `D[i]` is 0 initially.
    - Then for `j` from 2 to N-1:
        - Update range `[prev_occ[j]+1, j]` with +1. (Clamp indices to `[1, N-2]` for the segment tree range, but the update affects `i` up to `j`. Since we only query up to `j-1`, and `i` must be <= `j-1`, we can update up to `j` but it won't affect query for current `j` if we query before update? No, we update then query.
        - Wait, when we add `A[j]`, it affects `D[i]` for `i` in `(prev_occ[j], j]`. The query is for `i` in `[1, j-1]`. So the update affects the query range.
        - Query max in `[1, j-1]`.
        - Add `suf[j]`.
    - This is O(N log N).