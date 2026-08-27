1. The problem asks us to split an array into three non-empty contiguous subarrays and maximize the sum of distinct counts in each.
2. A naive O(N^2) approach checking all pairs (i,j) is too slow for N up to 3*10^5. We need an O(N) or O(N log N) approach.
3. Key observation: The total distinct count is maximized when we try to isolate unique elements or groups of unique elements. Specifically, if an element appears only once in the entire array, we can potentially "capture" it in one of the three segments without it being "wasted" by appearing in multiple segments (which doesn't happen since segments are disjoint) or being duplicated within a segment (which reduces the distinct count relative to its frequency).
4. Actually, a better approach is to iterate over the middle cut point `j` (from 2 to N-1) and for each `j`, find the best `i` (from 1 to j-1). However, this is still O(N^2) if not careful.
5. Let's use the property that the answer is at most 3 * (total distinct) but more tightly bounded. We can precompute prefix distinct counts and suffix distinct counts. Let `pre[i]` be the number of distinct elements in A[0..i-1] and `suf[j]` be the number of distinct elements in A[j..N-1].
6. For a fixed middle segment A[i..j-1] (0-indexed, so i from 1 to N-2, j from i+1 to N-1), the sum is `pre[i] + distinct(A[i..j-1]) + suf[j]`.
7. We can iterate `j` from 2 to N-1 (end of middle segment, 0-indexed j is the start of the right segment). For each `j`, we want to maximize `pre[i] + distinct(A[i..j-1])` for `1 <= i <= j-1`.
8. Let `mid[i][j]` be the distinct count of A[i..j-1]. This is hard to update quickly for all i.
9. Alternative: Iterate the right cut `j` (start of last segment). As we move `j` from 2 to N-1, the middle segment grows to the left? No, let's fix the middle segment's right end `k` (so middle is A[i..k-1]) and left end `i`.
10. Better strategy: Iterate the position of the second cut `j` (1-indexed, so right segment is A[j+1..N]). The middle segment is A[i+1..j]. We want to maximize `pre[i] + distinct(A[i+1..j]) + suf[j+1]`.
11. Let's iterate `j` from 2 to N-1. We maintain the distinct count of the middle segment as we vary `i`. This is tricky because changing `i` changes the prefix and the middle segment.
12. Standard solution for this problem: Iterate the middle cut `j` (from 2 to N-1). For each `j`, the term `suf[j+1]` is fixed. We need max over `i < j` of `pre[i] + distinct(A[i+1..j])`.
13. Notice that `distinct(A[i+1..j])` can be computed if we know the distinct count of `A[i+1..j-1]` and whether `A[j]` is new. But `pre[i]` also changes.
14. Efficient approach: Use the fact that most elements appear multiple times. The optimal solution often involves isolating elements that appear only once.
15. Let's count frequency of each element. Elements with freq 1 are "unique". Elements with freq > 1 are "common".
16. If we have many unique elements, we can put each in its own segment.
17. Algorithm:
    - Precompute `pre[i]` = distinct count in A[0..i-1] for all i.
    - Precompute `suf[i]` = distinct count in A[i..N-1] for all i.
    - Iterate `j` from 2 to N-1 (this is the end of the middle segment, 0-indexed, so middle is A[i..j-1] and right is A[j..N-1]). Wait, let's use 0-indexed carefully.
    - Let cuts be after index `i` and after index `j` with `0 <= i < j < N-1`.
    - Segments: A[0..i], A[i+1..j], A[j+1..N-1].
    - Sum = pre[i+1] + distinct(A[i+1..j]) + suf[j+1].
    - We iterate `j` from 1 to N-2. For each `j`, we want max over `0 <= i <= j-1` of `pre[i+1] + distinct(A[i+1..j])`.
    - Let `val[i] = pre[i+1] + distinct(A[i+1..j])`. When we move from `j` to `j+1`, the middle segment extends to include `A[j+1]`. The distinct count of A[i+1..j+1] is `distinct(A[i+1..j]) + (1 if A[j+1] not in A[i+1..j] else 0)`.
    - This still seems O(N^2) in worst case.
18. Optimized O(N) approach:
    - Count total distinct elements.
    - If all elements are distinct, answer is 3 * N? No, sum of distincts. If all distinct, any split gives 3 segments with distinct counts summing to N. So answer is N.
    - General case: The maximum possible answer is bounded by the total number of distinct elements in the array, plus potentially some "extra" if we can isolate duplicates? No, distinct counts in disjoint segments sum to at most the total distinct elements if each distinct element is counted once? No, a distinct element in a segment is counted once per segment it appears in? No, "count of distinct integers in subarray" means number of unique values in that subarray. Since subarrays are disjoint, a value appearing in multiple segments will be counted in each segment it appears in.
    - Example: 1, 2, 1. Split into [1], [2], [1]. Distincts: 1, 1, 1. Sum = 3. Total distinct in A is 2.
    - So we can "double count" values that appear in multiple segments.
    - Strategy: Iterate the middle segment's right boundary `j`. Maintain a data structure for `pre[i+1] + distinct(A[i+1..j])`.
    - Actually, we can iterate `j` from 1 to N-2. We maintain the array `D[i] = distinct(A[i+1..j])` for all `i < j`. When moving from `j` to `j+1`, `D[i]` increases by 1 if `A[j+1]` is not in `A[i+1..j]`.
    - This is still slow.
    - Known efficient solution: 
      1. Precompute `pre` and `suf`.
      2. Iterate `j` from 2 to N-1 (1-indexed, so right segment starts at j+1). Middle segment is A[i+1..j].
      3. For a fixed `j`, as `i` decreases from `j-1` to 1, `distinct(A[i+1..j])` increases.
      4. We can use a segment tree or similar to query max `pre[i+1] + distinct(A[i+1..j])`.
      5. When moving `j` to `j+1`, we update the distinct counts. The element `A[j+1]` will cause `distinct(A[i+1..j+1])` to increase for all `i` such that `A[j+1]` is not in `A[i+1..j]`. This corresponds to `i` being less than the previous occurrence of `A[j+1]`.
      6. Let `last_pos[x]` be the last seen position of value `x`. When processing `A[j+1]`, for all `i < last_pos[A[j+1]]`, the distinct count of the middle segment increases by 1. For `i >= last_pos[A[j+1]]`, it stays the same.
      7. So we need a range add on a segment tree for indices `0` to `last_pos[A[j+1]]-1` (adjusted for 0-indexing).
      8. The segment tree stores `pre[i+1] + current_distinct_middle[i]`. We query max over `i` in `[0, j-1]`.