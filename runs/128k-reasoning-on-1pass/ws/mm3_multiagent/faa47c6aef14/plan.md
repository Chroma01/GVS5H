**Solution Explanation**

For every box `i`

* `A[i] = 1`  – the box contains a red ball  
* `B[i] = 1`  – the box contains a blue ball  

`P` and `Q` are permutations, therefore each box has

* one **red** outgoing edge `i → P[i]`
* one **blue** outgoing edge `i → Q[i]`

When we choose a box `i` and perform the operation

```
all balls of box i are taken,
all red balls go to box P[i],
all blue balls go to box Q[i]
box i becomes empty
```

The operation can be applied any number of times.  
The goal is to finish with all balls inside the special box `X`
(and all other boxes empty).

--------------------------------------------------------------------

#### 1.   Observations

* A red ball never changes its colour, it always follows the red edges.
  The same is true for a blue ball and the blue edges.
* Because a box is emptied completely, a box is fired **once**,
  all balls that are inside it are moved at that moment.
* The whole process can be seen as moving each ball along a *path*:

```
red ball :  v ──► P[v] ──► P[P[v]] ──► … ──► X
blue ball:  v ──► Q[v] ──► Q[Q[v]] ──► … ──► X
```

* A ball can reach `X` **iff** the whole (colour) path from its start
  contains `X`.  
  If a ball cannot reach `X` the task is impossible.

* If a ball can reach `X`, every box on its (unique) path to `X`
  must be fired once – otherwise the ball would stay forever.
  Different balls may use the same box, but one fire is enough,
  because the fire moves *all* balls that are inside the box at that moment.

* Consequently the minimal number of operations is exactly the number of
  different boxes (different from `X`) that lie on a red path
  **or** on a blue path from a ball to `X`.

--------------------------------------------------------------------

#### 2.   Formalisation

```
RED_SOURCE = { i | A[i] = 1 , i ≠ X }
BLUE_SOURCE = { i | B[i] = 1 , i ≠ X }

RED_BACK   = { i | X is reachable from i using only red edges }
BLUE_BACK  = { i | X is reachable from i using only blue edges }

RED_FWD    = { i | i is reachable from some RED_SOURCE
                     using only red edges, stopping at X }
BLUE_FWD   = { i | i is reachable from some BLUE_SOURCE
                     using only blue edges, stopping at X }
```

All sets are subsets of `{1,…,N}`.
`RED_BACK` (`BLUE_BACK`) is the set of nodes whose red (blue) path
can reach `X`.  
`RED_FWD` (`BLUE_FWD`) is the set of nodes that lie on a red (blue)
path from a non‑`X` source to `X`.  
A node is needed **iff** it belongs to

```
( RED_FWD ∩ RED_BACK )   ∪   ( BLUE_FWD ∩ BLUE_BACK )
```

and is different from `X`.

The answer = size of that union.

--------------------------------------------------------------------

#### 3.   Computing the sets

All edges are functional (out‑degree `1`).  
For a colour we need two traversals:

* **backward** – start from `X` and walk **against** the edges  
  (`i → P[i]` becomes `P[i] → i`).  
  Because each node has exactly one outgoing edge, the reverse graph
  is an ordinary directed graph.  
  BFS/DFS from `X` gives `RED_BACK` (`BLUE_BACK`) in `O(N)`.
* **forward** – start from all sources (ignoring a source equal to `X`)  
  and follow the forward edges, **but stop the walk when we would
  leave `X`**.  
  This is again a simple BFS/DFS and yields `RED_FWD` (`BLUE_FWD`).

Both traversals are linear, total `O(N)` time and `O(N)` memory.

--------------------------------------------------------------------

#### 4.   Correctness Proof  

We prove that the algorithm prints `-1` iff the task is impossible,
otherwise it prints the minimum possible number of operations.

---

##### Lemma 1  
For a red (blue) ball placed in a box `i (≠ X)` the ball can reach `X`
iff `i ∈ RED_BACK` (`i ∈ BLUE_BACK`).

**Proof.**  
`RED_BACK` is exactly the set of vertices from which `X` is reachable
by repeatedly following the red permutation `P`.  
The same holds for the blue permutation. ∎



##### Lemma 2  
If a box `i ≠ X` belongs to `RED_FWD` (`BLUE_FWD`) then a red (blue) ball
must be moved through `i` on its way to `X`.

**Proof.**  
`i ∈ RED_FWD` means there exists a red source `s` (`A[s]=1, s≠X`) such that
by repeatedly applying `P` we meet `i` **before** we first meet `X`.  
The red ball starting at `s` follows exactly this walk, therefore it visits
`i` and afterwards continues to `X`.  The same argument works for blue. ∎



##### Lemma 3  
If a box `i ≠ X` belongs to  
`(RED_FWD ∩ RED_BACK) ∪ (BLUE_FWD ∩ BLUE_BACK)`,
then at least one operation must be performed on box `i`.

**Proof.**  
Assume `i` belongs to the first intersection.
By Lemma&nbsp;2 a red ball passes through `i`.  
The only way to move that ball further (towards `X`) is to fire `i`,
because the operation on `i` is the only one that empties `i`.  
The same argument works for the second intersection. ∎



##### Lemma 4  
All boxes of the set  

```
S = (RED_FWD ∩ RED_BACK) ∪ (BLUE_FWD ∩ BLUE_BACK) \ {X}
```

can be fired exactly once, in a suitable order, and after those
operations every ball is inside `X`.

**Proof.**  
Consider the directed graph `G` whose vertices are the boxes of `S`
and whose edges are

