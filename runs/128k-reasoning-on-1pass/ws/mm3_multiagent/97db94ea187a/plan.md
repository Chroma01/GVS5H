**Solution Explanation**

For a fixed vertex `1` (the root) let  

```
d(v) = shortest distance from 1 to v      ( 0 ≤ d(v) ≤ N-1 )
```

`d(1)=0`.  
All vertices with the same distance form a *layer* :

```
layer 0 : the root
layer 1 : vertices with d = 1
layer 2 : vertices with d = 2
...
```

If the graph is connected, the set of layers is exactly `{0,1,…,D}` for some `D`
(the distance of the farthest vertex).  
Therefore a connected graph with a given root gives a unique ordered
partition of the remaining `N‑1` vertices into non‑empty parts

```
n1 , n2 , … , nD      ( ni ≥ 1 , Σ ni = N-1 )
```

`ni` is the size of layer `i`.  
The parity condition of the problem is

```
#even layers (including the root) = N/2 .
```

Because the root is even, this means

```
1 + Σi even , i≥2  ni   = N/2      (even layers)
Σi odd            ni   = N/2      (odd layers)
```

--------------------------------------------------------------------

#### 1.   Which edges are allowed ?

Take a distance labelling `d`.  
If an edge `{u,v}` existed with `|d(u)-d(v)| ≥ 2`,
the shorter of the two paths would become a shorter path for one of the
endpoints – contradiction to the definition of the distances.
Hence every edge must satisfy  

```
|d(u)-d(v)| ≤ 1                                   (1)
```

Conversely, let a graph contain only edges satisfying (1) and
let every vertex `v≠1` have at least one neighbour in the previous layer.
Then the distance of `v` is exactly the length of a chain
`v – previous – previous – … – root`, i.e. `d(v)`.  
So the conditions are **necessary and sufficient**.

For a fixed layer sequence `(n0=1, n1,…,nD)` the admissible edges are

* **inside a layer** – any subset of the `C(ni,2)` possible edges,
* **between two consecutive layers** – a bipartite graph between the
  `ni‑1` vertices of the left layer and the `ni` vertices of the right
  layer, where each right vertex has degree at least `1`.

All these choices are independent for different pairs of layers.



--------------------------------------------------------------------

#### 2.   Counting graphs for a fixed layer sequence  

*Choosing the vertices of the layers*  
The root is fixed, the remaining `N‑1` labelled vertices are distributed
into the ordered layers.  
The number of ways to choose the sets of sizes `n1,…,nD` is the multinomial

```
(N-1)! / ( n1! n2! … nD! )
```

*Edges inside a layer of size `b`*  
`C(b,2)` possible edges, any subset may be taken.
The distribution of the number of internal edges `e` is

```
G[b][e] = C( C(b,2) , e )                         (2)
```

*Edges between two consecutive layers*  
Let the left layer have size `a`, the right layer size `b`.
We need binary `b × a` matrices with no zero row, the number of `1`s is `e`.
By inclusion–exclusion

```
F[a][b][e] = Σi=0..b  (-1)^i * C(b,i) * C( (b-i)*a , e )      (3)
```

(`i` rows are forced to be empty, the remaining `(b-i)*a` cells are
chosen arbitrarily).

*Both kinds together*  
For a transition from a layer of size `s` to a new layer of size `x`

```
H[s][x][e] = Σe1+e2=e  F[s][x][e1] * G[x][e2]                (4)
```

Only `e ≤ N(N-1)/2` are needed.

All these tables are pre‑computed once – `N ≤ 30`, therefore
`a , b , s , x ≤ 30` and the tables are tiny.



--------------------------------------------------------------------

#### 3.   Dynamic programming over the layers  

State  

```
t       : total number of vertices already placed
e       : how many of them belong to even layers (including the root)
s       : size of the last placed layer
p       : parity of that last layer (0 = odd, 1 = even)
```

