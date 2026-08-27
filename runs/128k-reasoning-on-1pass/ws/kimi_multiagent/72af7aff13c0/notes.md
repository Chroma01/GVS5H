
## ideation
- The movement story is mostly irrelevant: keep `cur=(sh,sw)`, for each query move one guaranteed-valid step, then assign `A[cur]=a_i`. The real task is: maintain, under point updates, the weighted monotone-path sum  
  `F = sum_{paths (1,1)->(H,W)} prod A_cell mod p`.
- Core DP: `S[h][w] = A[h][w] * (S[h-1][w] + S[h][w-1])`, with a virtual boundary so `(1,1)` is seeded correctly and `A[1][1]` is included exactly once.
- Since `HW <= 2e5`, `m=min(H,W) <= 447`. Transposing the grid preserves the answer, so we may assume the DP sweeps across the long dimension `n=max(H,W)` with state size `m`. Be careful to keep Takahashi’s movement in original coordinates and only transpose for computation/storage.
- A column transfer is linear and lower-triangular. For a column with values `a_1..a_m`, its matrix has entries `T[r][c] = prod_{k=c..r} a_k` for `r>=c`, else `0`. Applying one column to a vector is `O(m)`; materializing it densely is `O(m^2)`.
- Main difficulty: composing these transfers fast enough. Dense composition is `O(m^3)` naive and too slow; storing dense matrices for every column is also impossible in bad shapes (`n*m^2 = HW*m` can be ~9e7 entries, and segment-tree nodes multiply that). The plan needs a representation where internal nodes/blocks are composed in about `O(m^2)` or better, or a block size chosen to balance rebuild vs query.
- Promising algebraic angle: away from zeros, `T_a = D_prefix * J * D_prefix^{-1}` where `J` is the all-ones lower-triangular `(I-shift)^{-1}`. Products may reduce to conjugations plus range-sum/prefix-sum middle matrices; this might yield `O(m^2)` merge. Zeros break division, so either avoid inverses or handle zero runs explicitly.
- A sqrt/block decomposition over the long dimension is plausible: rebuild one block after an update, combine block transfers with a vector for the root answer. Need choose block size from `n,m,Q`; worst shapes differ radically: `2 x 100000`, `447 x 447`, `20 x 10000`.
- Pitfalls: noncommutative order of transfers; boundary seed; transpose/direction mapping; repeated updates to same cell; zeros making ratio/division invalid; memory blowup from dense leaves; Python speed for `m` near 447 even if `HW` is small.

## worker: Implement a correct baseline first: parse input, s
- The brute-force reference is the standard full DP
  `dp[h][w] = A[h][w] * (dp[h-1][w] + dp[h][w-1])`, with a virtual source before `(1,1)`.
- The fast solver maintains exactly the left DP frontier and right suffix frontier around Takahashi’s current column using two stacks:
  - moving right pushes a newly computed left frontier and pops a suffix frontier;
  - moving left does the reverse.
- Since updates occur only in the current column, all stored left and right frontier vectors remain valid. Crossing a column recomputes the one frontier that must change.
- For a cell `v`, the total path sum is affine in `A_v`:
  `F = F_without_v + A_v * L_v * R_v`,
  where `L_v` and `R_v` are path sums up to the predecessors and from the successors of `v`. Thus an update changes the answer by `(new-old)*L_v*R_v`.
- Within a column, `L` and `R` arrays are maintained lazily while walking vertically:
  - stepping down repairs `L` of the destination;
  - stepping up repairs `R` of the destination.
  The other value is guaranteed valid by the last time the walk crossed that cell.
- The grid is optionally transposed. The orientation is chosen to minimize
  `number_of_rows * number_of_horizontal_moves`.
- No division is used, so zero values and repeated updates are handled directly.
- Complexity is
  `O(HW + Q + min(H * #(L,R moves), W * #(U,D moves)))`
  up to the constant-factor two passes for a horizontal move. Memory is `O(HW)`.
- The frontier invariant was checked against the full `O(HW)` DP on small cases, including zeros, repeated cells, and direction reversals.
