
## ideation
The problem allows three operations:
1. Replace any `-1` in A with a non-negative integer.
2. Replace any `-1` in B with a non-negative integer.
3. Permute the elements of A arbitrarily.

Goal: make all entries non-negative and A_i + B_i equal to a common constant S for all i.

Key insight: Since A can be freely rearranged (whenever it helps), the pairing between fixed A-values and fixed B-values is flexible. The only thing that matters is the multiset of fixed A values and fixed B values, and the count of flexible slots on each side.

Let:
- `fixedA` = list of A_i that are not -1
- `fixedB` = list of B_i that are not -1
- `x` = count of -1 in A
- `y` = count of -1 in B

If `x == 0` and `y == 0`, no rearrangement and no replacements are possible. The answer is "Yes" iff the original A[i] + B[i] is already constant.

Otherwise, we have at least one flexible slot. We can permute A to pair the fixed A-values with fixed B-values in the way that makes matching easiest. The natural strategy: sort `fixedA` ascending and `fixedB` ascending and pair them up (or use all of one side's fixed values with the larger ones of the other, etc.). If the sorted pair sums `fixedA[i] + fixedB[i]` are all equal to some S, then:
- The `x` flexible A slots can be filled with 0.
- The `y` flexible B slots can be filled with S.
This works because each remaining slot is paired with a partner that already sums to S, and the new slot's value (0 or S) plus the partner's value gives S.

If the sorted pair sums are NOT all equal, can we still succeed by using a different pairing? No, because any pairing of k fixed A-values with k fixed B-values is achievable by permutation. The sorted (monotone) pairing is the only one that can equalize sums; any other pairing can only make things worse (by the rearrangement inequality / majorization argument). So the condition "sorted pair sums all equal" is both necessary and sufficient when flexibility exists.

Edge case: one of fixedA or fixedB may be empty. Then sorted pair sum check is vacuously true, meaning any S works. The flexible slots on the other side can be set to S - (the fixed value) or just S. This always succeeds as long as the fixed values on the non-empty side can be complemented to a constant S. Actually if fixedA is empty and fixedB has values, we can permute A (all -1) to pair with B, and set each A to S - B_i. As long as S >= max B_i, this is fine, and we can always pick S = max B_i. So it always works. The sorted check captures this (empty list trivially passes).

Therefore, the algorithm is:
1. If `x == 0 and y == 0`: check all A[i] + B[i] equal. Output Yes/No.
2. Else: sort `fixedA` and `fixedB` (in non-decreasing order). Check that `fixedA[i] + fixedB[i]` is the same for all valid i (i.e., min length of the two). Output Yes if all equal, else No.

Complexity: O(N log N) for sorting, N up to 2000, trivial.

Pitfalls:
- Forgetting the special case when x == 0 and y == 0 (no flexibility at all).
- When one side has no fixed values, the loop over pair sums is empty, which is vacuously true — correct, since we can always pick S appropriately.
- The values can be up to 1e9, but sums fit in 64-bit int (up to 2e9, no overflow in Python anyway).

## worker: Implement the `solve()` function in Python that re
The solution follows the plan exactly:

1. **Read input** and split into `fixedA`, `fixedB` with counts `x`, `y` for `-1` entries.
2. **Special case** (`x == 0 and y == 0`): No operations possible at all, so check if all `A[i] + B[i]` are already equal.
3. **General case**: With at least one flexible slot (either an `-1` to fill or the ability to permute A), sort the fixed values and verify the pairwise sums `fixedA[i] + fixedB[i]` are all constant.
4. **Edge case**: If one side has no fixed values (`k == 0`), the check is vacuously true — we can always pick a target sum `S` to accommodate.

The key reasoning: when flexibility exists, the rearrangement inequality tells us the monotone pairing (sort both, pair by index) is the pairing that equalizes sums. If even that pairing doesn't produce a constant sum, no other pairing can. If it does, the remaining flexible slots can be filled with `0` (for A) and `S` (for B) to complete the construction.