`dp[t][(e,s,p)]` is a vector indexed by the number of already used edges,
its entry is the number of different graphs (with the already placed
layers) that satisfy the data of the state.

*initial state*  

```
t = 1 , e = 1 , s = 1 , p = 1          (only the root)
dp[1][(1,1,1)][0] = 1
```

*transition* – add a new layer of size `x ( ≥ 1 )`

```
remaining = N - t
new_t      = t + x
new_p      = 1 - p
new_e      = e + (new_p * x)            // add only if the new layer is even
new_s      = x
factor     = C( remaining , x )        // choose the x vertices for the new layer
add_edges  = H[s][x]                    // distribution of edges added now
```

The new vector is the convolution of the old vector with `add_edges`,
multiplied by `factor`.  
All arithmetic is performed modulo the given prime `P`.

Only states with `new_e ≤ N/2` are kept – the final answer needs exactly
`N/2` even vertices.

The number of different states is small:

```
t ≤ 30 ,  e ≤ 15 ,  s ≤ 30 ,  p ∈ {0,1}
at most 30·16·31·2 ≈ 3·10^4 states
```

The whole DP finishes easily in well under a second.



--------------------------------------------------------------------

#### 4.   Collecting the answer  

After processing all layers we look at `t = N`.  
All states with `e = N/2` already satisfy the parity condition.
For every edge count `M` ( `N‑1 ≤ M ≤ N(N‑1)/2` ) we sum the
corresponding entries of the vectors of those states.

The required output is these sums for `M = N‑1 , … , N(N‑1)/2`.



--------------------------------------------------------------------

#### 5.   Correctness Proof  

We prove that the algorithm outputs exactly the number of
connected simple labelled graphs with the required property
for every edge number `M`.

---

##### Lemma 1  
For a connected graph the set of distances from vertex `1` is
`{0,1,…,D}` for some `D`.  
Consequently the vertices are uniquely partitioned into the
non‑empty layers `L0 , L1 , … , LD` with `|Li| = ni ≥ 1` and  
`Σ ni = N-1`.

**Proof.**  
If a vertex has distance `k>0` there is a neighbour of distance `k-1`,
otherwise a shorter path would exist.
Thus every distance `k (1≤k≤D)` forces a vertex of distance `k-1`.
Starting with distance `0` (the root) we obtain all distances `0…D`. ∎



##### Lemma 2  
Let a distance labelling `d` be fixed.
A simple graph has exactly these distances **iff**

* every edge `{u,v}` satisfies `|d(u)-d(v)| ≤ 1`, and
* every vertex `v≠1` has at least one neighbour with distance `d(v)-1`.

**Proof.**  
*Necessity* – if an edge had `|d(u)-d(v)| ≥ 2` the shorter endpoint
would obtain a shorter path, contradiction.
If a vertex `v` had no neighbour in the previous layer,
all its neighbours are at distance at least `d(v)`,
hence a shortest path could not be shorter than `d(v)+1` – contradiction.

* Sufficiency –* the conditions guarantee a chain  
`v – … – 1` of length exactly `d(v)`, so the distance is at most `d(v)`.
Because edges can only connect vertices whose distances differ by at most
`1`, no shorter chain exists. ∎



##### Lemma 3  
For fixed layer sizes `(n0=1,n1,…,nD)` the number of graphs
satisfying Lemma&nbsp;2 equals  

```
  (N-1)!/(n1!…nD!)   ×   Π_{k=1..D}   F[n_{k-1}][n_k]   ×   Π_{k=1..D}   G[n_k]            (5)
```

where `F` and `G` are given by (3) and (2).

**Proof.**  
*Choosing the vertices* – the multinomial factor counts the ways to assign
the labelled vertices to the ordered layers.

*Edges inside a layer* – any subset of the `C(ni,2)` possible edges,
exactly the binomial coefficient `G[ni][e]`.

*Edges between two consecutive layers* – the bipartite adjacency matrix
must have no zero row; the number of such matrices with `e` ones is
`F[n_{k-1}][n_k][e]` (inclusion–exclusion).

