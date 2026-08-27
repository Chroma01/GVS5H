
## ideation
The core difficulty is that each ball follows a deterministic route: a red ball repeatedly uses the edges \(i \to P_i\), while a blue ball uses \(i \to Q_i\). A ball can reach \(X\) only if its starting box lies on the same permutation cycle as \(X\) for its color. Otherwise the answer is impossible.

For one color, all balls on the cycle containing \(X\) impose one ordered chain of required operations: starting from the ball farthest from \(X\) in the direction of the permutation, every box on the route up to (but excluding) \(X\) must be operated. Balls of the same color can share operations once their routes meet, so only the union of these routes matters.

The remaining issue is that red and blue chains may share boxes. Operating a shared box at a suitable time can advance both chains simultaneously, reducing the number of operations. However, shared boxes cannot always all be synchronized: their orders may differ in the two chains. The maximum number of synchronizable boxes is an order-preserving common-subsequence problem.

Important pitfalls:
- A ball initially at \(X\) needs no operation.
- A color with no balls contributes no chain.
- A ball outside the cycle of \(X\) for its color makes the result impossible, even if the other color can reach \(X\).
- Operating \(X\) is never useful, since it would move balls away from the target.
- Simply counting the union of required boxes is incorrect when red and blue require opposite orders; repeated operations may then be necessary.
- Empty boxes should not be operated unless they are needed as transit points for a ball.
- The all-zero case must return zero immediately.

## worker: Derive and validate the exact minimum-operation fo
For each color, its movement follows a permutation cycle. Therefore every ball can reach `X` only if its initial box lies in the cycle of `X` for that color; otherwise the answer is `-1`.

Inside the relevant cycle, list boxes by increasing distance from `X` under the inverse permutation. If the farthest initial ball is at distance `D`, then every box on the route is needed, and the required operation order is the chain of those `D` boxes from farthest to nearest.

A valid operation sequence must contain the red chain and blue chain as subsequences. Conversely, any common supersequence of the two chains gives a valid schedule. Thus the minimum number of operations is the shortest common supersequence length:

`len(red) + len(blue) - LCS(red, blue)`.

Each chain has distinct vertices, so the LCS is computed by mapping blue-chain vertices to their positions and finding the LIS of the resulting red positions in `O(N log N)` time.

## worker: Fix `build_chain` so balls initially in box `X` ar
- Balls initially in box `X` are already at the target and are ignored.
- Any occupied box other than `X` must lie on the corresponding permutation cycle containing `X`; otherwise the answer is impossible.
- For each color, required operations form a chain from the farthest occupied box toward `X`.
- The minimum schedule is a shortest common supersequence of the red and blue chains, whose length is `len(red) + len(blue) - LCS`.
- Since each chain has distinct boxes, the LCS is computed in `O(N log N)` using LIS.
- The empty-chain case is handled explicitly, avoiding accidental inclusion of the entire cycle.
