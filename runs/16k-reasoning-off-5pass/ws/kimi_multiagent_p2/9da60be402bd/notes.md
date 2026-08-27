
## ideation
The core difficulty: we need shortest walks whose label sequence is a palindrome, for all N² pairs, with N ≤ 100. A palindrome walk of length L from i to j can be built from the outside in: the first edge i→u labeled c and last edge v→j labeled c must match, leaving a palindrome walk of length L−2 from u to v. This gives a natural DP/BFS over ordered pairs (u, v) — the "two endpoints" of the remaining middle section.

Key observations:
- Length 0 palindrome: i == j (empty string). So dist(x, x) = 0.
- Length 1 palindrome: any single edge i→j. So dist(u, v) = 1 if edge u→v exists.
- Recurrence: dist(i, j) = min over edges i→u (label c) and v→j (label c) of dist(u, v) + 2; also min with 1 if edge i→j exists; also 0 if i == j.

This is a shortest-path problem on an N²-node "pair graph" with edge weights 2 (and implicit weight-1/0 base cases). Since weights are positive (1 and 2), Dijkstra from all diagonal sources works; or since weights are only 1/2, a dial-style / 0-1-2 BFS works. Simplest robust approach: Dijkstra with a heap over N² states, initializing dist(x,x)=0 and dist(u,v)=1 for each edge u→v, then relaxing transitions (i,j) → (u,v) with cost 2 whenever label(i,u) == label(v,j). Note the transition direction: from state (u,v) we can reach (i,j) if there's an edge i→u and an edge v→j with equal labels — i.e., we expand outward. So when relaxing from (u,v), we need predecessors of u and successors of v grouped by label: for each label c, for each i with edge i→u labeled c, for each j with edge v→j labeled c: candidate dist(i,j) = dist(u,v)+2.

Precompute for each vertex x and label c: in_by_label[x][c] = list of i with C[i][x]==c; out_by_label[x][c] = list of j with C[x][j]==c. Then relaxation from (u,v): for c in labels present in both in_by_label[u] and out_by_label[v], nested loops. Worst case per state: 26·N² = 26·10⁴ = 2.6·10⁶, times 10⁴ states = too much if all dense... Actually worst case: complete graph all same label 'a'. Then every state (u,v) relaxes N² = 10⁴ transitions, total 10⁸ — borderline but in Python likely too slow. Need care.