All choices for different pairs of layers are independent, giving the
product in (5). ∎



##### Lemma 4  
For a fixed layer sequence the distribution of the total number of
edges `M` contributed by (5) is exactly the convolution `H` defined in (4)
applied step by step.

**Proof.**  
When the last placed layer has size `s` and a new layer of size `x` is
added, the newly created edges are

* `e1` edges between the two layers, counted by `F[s][x]`,
* `e2` internal edges of the new layer, counted by `G[x]`.

All possibilities for the pair `(e1,e2)` are independent,
therefore the combined distribution is the convolution
`H[s][x] = F[s][x] * G[x]`.  Repeating this for every transition
produces the whole distribution. ∎



##### Lemma 5  
The dynamic programming described in Section&nbsp;3 computes, for every
reachable state `(t,e,s,p)`, exactly the vector

```
dp[t][(e,s,p)][M] = number of ways to choose
        • a partition of the first t vertices into layers ending with
          a layer of size s and parity p,
        • and to add edges inside the layers and between consecutive layers,
          such that the total number of edges is M .
```

**Proof.**  
Induction over `t`.

*Base `t=1`* – only the root, no edges, the initial vector is `{0:1}` –
correct.

*Induction step* – assume the statement true for total size `t`.
Take a state `(e,s,p)` with distribution `cur`.
To add a new layer of size `x` we must

1. choose the `x` vertices among the still unused `N-t` vertices –
   `C(N-t,x)` possibilities,
2. add the edges contributed by the new layer – distribution `H[s][x]`,
3. update the number of even vertices (`e` grows by `x` exactly when the
   new layer is even).

The transition described in the algorithm multiplies the old distribution
by `C(N-t,x)`, convolves it with `H[s][x]` and stores the result in the
corresponding new state.  Hence the new state contains precisely the
numbers claimed in the lemma for total size `t+x`. ∎



##### Lemma 6  
For `t = N` a state with `e = N/2` corresponds exactly to a connected
graph on all `N` vertices whose vertex set is partitioned into the
recorded layers, all edges respect the distance constraints,
and the number of even‑distance vertices equals the number of odd‑distance
vertices.

**Proof.**  
By Lemma&nbsp;5 the state enumerates all ways to choose the layers
(and their internal edges) and all admissible edges between consecutive
layers.  Lemma&nbsp;2 guarantees that such a graph has the prescribed
distances, therefore it is connected (every vertex follows its parent
chain to the root).  The condition `e = N/2` is exactly the required
parity condition. ∎



##### Lemma 7  
Every connected simple graph on the labelled vertices `{1,…,N}`
satisfying the parity condition appears **once** in the DP state
`dp[N][(N/2, s, p)]` for a unique `s` and `p`,
and its contribution to the vector entry `M` is exactly `1`.

**Proof.**  
Take such a graph `G`.  
Its distances from vertex `1` are uniquely defined, thus the partition
into layers is uniquely determined (Lemma&nbsp;1).  
The root is in layer `0`, the last layer has a certain size `s` and parity
`p`; the number of even vertices is `N/2`, therefore the state is
`(N, N/2, s, p)`.  
All edges of `G` satisfy `|d(u)-d(v)| ≤ 1` and each non‑root vertex has
a neighbour in the previous layer, consequently (Lemma&nbsp;2) the graph
is counted by the DP when the layers are added in the natural order.
No other ordering of the layers exists, so the graph is counted exactly
once.  The DP stores the number of **different** edge sets for the fixed
layer partition; `G` is one of them, therefore its contribution to the
corresponding entry is `1`. ∎



##### Lemma 8  
For every `M ( N-1 ≤ M ≤ N(N-1)/2 )` the sum taken by the algorithm

```
Ans[M] = Σ_{(e=N/2,s,p)} dp[N][(e,s,p)][M]   (mod P)
```

