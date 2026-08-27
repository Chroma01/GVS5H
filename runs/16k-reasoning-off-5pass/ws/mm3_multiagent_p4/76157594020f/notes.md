
## ideation
The problem asks for the minimum possible length of the longest uniform substring after at most `numOps` flips.

**Core difficulty:** Deciding how flips should be distributed to break long runs into shorter ones. The constraint `n ≤ 1000` allows `O(n log n)` or `O(n²)` solutions, but `O(n log n)` is preferable.

**Key insight:** The answer is monotonic in `L`. If we can achieve a maximum run length ≤ `L`, we can also achieve ≤ `L+1` (by doing nothing extra). So binary search on `L` is valid.

**Greedy check for a given `L`:** Scan `s` left to right. Maintain the length of the current run of identical characters. When the run length would become `L+1`, flip the current character (cost 1 op) to reset the run length. This greedy is optimal because flipping earlier only helps break the current run; postponing the flip would still need a flip somewhere in the run.

**Complexities:** 
- Binary search over `L` ∈ [1, n] → `O(log n)` steps.
- Each feasibility check → `O(n)`.
- Total: `O(n log n)`, which fits `n ≤ 1000`.

**Edge cases:** 
- `numOps = 0` → answer is the maximum run length in the original string.
- `numOps ≥ n` → we can alternate to make all runs length 1, so answer is 1 (but if `n=1`, answer is 1 regardless).
- Single character string → answer is 1.

**Pitfalls:** 
- Off-by-one errors when checking run lengths.
- Not handling the case where flipping a character changes the run of the *next* character (greedy naturally handles this).
- Binary search bounds: `low = 1`, `high = n` (inclusive). We want the minimum feasible `L`, so we use `while low < high: mid = (low + high) // 2` and adjust.

**Alternative approach (not needed):** DP or group runs and distribute flips among them. Possible but more complex.

## worker: Implement the `minLength` method in the `Solution`
- **Binary search** on the answer `L` (the maximum allowed run length). Monotonicity holds: if it's possible with max run ≤ L, it's also possible with max run ≤ L+1 (just do nothing extra).
- **Greedy check (`canAchieve`):** Scan left to right, tracking the current run length. When it reaches `L+1`, flip the current character (costs 1 op) and reset the run. This greedy is optimal: flipping the current position is the earliest opportunity to break the run, and any later flip would require at least as many operations.
- **Time complexity:** `O(n log n)` per test case. With `n ≤ 1000`, this is very efficient.
- **Edge cases handled:** `numOps = 0` (just find longest existing run), `numOps >= n` (answer is 1 for n > 1), single-character strings.
- All three examples pass, plus additional edge cases (single char, all same with various ops).
