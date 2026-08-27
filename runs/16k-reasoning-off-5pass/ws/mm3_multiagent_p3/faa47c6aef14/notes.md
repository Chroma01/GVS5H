
## ideation
The problem couples two independent permutation systems (red via P, blue via Q) through shared operations. A red ball at node v reaches X only if v is in the P-cycle of X, by following P repeatedly. Same for blue with Q. If any ball is outside its respective X-cycle, the goal is impossible.

For one color, let `max_dist` be the maximum distance to X of any ball in X's cycle. To bring the furthest ball to X, we must operate on every node at distances 1..`max_dist` (each ball steps through each node). This needs exactly `max_dist` operations. The required nodes for red are the first `max_red` nodes going backward along P from X; similarly for blue.

These two sets of nodes can be processed in a single sequence because the precedence graph (red edges P, blue edges Q) is acyclic: each red edge strictly decreases P-distance, each blue edge strictly decreases Q-distance, so no cycles are possible. We can topologically sort to get a valid schedule where each node in the union is operated on exactly once. Thus the minimum number of operations is the size of the union of the two sets.

## worker: Implement the algorithm in Python: parse input, bu
The solution leverages the permutation cycle structure. For each color (red/blue), balls can only reach X if they lie in the same permutation cycle as X. Within that cycle, to consolidate all balls at X, we must operate on every node from the furthest ball down to distance 1. This requires `max_dist` operations per color. Since the two precedence constraints (red P-edges and blue Q-edges) both strictly decrease their respective distances, the combined dependency graph is a DAG, allowing a single topological pass where each node in the union is operated on exactly once. The minimum number of operations is therefore the size of the union of the two required node sets.
