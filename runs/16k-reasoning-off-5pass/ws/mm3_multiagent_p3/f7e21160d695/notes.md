
## ideation
The problem asks for the minimum possible sum of `f(A_i, B_{π(i)})`, where `f(x,y)` is the minimum possible maximum edge weight on a path between `x` and `y`.  

**Key observations**

1. `f(x,y)` equals the maximum edge weight on the unique path between `x` and `y` in **any** Minimum Spanning Tree (MST) of the graph (the MST is a minimum‑bottleneck spanning tree).  
2. Hence we can build one MST, and on this tree the value `f(x,y)` is just the maximum edge weight on the tree path.  
3. For a pair `(a,b)` the value `f(a,b)` is exactly the weight of the edge that first connects the two components containing `a` and `b` when we process the MST edges in **increasing order of weight** (Kruskal’s process).  

Thus each MST edge `e` of weight `w(e)` will be the “bottleneck” for some subset of the `K` pairs. If we let `x(e)` be the number of matched pairs that become connected when we add `e`, the total cost is  

```
answer = Σ w(e) * x(e)
```

`x(e)` is exactly the amount of flow that must cross the cut created by `e`. This is a classic min‑cost flow on a tree where each edge has a linear cost `w(e)`. The optimal flow can be found greedily:

* Process MST edges from smallest weight to largest.  
* Keep, for every current DSU component, the number of still‑unmatched `A` vertices (`a`) and `B` vertices (`b`).  
* When joining two components with an edge of weight `w` we may match  
  * `t1 = min(a_left, b_right)` pairs using an `A` from the left and a `B` from the right,  
  * `t2 = min(a_right, b_left)` pairs using an `A` from the right and a `B` from the left.  
  The total number of pairs matched now is `t1 + t2`, each incurring cost `w`.  
  Afterwards the component contains `a_left + a_right - (t1+t2)` unmatched `A`s and `b_left + b_right - (t1+t2)` unmatched `B`s.

Because edges are processed in non‑decreasing weight order, using a cheap edge as much as possible can never be worse than postponing a match to a more expensive edge – a standard exchange argument shows this greedy yields the global optimum.

## worker: Build an MST using Kruskal's algorithm on the give
- An MST is built using Kruskal's algorithm. For each edge that joins two different components we store it; this gives a tree with `N‑1` edges.
- The function `f(x,y)` equals the maximum edge weight on the unique path between `x` and `y` in any MST, so the tree obtained is sufficient.
- The problem becomes a minimum‑cost flow on a tree where each edge has linear cost equal to its weight. Processing edges from cheapest to most expensive and matching as many remaining `A`‑`B` pairs as possible at each step yields the optimal total cost.  
  This is a standard greedy exchange argument: postponing a match to a more expensive edge can only increase the total cost.
- The algorithm runs in `O((N+M) log N)` time (Kruskal sorting + DSU operations) and `O(N)` memory, well within the limits for `N, M ≤ 2·10⁵`.