equals the number of connected graphs with `M` edges satisfying the
parity condition.

**Proof.**  
By Lemma&nbsp;6 each summand counts the graphs whose layer partition ends
with size `s` and parity `p`.  
By Lemma&nbsp;7 every admissible graph is counted once in exactly one of
those summands, and contributes `1` to the entry `M`.  
Hence the sum counts each admissible graph with `M` edges exactly once. ∎



##### Theorem  
The program prints, for all `M = N-1 , … , N(N-1)/2`,
the number of connected simple undirected graphs on the labelled
vertices `{1,…,N}` having `M` edges and satisfying

```
# { v | distance(1,v) is even }  =  # { v | distance(1,v) is odd } .
```

The numbers are given modulo the given prime `P`.

**Proof.**  
The DP computes the vectors `dp[N][(N/2,s,p)]` (Lemma&nbsp;5).  
Lemma&nbsp;8 shows that the final sum performed by the program is exactly
the desired number for each `M`.  All operations are performed modulo the
prime `P`, therefore the printed values are the required answers. ∎



--------------------------------------------------------------------

#### 6.   Complexity Analysis  

`N ≤ 30`, `Mmax = N(N‑1)/2 ≤ 435`.

*Precomputation*  

* factorials up to `N·N = 900` – `O(N²)`.
* tables `F[a][b]` – `O(N³·Mmax) ≤ 30³·435 ≈ 1.2·10⁶`.
* tables `G[b]` – `O(N·Mmax)`.
* tables `H[s][x]` – convolution of `F` and `G`,  
  at most `30·30·Mmax² ≈ 1.7·10⁸` elementary operations,
  but because the involved vectors are short (≤ 435) the real running
  time is well below one second.

*Dynamic programming*  

Number of states ≤ `30·16·31·2 ≈ 3·10⁴`.  
For each state at most `N‑t ≤ 30` transitions.
For a transition the inner work is
`(#non‑zero edge counts of the current vector) × |H_nonzero|`,
both bounded by `Mmax = 435`.  
Hence the total number of elementary operations is below `2·10⁸`,
comfortably fast in Python.

Memory consumption  

* factorials – `O(N²)`.
* tables `F`, `G`, `H` – `O(N²·Mmax) ≤ 30·30·435 ≈ 4·10⁵` integers.
* DP vectors – at most `3·10⁴` vectors, each of length `C(t,2)+1 ≤ 435`,
  i.e. about `1.6·10⁶` integers (≈ 50 MiB with Python `int`s).

All limits are easily satisfied.



--------------------------------------------------------------------

#### 7.   Reference Implementation  (Python 3)

