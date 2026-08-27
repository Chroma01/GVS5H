
## ideation
The core difficulty lies in efficiently identifying the maximum size induced subgraph that matches the strict hierarchical structure of a Snowflake Tree. A Snowflake Tree is defined by a center vertex, $x$ hub vertices connected to it, and $y$ leaf vertices connected to each hub. The key insight is that for a fixed center vertex, the optimal configuration depends on selecting hubs with the largest available degrees to maximize the number of leaves $y$ they can support. Since $y$ is constrained by the hub with the fewest available neighbors (excluding the center), sorting neighbor degrees in descending order allows us to greedily evaluate all valid numbers of hubs $x$ in linear time relative to the degree of the center. The main challenge is ensuring the $O(N \log N)$ complexity stays within limits and correctly handling the constraint $y \ge 1$.

Potential pitfalls include:
- Incorrectly computing the total vertex count (must be $1 + x + x \cdot y$, which simplifies to $1 + x \cdot d_{(x)}$ where $d_{(x)}$ is the degree of the $x$-th hub).
- Forgetting that hubs must have degree $\ge 2$ to support at least one leaf ($y \ge 1$).
- Overlooking that the "center" of the Snowflake in the induced subgraph might originally be a leaf in $T$, so we must check every vertex as a potential center.
- Time complexity blow-up if sorting is not done efficiently or if unnecessary data structures are created.
