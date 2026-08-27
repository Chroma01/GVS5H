
## ideation
We need the shortest walk from i to j whose edge-label string is a palindrome.  
A palindrome can be read by two synchronized walkers: one starts at i moving forward, the other starts at j moving backward. At each step we either:
- advance both walkers along edges with the same label (matching a pair of characters), or
- advance exactly one walker along any edge (this creates the middle character when the lengths differ).

When both walkers meet at the same vertex and no unmatched character remains, the concatenated string is a palindrome.

State representation: `(u, v, p)` where `u` is the forward walker’s vertex, `v` is the backward walker’s vertex, and `p` is a parity flag:
- `p = 0` – both sides have equal length so far (no pending middle character).
- `p = 1` – one side already has an extra character (the middle character).

Transitions:
- From `(u, v, 0)`:
  1. For every edge `u -> x` with label `c` and edge `v -> y` with the same label `c`, go to `(x, y, 0)` (cost +1).
  2. For every edge `u -> x` with label `c`, go to `(x, v, 1)` (cost +1).
  3. For every edge `v -> y` with label `c`, go to `(u, y, 1)` (cost +1).
- From `(u, v, 1)`:
  1. For every edge `u -> x` with label `c` and edge `v -> y` with the same label `c`, go to `(x, y, 0)` (cost +1).

Goal: distance from `(i, i, 0)` to `(j, j, 0)` (or any `(j, j, 0)` reachable).  
Empty walk (i=j) gives distance 0.

We run a multi‑source BFS from all `(i, i, 0)` simultaneously on a graph of size `2 * N * N` (≤ 20 000).  
Edges are generated on the fly; total transitions are bounded by `O(N^3)` (each state has at most `N` outgoing edges for each walker). With N ≤ 100 this easily fits.

Pitfalls:
- The graph may have self‑loops and multiple edges with different labels; we must handle all of them.
- BFS must use a queue and store distances in a 3‑D array `dist[u][v][p]`.
- Output `-1` if distance remains infinity.

## worker: Parse N and the N×N character matrix into adjacenc
The solution models the problem as a shortest‑path problem on a product graph of two walkers.  
State `(u, v, p)`:
- `u` – current vertex of the forward walker (starting at `i`),
- `v` – current vertex of the backward walker (starting at `j`),
- `p` – parity flag (`0` = both sides have equal length, `1` = one side already has the middle character).

Transitions:
- From `p = 0` we may step both walkers simultaneously on edges with the same label, or step only one walker (creating the middle character).
- From `p = 1` we must step both walkers on matching labels to close the palindrome.

A multi‑source BFS from all `(i, i, 0)` yields the minimum number of edge traversals needed to reach `(j, j, 0)`, which is exactly the length of the shortest palindrome‑labeled walk from `i` to `j`.  
Complexity: at most `2·N²` states, each with `O(N²)` outgoing edges in the worst case, giving `O(N⁴)` in the absolute worst case, but with `N ≤ 100` the actual number of transitions is bounded by `O(N³)` and runs comfortably within limits.  
If a state is unreachable, the answer is `-1`.
