**Solution Explanation**

For every vertex `v` we keep the two pieces

* piece **A** – its current vertex is called `a`
* piece **B** – its current vertex is called `b`

A move is

```
(a , b) → (a' , b)   if a' is adjacent to a and a' ≠ b
(a , b) → (a , b')   if b' is adjacent to b and b' ≠ a
```

The start state is `(S , T)` and the goal state is `(T , S)`.

--------------------------------------------------------------------

#### 1.   From states to paths

Look at the two pieces only by their positions.
The whole sequence of moves can be described as

* piece **A** walks from `S` to `T` along a simple path `P₁`
* piece **B** walks from `T` to `S` along a simple path `P₂`

The two paths must be **internally vertex‑disjoint**,
otherwise at some moment both pieces would be on the same vertex.
If such two disjoint paths exist we can interleave the moves
(step of `P₁`, step of `P₂`, …) and the pieces never meet.
The number of performed moves is exactly  

```
|P₁| + |P₂|          (|P| … length of the path)
```

Consequently the task is:

*Find two internally vertex‑disjoint `S‑T` paths whose total length is minimum.*

If no such pair exists the answer is `-1`.

--------------------------------------------------------------------

#### 2.   Minimum‑cost flow formulation

The above problem is a classic “two vertex‑disjoint paths of minimum total
length”.  
It can be solved by a **min‑cost max‑flow** computation.

**Vertex capacity**  
To forbid using the same internal vertex in both paths we give every
vertex capacity `1`.  
A vertex `v` is split into two nodes `v_in → v_out` with capacity `1`
(and cost `0`).  
Only one unit of flow may pass `v_in → v_out`, i.e. only one of the
paths may use `v` as an internal vertex.

**Edges**  
For every original edge `{u , v}` we add two directed edges

```
u_out → v_in   (capacity 1, cost 1)
v_out → u_in   (capacity 1, cost 1)
```

Using such an edge means that a piece moves from `u` to `v`
(or the opposite direction) – exactly one move, therefore cost `1`.

**Source and sink**  
The first piece starts in `S`, the second piece in `T`.
We set  

```
source = S_out          (the “out” side of S)
sink   = T_in           (the “in”  side of T)
```

The two pieces are allowed to start / finish at `S` and `T`,
but they are not allowed to use the split edges of `S` and `T`
as internal vertices – which is exactly what the construction does.

Now we send **two units of flow** from `source` to `sink`.

* If the maximal flow is `< 2` there is no pair of disjoint paths → answer `-1`.
* Otherwise the minimum cost of sending two units is the smallest possible
  `|P₁| + |P₂|`.  
  This cost is the required minimum number of moves.

All capacities are `0/1`, the total number of vertices after splitting is
`2·N ≤ 4·10⁵`, the number of edges is `2·M + N ≤ 6·10⁵`.
We need only two augmentations, each Dijkstra (with potentials) costs  
`O(E log V)`.  
The whole algorithm works in `O((N+M) log N)` time and `O(N+M)` memory.

--------------------------------------------------------------------

#### 3.   Correctness Proof  

We prove that the algorithm prints `-1` iff the swap is impossible,
otherwise it prints the minimum number of moves.

---

##### Lemma 1  
If two pieces can be swapped, there exist two internally vertex‑disjoint
`S‑T` paths `P₁` (for A) and `P₂` (for B).