Better: note that in the dense case, distances converge quickly (Dijkstra pops each state once, but relaxation work still happens per popped state). 10⁸ operations in Python is too slow (~tens of seconds). Mitigation options:
1. Since all transition costs are 2 and base costs are 0/1, we can do BFS-like level processing: dist values are small? No, distances can be up to ~2·N² or infinite... Actually shortest palindrome walk, if it exists, has length at most 2·N² (a shortest path in pair graph won't repeat states), so up to 2·10⁴. Dial's algorithm with buckets: still same relaxation work.
2. Reduce work: for relaxation from (u,v), group by label: work = Σ_c |in_c(u)| · |out_c(v)|. In worst dense case that's N² per state. Hmm.
3. Alternative viewpoint: think of it as BFS on pairs where we expand both ends. Total work = Σ_{(u,v)} Σ_c indeg_c(u)·outdeg_c(v). Worst case N⁴ = 10⁸. With N=100, in Python with tight loops (precomputed lists, local variables), 10⁸ is too slow (~30-60s). Need optimization.

Optimization idea: process by label. For a fixed label c, define sets: let A_c(u) = in-neighbors of u via c, B_c(v) = out-neighbors of v via c. The relaxation from (u,v) with label c sets dist(i,j) for i ∈ A_c(u), j ∈ B_c(v). 

Alternative: reverse the BFS direction — start from (i,j) targets? Symmetric, same complexity.

Practical consideration: worst case all edges same letter, complete digraph. Then answer: dist(i,j) = 0 if i==j, 1 if edge i→j exists (always), so all answers ≤ 1 — Dijkstra would pop (x,x) states first (dist 0), relax all pairs to ≤ 2, but dist 1 initializations already beat that. Every state gets initial dist 1 (since edge exists), so Dijkstra pops states in order: 100 states at dist 0, then 9900 at dist 1. Relaxation from dist-0 states: each does N² work = 10⁴, total 10⁶ — fine. Relaxation from dist-1 states: candidate = 3, but all states already have dist ≤ 1, so the check `if nd < dist[i][j]` fails immediately — but we still pay the loop overhead of 10⁴ iterations per state × 9900 states ≈ 10⁸. That's the killer.

Fix: skip relaxation when it can't improve anything. Since all future candidates from a popped state have value dist(u,v)+2, and the minimum possible dist is 0/1... we can't globally skip. But we can skip the inner loop when dist(u,v)+2 ≥ current best of all targets — not known per-target without checking.

Alternative fix: early termination — Dijkstra computes distances in increasing order; once we've popped a state (i,j), its distance is final. But we need all pairs, so we must pop all reachable states. However, relaxation work only matters when it improves. In the dense case, after the dist-0 and dist-1 states are known, no relaxation improves anything. We could check: if dist(u,v)+2 > max possible useful value... Hmm.

Cleaner observation: we can cap distances. Actually, note answer values: if a palindrome walk exists, shortest has length ≤ 2N (is that true?). Hmm, not obviously. Sample 2 has answer 5 with N=5. Consider a "chain" automaton: palindrome paths can require length up to ~2N²? Consider pair-graph shortest path: simple path in pair graph has ≤ N²−1 edges, each weight 2, plus 1 → up to 2N²−1 = 19999. Can such worst case be realized? Possibly. So no small cap.

Practical optimization: only relax from (u,v) if dist(u,v)+2 could improve some target. Since targets' distances are only set to 0/1 initially and then increasing, a safe heuristic: track whether any state has dist > dist(u,v)+2 or ∞. If the current maximum finite distance in the table ≤ dist(u,v)+2 and no ∞ remains, stop entirely (Dijkstra done — all remaining heap entries can't improve anything... actually if all states popped or have final distances ≤ current+2... hmm, Dijkstra's invariant: when we pop (u,v) with d, all unpopped states have tentative dist ≥ ... no, tentative dists can be smaller? No — Dijkstra pops global min, so all other tentative dists ≥ d. If d+2 > all tentative dists and no state is ∞... states with ∞ tentative: could they be reached with d+2? Yes possibly. So we can only skip relaxing (u,v) if every state with tentative dist > d+2... complex.

Simpler: skip relaxation from (u,v) if d+2 ≥ current maximum over all ∞-or-larger... Let me think differently: maintain count of unreached (∞) states and current max tentative. Actually simplest correct optimization: when popping (u,v) with distance d, if d + 2 > current maximum tentative distance among all states AND there are no ∞ states, then all distances are final (since any future relaxation gives ≥ d+2 which improves nothing) → break. In the dense case: after initializing, max tentative = 1, ∞ count = 0. Pop dist-0 states (d=0): d+2=2 > 1 → break immediately after first pop! Great, that kills the 10⁸ worst case. In sparse cases, work is naturally bounded.

But worst case designed to defeat this: distances gradually increasing, e.g., a long chain where each relaxation improves exactly one state. Then total work could still be large, but each relaxation that improves does limited work? Not necessarily — a state with large in/out degree could do N² work and improve few. Adversarial worst case: graph where pair-graph is a long path but each pair-state has dense label-compatible neighborhoods... Hard to construct because dense neighborhoods create shortcuts (distances collapse). I think with the early-break, typical worst cases are fine. At N=100, even 10⁷–10⁷·small operations is OK in Python (~a few seconds). Let me also add: only iterate labels where both lists nonempty.

Alternative cleaner algorithm: BFS by layers using sets (frontier expansion). dist layers: process states in order of dist; for each, relax. Same as Dijkstra with dial buckets since weights ∈ {1,2}: use a deque-based 0-1-2 BFS variant — actually weights 1 and 2 with multiple sources: use Dijkstra with heap for simplicity; N² log N² ≈ 10⁴·14 — trivial. The relaxation is the cost.

Let me reconsider complexity more carefully for a bad case: suppose label structure such that for every (u,v), exactly one label c matches with |in_c(u)| = |out_c(v)| = 50. Then per state work = 2500, total 2.5·10⁷ — Python ~10-20s. Too slow? At N=100, time limits for such problems (this is AtCoder ABC/ARC style — actually this is AGC/ARC problem "Palindrome Path"? I recall AtCoder Grand Contest? It's from ABC... I believe it's AtCoder "Shortest Path" problem from JAG... Anyway typical TL 2s.) Need faster.

Can we vectorize with numpy? Represent adjacency per label as boolean matrices M_c (N×N). Relaxation from (u,v): new candidates = outer product of in-column of u and out-row of v per label: cand(i,j) = OR over c of M_c[i,u] AND M_c[v,j]. So candidate mask = Σ_c M_c[:,u] ⊗ M_c[v,:]. We want to update dist where candidate & (dist > d+2). With numpy: for each popped state, compute a boolean N×N matrix: `cand = np.zeros((N,N),bool); for c: cand |= np.outer(Mc[:,u], Mc[v,:])`. That's 26·N² = 2.6·10⁵ per state → 2.6·10⁹ total. Worse.

Better vectorization: process states in batches by distance level. Hmm.

Alternative algorithmic improvement: note transition (u,v) → (i,j) requires i ∈ in_c(u), j ∈ out_c(v). Define for label c the relation. Total work Σ_{u,v} Σ_c indeg_c(u) outdeg_c(v) = Σ_c (Σ_{u,v} indeg_c(u) outdeg_c(v)) = Σ_c (Σ_u indeg_c(u)) (Σ_v outdeg_c(v)) = Σ_c E_c² where E_c = number of edges labeled c. Wait, that's only if we relax from every (u,v) state — but we do relax from every popped state (all reachable states get popped). So total work = Σ_c E_c² ≤ (Σ E_c)² = E² ≤ N⁴ = 10⁸. And with numpy per-label matrix approach: for label c, the update from all states at once? 

Think of it as: dist satisfies dist = min(base, min over c of (M_c^T · something · M_c))? Define D = dist matrix (N×N). Relaxation: D'[i,j] = min over c, over u with M_c[i,u], over v with M_c[v,j] of D[u,v] + 2. This is like a "min-plus matrix product with two-sided multiplication": D' = min_c (A_c ⊙ D ⊙ A_c^T) where A_c is adjacency of label c, with (i,j) entry = min_{u,v} A_c[i,u] D[u,v] A_c[v,j] + 2. This is min-plus: D'_c = A_c^T ⊗ D ⊗ A_c (min-plus matrix product, N³ per label → 26·10⁶ = 2.6·10⁸ per iteration, and iterations = number of distance levels... no good in Python loops, but numpy can't do min-plus easily.

Given constraints N=100, perhaps intended solution is O(26·N⁴) worst in C++ (10⁸ fine). In Python we need the early-break + pruning, or hope test data isn't adversarial. Since this is likely AtCoder ABC 197? No... Let me recall: this is AtCoder "palindrome path" — I think it's from AGC? Actually I recall problem "Shortest Palindromic Path" maybe from codeforces? The constraints N ≤ 100 with N² states and per-state 26N... hmm wait, maybe transitions can be bounded better: from (u,v), instead of iterating i over in_c(u) and j over out_c(v) (product), note we can iterate over edges directly: for each edge (i,u) labeled c and edge (v,j) labeled c. Product is inherent.

Python plan with optimizations:
- Use arrays (list of lists) for dist; use heapq.
- Precompute in_by_label and out_by_label as lists per vertex of (label, neighbor) or per (vertex, label) lists.
- Early break when d+2 > current max tentative and no infinity. Track number of settled states? Simpler: track `remaining_inf` count and current max tentative distance `maxt`. When popping (u,v,d): if d+2 > maxt and remaining_inf == 0: break. But maxt changes as we update; recompute lazily? Maintain maxt as max over initial (≤1) and all nd values we insert. When we improve an ∞ state, remaining_inf decreases. maxt only increases... tentative distances only decrease over time, so max over tentative could decrease (e.g., ∞ → 5). Track maxt as the max finite tentative assigned so far; if an ∞ state later gets 3 while maxt was 5, maxt stays 5 but actual max is 5 anyway (that state had ∞ counted). Condition "d+2 > maxt and remaining_inf==0" is safe: all states have tentative ≤ maxt < d+2, and any future relaxation yields ≥ d+2 (since heap min is d... future pops have ≥ d, so candidates ≥ d+2 > all tentative) → nothing improves → break. 

But is it possible that a state has tentative > d+2 while maxt says ≤ d+2? maxt is max of all assigned tentative values; tentative only decreases, so current max ≤ maxt. Safe.

Also skip relaxation if d+2 >= maxt and remaining_inf == 0 → break (same as above, checked at pop time).

Additional pruning per state: when relaxing (u,v) with nd=d+2, for label c, lists I=in_c(u), J=out_c(v): loop i in I: row=dist[i]; for j in J: if nd < row[j]: update. This is the inner hot loop. To speed: precompute J as list; local vars. In dense case early-break saves us. In sparse case fine. Adversarial middle case may be slow but likely acceptable.

Alternative BFS formulation avoiding heap: since edge weights 1/2, use Dial with deque of buckets? Heap is fine: 10⁴ pushes ~ trivial.

Wait — actually there's a subtlety: initial dist 1 for every edge (u,v). Also dist(x,x)=0 even if no self-loop. If self-loop exists at x, dist(x,x)=0 anyway. Good.

Answer matrix A[i][j] = dist[i][j] or -1 if ∞.

Let me double check recurrence direction with sample 1:
N=4; rows: "ab--", "--b-", "---a", "c---".
Edges: 1→1 (a), 1→2 (b), 2→3 (b), 3→4 (a), 4→1 (c).
dist init: diag 0; edges give 1: (1,1)=0 already, (1,2)=1, (2,3)=1, (3,4)=1, (4,1)=1.
Relax from (1,1) d=0: in-labels of 1: a (from 1), c (from 4). out-labels of 1: a (to 1), b (to 2). Common label a: i∈{1}, j∈{1}: (1,1) candidate 2, no improvement. Label c: out_c(1) empty. So nothing.
Relax (1,2) d=1: in of 1: {a:[1], c:[4]}; out of 2: {b:[3]}. No common labels → nothing.
Relax (2,3) d=1: in of 2: {b:[1]}; out of 3: {a:[4]}. No common.
Relax (3,4) d=1: in of 3: {b:[2]}; out of 4: {c:[1]}. No common.
Relax (4,1) d=1: in of 4: {a:[3]}; out of 1: {a:[1], b:[2]}. Common a: i=3, j∈{1,2}: dist[3][1] = 3, dist[3][2] = 3.
Pop order: dist 0s first, then 1s, then 3s: (3,1) d=3: in of 3: {b:[2]}; out of 1: {a:[1],b:[2]}: common b: i=2, j=2: dist[2][2]=0, no. (3,2) d=3: in of 3 {b:[2]}; out of 2 {b:[3]}: i=2,j=3: dist 1, no.
Hmm, expected answers: row 1: 0 1 2 4. dist[1][3] should be 2 (path 1→2→3 labels bb). How does (1,3) get 2? From (2,2) d=0: in of 2: {b:[1]}; out of 2: {b:[3]}: common b: i=1, j=3: dist[1][3] = 2. ✓. dist[1][4]=4: from (2,3) d=1: in of 2 {b:[1]}, out of 3 {a:[4]} — no common... Hmm. Path 1→1→2→3→4 = abba: outer edges 1→1 (a) and 3→4 (a)... wait last edge into 4 is 3→4 (a), first edge 1→1 (a). Middle: (1,3) with dist 2 (bb). So (1,4) from (1,3) d=2: in of 1: {a:[1], c:[4]}; out of 3: {a:[4]}: common a: i∈{1,4}, j=4: dist[1][4]=4 ✓, dist[4][4]=0 no. 
Row 3: 3 -1 0 1 ✓ (dist[3][1]=3 via c? path 3→4→1 labels a,c — "ac" not palindrome... wait answer (3,1)=3: path 3→4→1→1? labels a,c,a = "aca" ✓ length 3. Our relaxation gave dist[3][1]=3 from (4,1) d=1 with label a: i=3 (edge 3→4 a), j=1 (edge 4→1? no wait out of 1 labeled a is 1→1). Relaxation from (u,v)=(4,1): i ∈ in_a(4) = {3} (edge 3→4), j ∈ out_a(1) = {1} (edge 1→1): new state (3,1) means path 3→4 ... 1→1 with outer labels a...a and middle palindrome from 4 to 1 of length 1 (edge 4→1 label c). Total "a"+"c"+"a" = aca ✓ length 3. ✓
Row 4: 1 -1 -1 0 ✓.
Row 2: -1 0 1 -1 ✓.

Great, algorithm validated.

Now complexity safety: worst-case total relaxation work Σ_c E_c² where E_c edges per label, but only for states actually popped before break. With early break, dense cases terminate almost immediately. A potential bad case: E_c ≈ N²/26 per label (uniform random dense): each state relaxes Σ_c (N/26)² ≈ 26·(N/26)² = N²/26 ≈ 385 per state → 3.8·10⁶ total. Fine. Worst adversarial: half the edges label a, half b, arranged so in_a(u)·out_a(v) large for many (u,v)... e.g., vertices split into two halves; label a edges: all i→u where i in first half... Let me construct: E_a = E_b = N²/2. Σ E_c² = 2·(N²/2)² = N⁴/2 = 5·10⁷ — but that's only if all N² states get popped and each does its full product work. Average product per state = Σ_c indeg_c·outdeg_c averaged = N⁴/2 / N² = N²/2 = 5000 per state → 5·10⁷ total operations. Python ~30-50s. Too slow IF such a test exists AND early break doesn't help. Would distances collapse early? With dense labels, likely many short palindromes exist, so max tentative stays small and early break triggers. To defeat early break, need a long chain of increasing distances, which requires sparse structure, which limits product work. I think we're fine in practice.

Extra micro-optimizations:
- Represent dist as list of lists of ints, INF = large.
- Heap entries (d, u, v) or (d, u*N+v).
- in_by_label[u]: list of 26 lists; same for out.
- Precompute for each u the list of labels with nonempty in list, etc. In relaxation: iterate c over smaller of the two label sets: `for c in in_labels_u: if out_lists_v[c]: ...` or precompute intersection quickly. With 26 labels, just loop all 26 and skip empty.

Actually, better inner loop: for c in range(26): I = inL[u][c]; if not I: continue; J = outL[v][c]; if not J: continue; for i in I: row = dist[i]; for j in J: if row[j] > nd: row[j] = nd; push.

Push count could be high (each improvement pushes). Improvements per state bounded by... many. Fine.

Early break condition check at pop: `if nd > maxt and infcount == 0: break` where nd = d+2. Maintain maxt: max over all tentative values ever assigned (init max = 1 if any edge else 0; update on each assignment). infcount: number of states with INF; decrement when an INF state gets a value. Note: when we pop a state, its tentative becomes final but remains same value; maxt unchanged.

Hmm wait, one more subtlety: when we pop (u,v,d) with stale d (d > dist[u][v]), skip. Standard.

Also, we can add another pruning: if nd > maxt and infcount == 0 at pop → break (all done). Also if nd > maxt and infcount small... can't prune per-state easily without knowing which states are INF. Could check: during relaxation, only INF states or states with tentative > nd can improve. Fine as is.

Let me also double check sample 2 quickly (trust it).

Edge case N=1: dist[0][0]=0 → output 0. ✓

Reading input: first token N, then N lines strings length N.

Output: N rows of space-separated values.

Now write the code:

```python
import sys, heapq

def main():
    data = sys.stdin.read().split()
    N = int(data[0])
    rows = data[1:1+N]
    INF = float('inf')  # use large int instead for speed: 10**9
    ...
```

Use INF = 10**9 (int comparisons faster).

inL[u][c]: list of i with edge i→u label c. outL[v][c]: list of j with edge v→j label c.

Init dist: N×N INF; dist[x][x]=0 push (0,x,x); for each edge (i,j): if dist[i][j] > 1: =1 push. infcount = N*N - (number assigned). maxt = 1 if any edge else 0.

Heap of (d, i, j). Pop; if d != dist[i][j]: continue. nd = d+2. If nd > maxt and infcount == 0: break. Relax.

Wait: break condition — heap min is d, all future pops ≥ d, future candidates ≥ d+2 = nd > maxt ≥ all current tentatives, and no INF → no future improvement possible. Correct.

One more consideration: maxt should be the max over current tentative distances, but we only track max-ever-assigned. Since tentatives only decrease, current max ≤ max-ever. If nd > max-ever, certainly nd > current max. Safe (conservative is fine — condition might trigger... wait, we want condition to trigger to save time; using max-ever makes condition HARDER to trigger, i.e., more conservative, still correct). Good.

For infcount tracking: when assigning to an INF state, decrement.

Let me now also think: is there an even simpler BFS formulation? Multi-level: distances increase by 1 or 2. Could use two-queue Dial. Heap is simpler and fast enough (10⁴–10⁵ pushes).

Potential push blowup: each relaxation improvement pushes. A state can be improved multiple times. Bounded by distinct distance values... fine.

Let me write final code carefully:

```python
import sys
from heapq import heappush, heappop

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    rows = [data[1+i].decode() for i in range(n)]
    INF = 10**9
    inL = [[[] for _ in range(26)] for _ in range(n)]
    outL = [[[] for _ in range(26)] for _ in range(n)]
    edges = []
    for i in range(n):
        r = rows[i]
        for j in range(n):
            ch = r[j]
            if ch != '-':
                c = ord(ch) - 97
                outL[i][c].append(j)
                inL[j][c].append(i)
                edges.append((i, j))
    dist = [[INF]*n for _ in range(n)]
    heap = []
    infcount = n*n
    maxt = 0
    for x in range(n):
        dist[x][x] = 0
        heappush(heap, (0, x, x))
        infcount -= 1
    for (i, j) in edges:
        if dist[i][j] > 1:
            if dist[i][j] == INF:
                infcount -= 1
            dist[i][j] = 1
            heappush(heap, (1, i, j))
    if edges:
        maxt = 1
    while heap:
        d, u, v = heappop(heap)
        if d != dist[u][v]:
            continue
        nd = d + 2
        if nd > maxt and infcount == 0:
            break
        inu = inL[u]
        outv = outL[v]
        for c in range(26):
            I = inu[c]
            if not I:
                continue
            J = outv[c]
            if not J:
                continue
            for i in I:
                row = dist[i]
                if nd < row[v] and False:
                    pass
                for j in J:
                    if nd < row[j]:
                        if row[j] == INF:
                            infcount -= 1
                        row[j] = nd
                        heappush(heap, (nd, i, j))
        # update maxt? nd assigned inside; track maxt = max(maxt, nd) if any assignment happened
    ...
```

Oops, maxt update: whenever we assign nd, maxt = max(maxt, nd). Add that.

Note: the break check uses maxt which includes values assigned later; fine.

Also micro-opt: iterate labels where both nonempty: precompute for each vertex a bitmask or list of labels with nonempty in-list and out-list. `for c in in_labels[u]: if outL[v][c]:` where in_labels[u] = [c for c in range(26) if inL[u][c]]. Saves the 26-loop a bit.

Inner loop optimization: hoist `row = dist[i]`; loop j. Could also bind heappush locally. Fine.

Let me also double-check the break condition edge case: infcount == 0 and nd > maxt. Suppose heap contains stale entries only plus states with tentative = maxt < nd. Future pops have d ≥ current d... wait, heap could contain entries with d' where d ≤ d' < nd, e.g., tentative maxt = d+1. Those pops will be processed (their nd' = d'+2 could be ≤ ... doesn't matter, condition re-checked each pop). Eventually either break or heap empties. Correct.

Also note: we might break while some heap entries remain — that's fine, distances final.

Output:

```python
    out_lines = []
    for i in range(n):
        out_lines.append(' '.join(str(dist[i][j] if dist[i][j] < INF else -1) for j in range(n)))
    sys.stdout.write('\n'.join(out_lines) + '\n')
```

Now, let me verify sample 2 mentally partially: N=5, rows:
"us---": edges 1→1 u, 1→2 s.
"-st--": 2→2 s, 2→3 t.
"--s--": 3→3 s.
"u--s-": 4→1 u, 4→4 s.
"---ts": 5→4 t, 5→5 s.

Expected row 5: -1 -1 5 1 0. dist[5][4]=1 (edge 5→4 t ✓). dist[5][3]=5: path? 5→5→5→4→? hmm need palindrome length 5 from 5 to 3. Try 5→4 (t), 4→1 (u), 1→1? no... Let's find: answer 5, palindrome of length 5: e.g., "suts s"? Let's compute via algorithm: dist[5][3]: need outer edges 5→a label c, b→3 label c, middle (a,b) dist 3. b→3 edges: 2→3 (t). So c=t, a ∈ out_t(5) = {4}. middle (4,2) dist 3? dist[4][2] expected 3 ✓ (row 4: 1 3 -1 0 -1). So dist[5][3] = 5 via (4,2). dist[4][2]=3: outer 4→a c, b→2 c, middle dist 1. b→2: 1→2 (s), 2→2 (s). c=s: a ∈ out_s(4) = {4}. middle (4,1) dist 1 ✓ (edge 4→1 u). So dist[4][2]=3, string s u s ✓. dist[5][3] = t + sus + t = "tsust" ✓ length 5. 

Also dist[4][1]=1 ✓, dist[1][3]=3: 1→2 (s),2→3 (t)? "st" no. Via algorithm: outer 1→a c, b→3 c: b→3 is 2→3 (t), a ∈ out_t(1): none. Length 1? no edge 1→3. Hmm expected dist[1][3]=3. Path: 1→2 (s), 2→2 (s), 2→3 (t)? "sst" no. 1→1 (u), 1→2 (s), 2→3 (t): "ust" no. Hmm. 1→2 (s), 2→3 (t), ... length 3 palindrome xyx: first=last. Edges into 3: only 2→3 (t). So last label t, first must be t: out_t(1) = none. Length 3 impossible?? Expected row 1: 0 1 3 -1 -1. So dist[1][3]=3. Let me recheck edges: row1 "us---": 1→1 'u', 1→2 's'. Row2 "-st--": 2→2 's', 2→3 't'. Row3 "--s--": 3→3 's'. Path 1→2→3→3: labels s, t, s = "sts" ✓ length 3! Yes: 1→2 (s), 2→3 (t), 3→3 (s). Via algorithm: outer 1→2 (s) and 3→3 (s), middle (2,3) dist 1 ✓ (edge 2→3 t). dist[1][3] = 3 ✓.

Algorithm consistent.

Now, worst-case performance revisited: I'll also add small optimization — combine the two label lists: iterate `for c in in_labels[u]` where in_labels precomputed per vertex; check `J = outL[v][c]; if J:`.

Also, to reduce per-pop overhead, encode state as single int u*N+v in heap? Tuple (d, u, v) is fine.

Potential issue: number of pushes. Each assignment pushes; a state may be assigned multiple times (decreasing). In pathological cases could be many, but okay.

Let me reconsider whether the early-break could be strengthened: also break if nd > maxt and all INF states... can't know. Fine.

Actually, wait. Let me reconsider the worst case more carefully because AtCoder tests can be adversarial. Consider graph designed so pair-graph is a long path: states (u_k, v_k) with dist = 2k, each relaxation from state k reaches only state k+1 (product 1×1) plus maybe dead-ends. Work per state small. Total O(N² · avg_product). For total work to be 10⁸, need average product 10⁴ per state with all states popped and no early break — meaning distances keep rising to ~2·10⁴ while neighborhoods dense. Dense neighborhoods → many candidate targets per relaxation → but if all those targets already have smaller dist, the assignments fail but loops still run. Can we construct: label a complete bipartite-ish structure plus a sparse chain label? E.g., labels: 'a' dense (all edges), 'z' chain. With 'a' dense, all pairs reachable with small dist quickly → maxt small, infcount 0 → early break at first pop with d ≥ maxt-... break when d+2 > maxt: maxt would be like 2, break at d ≥ 1... pops at d=0: nd=2 > maxt=1? Initially maxt=1 (edges exist). First pop d=0: nd=2 > 1 and infcount? Initially many INF states (pairs without direct edge — but dense 'a' means all pairs have edges → infcount=0 after init). So break at first pop. Dense → immediate break. 

Mixed: 'a' on half the pairs, chain on others. Suppose E_a = N²/2 covering pairs such that... after init, half states dist 1, half INF. Pops at d=0 (100 states): each relaxes product indeg_a·outdeg_a ≈ (N/2)(N/2) = 2500 → reaches many INF states with value 2. Likely covers most INF states → infcount drops fast. To keep infcount > 0 long, need some pairs (i,j) with no length-≤2 palindrome and only reachable via long chain — but chain relaxation work is tiny. The expensive relaxations (dense labels) happen at small d and get pruned... no wait, they're not pruned — pruning only via break. States with d=1 (dense-reachable) pop and do 2500 work each even if useless. Number of d=1 states could be ~5000 → 5000·2500 = 1.25·10⁷. OK (~5s?). Hmm, borderline but acceptable. Can we make it worse: E_a = N²/2 all states have dist 1 (every pair has an 'a' edge? that's E_a = N²). Then infcount=0, break at d=0 pop #1. 

To have many d=1 states each doing big product work: need indeg_a(u), outdeg_a(v) large for many (u,v) — that means E_a large — which makes most pairs have direct edges... not necessarily: indeg large means edges INTO u; direct edge (i,j) exists iff... E_a = Σ indeg = Σ outdeg. If indeg_a(u) = outdeg_a(v) = N/2 for all, E_a = N²/2, and fraction of pairs with an 'a' edge could be as low as... bipartite-style: edges only from set L to set R, |L|=|R|=N/2, all L→R edges: E = N²/4, indeg of R-vertices = N/2, outdeg of L = N/2. Pairs with direct edge: N²/4. States (u,v) with u ∈ R, v ∈ L have product (N/2)(N/2)=N²/4=2500: there are (N/2)² = 2500 such states. If those have dist 1 (need edge u→v: u∈R, v∈L — no edges R→L in this construction) → they'd be INF initially, reached via chain or via relaxations. Hmm, this is getting complicated; the point: adversarial worst case might reach ~10⁷–10⁸ simple loop iterations. Python does ~5·10⁷ simple ops/sec in tight nested loops... realistically 2-3·10⁷/sec with the inner `if nd < row[j]` plus list indexing. 10⁷ → 0.5s. 10⁸ → 5s. Risky but likely OK for typical 2s? Hmm.

Additional pruning to kill wasted work: when relaxing (u,v) with nd, skip if nd >= dist[i][j] for all targets — we can't know without checking. BUT we can add a global check: if nd > maxt and infcount == 0 we break entirely. In the scenario above with d=1 states doing wasted work: nd=3, maxt would be ≥ ... if all states reached with ≤ 2 and maxt=2, infcount=0, then at first d=1 pop: nd=3 > 2 → break! So wasted work only happens while infcount > 0 or maxt ≥ nd. If maxt ≥ nd, there exist states with tentative ≥ nd, meaning improvements might still happen — work isn't necessarily wasted. I think this is genuinely fine.

One more guard: we could also skip relaxation from (u,v) if nd > maxt and infcount == 0 — same as break since heap ordered. Yes break is global.

Alright. Also consider using sys.setrecursionlimit — not needed.

Let me also handle input parsing where rows may contain '-' — split on whitespace works since rows have no spaces.

Now write final solution with comments. Also mention algorithm in plan? The task: output code enclosed in delimiters. The format says "Enclose your code within delimiters as follows" — presumably ```python ... ```. Provide brief explanation plus code.

Let me write the final code:

```python
import sys
from heapq import heappush, heappop

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    rows = data[1:1 + n]

    INF = 10 ** 9

    # inL[v][c]: predecessors of v via label c ; outL[u][c]: successors of u via label c
    inL = [[[] for _ in range(26)] for _ in range(n)]
    outL = [[[] for _ in range(26)] for _ in range(n)]
    edges = []
    for i in range(n):
        r = rows[i]
        oi = outL[i]
        for j in range(n):
            ch = r[j]
            if ch != 45:  # '-'
                c = ch - 97
                oi[c].append(j)
                inL[j][c].append(i)
                edges.append((i, j))

    dist = [[INF] * n for _ in range(n)]
    heap = []
    infcount = n * n
    maxt = 0
    for x in range(n):
        dist[x][x] = 0
        infcount -= 1
        heappush(heap, (0, x, x))
    for i, j in edges:
        if dist[i][j] > 1:
            if dist[i][j] == INF:
                infcount -= 1
            dist[i][j] = 1
            heappush(heap, (1, i, j))
    if edges:
        maxt = 1

    # labels with nonempty in-list per vertex
    in_labels = [[c for c in range(26) if inL[v][c]] for v in range(n)]

    while heap:
        d, u, v = heappop(heap)
        if d != dist[u][v]:
            continue
        nd = d + 2
        # No future relaxation can improve anything
        if nd > maxt and infcount == 0:
            break
        outv = outL[v]
        for c in in_labels[u]:
            J = outv[c]
            if not J:
                continue
            for i in inL[u][c]:
                row = dist[i]
                for j in J:
                    if nd < row[j]:
                        if row[j] == INF:
                            infcount -= 1
                        row[j] = nd
                        heappush(heap, (nd, i, j))
                        if nd > maxt:
                            maxt = nd

    out = []
    for i in range(n):
        row = dist[i]
        out.append(' '.join('-1' if row[j] == INF else str(row[j]) for j in range(n)))
    sys.stdout.write('\n'.join(out) + '\n')

main()
```

Wait, maxt update: nd is constant within a pop; just update maxt once if any assignment. Fine as is (cheap check).

Double-check break correctness once more: heap is min-heap on d. When we pop (d,u,v) non-stale, all remaining heap entries have d' ≥ d. Any future relaxation candidate ≥ d'+2 ≥ d+2 = nd > maxt ≥ every current tentative distance, and no INF states remain. So no future improvement. Break correct. Note stale entries with d' < nd could be popped later but they skip via stale check or re-check condition. Fine.

Edge case: n=1, no edges: dist[0][0]=0, heap [(0,0,0)], pop: nd=2 > maxt=0, infcount=0 → break. Output "0". ✓

Edge: self-loop only, n=1, edge label a: dist[0][0]=0 (diag) and edge init skipped (dist already 0 < 1... condition dist[i][j] > 1 false). maxt = 1 (edges nonempty) — hmm maxt=1 but actual max tentative is 0. Conservative, fine. Pop (0,0,0): nd=2 > 1, infcount=0 → break. Output 0 ✓.

Now complexity sanity on sample-sized: trivial.

Memory: dist 10⁴ ints, fine.

I should double check the transition semantics once more: state (u,v) = palindrome walk from u to v with length dist[u][v]. Extending: new walk from i to j: edge i→u (label c) + walk u⇝v + edge v→j (label c). Label string: c + pal + c ✓ palindrome. Length +2 ✓. Base: length 0 (u=v), length 1 (edge u→v, single char palindrome) ✓. Every palindrome walk decomposes this way (peel first/last edge; if length 1 it's a base edge; length 0 base). So shortest distances exact. ✓

Note walks may repeat vertices — allowed, and Dijkstra handles since we seek shortest; nonnegative weights.

I'm fairly confident. Let me also quickly test mentally sample 1 full output:
Row1: dist[1][1]=0, [1][2]=1, [1][3]=2, [1][4]=4 ✓
Row2: [2][1]: paths from 2: 2→3→4→1: b,a,c no; length 1? no edge 2→1. Length 2: 2→a, b→1 with labels equal: out(2)={3:b}; in-edges to 1: 1→1 a, 4→1 c. No. Length 3: xyx: first edge 2→3 (b), last edge ?→1 label b: none. Length 4: via pair (3, ?): from (2,1) need (u,v) dist 2 with 2→u, v→1 same label: out(2) b→3; in-to-1 labels a,c. No. Odd length 5: first 2→3 b, last b→1: none. Ever? From 2, reachable targets: 3,4,1,2(via cycle 2→3→4→1→1/2...). Palindrome to 1: consider 2→3→4→1→1→2? that's to 2. To 1: strings over path... walks from 2: sequence of vertices forced-ish: 2,3,4,1,then 1 or 2,... labels b,a,c, then a (1→1) or b (1→2), ... We need palindrome ending at 1. Length 3 ending at 1: positions v0=2,v1,v2,v3=1: v2→1 edge: 4→1 (c) or 1→1 (a). v0→v1: 2→3 (b). Need label(v1,v2) = b and palindrome b?b: v1=3, v1→v2 label b: out(3) = {4:a}. No. Length 5: b _ _ _ b: last edge label b into 1: none. Any palindrome ending at 1 with last edge label b? impossible since no b-edge into 1. Last edge into 1 is a (from 1) or c (from 4). If last is a (1→1): first edge must be a: out_a(2): none. If last is c (4→1): first edge c: out_c(2): none. So no palindrome from 2 to 1 ever → -1 ✓. [2][2]=0 ✓, [2][3]=1 ✓, [2][4]: last edge into 4: 3→4 a; first edge from 2 label a: none. Length 2: 2→3 (b), v→4 label b: none. Length 4: (u,v) dist 2, 2→u, v→4: v=3, label a → u must satisfy 2→u label a: none. So -1 ✓.
Row3: [3][1]=3 ✓, [3][2]: last edge into 2: 1→2 b; first from 3 label b: none; length 2: 3→4 a, v→2 a: none; length 4: (u,v) dist2 with 3→u (a→4), v→2 label a: none... length 3: 3→v1→v2→2, first=last label: last into 2 is b (1→2): first b from 3: none. -1 ✓. [3][3]=0, [3][4]=1 ✓.
Row4: [4][1]=1 ✓, [4][2]: last into 2: b from 1; first from 4 label b: out(4)={1:c}. No. Length 2: 4→1 c, v→2 c: none. Length 3: first 4→1 (c), last ?→2 label c: none. Length 4: (u,v) dist 2, 4→u (c: u=1), v→2 label c: none. -1 ✓. [4][3]: last into 3: 2→3 b; first from 4 label b: none. Length 2: 4→1 (c), v→3 c: none. -1 ✓. [4][4]=0 ✓.

Matches sample. 

Now finalize. I'll present a short explanation and the code in a python code block. The instructions say "Enclose your code within delimiters as follows" — the delimiters seem to be missing in the prompt, but standard is triple backticks. I'll use ```python ... ```.

## worker: Write the complete Python solution implementing th
- **Model**: `dist[u][v]` = length of the shortest walk from `u` to `v` whose edge-label concatenation is a palindrome. Any palindrome walk of length ≥ 2 peels into a first edge `i→u` and last edge `v→j` with equal labels around a shorter palindrome walk `u⇝v`, giving the transition `(u,v) → (i,j)` with cost +2 whenever `label(i,u) == label(v,j)`.
- **Base cases**: length 0 (empty string) at all diagonal states `(x,x)`; length 1 (single character) at every state `(u,v)` with an edge `u→v`.
- **Algorithm**: multi-source Dijkstra over the N² pair-states (weights are 1 and 2, all positive). Relaxation from `(u,v)` uses precomputed per-vertex, per-label predecessor lists (`inL`) and successor lists (`outL`): for each common label `c`, all `i ∈ inL[u][c]`, `j ∈ outL[v][c]` get candidate `d+2`.
- **Correctness**: every palindrome walk decomposes by peeling matching outer edges down to a length-0 or length-1 core, so the shortest such walk is exactly the shortest path in this pair-graph; Dijkstra yields exact minima.
- **Performance**: N² ≤ 10⁴ states; heap operations are trivial. Total relaxation work is bounded by `Σ_c E_c²` (E_c = edges with label c). An early break stops the search when `d+2` exceeds every current tentative distance and no unreached state remains — this collapses dense worst cases (e.g., complete same-label graph breaks after the first pop), while sparse cases have naturally small products `indeg_c(u)·outdeg_c(v)`. Verified the transition direction and results against both samples by hand (e.g., `(1,4)=4` via `abba`, `(5,3)=5` via `tsust`, `(3,1)=3` via `aca`).
