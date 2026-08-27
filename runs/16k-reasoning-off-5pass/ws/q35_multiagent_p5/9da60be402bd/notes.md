
## ideation
The core difficulty lies in efficiently finding the shortest path where the edge labels form a palindrome. A naive BFS on the graph itself doesn't capture the palindrome constraint. The key insight is to model the state as a pair of vertices `(u, v)` representing the current "frontiers" of a palindrome being built from both ends.
1.  **State Definition**: `dist[u][v]` stores the minimum length of a path from `u` to `v` that forms a palindrome.
2.  **Transitions**:
    *   **Base Cases**:
        *   Length 0: `dist[i][i] = 0` for all `i` (empty path).
        *   Length 1: `dist[u][v] = 1` if there is an edge `u -> v`.
    *   **Expansion**: If we have a palindrome path from `y` to `x` of length `L` (state `(y, x)` with distance `L`), we can extend it to a palindrome from `u` to `v` of length `L+2` if there exists a character `c` such that:
        *   There is an edge `u -> y` with label `c`.
        *   There is an edge `x -> v` with label `c`.
        *   This corresponds to adding `c` to the beginning and `c` to the end of the existing palindrome.
3.  **Algorithm**: Multi-source BFS.
    *   Initialize `dist` matrix with infinity, `dist[i][i] = 0`.
    *   Identify all edges `u -> v`. Set `dist[u][v] = 1`.
    *   Queue contains all `(i, i)` with dist 0 and all `(u, v)` with dist 1.
    *   Process queue: For each `(y, x)` popped with distance `d`, iterate over all characters `c`. Find all incoming edges to `y` with label `c` (sources `u`) and all outgoing edges from `x` with label `c` (destinations `v`). For each pair `(u, v)`, if `d + 2 < dist[u][v]`, update `dist[u][v] = d + 2` and push `(u, v)`.
4.  **Complexity**: There are $N^2$ states. For each state, we iterate over 26 characters. For each character, we iterate over incoming/outgoing edges. In the worst case, a vertex has $N$ edges, so checking all pairs for a character takes $O(N^2)$. Total complexity $O(26 \cdot N^2 \cdot N^2) = O(26 N^4)$. With $N=100$, $N^4 = 10^8$, and $26 \cdot 10^8$ is too slow for typical time limits (usually $\sim 10^7-10^8$ ops/sec).
5.  **Optimization**: Instead of iterating all pairs for each character, we can precompute adjacency lists grouped by character.
    *   `incoming[c][v]`: list of `u` such that `u -> v` has label `c`.
    *   `outgoing[c][u]`: list of `v` such that `u -> v` has label `c`.
    *   When processing `(y, x)` with distance `d`, for each char `c`:
        *   Get list `U = incoming[c][y]`.
        *   Get list `V = outgoing[c][x]`.
        *   For each `u` in `U` and `v` in `V`, update `dist[u][v]`.
    *   The number of updates is bounded by the number of edges squared in the worst case, but typically much less. However, worst case is still dense.
    *   Actually, we can optimize further: The total number of edges is at most $N^2$. The inner loop runs for each character. The sum of sizes of `incoming[c][y]` over all `c` is `in_degree(y)`. Similarly for `outgoing`. The work per state `(y,x)` is $\sum_c |incoming[c][y]| \cdot |outgoing[c][x]|$. This is bounded by $N^2$ per state in worst case (e.g., all edges same label). So total is $O(N^4)$. $100^4 = 10^8$. This might be acceptable in C++ but risky in Python.
    *   Wait, is $O(N^4)$ really the bound? Yes. $N=100$ is small enough that $10^8$ simple operations might pass in 2 seconds in PyPy or even CPython if optimized, but it's tight.
    *   Let's check constraints again. $N \le 100$.
    *   Alternative: Floyd-Warshall like approach? No, BFS is better for shortest path.
    *   We must implement the BFS carefully.

Pitfalls:
- Forgetting that `dist[i][i] = 0` is a valid palindrome.
- Not handling the transition from length 0 to length 2 correctly (e.g., `i -> j -> i` with same label).
- Not initializing the queue with all base cases (0 and 1).
- Infinite loops if not checking `dist` before pushing.

## worker: Implement reading the input and constructing the g
The solution uses a multi-source BFS on the state space of vertex pairs `(u, v)`. The state `(u, v)` represents that we have found a palindrome path from `u` to `v`. The base cases are:
1.  `dist[i][i] = 0` for all `i` (empty path).
2.  `dist[u][v] = 1` if there is a direct edge `u -> v`.

The BFS expansion works by "growing" the palindrome from the inside out. If we have a palindrome path from `u` to `v` of length `d`, we can form a longer palindrome from `x` to `y` of length `d+2` if there exists a character `c` such that there is an edge `x -> u` with label `c` and an edge `v -> y` with label `c`. This corresponds to adding `c` to the beginning and `c` to the end of the existing palindrome.

The algorithm initializes the queue with all base cases. Then, it processes each state `(u, v)` by iterating over all 26 possible characters. For each character, it finds all possible predecessors `x` of `u` and successors `y` of `v` that use that character. If a new shorter path to `(x, y)` is found, it updates the distance and enqueues the new state.

The complexity is roughly $O(26 \cdot N^4)$ in the worst case due to the nested loops over sources and destinations for each character. Given $N \le 100$, this is approximately $2.6 \times 10^8$ operations, which might be tight for Python but should pass within typical time limits (2-3 seconds) if the constant factor is small, as many states will not have many incoming/outgoing edges for each specific character. The use of adjacency lists grouped by character helps prune the search space.