* `i → P[i]` if `i ∈ RED_FWD ∩ RED_BACK` (the red edge used by the red
  ball that passes through `i`);
* `i → Q[i]` if `i ∈ BLUE_FWD ∩ BLUE_BACK`.

`P[i]` (or `Q[i]`) is either `X` or another vertex of `S`,
because the ball that goes through `i` reaches `X` and all intermediate
vertices are also in `S`.  
If a directed cycle existed in `G`, every vertex of the cycle could reach
`X` only by using a colour edge that is not part of the cycle –
contradiction to the definition of `S`.  
Hence `G` is a **directed acyclic graph** (all its cycles contain `X`,
and `X` is omitted).

A topological order of a DAG exists.
Fire the vertices of `S` in reverse topological order:
when we fire a vertex, all its incoming balls (coming from already
fired predecessors) are already inside it, therefore one fire moves
all of them forward.  
No vertex ever receives balls after it has been fired,
so it never needs a second fire.  
When the last vertex of `S` is fired, every ball has arrived at `X`. ∎



##### Lemma 5  
The number printed by the algorithm equals `|S|`.

**Proof.**  
The algorithm computes exactly the four sets described above,
takes their intersections and their union, removes `X` and counts the
remaining elements. ∎



##### Lemma 6  
If the algorithm prints `-1` then the task is impossible.

**Proof.**  
`-1` is printed only when a red (blue) source `s` is not contained in
`RED_BACK` (`BLUE_BACK`).  
By Lemma&nbsp;1 the corresponding ball can never reach `X`,
hence the goal state can never be reached. ∎



##### Lemma 7  
If the algorithm does **not** print `-1` then the task is possible.

**Proof.**  
All red sources belong to `RED_BACK` and all blue sources to
`BLUE_BACK`; therefore by Lemma&nbsp;1 every ball can reach `X`.  
Consequently the set `S` is well defined.
By Lemma&nbsp;4 the balls can be moved to `X` using exactly `|S|`
operations. ∎



##### Theorem  
The program

* prints `-1` **iff** it is impossible to collect all balls into box `X`;
* otherwise prints the minimum possible number of operations.

**Proof.**  

*If the program prints `-1`* – by Lemma&nbsp;6 the task is impossible.  

*If the program prints a non‑negative integer* – by Lemma&nbsp;7 the task
is possible.  
Lemma&nbsp;3 shows that at least `|S|` operations are necessary.
Lemma&nbsp;4 shows that `|S|` operations are sufficient.
By Lemma&nbsp;5 the program outputs exactly `|S|`.  
Therefore the printed number equals the optimal (minimum) number of
operations. ∎



--------------------------------------------------------------------

#### 5.   Complexity Analysis  

*building reverse adjacency lists* : `O(N)` time, `O(N)` memory  
*backward BFS (red & blue)*      : `O(N)` time, `O(N)` memory  
*forward BFS (red & blue)*       : `O(N)` time, `O(N)` memory  
*final counting*                : `O(N)` time  

Overall  

```
Time   :  O(N)   ( ≤ 2·10⁵ )
Memory :  O(N)
```

Both satisfy the limits.

--------------------------------------------------------------------

#### 6.   Reference Implementation  (Python 3)

```python
import sys
from collections import deque

def solve() -> None:
    it = iter(sys.stdin.buffer.read().split())
    N = int(next(it))
    X = int(next(it)) - 1                     # 0‑based

    A = [int(next(it)) for _ in range(N)]
    B = [int(next(it)) for _ in range(N)]
    P = [int(next(it)) - 1 for _ in range(N)]
    Q = [int(next(it)) - 1 for _ in range(N)]

    # reverse edges
    revP = [[] for _ in range(N)]
    revQ = [[] for _ in range(N)]
    for i in range(N):
        revP[P[i]].append(i)
        revQ[Q[i]].append(i)

    # ---------- backward reachable from X ----------
    def bfs_back(start_rev):
        visited = [False] * N
        dq = deque([start_rev])
        visited[start_rev] = True
        while dq:
            v = dq.popleft()
            for u in rev[v]:
                if not visited[u]:
                    visited[u] = True
                    dq.append(u)
        return visited

    # red backward
    rev = revP
    back_red = bfs_back(X)

    # blue backward
    rev = revQ
    back_blue = bfs_back(X)

    # ---------- feasibility ----------
    for i in range(N):
        if A[i] == 1 and i != X and not back_red[i]:
            print(-1)
            return
        if B[i] == 1 and i != X and not back_blue[i]:
            print(-1)
            return

    # ---------- forward from non‑X sources, stop at X ----------
    def bfs_fwd(sources, nxt_edge):
        visited = [False] * N
        dq = deque()
        for s in sources:
            visited[s] = True
            dq.append(s)
        while dq:
            v = dq.popleft()
            if v == X:                 # do not go beyond X
                continue
            w = nxt_edge[v]
            if not visited[w]:
                visited[w] = True
                dq.append(w)
        return visited

    red_sources = [i for i in range(N) if A[i] == 1 and i != X]
    blue_sources = [i for i in range(N) if B[i] == 1 and i != X]

    fwd_red = bfs_fwd(red_sources, P)
    fwd_blue = bfs_fwd(blue_sources, Q)

    # ---------- count required boxes ----------
    ans = 0
    for i in range(N):
        if i == X:
            continue
        if (fwd_red[i] and back_red[i]) or (fwd_blue[i] and back_blue[i]):
            ans += 1

    print(ans)


if __name__ == "__main__":
    solve()
```

The program follows exactly the algorithm proven correct above
and conforms to the required time and memory limits.