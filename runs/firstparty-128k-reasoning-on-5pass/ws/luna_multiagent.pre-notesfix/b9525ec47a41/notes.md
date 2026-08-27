
## ideation
The core difficulty is counting distinct indegree sequences rather than edge orientations. Different choices of cycle directions and spoke directions can produce the same local indegrees, so directly counting all orientations overcounts substantially.

Let a cycle edge variable record whether the edge from i to i+1 points into i+1. If the previous and current cycle variables are x_{i-1} and x_i, the cycle contributes 1 + x_{i-1} - x_i to vertex i. A spoke, when present, may add either 0 or 1. Thus each local indegree determines a relation between the incoming and outgoing cycle states, but at a spoke vertex some indegrees correspond to multiple possible transitions.

A useful observation is that the hub indegree does not need to be tracked separately. The sum of the local indegrees is N plus the number of spokes directed into their cycle endpoints, so it uniquely determines the hub indegree. Consequently, every valid local indegree word corresponds to exactly one complete indegree sequence, even if it has several orientation realizations.

The main task is therefore to count distinct length-N words accepted by a small position-dependent nondeterministic automaton:
- The state is the direction state of the cycle edge immediately before the current vertex, with two possible values.
- At a position with s_i = 0, each observed indegree allows only the corresponding cycle contribution.
- At a position with s_i = 1, an observed indegree can arise either from the cycle contribution alone or from the cycle contribution plus an incoming spoke.
- A word is valid if there is a cyclic path whose initial and final cycle states agree.

To remove overcounting caused by multiple paths for the same word, determinize at the level of binary relations on the two cycle states. A prefix induces a relation from its starting state to its ending state. There are only 16 possible relations on a two-element set, and starting from the identity relation, each possible observed indegree updates the relation by composition with a small transition relation determined by s_i and the indegree. After all N positions, accept exactly those relations containing (0,0) or (1,1), since some initial state must return to itself. Each observed indegree is counted once by the deterministic relation-state DP.

The alphabet is tiny:
- At a zero position, possible local indegrees are 0, 1, and 2.
- At a one position, possible local indegrees are 0, 1, 2, and 3.
The final DP therefore runs in O(N) time with a constant-sized state space and O(1) memory if only the current relation counts are retained. All counts are taken modulo 998244353.

Potential implementation checks:
- For a zero position, indegree 0 corresponds to cycle transition 0 to 1, indegree 2 to transition 1 to 0, and indegree 1 to staying in the same state.
- For a one position, indegree 1 is the union of the indegree-1 cycle transition and the indegree-0 transition followed by an incoming spoke; similarly indegree 2 is the union of the indegree-2 and indegree-1 possibilities. The indegrees 0 and 3 remain single transitions.
- Relation composition must preserve existential reachability, not count paths.
- Acceptance must test whether the final relation has a diagonal pair, rather than merely being nonempty.
- The hub is not an additional multiplicative choice: once the local indegrees are fixed, its indegree is forced.

## worker: Implement the 16-state relation-automaton DP, incl
Each cycle edge is represented by a bit indicating whether it points forward. At vertex `i`, if the previous and next cycle states are `a` and `b`, the cycle contributes `1 + a - b` to the indegree.

For a fixed observed local indegree, this gives a binary relation from `a` to `b`. A prefix of the cycle word therefore induces one of only 16 possible relations on two states. The DP counts distinct observed words by their induced relation, composing relations position by position.

The initial relation is the identity. After all `N` positions, cyclic consistency requires that the relation contain `(0,0)` or `(1,1)`.

The hub indegree is uniquely determined by the local indegrees, since the total indegree over all vertices equals the number of graph edges. Thus counting accepted local indegree words is exactly the desired answer.

The implementation uses constant-sized relation transitions and runs in `O(N)` time and `O(1)` additional memory.

## worker: Fix `zero_masks` so indegree 0 uses relation mask 
Fixed `zero_masks[0]` from `1` to `2`, correctly representing transition `(0,1)` for local indegree `0`.

The one-spoke masks remain `(2, 11, 13, 4)`. The DP determinizes all possible cycle-state relations, so each distinct local indegree sequence is counted exactly once. The hub indegree is uniquely determined by the local indegrees and the fixed total number of edges.

The corrected implementation gives `14` for sample 1 and `261339902` for sample 2. Exhaustive enumeration of all edge orientations on small instances also agrees with the relation-DP result.
