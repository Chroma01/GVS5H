- **Label derivation:** Let `a_i = 1` mean cycle edge `(i, i+1 mod N)` is oriented `i -> i+1`, otherwise `0`. The cycle-edge contribution to vertex `i` is `c_i = a_{i-1} + (1 - a_i) = 1 + a_{i-1} - a_i`. Thus for transition `(a_{i-1}, a_i)`: `00 -> c=1`, `01 -> c=0`, `10 -> c=2`, `11 -> c=1`. If `s_i = 0`, `d_i = c_i`, so labels are `0,1,2` with forced transitions `01, {00,11}, 10`. If `s_i = 1`, the spoke may add `0` or `1` to `d_i`, giving labels: `0 -> 01`, `1 -> {00,01,11}`, `2 -> {00,10,11}`, `3 -> 10`.
- **Center degree uniqueness:** Let `K = popcount(s)`. Total edges are `N + K`, and the sum of all in-degrees equals the number of edges. Therefore `d_N = N + K - sum_{i=0}^{N-1} d_i`. Hence the center degree is uniquely determined by the first `N` degrees, so it is enough to count feasible prefixes.
- **Automaton view:** A prefix degree sequence is feasible iff it labels a walk in the two-state automaton whose states are the cycle-edge orientation bits. A full cycle is feasible iff the composed relation has a diagonal pair `(0,0)` or `(1,1)`.
- **Relation DP:** Track the binary relation from starting state to current state. Encode a subset of `{0,1}` as `0=empty, 1={0}, 2={1}, 3={0,1}`. A relation is a pair `(S0, S1)`, where `S0` is the set of reachable current states from start `0`, and `S1` from start `1`. Initial relation is `(1,2)`.
- **Transition functions on subsets:** For the four label types:
  - `U` (label `0`, edge `0->1`): `[0,2,0,2]`
  - `D` (forced down, edge `1->0`): `[0,0,1,1]`
  - `LE` (label `1` when `s_i=1`, relation `<=`): `[0,3,2,3]`
  - `GE` (label `2` when `s_i=1`, relation `>=`): `[0,1,3,3]`
  For `s_i=0`, labels use `U, identity, D`. For `s_i=1`, labels use `U, LE, GE, D`. Apply the same function to both components of `(S0,S1)`.
- **Reachable states:** Only 13 relations are reachable. The code uses this order:
  `0:(1,2), 1:(2,0), 2:(0,1), 3:(0,0), 4:(1,0), 5:(0,2), 6:(3,2), 7:(1,3), 8:(3,0), 9:(0,3), 10:(2,2), 11:(3,3), 12:(1,1)`.
  Invalid (no diagonal) states are exactly `1,2,3`; all others are accepted.
- **Implementation:** The code unrolls the inverse transition formulas for the two possible characters, giving O(N) time and O(1) memory. Counts are reduced modulo `998244353` every 14 characters to keep Python integers small while avoiding a modulo operation on every state update.