**Proof.**  
Take any successful sequence of moves.
Look at the vertices visited by piece **A** – they form a walk from `S`
to `T`. Removing possible repetitions yields a simple path `P₁`
(we may shortcut cycles because they only waste moves).
The same for piece **B` gives a simple path `P₂` from `T` to `S`.
If `P₁` and `P₂` shared an internal vertex, at the moment when
both pieces were at that vertex the move would be illegal,
contradiction. ∎



##### Lemma 2  
If two internally vertex‑disjoint `S‑T` paths exist,
the pieces can be swapped in exactly `|P₁|+|P₂|` moves.

**Proof.**  
Let `P₁ = (S = p₀, p₁, …, p_k = T)` and  
`P₂ = (T = q₀, q₁, …, q_ℓ = S)`.  
Because the paths are internally disjoint, the only common vertices of
the two sequences are the two ends `S` and `T`.

We interleave the moves as follows:

```
for i = 1 … k   move A from p_{i-1} to p_i
for j = 1 … ℓ   move B from q_{j-1} to q_j
```

During a move of **A** the vertex `p_i` is free
(`B` is still at some vertex of `P₂` and the only common vertex
`T` is already left by `B` in its first step).  
Analogously for a move of **B**.  
Thus every single move is legal, we never put two pieces on the same
vertex, and after the described steps **A** is at `T`,
**B** at `S`. The number of performed moves is `k+ℓ = |P₁|+|P₂|`. ∎



##### Lemma 3  
For any feasible swap sequence the total number of moves is at least
the minimum possible value of `|P₁|+|P₂|` over all pairs of
internally vertex‑disjoint `S‑T` paths.

**Proof.**  
By Lemma&nbsp;1 the swap yields two disjoint paths.
The total number of moves of the swap is exactly the sum of the lengths
of those two paths (each move walks one edge of one of the paths).
Therefore the swap’s length is at least the minimum achievable sum. ∎



##### Lemma 4  
In the flow network, a flow of value `2` corresponds one‑to‑one to a pair
of internally vertex‑disjoint `S‑T` paths, and its cost equals the sum
of the two path lengths.

**Proof.**  
*Path → flow*  
Take a path `P`. Walk along it: start at `S_out`, go through the edge
`S_out → v₁_in` (cost 1), then `v₁_in → v₁_out` (cost 0), then
`v₁_out → v₂_in` (cost 1), …, finally `T_in`.  
All used edges respect their capacities (each directed edge once,
each vertex‑split edge at most once).  
Sending one unit of flow along this walk gives a feasible flow.
Doing it for two disjoint paths gives a flow of value 2.

*Flow → paths*  
A unit of flow must enter the network at `S_out` and leave at `T_in`.
Because the only edges leaving a vertex `v_in` go to `v_out`,
the flow must pass `v_in → v_out`. Its capacity is 1,
hence at most one unit of flow can use a vertex `v` as an internal
vertex. Consequently the two units of flow use vertex‑disjoint sets of
internal vertices – they are two internally vertex‑disjoint `S‑T` paths.
The cost of a unit of flow is the sum of the costs of the used
original edges, i.e. the length of the corresponding path. ∎



##### Lemma 5  
The min‑cost flow of value 2 (if it exists) has cost equal to the
minimum possible `|P₁|+|P₂|`.

**Proof.**  
*Upper bound.*  
Take a pair of disjoint paths with minimum total length.
By Lemma&nbsp;4 they form a feasible flow of value 2 whose cost equals
that total length. Hence the optimum flow cost cannot be larger.

*Lower bound.*  
Let the optimum flow have cost `C`. By Lemma&nbsp;4 it corresponds to two
disjoint paths whose lengths sum to `C`. By definition of the minimum,
`C` is at least the minimum possible sum of lengths.

Thus the optimum flow cost equals that minimum. ∎



##### Lemma 6  
If the maximum flow value is smaller than `2` the swap is impossible.

**Proof.**  
If a feasible swap existed, Lemma&nbsp;1 gives two internally
vertex‑disjoint `S‑T` paths.
By Lemma&nbsp;4 they yield a flow of value 2.
Hence a flow of value 2 must exist – contradiction. ∎



##### Theorem  
The algorithm outputs  

* `-1` iff the pieces cannot be swapped,
* otherwise the minimum possible number of moves.

**Proof.**  

*If the algorithm prints `-1`.*  
That happens exactly when the max‑flow value `< 2`.
By Lemma&nbsp;6 the swap is impossible.

*If the algorithm prints a non‑negative integer `Ans`.*  
Then the max‑flow value is `2` and `Ans` is the minimum cost of sending
two units of flow.
By Lemma&nbsp;5 this cost equals the minimum possible sum of lengths of
two internally vertex‑disjoint `S‑T` paths.
By Lemma&nbsp;2 the pieces can be swapped in exactly that many moves,
and by Lemma&nbsp;3 no swap can use fewer moves.
Therefore `Ans` is the optimal answer.

Both directions are proved, completing the theorem. ∎



--------------------------------------------------------------------

#### 4.   Complexity Analysis  

*Vertices after splitting* : `2·N ≤ 4·10⁵`  
*Edges* : `2·M + N ≤ 6·10⁵`  

We run a standard successive‑shortest‑augmenting‑path min‑cost flow
with `2` augmentations.

```
Each Dijkstra :  O(E log V)
Two augmentations :  O(E log V)  =  O((N+M) log N)
Memory consumption :  O(N+M)
```

Both limits satisfy the constraints (`N, M ≤ 2·10⁵`).

--------------------------------------------------------------------

#### 5.   Reference Implementation  (C++17)

```cpp
#include <bits/stdc++.h>
using namespace std;

