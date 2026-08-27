
## ideation
- The array is already sorted non‑decreasing, so a pair (i, j) with i < j is valid iff `2 * A[i] <= A[j]`.
- The problem asks for the maximum number of **disjoint** pairs satisfying that condition.
- This is a classic “matching” problem on a sorted sequence with a simple greedy: always try to pair the smallest still‑available mochi with the smallest larger mochi that can host it.
- Two‑pointer algorithm:
  * `i` points to the smallest mochi not yet used.
  * `j` scans from left to right as the potential top mochi.
  * For each `j`, move `i` forward until either `i == j` or `2 * A[i] <= A[j]`.
  * If `i < j` and the condition holds, pair them, increment answer, advance `i`.
  * If `i == j`, we cannot pair this `j` with anything; continue.
- Complexity: O(N) time, O(1) extra space; N ≤ 5·10⁵, A_i ≤ 10⁹ → 2·A_i fits in 64‑bit, but using Python integers is safe.
- Pitfalls:
  * Must ensure `i` never overtakes `j`.
  * After a successful pair, `i` should be incremented before moving to the next `j`.
  * Edge cases: N = 2, all elements equal, strictly increasing.

## worker: Implement the two-pointer greedy solution in Pytho
The algorithm uses a two‑pointer greedy: the array is already sorted, so we keep a pointer `i` to the smallest unused mochi and a pointer `j` scanning the larger ones. For each `j`, we try to pair it with the current `i` if `2 * A[i] <= A[j]`. If the condition holds, we form a pair, increment the answer, and advance `i`. If `i` reaches `j`, we skip this `j` by incrementing `i` (so `i` stays ahead of `j`). This yields the maximum number of pairs in O(N) time and O(1) extra space. The multiplication `A[i] * 2` is safe in Python (arbitrary precision). The loop correctly handles cases where no pair can be made (e.g., all elements equal) and large inputs up to 5·10⁵.
