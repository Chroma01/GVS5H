- **Feasibility:** A red ball follows the directed cycle of permutation `P`, while a blue ball follows the directed cycle of `Q`. Every ball must belong to the cycle containing `X` for its color; otherwise it can never reach `X`, so the answer is `-1`.

- **Cycle direction:** Traverse a color’s cycle starting at `X`: `[X, v1, v2, ...]`, where each vertex points to the next one under that color’s permutation. A ball at `vk` moves forward through `vk, v{k+1}, ...` and eventually reaches `X`.

- **Active sequence:** If the earliest positive cycle position containing a ball is `k`, then all vertices from `vk` through the end of the cycle must be operated. The required event sequence is therefore the forward suffix `cycle[k:]`. Balls initially at `X` require no operation. If all balls are at `X` or absent, the sequence is empty.

- **One event per active vertex:** For one color, every vertex in its active suffix must be operated at least once. Operating those vertices exactly once in suffix order is sufficient because all balls move forward toward `X`, and all balls at a vertex can be transferred together.

- **Combining colors:** An operation can simultaneously realize one red event and one blue event only if both event sequences request the same vertex at that point. Shared operations must preserve the order in each sequence, so the shared vertices form a common subsequence.

- **Optimality:** Given a common subsequence of length `L`, merge the two event sequences by identifying those matching events, obtaining `len(red) + len(blue) - L` operations. Conversely, every shared operation yields a common subsequence, so no schedule can save more than the LCS length.

- **LCS computation:** Each active sequence contains distinct vertices. Map blue vertices to their positions, keep the positions corresponding to red vertices also appearing in blue, and compute the longest strictly increasing subsequence. This equals the LCS and takes `O(N log N)` time.

- **Complexity:** Cycle traversal and feasibility checks take `O(N)` time. The LIS computation takes `O(N log N)` time, with `O(N)` memory.
