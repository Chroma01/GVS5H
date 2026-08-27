**Solution Explanation**

For every ordered pair of vertices `(i , j)` we have to know the smallest number of
edges of a walk  

```
i = v0 → v1 → … → vk = j
```

such that the concatenation of the edge labels is a palindrome.
The walk may repeat vertices.

--------------------------------------------------------------------

#### 1.   Observations

*The empty walk is a palindrome* – therefore `i = j` has answer `0`.  
If there is a single edge `i → j` the string consisting of its label has length `1`
and is a palindrome – answer `1`.

Take any palindrome walk of length `≥ 2`

```
i = p0 → p1 → … → pℓ-1 → pℓ = j          (ℓ ≥ 2)
```

The first and the last label are equal, remove them.
What remains is again a palindrome walk

```
p1 → … → pℓ-1
```

whose length is `ℓ‑2`.  
Consequently a longer palindrome walk can be built from a shorter one by
adding a *pair* of equal labels, one at the left end and one at the right
end.

--------------------------------------------------------------------

#### 2.   State graph

A state is an **ordered pair** `(u , v)`.  
If we already know a shortest palindrome walk from `u` to `v`,
we may extend it:

* pick a vertex `x` with an edge `x → u` labelled `c`,
* pick a vertex `y` with an edge `v → y` labelled `c`,
* the new walk `x → … → y` has length `+ 2`.

So from a state `(u , v)` we can go to any state `(x , y)` for which

```
x → u   (incoming edge to u)   and   v → y   (outgoing edge from v)
```

have the **same label**.

All edges of the state graph have the same weight `2`.  
The start states are

```
(i , i)   distance 0                     (empty walk)
(i , j)   distance 1   for every edge i → j
```

Because all weights are positive, a **Breadth First Search** (BFS) over the
state graph visits the states in non‑decreasing order of the answer.
The first time we reach a pair `(i , j)` we have found the shortest possible
palindrome walk, i.e. the required answer.

--------------------------------------------------------------------

#### 3.   Data structures

* `out[u][c]` – list of vertices `w` with an edge `u → w` labelled `c`.
* `inc[u][c]` – list of vertices `w` with an edge `w → u` labelled `c`.

Both structures contain at most `N` entries per vertex per letter.

* `dist[i][j]` – current best length of a palindrome walk from `i` to `j`
  (initialised with `INF`, `dist[i][i]=0`,
  `dist[i][j]=1` for every existing edge `i→j`).

* ordinary FIFO queue (`collections.deque`) for the BFS.

--------------------------------------------------------------------

#### 4.   BFS transition

```
state = (u , v)   with current distance d
for every letter c (0 … 25):
        pre = inc[u][c]          # vertices x with x → u (label c)
        nxt = out[v][c]          # vertices y with v → y (label c)
        if pre empty or nxt empty: continue
        nd = d + 2
        for x in pre:
            for y in nxt:
                if dist[x][y] > nd:
                        dist[x][y] = nd
                        queue.append( (x , y) )
```

`dist[x][y]` is improved at most once, therefore each pair is inserted into the
queue at most once.

--------------------------------------------------------------------

#### 5.   Correctness Proof  

We prove that the algorithm outputs the required shortest palindrome length for
every pair of vertices.

---

##### Lemma 1  
For any vertices `i , j` the length `dist[i][j]` after the BFS finishes equals
the length of the shortest palindrome walk from `i` to `j`.

*Proof.*

*Base cases.*

* `i = j` – the empty walk (length 0) is a palindrome, and `dist[i][i]` is
  initialised with `0`. No walk can be shorter, therefore the statement holds.

* direct edge `i → j` – a walk of length 1 is a palindrome, and `dist[i][j]` is
  initialised with `1`. No walk can be shorter, thus the statement holds.

*Induction step.*  
Assume the statement true for all pairs whose current distance in the BFS
queue is `< d`.  
Take a pair `(x , y)` that obtains distance `d` for the first time during the
BFS. By the transition rule there exists a vertex `u , v` with

```
x → u   (label c) ,   v → y   (label c)   and   dist[u][v] = d-2 .
```

Because `dist[u][v] = d‑2` is already minimal (induction hypothesis),
there is a palindrome walk `P` from `u` to `v` of length `d‑2`.  
Adding the two edges `x → u` and `v → y` yields a walk from `x` to `y`
of length `d` whose label string is `c + (label of P) + c`,
a palindrome. No shorter palindrome walk can exist,
otherwise the algorithm would have discovered `dist[x][y]` earlier
(the BFS processes states in increasing distance order). ∎



##### Lemma 2  
Whenever the algorithm relaxes `dist[x][y]` from `INF` to a finite value,
the used transition corresponds to a valid palindrome walk of that length.

*Proof.*  
The relaxation uses a state `(u , v)` already known to be reachable by a
palindrome walk of length `dist[u][v]`.  
It appends a pair of equal‑labelled edges `x → u` and `v → y`.
The concatenated label string becomes the old palindrome string surrounded by
the same character `c`, therefore it is still a palindrome.
Its length is `dist[u][v] + 2`. ∎



