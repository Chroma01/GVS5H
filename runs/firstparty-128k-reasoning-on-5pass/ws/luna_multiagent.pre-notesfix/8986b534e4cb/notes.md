
## ideation
The core reduction is to prefix potentials: let \(X_1=0\) and \(X_{j+1}=X_j+w_j\). For a person traveling from \(S\) to \(T\), zero stamina at both endpoints means \(X_S=X_T\). For every internal town \(v\), the inequality depends on travel direction: if \(S<T\), then \(X_v>X_S\); if \(S>T\), then \(X_v<X_S\). Thus each person contributes one equality between two towns and many strict difference constraints.

For any fixed set of people, contract all towns joined by the equality constraints. The remaining strict constraints form a directed graph: an edge \(u\to v\) means \(X_v\ge X_u+1\). The system is feasible exactly when this graph has no directed cycle, including a self-loop created when an equality component contains a constrained internal town. If the graph is acyclic, assigning each component a sufficiently large topological rank gives valid integer potentials.

The difficult part is answering up to \(2\cdot 10^5\) contiguous-subarray feasibility queries without rebuilding this contracted directed graph for every query. Adding a person both introduces an equality merge and introduces many directed interval constraints; equality merges can change the meaning of all previously added edges, so a simple union-find alone is insufficient. Direction must also be handled carefully: reversing a person reverses every inequality.

## worker: Derive a necessary-and-sufficient structural chara
The program contracts all endpoint equalities with DSU. Strict inequalities are represented as directed edges:

- For a journey from `a` to `b` with `a < b`, the endpoint component must precede every selected endpoint strictly inside `(a,b)`.
- For the reverse direction, every selected endpoint inside `(a,b)` must precede the endpoint component at `b`.

A segment tree compactly represents all selected endpoints inside an interval. The resulting directed graph is feasible exactly when it is acyclic, which is checked by Kahn’s algorithm.

## worker: Derive and implement a near-linear or \(O((N+M)\lo
- Each journey becomes an interval `[a,b]` with a sign:
  - `+`: every internal potential is larger than the endpoint potential.
  - `-`: every internal potential is smaller.
- A set is infeasible exactly when it contains:
  1. Two intervals with the same left endpoint.
  2. Two intervals with the same right endpoint.
  3. Two strictly crossing intervals with the same sign.
- Properly nested intervals and intervals that merely touch (`a < b == c < d`) do not conflict.
- The sweep processes people in order of their indices. Two segment trees per sign report and deactivate earlier intervals that become conflicting with the current interval.
- Each interval is deactivated at most once, so the total reporting work is near-linear; tree operations cost `O(log N)` amortized per interval.
- `boundary[L]` is the first index that causes a conflict in a suffix beginning at `L`. A query `[L,R]` is feasible iff `R < boundary[L]`.
