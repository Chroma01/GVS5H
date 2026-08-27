
## ideation
**Core difficulty:**  
The problem is a variant of "select k points on a circle to maximize the minimum pairwise distance". The twist is the boundary points of a square, and the Manhattan distance along the perimeter behaves like a 1‑D circular distance.

**Key transformation:**  
Parameterize each boundary point by a single perimeter coordinate `p` (0 ≤ p < 4*side) obtained by walking the boundary in a fixed order (e.g. (0,0) → (side,0) → (side,side) → (0,side) → back to (0,0)). For any two points, the Manhattan distance along the boundary equals the circular distance on this 1‑D ring. (Because the square boundary is a closed loop, Manhattan distance measured along the boundary is exactly the minimal arc length between the points.)

**Reduction to 1‑D circular selection problem:**  
Sort the points by `p`. For a candidate distance `d`, the task becomes: can we pick `k` points on the ring such that every pair is at least `d` apart circularly? This is equivalent to finding a starting point `i` and then repeatedly jumping to the next valid point (the smallest index `j > i` with `p[j] - p[i] >= d`) `k‑1` times, requiring that after `k-1` jumps the last point is still within `<= 4*side - d` (i.e. the chain wraps around without violating spacing).

**Feasibility check details:**  
- Pre‑compute for each index `i` the smallest `j > i` with `p[j] - p[i] >= d`. This can be done with two pointers in O(n) per distance.
- For every start `i`, perform a greedy chain of `k-1` jumps. If the `k-1`‑th jump fits (the final index `< i + n` and the final point is within `4*side - d` of the start when unwrapped), then `d` is feasible.
- The number of starts is `n` and each chain is `O(k)`, giving `O(nk)` per feasibility test.

**Binary search:**  
The answer lies in `[0, 4*side]`. We binary search on integer `d`. There are at most `O(log(4*side)) ≈ O(log side + 2)` steps. Total complexity: `O(n log n + nk log side)`. With `n ≤ 15000` and `k ≤ 25`, this easily fits.

**Pitfalls to avoid:**  
- The mapping from 2‑D points to perimeter coordinate must respect the chosen order; any inconsistency will break the distance equivalence.
- The circular wrap‑around: the last selected point must be at most `4*side - d` ahead of the start, ensuring the arc from the last point back to the first point is also at least `d`.
- When pre‑computing `next[i]`, be careful that `next[i] - i` is a jump length in terms of indices, not necessarily `>= d` in coordinate difference; use the two‑pointer technique to guarantee `p[next[i]] - p[i] >= d`.
- The total perimeter `4*side` can be up to 4·10⁹, which exceeds 32‑bit int; use Python's arbitrary precision ints (no issue) but avoid overflow in other languages.
- Duplicate points are excluded by constraints, but we must handle the case where the array length is exactly `k` (then the only feasible `d` is the minimal pairwise distance, not necessarily `0`).

**Alternative approaches considered:**  
- DP on subsets (bitmask) is impossible because `n` is up to 15000.
- Greedy alone does not work for maximizing the minimum distance on a circle; binary search is required.
- Using the transformation to a 1‑D problem with a circular array and a “first point” enumeration is standard.

**Edge cases:**  
- `k == n`: answer is the minimum circular distance among all points; the algorithm still works.
- Points clustered together: the answer could be 0.
- `side == 1` and points on a small square: the perimeter is 4, distances are small.

## worker: Implement the solution: perimeter mapping, sorting
- Mapped each boundary point to a perimeter coordinate using the standard traversal order.
- Sorted the coordinates to enable two-pointer jumps.
- Duplicated the sorted array with `+perim` to handle circular wrap-around without modular arithmetic.
- The feasibility function precomputes `nxt[i]` for all `i < 2n` using a sliding window (two pointers) in O(n) time. Then for each of the `n` possible start indices, it greedily jumps `k-1` times. If the final point's coordinate minus the start is `<= perim - d`, the distance is feasible.
- Binary search over `[0, 4*side]` finds the maximum feasible `d`. Each step is O(n) + O(nk) = O(nk) (k ≤ 25, n ≤ 15000, so ~375k operations per step, times ~32 steps = ~12M, easily fits).
- Edge cases handled: `d = 0` (always feasible if k ≤ n), large perimeter, small `k`.