##### Lemma 3  
If a palindrome walk of length `L` exists from `i` to `j`,
the algorithm will eventually set `dist[i][j] ≤ L`.

*Proof.*  
Induction over `L`.

* `L = 0` – handled by initialization (`dist[i][i]=0`).

* `L = 1` – handled by initialization (`dist[i][j]=1`).

* `L ≥ 2`.  
  The first and the last edge of the walk have the same label `c`.
  Removing them yields a palindrome walk of length `L‑2`
  from `u` to `v` (the inner vertices).  
  By the induction hypothesis the algorithm will obtain
  `dist[u][v] = L‑2`.  
  When `(u , v)` is processed the transition adds the two outer edges
  and relaxes `dist[i][j]` to `L`. ∎



##### Lemma 4  
When the BFS terminates, for every pair `(i , j)` the value `dist[i][j]`
is the minimum possible length of a palindrome walk from `i` to `j`.

*Proof.*  
*Upper bound*: By Lemma&nbsp;3 any existing palindrome walk yields a finite
value, therefore after termination `dist[i][j]` is at most the optimum.

*Lower bound*: Lemma&nbsp;2 shows that any finite value stored in `dist[i][j]`
corresponds to an actual palindrome walk of that length.
Consequently `dist[i][j]` cannot be smaller than the optimum.
Both bounds coincide, hence `dist[i][j]` equals the optimum. ∎



##### Theorem  
The program prints for every ordered pair `(i , j)` the length of the
shortest (possibly non‑simple) path whose edge‑label concatenation is a
palindrome, or `-1` if no such path exists.

*Proof.*  
By Lemma&nbsp;4 `dist[i][j]` equals that shortest length whenever a palindrome
walk exists; otherwise it stays at `INF`.  
The output routine writes `dist[i][j]` if it is finite and `-1` otherwise,
exactly as required. ∎



--------------------------------------------------------------------

#### 6.   Complexity Analysis  

`N ≤ 100`.

*Number of states* – `N²` (at most `10⁴`).  
Each state is processed once.

For a state `(u , v)` we iterate over the 26 letters.
For a fixed letter `c` we need all pairs  
`x ∈ inc[u][c]` and `y ∈ out[v][c]`.  
Hence the total number of inner pair inspections is  

```
 Σ_{states (u,v)} Σ_{c} |inc[u][c]| · |out[v][c]|
 ≤ N² · N² = N⁴   (worst case, every vertex has N edges of the same letter)
```

For `N = 100` this is at most `10⁸` elementary operations – easily fast enough
in Python.

Memory consumption:

* adjacency lists – `O(N·26·N) = O(N²)`  
* distance matrix – `N²` integers  
* queue – at most `N²` pairs  

Overall `O(N²)` memory, well within limits.

--------------------------------------------------------------------

#### 7.   Reference Implementation  (Python 3)

```python
import sys
from collections import deque

def solve() -> None:
    input = sys.stdin.readline
    N = int(input())
    # out[u][c] : destinations of edges u -> * with label c
    out_adj = [ [ [] for _ in range(26) ] for _ in range(N) ]
    # inc[u][c] : sources of edges * -> u with label c
    inc_adj = [ [ [] for _ in range(26) ] for _ in range(N) ]

    for i in range(N):
        row = input().strip()
        for j, ch in enumerate(row):
            if ch != '-':
                c = ord(ch) - 97
                out_adj[i][c].append(j)
                inc_adj[j][c].append(i)

    INF = 10 ** 9
    dist = [ [ INF ] * N for _ in range(N) ]

    # distance 0 : i -> i
    for i in range(N):
        dist[i][i] = 0

    # distance 1 : direct edges
    for i in range(N):
        for c in range(26):
            for j in out_adj[i][c]:
                if dist[i][j] > 1:
                    dist[i][j] = 1

    q = deque()
    for i in range(N):
        for j in range(N):
            if dist[i][j] != INF:
                q.append((i, j))

    while q:
        u, v = q.popleft()
        cur = dist[u][v]
        nd = cur + 2
        inc_u = inc_adj[u]
        out_v = out_adj[v]
        for c in range(26):
            pre = inc_u[c]          # vertices x with edge x -> u (label c)
            nxt = out_v[c]          # vertices y with edge v -> y (label c)
            if not pre or not nxt:
                continue
            for x in pre:
                # inner loop over y
                for y in nxt:
                    if dist[x][y] > nd:
                        dist[x][y] = nd
                        q.append((x, y))

    out_lines = []
    for i in range(N):
        row = []
        for j in range(N):
            val = dist[i][j]
            row.append(str(val) if val != INF else "-1")
        out_lines.append(" ".join(row))
    sys.stdout.write("\n".join(out_lines))

if __name__ == "__main__":
    solve()
```

The program follows exactly the algorithm proven correct above
and conforms to the required input / output format.