```python
import sys

def solve() -> None:
    sys.setrecursionlimit(10000)
    N, P = map(int, sys.stdin.readline().split())
    half = N // 2
    maxM = N * (N - 1) // 2
    max_n = N * N                     # for binomial coefficients

    # ---------- factorials and binomials ----------
    fact = [1] * (max_n + 1)
    for i in range(1, max_n + 1):
        fact[i] = fact[i - 1] * i % P
    inv_fact = [1] * (max_n + 1)
    inv_fact[max_n] = pow(fact[max_n], P - 2, P)
    for i in range(max_n, 0, -1):
        inv_fact[i - 1] = inv_fact[i] * i % P

    def comb(n: int, k: int) -> int:
        if k < 0 or k > n:
            return 0
        return fact[n] * inv_fact[k] % P * inv_fact[n - k] % P

    # ---------- table F[a][b] : bipartite matrices, no zero row ----------
    F = [[None] * (N + 1) for _ in range(N + 1)]          # F[a][b] is a list length maxM+1
    F_nonzero = [[None] * (N + 1) for _ in range(N + 1)]  # list of (e, val)
    for a in range(1, N + 1):
        for b in range(1, N + 1):
            limit = min(a * b, maxM)
            f = [0] * (maxM + 1)
            for i in range(0, b + 1):
                coeff = comb(b, i)
                if coeff == 0:
                    continue
                n_rem = (b - i) * a
                max_e_i = min(n_rem, maxM)
                for e in range(0, max_e_i + 1):
                    c = comb(n_rem, e)
                    if c == 0:
                        continue
                    term = coeff * c % P
                    if i & 1:
                        f[e] = (f[e] - term) % P
                    else:
                        f[e] = (f[e] + term) % P
            F[a][b] = f
            nz = [(e, f[e]) for e in range(limit + 1) if f[e] != 0]
            F_nonzero[a][b] = nz

    # ---------- table G[b] : internal edges of a layer ----------
    G = [None] * (N + 1)
    G_nonzero = [None] * (N + 1)
    for b in range(0, N + 1):
        internal = b * (b - 1) // 2
        g = [0] * (maxM + 1)
        for e in range(0, internal + 1):
            g[e] = comb(internal, e)
        G[b] = g
        G_nonzero[b] = [(e, g[e]) for e in range(internal + 1) if g[e] != 0]

    # ---------- table H[s][x] : edges added when a layer of size s is followed by size x ----------
    H_nonzero = [[None] * (N + 1) for _ in range(N + 1)]
    for s in range(1, N + 1):
        for x in range(1, N + 1):
            h = [0] * (maxM + 1)
            f_list = F_nonzero[s][x]
            g_list = G_nonzero[x]
            for e1, fv in f_list:
                for e2, gv in g_list:
                    e = e1 + e2
                    if e > maxM:
                        break
                    h[e] = (h[e] + fv * gv) % P
            # keep only non‑zero entries, sorted by e (they are produced in increasing order)
            nz = [(e, h[e]) for e in range(maxM + 1) if h[e] != 0]
            H_nonzero[s][x] = nz

    # ---------- DP over layers ----------
    max_edges = [i * (i - 1) // 2 for i in range(N + 1)]

    dp = [dict() for _ in range(N + 1)]
    init_vec = [1]                     # length 1, index 0 = 1
    dp[1][(1, 1, 1)] = init_vec        # (e, size_of_last_layer, parity_of_last_layer)

    for t in range(1, N):
        cur_dict = dp[t]
        if not cur_dict:
            continue
        remaining = N - t
        for (e, s, parity), cur in cur_dict.items():
            # list of non‑zero entries of cur (to avoid scanning zeros many times)
            non_zero = [(idx, val) for idx, val in enumerate(cur) if val != 0]
            cur_max = max_edges[t]
            for x in range(1, remaining + 1):
                new_t = t + x
                new_parity = 1 - parity
                new_e = e + (new_parity * x)
                if new_e > half:          # cannot exceed required number of even vertices
                    continue
                factor = comb(remaining, x)
                if factor == 0:
                    continue
                add_list = H_nonzero[s][x]
                if not add_list:
                    continue
                new_max = max_edges[new_t]
                key = (new_e, x, new_parity)
                new_vec = dp[new_t].get(key)
                if new_vec is None:
                    new_vec = [0] * (new_max + 1)
                    dp[new_t][key] = new_vec
                # convolution
                for e_cur, val_cur in non_zero:
                    max_add = new_max - e_cur
                    for add, val_add in add_list:
                        if add > max_add:
                            break
                        new_m = e_cur + add
                        inc = val_cur * factor % P * val_add % P
                        new_vec[new_m] = (new_vec[new_m] + inc) % P

    # ---------- collect answer ----------
    ans = [0] * (maxM + 1)
    target_e = half
    for (e, s, parity), vec in dp[N].items():
        if e != target_e:
            continue
        for m in range(N - 1, maxM + 1):
            ans[m] = (ans[m] + vec[m]) % P

    out = ' '.join(str(ans[m] % P) for m in range(N - 1, maxM + 1))
    print(out)


if __name__ == "__main__":
    solve()
```

The program follows exactly the algorithm proven correct above
and conforms to the required input‑output format.