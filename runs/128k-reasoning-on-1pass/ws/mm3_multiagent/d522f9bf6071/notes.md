
## ideation
**Core difficulty:** Select up to 4 non-overlapping intervals (strict non-overlap: `r[a] < l[b]`) with maximum total weight, and return the lexicographically smallest index set among all optimal solutions. The `n ≤ 5·10⁴` constraint and the need for tie-breaking (lexicographic order) make this a non-trivial DP problem.

**Key observations from the plan:**
- The "at most 4" constraint is a small constant → we can afford a DP with dimension `k = 0..4`.
- After sorting by right endpoint, the predecessor `prev[i]` (largest `j < i` with `r[j] < l[i]`) is found via binary search in `O(log n)`.
- For each `k`, we need the best `(weight, sorted_index_list)` among all `≤k`-interval solutions that end at or before index `j` — a prefix maximum query.
- A Fenwick tree (BIT) storing `(weight, list)` pairs with a custom comparator works for `O(log n)` updates and queries.
- Final answer picks best among `dpPrev[0..4]`.

**Pitfalls / risks:**
1. **Lexicographic comparison** must be on sorted index tuples, and ties on weight must be resolved by smaller index list.
2. **List construction**: when adding `orig[i]` to `bestPrevL`, must re-sort; could be slow if lists get large. With at most 4 indices, list length ≤ 4, so sorting is cheap.
3. **Strict non-overlap**: use `bisect_left(ends, l[i])` (not `bisect_right`) to ensure `r[j] < l[i]`.
4. **k = 0** represents "no intervals selected" — should always be `(0, ())`.
5. **Indexing**: examples show 0-based original indices; `enumerate` gives 0-based.
6. **Weights up to 10⁹, up to 4 intervals** → total ≤ 4·10⁹, fits in Python int.
7. **Empty result** is possible if `n = 0`? Constraint says `n ≥ 1`, but `k=0` (empty list) might be optimal if all weights are 0 (but weight ≥ 1 per constraints), so answer is never empty unless... actually weights are ≥ 1, so we always pick at least one interval if `n ≥ 1`. Still, the code should handle `k=0` correctly for completeness.
8. **BIT comparator**: must compare weight first, then lexicographic list. Python tuple comparison `<` works directly for the list part.
9. **Storing tuples in BIT**: using `()` for empty list is fine; comparison works.
10. **Performance**: O(n·k·log n) with n=5·10⁴, k=4, log n ≈ 16 → ~3.2·10⁶ ops, well within limits.

**Candidate alternative approaches considered:**
- **Segment tree**: works but BIT is simpler and sufficient.
- **O(n²) DP**: too slow for n=5·10⁴.
- **Greedy**: fails because weights are not proportional to length; need exact max-weight.
- **Knapsack-style DP**: doesn't apply because of interval structure.

**Plan validation:** The plan is sound and complete. The DP recurrence `dp[k][i] = max(dp[k][i-1], w[i] + best(k-1 prefix before i))` is correct, and the BIT-based prefix maximum is the right data structure.

## worker: Implement the full solution: sort intervals by rig
- **Sorting & predecessor** – Intervals are sorted by right endpoint `r` (ties by left). For each interval we compute `prev[i]` = largest index `j < i` with `r_j < l_i` using binary search (`bisect_left`). This guarantees that any interval placed before `i` must end before `i` starts (strict non‑overlap).
- **DP state** – `dpPrev[k]` stores the best `(weight, sorted_index_tuple)` using at most `k` intervals among intervals processed so far. The transition:
  * either skip interval `i` → keep `dpPrev[k]`,
  * or take interval `i` as the last one → add its weight to the best `(k‑1)`‑interval solution that ends before `l_i`.  
  The latter is obtained by a Fenwick tree prefix query.
- **Fenwick tree** – One BIT per `k` (0..4) stores the best state for each prefix. Each node keeps the better of its current value and a new value on update, and queries combine the best of the visited nodes. The comparator treats larger weight as better; on equal weight the lexicographically smaller sorted tuple wins.
- **Lexicographic tie‑breaking** – All lists are kept sorted. The BIT comparator and the final selection both compare tuples, which matches the required lexicographic order (shorter prefix is considered smaller).
- **Complexity** – Sorting `O(n log n)`, binary searches `O(n log n)`, DP `O(n·k·log n)` with `k = 4` → well under 10⁶ operations for `n = 5·10⁴`. Memory `O(n)` (five BITs + a few linear arrays).
