
## ideation
The operation moves every piece one step towards the chosen square i.  
Consequences:

* the number of pieces never changes;
* the distance between any two pieces never increases – it can only stay the same or shrink;
* after t steps each piece can move at most t squares, therefore a piece starting at p can be only at a position q with |p−q|≤t.

The pieces are indistinguishable and may share a square, so it is enough to have **at least one** piece on every square where B_i=1.

For a fixed t we ask whether we can choose distinct pieces for all target squares so that after t steps they can occupy those squares.  
If piece p is used for target x we need |p−x|≤t.  
If two consecutive chosen pieces are at positions p<q and are used for targets x<y, the distance between them must not increase, thus

```
y − x ≤ q − p .
```

These two conditions are also sufficient: when they hold we can move the chosen pieces towards their targets while keeping the intermediate pieces merged with one of the neighbours; the monotonicity of the distances guarantees that a suitable pivot exists at each step.

Hence the problem reduces to the following:

* let **P** = sorted positions of pieces (|P| = M);
* let **T** = sorted positions of target squares (|T| = K);
* we need M ≥ K, otherwise impossible;
* find the smallest integer t for which there exist indices  
  i₀ < i₁ < … < i_{K‑1} with

```
|P[i_j] − T[j]| ≤ t                (distance)
T[j+1] − T[j] ≤ P[i_{j+1}] − P[i_j] (gap)
```

The existence for a given t can be checked greedily: scan the targets in order, keep a pointer into **P**, and for the current target T[j] advance the pointer until the piece satisfies the lower bound  

```
lower = max( T[j] − t , last_p + (T[j] − T[j‑1]) )
```

where `last_p` is the position of the piece used for the previous target.  
If after advancing we have no piece or the piece is farther than `T[j] + t`, the test fails.

The minimal t can be found by binary search in the range `[0, N]` (the answer never exceeds N).  
If even `t = N` is infeasible, the task is impossible.

The whole procedure is linear in the size of the strings for each feasibility test, and binary search adds a factor log N.  
The sum of N over all test cases is ≤ 10⁶, so the total complexity is well within limits.

## worker: Parse each test case: read N, strings A and B.
**Why the greedy test works**  
Let the sorted positions of pieces be `P = (p₁ < p₂ < … < p_M)` and the required
positions be `T = (t₁ < t₂ < … < t_K)`.  
During the whole process the relative order of pieces never changes, therefore
the piece that finally occupies `t₁` must be the leftmost piece that reaches it,
the piece for `t₂` must be to the right of that piece, and so on.  

If a piece `p` is assigned to a target `t`, it needs at least `|p‑t|` steps.
For a fixed number of steps `d` the condition “piece `p` can cover target `t`”
is simply `t‑d ≤ p ≤ t+d`.  
Additionally the ordering forces the gap condition
`p_{j+1} – p_j ≥ t_{j+1} – t_j` for two consecutive assigned pieces.

The greedy scan described in `feasible(d)` checks exactly those constraints:
for the current target `t` it chooses the earliest still‑unused piece whose
position is at least `max(t‑d, previous_piece + (t‑previous_target))`
and not larger than `t+d`.  
If any target cannot be satisfied, no other assignment can – an exchange
argument shows the greedy choice never harms feasibility.  
Thus `feasible(d)` is true **iff** the configuration can be reached in `d`
operations.

**Searching the answer**  
The answer is the smallest `d` with `feasible(d) = true`.  
`feasible(d)` is monotone (if it works for `d`, it works for any larger `d`),
so binary search on `d ∈ [0, N]` finds the minimum in `O(log N)` steps.
The total work per test case is `O((M+K) log N)`, and the sum of `N` over all
test cases is ≤ 10⁶, easily fast enough.
