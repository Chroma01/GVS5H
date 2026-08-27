**Solution Explanation**

For every `i (1 ≤ i ≤ N)` the value `x_i` has to satisfy  

```
x_i ≤ x_{A_i}                (1)
```

`A` is a functional graph – each vertex has exactly one outgoing edge.
A functional graph consists of several directed cycles, each with a rooted
tree whose edges are directed towards the cycle.

```
          tree                tree
            \                /
             v              v
      … → u → c1 → c2 → … → ck   (a directed cycle)
```

*   Along a directed edge the values must be non‑decreasing.
*   Traversing a path repeatedly gives `x_i ≤ x_j` for every reachable `j`.

Therefore for every vertex `v`

```
x_v ≤ x_root_of_its_component          (2)
```

where the *root* is the (unique) vertex of the directed cycle that is
reached from `v`.  
All vertices of one cycle must have the same value (the cycle forces
`x ≤ x ≤ … ≤ x`).

So a component is completely described by

* the common value `c` of its cycle (`1 … M`);
* for every tree attached to a cycle vertex, the values inside the tree
  are only constrained by `x ≤ c`.

--------------------------------------------------------------------

#### 1.   DP for a tree

For a vertex `v` belonging to a tree (i.e. `v` is not on a cycle) let  

```
dp[v][k] = number of assignments of the subtree of v
           with x_v = k        ( 1 ≤ k ≤ M )
```

If `v` is a leaf, `dp[v][k] = 1` for all `k`.
Otherwise let `children(v)` be the vertices `u` with `A_u = v`.
A child may only take a value `≤ k`, therefore

```
dp[v][k] = ∏_{u ∈ children(v)}   ( Σ_{t=1..k} dp[u][t] )            (3)
```

Define the prefix sums

```
pref[v][k] = Σ_{t=1..k} dp[v][t]        (k ≥ 1)
```

For a leaf `pref[v][k] = k`.  
All `pref` values are needed for the parent, so they are stored.

Processing order  
All tree vertices are removed first by a Kahn‑style elimination of
vertices with indegree `0`.  
The order in which they are removed is a topological order from leaves
to the cycle.  
Processing the vertices **in reverse** of this order guarantees that
all children of a vertex are already known – exactly what the DP needs.

The whole DP needs `O(N·M)` time and `O(N·M)` memory
(`N , M ≤ 2025` → about 4·10⁶ integers).

--------------------------------------------------------------------

#### 2.   Counting a component

For a component (one directed cycle) let  

```
R = list of roots of the trees attached to the cycle
```

For a fixed common cycle value `c`

```
contribution of the component for value c
      = ∏_{r ∈ R} pref[r][c]                                 (4)
```

`pref[r][c]` already counts all possibilities of the tree whose root is
`r` and whose maximal allowed value is `c`.

The component may be assigned any value `c = 1 … M`, therefore

```
value_of_component = Σ_{c=1..M}  ( ∏_{r∈R} pref[r][c] )       (5)
```

If a component has no attached tree the product is `1` and the sum is
`M` – exactly the number of ways to choose the common cycle value.

--------------------------------------------------------------------

#### 3.   Whole answer

Different components are independent, thus the final answer is the
product of the values of all components, taken modulo  

```
MOD = 998244353
```

--------------------------------------------------------------------

#### 4.   Correctness Proof  

We prove that the algorithm returns the number of sequences `x`
satisfying (1).

---

##### Lemma 1  
For every vertex `v` that is not on a cycle and for every `k (1≤k≤M)`  
`dp[v][k]` equals the number of assignments of the subtree of `v`
with `x_v = k`.

**Proof.** By induction on the height of `v`.

*Base – leaf.*  
A leaf has no children, the only restriction is `x_v = k`.  
Exactly one assignment exists, `dp = 1`.

*Induction step.*  
Assume the statement true for all children of `v`.  
A child `u` may take any value `t` with `1 ≤ t ≤ k`; by induction the
number of possibilities for the child subtree with `x_u = t` is
`dp[u][t]`. Summation over all admissible `t` gives
`Σ_{t=1..k} dp[u][t]`.  
All children are independent, therefore the product over all children
counts exactly the assignments with `x_v = k`. This is exactly (3). ∎



##### Lemma 2  
For every non‑cycle vertex `v` and every `k`  

`pref[v][k] = Σ_{t=1..k} dp[v][t]` holds,
i.e. `pref[v][k]` is the number of assignments of the subtree of `v`
with `x_v ≤ k`.

**Proof.** Immediate from the definition of `pref` and Lemma&nbsp;1. ∎



##### Lemma 3  
Consider a component consisting of a directed cycle `C` and the set `R`
of roots of the trees attached to the vertices of `C`.  
For a fixed integer `c (1≤c≤M)` the number of assignments of the whole
component with the common cycle value `c` equals  

```
∏_{r∈R} pref[r][c] .
```

**Proof.**  
All vertices of `C` must have the value `c`.  
Take a tree rooted at `r∈R`.  
Every vertex of the tree is ≤ its parent, therefore the maximal value
appearing in the tree is at most `c`.  
Conversely, for any assignment of the tree whose values do not exceed `c`
the root’s value is some `k ≤ c`; the number of such assignments is
`pref[r][c]` by Lemma&nbsp;2.  
Trees are attached to different cycle vertices, hence they are independent.
Multiplying the numbers of possibilities of all trees yields the formula. ∎



##### Lemma 4  
For a component the algorithm computes  

