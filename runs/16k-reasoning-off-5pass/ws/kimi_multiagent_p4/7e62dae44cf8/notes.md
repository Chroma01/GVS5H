
## ideation
Core mechanics: Takahashi's occupied region grows by absorbing adjacent slimes; gaps are filled, so the region stays connected and the frontier is just all unabsorbed cells 4-adjacent to the region. Absorption condition: slime strength s is absorbable iff s < cur/X, i.e., s*X < cur (strict). Absorbing always strictly increases cur, which can only unlock more slimes — never hurts. Therefore greedy "absorb everything absorbable" is optimal; order among absorbable slimes doesn't matter for the final reachable set (monotone expansion: the set of absorbable cells only grows as cur grows).

Key insight for correctness: process frontier with a min-heap keyed on strength. Pop the smallest frontier slime; if s*X < cur, absorb it (cur += s, push its unvisited neighbors). If not absorbable, since it's the minimum on the frontier, no other frontier slime is absorbable either, so stop. This is O(HW log(HW)) — fine for 250k cells.

Pitfalls:
- Strict inequality: s*X < cur (not ≤). Sample 2 (X=1) tests this: equal strength can't be absorbed.
- Overflow: s up to 1e12, X up to 1e9 → s*X up to 1e21. Python handles big ints natively; in C++ need __int128 or careful division. Using Python here so it's safe.
- cur can grow to sum of all slimes ≈ 2.5e17, fine.
- Don't revisit cells: mark visited when pushed into heap to avoid duplicates (or when popped; pushing-time marking is cleaner and keeps heap smaller).
- Start: cur = S[P][Q], mark start visited, push its 4 neighbors.
- Answer is final cur (even if zero moves made).

Edge cases: 1x1 grid (no neighbors, answer is S[P][Q]); X=1 means only strictly smaller slimes absorbable; very large X means almost everything absorbable once frontier reached.

## worker: Implement the full Python solution: parse input, r
- Modeled Takahashi's occupied region as a growing connected set; the frontier is all unvisited cells 4-adjacent to it.
- Greedy optimality: absorbing any absorbable slime strictly increases `cur`, which can only enlarge the set of absorbable slimes (monotone). So absorbing everything absorbable yields the maximum final strength.
- Min-heap keyed on strength: pop the smallest frontier slime. If `s * X < cur` (strict inequality per problem statement), absorb it and push its unvisited neighbors. Otherwise, since it's the minimum, no frontier slime is absorbable — terminate.
- Mark cells visited at push time to avoid duplicates in the heap.
- Python big ints handle `s * X` up to 1e21 and `cur` up to ~2.5e17 without overflow concerns.
- Complexity: O(HW log(HW)) time, O(HW) space — fine for H,W ≤ 500 (250k cells).
- Verified logic against samples: Sample 1 → 28 (absorb 4, 6, 9; then 14*2=28 not < 28, stop). Sample 2 → 5 (X=1, equal strengths not absorbable). Sample 3 → 1343.
