
## ideation
The problem asks to simulate the presence of smoke at a fixed cell `(R,C)` at each half-integer time `t+0.5` for `t=1..N`, given a sequence of wind directions. The process starts with a particle at `(0,0)`. At each integer time `t`, all existing particles are shifted by the wind vector, and if the origin `(0,0)` is empty after the shift, a new particle is generated there.

A careful analysis of the birth times reveals that a new particle is generated at time `b` (`b ≥ 1`) if and only if the prefix sum `P_b` (the position of the initial particle after wind `b`) is not equal to any `P_{b'}` for previous birth times `b' < b`. The set of birth times `B` can be computed iteratively: start with `B = {0}`, and for `i = 1..N`, add `i` to `B` if `P_i` is not in the set `{P_j : j ∈ B, j < i}`.

The set of occupied cells at time `t` is then `{ P_t - P_b : b ∈ B, b ≤ t }`. Thus, `(R,C)` is occupied at time `t+0.5` iff there exists a birth time `b ∈ B` with `b ≤ t` such that `P_b = P_t - (R,C)`. This can be checked efficiently for all `t` by maintaining a hash set of the prefix sums at birth times as we iterate `t` from 1 to `N`, and for each `t` testing whether `P_t - (R,C)` is in that set. The answer is 1 if it is, else 0.

The constraints allow an `O(N)` solution with a hash set. The prefix sums are pairs `(r,c)`, and we can use a dictionary mapping tuples to booleans or store them in a set of encoded integers (e.g., `(r << 32) | (c & 0xffffffff)`) to be safe with Python's integer sizes.

## worker: <omitted because the solution is already correct a
The algorithm works by maintaining the set of prefix sums at birth times. A new particle is generated at time `t` iff the prefix sum `P_t` is not already in the set of prefix sums at previous birth times. The query at time `t+0.5` is answered by checking if `P_t - (R,C)` is in that set, with a special case for the origin. The time complexity is `O(N)` and memory `O(N)`.
