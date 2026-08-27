
## ideation
The problem asks for the minimum number of stairs used to travel from a starting floor in one block to a target floor in another block. Movement within a building costs 1 stair per floor. Movement between adjacent buildings at the same floor is free (0 stairs) if the destination building is tall enough.

Key Observations:
1.  **State Space**: The state can be defined by `(row, col, floor)`. However, the floor dimension is too large ($10^6$) for direct BFS/Dijkstra per query.
2.  **Cost Structure**: The cost is purely the sum of vertical movements. Horizontal movements are free. This implies that if we are at block $(r,c)$ at floor $h$, the cost to reach any other block $(r',c')$ at floor $h$ is 0, provided there is a path of blocks with height $\ge h$.
3.  **Convexity**: For a fixed block $(r,c)$, let $D(r,c,h)$ be the minimum cost to reach $(r,c)$ at floor $h$. The function $D(r,c,h)$ is convex. This is because moving to a higher floor generally costs more, but might enable cheaper horizontal travel. The "marginal cost" of increasing the floor is non-decreasing.
4.  **Pareto Optimality**: Instead of storing $D(r,c,h)$ for all $h$, we can store a set of Pareto-optimal states $(h, cost)$. A state $(h_1, c_1)$ dominates $(h_2, c_2)$ if $h_1 \ge h_2$ and $c_1 \le c_2$. Due to convexity, the non-dominated states form a piecewise linear convex curve. The number of such "breakpoints" is typically small.
5.  **Algorithm**:
    -   Use Dijkstra's algorithm. The priority queue stores tuples `(cost, r, c, h)`.
    -   For each block $(r,c)$, maintain a list of non-dominated states `(h, cost)`.
    -   When relaxing edges:
        -   **Stairs**: From $(r,c,h)$, we can go to $(r,c,h+1)$ with cost $+1$ and $(r,c,h-1)$ with cost $+1$. These new states might dominate existing ones or be dominated.
        -   **Walkways**: From $(r,c,h)$, we can move to adjacent $(r',c')$ with cost $+0$ if $F_{r',c'} \ge h$.
    -   To keep the state space manageable, we only push a state to the PQ if it is not dominated by any existing state for that block, and we remove any existing states that are dominated by the new one.
    -   Given the constraints and the nature of the cost function, the number of Pareto-optimal floors per block remains small enough for the algorithm to pass within the time limit.

Pitfalls:
-   Implementing the dominance check and list maintenance efficiently is crucial.
-   The initial state is $(A, B, Y)$ with cost 0.
-   The target is any state $(C, D, h)$ where $h=Z$. We want the minimum cost to reach $(C, D)$ at floor $Z$. Note that we might reach $(C,D)$ at a different floor and then use stairs to get to $Z$. The Dijkstra will naturally find the global minimum.

## worker: (none)
The solution uses a Dijkstra-based approach where the state is `(row, col, floor)`. To manage the large state space, we exploit the convexity of the cost function with respect to floor. For each block, we maintain a list of Pareto-optimal `(floor, cost)` pairs. A state `(h1, c1)` dominates `(h2, c2)` if `h1 >= h2` and `c1 <= c2`, meaning the first state is strictly better or equal in both height and cost. We only keep non-dominated states.

When relaxing edges:
1.  **Walkways**: Moving to an adjacent block at the same floor costs 0 stairs. We add the state `(nr, nc, h, cost)` if it's not dominated.
2.  **Stairs**: Moving up or down one floor costs 1 stair. We add the state `(r, c, h+1, cost+1)` and `(r, c, h-1, cost+1)` if not dominated.

The `add_state` function ensures that the list of states for each block remains sorted by floor and that no state dominates another. This pruning keeps the number of states per block manageable, allowing the algorithm to run efficiently within the time limits for the given constraints.