```
value_of_component = Σ_{c=1..M}  ( ∏_{r∈R} pref[r][c] ) .
```

**Proof.**  
The algorithm multiplies the arrays `pref[r][c]` (one entry for each `c`)
over all roots `r∈R`. This yields exactly the product
`∏_{r∈R} pref[r][c]` for every `c`.  
Summation over `c = 1 … M` gives the claimed expression. ∎



##### Lemma 5  
For a component the value computed in Lemma&nbsp;4 equals the number of
assignments of the whole component that satisfy (1).

**Proof.**  
By Lemma&nbsp;3, for a fixed common cycle value `c` the number of
assignments equals the product `∏_{r∈R} pref[r][c]`.  
Summation over all possible `c` counts every valid assignment of the
component exactly once (its common cycle value is uniquely determined).
Thus Lemma&nbsp;4 gives precisely the total number of assignments of the
component. ∎



##### Lemma 6  
Assignments of different components are independent.

**Proof.**  
There is no edge between two different cycles of the functional graph.
Hence the constraints (1) never involve vertices from distinct components.
Consequently the choices made in one component do not restrict the
choices in any other component. ∎



##### Theorem  
The algorithm outputs, modulo `998244353`, the number of sequences
`x = (x₁,…,x_N)` with `1 ≤ x_i ≤ M` that satisfy `x_i ≤ x_{A_i}` for
every `i`.

**Proof.**  

*Step 1* – the DP computes correct `dp` and `pref` for every non‑cycle
vertex (Lemmas&nbsp;1 and&nbsp;2).

*Step 2* – for each component the algorithm obtains the number of its
valid assignments (Lemma&nbsp;5).

*Step 3* – because components are independent (Lemma&nbsp;6) the total
number of global assignments is the product of the numbers of all
components. The algorithm multiplies exactly these values, always taken
modulo `MOD`. ∎



--------------------------------------------------------------------

#### 5.   Complexity Analysis

```
N ≤ 2025 ,  M ≤ 2025
```

* building the graph, finding cycles, collecting roots: `O(N)`
* DP over all non‑cycle vertices:   `O(N·M)` time, `O(N·M)` memory
* final multiplication over components: `O(N·M)` time
* total time   `O(N·M)  ≤ 4·10⁶` elementary operations
* total memory `O(N·M)` integers (≈ 4·10⁶) – well inside the limits for
  Python (≈ 150 MiB).

--------------------------------------------------------------------

#### 6.   Reference Implementation  (Python 3)

```python
import sys
from collections import deque

MOD = 998244353

def solve() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    M = int(next(it))
    A = [int(next(it)) - 1 for _ in range(N)]          # 0‑based

    # adjacency list of incoming edges and indegrees
    children = [[] for _ in range(N)]
    indeg = [0] * N
    for i, p in enumerate(A):
        children[p].append(i)
        indeg[p] += 1

    # ---- remove all vertices that are not on a directed cycle ----
    q = deque([i for i in range(N) if indeg[i] == 0])
    removed = []                     # order of removal (leaves → root)
    while q:
        v = q.popleft()
        removed.append(v)
        p = A[v]
        indeg[p] -= 1
        if indeg[p] == 0:
            q.append(p)

    # vertices that still have indegree > 0 belong to cycles
    is_cycle = [indeg[i] > 0 for i in range(N)]

    # ---- group remaining vertices into cycles (components) ----
    visited = [False] * N
    comp_of = [-1] * N                # which component a cycle vertex belongs to
    comp_roots = []                   # list of list of tree‑roots for each component
    for i in range(N):
        if is_cycle[i] and not visited[i]:
            cur = i
            comp_nodes = []
            while not visited[cur]:
                visited[cur] = True
                comp_nodes.append(cur)
                cur = A[cur]
            cid = len(comp_roots)
            comp_roots.append([])
            for v in comp_nodes:
                comp_of[v] = cid

    # ---- attach tree roots to their component ----
    for i in range(N):
        if is_cycle[i]:
            for ch in children[i]:
                if not is_cycle[ch]:          # ch is a root of a tree
                    comp_roots[comp_of[i]].append(ch)

    # ---- DP for all non‑cycle vertices (bottom‑up) ----
    pref = [None] * N                     # pref[v][k] only for non‑cycle v
    for v in reversed(removed):           # children are already processed
        childs = children[v]              # all children are non‑cycle
        if not childs:                     # leaf
            arr = [0] * (M + 1)
            cur = 0
            for k in range(1, M + 1):
                cur = (cur + 1) % MOD
                arr[k] = cur
            pref[v] = arr
        else:
            child_pref = [pref[ch] for ch in childs]
            arr = [0] * (M + 1)
            cur = 0
            for k in range(1, M + 1):
                prod = 1
                for cp in child_pref:
                    prod = (prod * cp[k]) % MOD
                cur = (cur + prod) % MOD
                arr[k] = cur
            pref[v] = arr

    # ---- multiply contributions of all components ----
    answer = 1
    for roots in comp_roots:
        # product over all roots for each possible cycle value c
        comp_prod = [1] * (M + 1)          # index 0 unused
        for r in roots:
            pr = pref[r]
            for c in range(1, M + 1):
                comp_prod[c] = (comp_prod[c] * pr[c]) % MOD
        comp_sum = sum(comp_prod[1:]) % MOD
        answer = (answer * comp_sum) % MOD

    print(answer)


if __name__ == "__main__":
    solve()
```

The program follows exactly the algorithm proven correct above
and conforms to the required input‑output format.