struct Edge {
    int to;       // target vertex
    int rev;      // index of reverse edge in adjacency list of 'to'
    int cap;      // remaining capacity
    int cost;     // cost per unit of flow
};

struct MinCostMaxFlow {
    int N;
    vector<vector<Edge>> G;
    MinCostMaxFlow(int n = 0) { init(n); }

    void init(int n) {
        N = n;
        G.assign(N, {});
    }

    // add directed edge s -> t
    void addEdge(int s, int t, int cap, int cost) {
        Edge a{t, (int)G[t].size(), cap, cost};
        Edge b{s, (int)G[s].size(), 0, -cost};
        G[s].push_back(a);
        G[t].push_back(b);
    }

    // returns {flow, cost}
    pair<int, long long> minCostFlow(int s, int t, int maxFlow) {
        const long long INF = (1LL << 60);
        int flow = 0;
        long long cost = 0;
        vector<long long> dist(N), potential(N, 0);
        vector<int> pv(N), pe(N);

        while (flow < maxFlow) {
            fill(dist.begin(), dist.end(), INF);
            dist[s] = 0;
            priority_queue<pair<long long,int>,
                           vector<pair<long long,int>>,
                           greater<pair<long long,int>>> pq;
            pq.emplace(0, s);
            while (!pq.empty()) {
                auto [d, v] = pq.top(); pq.pop();
                if (d != dist[v]) continue;
                for (int i = 0; i < (int)G[v].size(); ++i) {
                    Edge &e = G[v][i];
                    if (e.cap > 0) {
                        long long nd = d + e.cost + potential[v] - potential[e.to];
                        if (nd < dist[e.to]) {
                            dist[e.to] = nd;
                            pv[e.to] = v;
                            pe[e.to] = i;
                            pq.emplace(nd, e.to);
                        }
                    }
                }
            }
            if (dist[t] == INF) break;          // cannot augment more

            for (int v = 0; v < N; ++v)
                if (dist[v] < INF) potential[v] += dist[v];

            int add = maxFlow - flow;
            for (int v = t; v != s; v = pv[v])
                add = min(add, G[pv[v]][pe[v]].cap);

            for (int v = t; v != s; v = pv[v]) {
                Edge &e = G[pv[v]][pe[v]];
                e.cap -= add;
                G[v][e.rev].cap += add;
                cost += 1LL * add * e.cost;
            }
            flow += add;
        }
        return {flow, cost};
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int N, M, S, T;
    if (!(cin >> N >> M >> S >> T)) return 0;
    --S; --T;                     // 0‑based

    int V = 2 * N;                // split each vertex
    MinCostMaxFlow mcmf(V);

    // vertex splitting edges (capacity 1)
    for (int i = 0; i < N; ++i) {
        int in  = i * 2;
        int out = i * 2 + 1;
        mcmf.addEdge(in, out, 1, 0);
    }

    // original edges
    for (int i = 0; i < M; ++i) {
        int u, v;  cin >> u >> v;
        --u; --v;
        int u_out = u * 2 + 1, u_in = u * 2;
        int v_out = v * 2 + 1, v_in = v * 2;
        mcmf.addEdge(u_out, v_in, 1, 1);
        mcmf.addEdge(v_out, u_in, 1, 1);
    }

    int source = S * 2 + 1;   // S_out
    int sink   = T * 2;       // T_in

    auto res = mcmf.minCostFlow(source, sink, 2);
    if (res.first < 2) {
        cout << -1 << '\n';
    } else {
        cout << res.second << '\n';
    }
    return 0;
}
```

The program follows exactly the algorithm proven correct above
and conforms to the required `O((N+M) log N)` time bound.