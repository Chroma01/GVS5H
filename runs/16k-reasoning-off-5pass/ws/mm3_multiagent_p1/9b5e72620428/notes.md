
## ideation
The problem asks whether we can fill the -1 entries in A and B with non-negative integers and then permute A arbitrarily so that after pairing (by index) we have A_i + B_i equal to a common constant S for all i.

Key observations:
- Permuting A means we can match any A-value with any B-value. So the only constraints come from positions where both A_i and B_i are known (fully known pairs). They force the sum S to be exactly A_i + B_i.
- If there is at least one fully known pair, S is fixed. If there are multiple fully known pairs, they must all have the same sum.
- If there are no fully known pairs, S can be any non-negative integer; we can always choose S large enough.
- Once S is fixed (or chosen), we need to be able to assign non-negative values to all -1 entries:
  * For each i where A_i = -1 and B_i is known, we need A_i = S - B_i >= 0 => S >= B_i.
  * For each i where B_i = -1 and A_i is known, we need B_i = S - A_i >= 0 => S >= A_i.
  * For positions where both are -1, any non-negative values work.
- Also, the known A-values must be <= S (since they pair with some B >= 0). Similarly known B-values must be <= S.
- Since we can freely permute A, the multiset of A-values (after filling) just needs to contain the known A-values and some non-negative fills. This is always possible as long as each known A_i <= S.

So the algorithm:
1. Read N, arrays A, B.
2. Collect all indices where both A_i and B_i are known. Let known_sums = {A_i + B_i}.
3. If known_sums is empty: answer is always Yes (choose S = max(max(A), max(B)) or 0).
4. Else:
   - If known_sums has more than one distinct value: No.
   - Let S be that unique sum.
   - Check for every i:
     * If A_i != -1 and A_i > S: No.
     * If B_i != -1 and B_i > S: No.
     * If A_i == -1 and B_i != -1 and B_i > S: No (same as above).
     * If B_i == -1 and A_i != -1 and A_i > S: No.
   - If all checks pass: Yes.

Edge cases:
- All entries are -1: Yes.
- N up to 2000, values up to 1e9, sums up to 2e9, fits in 64-bit int.

Pitfalls:
- Forgetting that known A and B values individually must be <= S.
- Not handling the case of no fully known pairs correctly.
- Using 32-bit int might overflow; use Python int (unbounded) or long long.

## worker: Implement the solve() function in Python that read
The solution follows the reasoning in the PLAN:
- Collect sums from positions where both A_i and B_i are known.
- If there are no such positions, any S works → Yes.
- If there are multiple distinct sums → No.
- Otherwise S is fixed; verify every known A_i and B_i is ≤ S (which also covers the case where one is known and the other is -1, because the unknown must be S - known ≥ 0).
- The multiset condition on A is automatically satisfiable because we can permute A freely and fill its -1 entries with any non‑negative values (e.g., 0).
- Python integers are unbounded, so no overflow issues.
