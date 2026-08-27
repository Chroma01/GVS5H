
## ideation
The plan is essentially the standard AtCoder ABC-style solution (this is ABC 197 F or similar — actually it's a known problem). Key points to verify:

1. **State space**: pairs (u, v), ordered, N² ≤ 10⁴ states. Distance = length of palindrome walk from u to v.
2. **Sources**: (i, i) dist 0; (i, j) dist 1 if edge i→j exists (any single edge is a palindrome of length 1).
3. **Transition**: from (u, v) with dist d, for each letter c, for each in-neighbor x of u via c (edge x→u labeled c) and out-neighbor y of v via c (edge v→y labeled c): state (x, y) gets dist d+2.
4. **BFS correctness**: all edges in the state graph have weight 2, sources have weight 0 or 1. A plain FIFO BFS works if we process carefully: states with dist d generate states with dist d+2. Since all transitions add exactly 2, a simple queue BFS where we only relax when undiscovered gives shortest distances (BFS on unweighted graph where edges have uniform weight 2 — distances from sources are 0/1, and every step adds 2, so FIFO order is non-decreasing in distance). This is correct.
5. **Complexity**: For each state (u,v), iterate over letters c, in-neighbors of u with label c × out-neighbors of v with label c. Worst case per state: sum over c of indeg_c(u) * outdeg_c(v). With N=100, worst case could be 100*100 = 10⁴ per state → 10⁸ total, too slow in Python potentially. Need to think about optimization.

   Optimization: instead of iterating per state over in-neighbors × out-neighbors, we can precompute for each letter c the list of edges. Alternative approach: for each state (u,v), iterate over in-edges (x,u,c) and check whether there is an out-edge (v,y,c) — iterate y over out-neighbors of v with label c. Same thing.

   Better: precompute for each letter c, adjacency bitsets. For fixed c, in-neighbors of u form a set, out-neighbors of v form a set; the product can be large. Worst case: complete graph all labeled 'a' — then from every state we'd relax all 10⁴ pairs, but each state is relaxed only once. Total work = sum over states of (work when first popped). When state (u,v) is popped, we do indeg(u)*outdeg(v) work (for the single letter). With complete graph, that's 100*100=10⁴ per state × 10⁴ states = 10⁸. In Python that's ~ tens of seconds. Too slow.

   Key observation: once a state (x, y) is visited, we don't need to generate it again, but we still enumerate the product. However, we can bound: total relax attempts = sum over popped (u,v) of product. In the worst case (complete graph, one letter), BFS from sources: dist-1 sources are all (i,j) pairs — all states are sources! So no transitions are ever needed (all visited at distance ≤ 1). Actually with complete graph, every (i,j) has an edge, so all states are dist ≤ 1, and we can skip processing states... but BFS would still pop them and iterate. We can skip expanding a state if... no, we can't skip in general, but we can check: when we pop (u,v), all neighbors would get dist d+2; if d+2 ≥ already-known distances we still must check each. Hmm.

   Practical optimization: iterate over the smaller side. For state (u,v), choose to iterate over in-neighbors of u (across all letters) and for each, look up out-neighbors of v with same letter. Precompute out[v] as dict letter → list of vertices. Then work per state = sum over in-edges (x,u,c) of len(out_by_letter[v][c]). Worst case still 10⁸ in adversarial dense graph, but dense graph means everything is distance ≤1 and... we could add an early termination: if all states visited, stop. In dense case all 10⁴ states are sources, queue empties quickly? No — sources are all enqueued initially (10⁴ states), and we'd pop each and iterate 10⁴ work each → 10⁸. But we can avoid expanding states whose distance + 2 cannot improve anything... it can improve unvisited states only. If no unvisited states remain, break. In dense case, after initialization all states are visited, so we can skip expansion entirely — just check `if not remaining: break` or check before expanding whether any unvisited states exist. That handles dense case.

   For sparse/medium graphs, work is manageable. Realistic worst case for Python: moderate. With N=100, typical AtCoder Python solutions pass with this approach using lists. Let me estimate worst genuine case: half the pairs are sources (dist 1), others reached at dist 2... Actually let's think: worst case total work = Σ_{(u,v) expanded} Σ_{(x,u,c) ∈ in-edges} |out_c(v)|. Each in-edge (x,u,c) paired with out_c(v) list. Hard to bound below 10⁸ adversarially, but with the "stop when all visited" trick and the fact that distances are small in dense graphs, it should be fine. AtCoder's actual constraints (N ≤ 100) with Python solutions using this exact method pass (typical editorial approach). We'll implement with lists and dict-of-lists, plus early exit.

   Additional micro-optimizations:
   - Represent dist as a flat list of size N*N, initialized to -1.
   - Queue as collections.deque of integer state ids.
   - Precompute in_edges[u] = list of (x, c_index) and out_by_letter[v] = list of 26 lists.
   - When expanding (u,v): for (x, c) in in_edges[u]: for y in out_by_letter[v][c]: if dist[x*N+y] < 0: set, append.
   - Track count of unvisited; break when 0.

6. **Edge case**: self-loops — edge i→i labeled c gives palindrome "c" of length 1 from i to i, but dist 0 is already better. Fine. Also note single edge i→j is palindrome length 1 — handled as source.

7. **Answer extraction**: A_{i,j} = dist[i*N+j]. Note dist for (i,i) = 0. Output -1 if unreached.

Let me double check the transition direction: palindrome built from both ends. State (u, v) means we have a palindrome walk from u to v. To extend by 2: prepend edge x→u (label c) and append edge v→y (label c): new walk x→u ⇝ v→y has labels c + palindrome + c — palindrome from x to y. Yes, correct.

BFS order correctness: sources have dist 0 and 1 mixed in queue. Transitions add 2. A dist-1 source popped before dist-0 source could generate dist-3 states before dist-0 source generates dist-2 states — but FIFO still processes in non-decreasing order? Queue: [dist0 sources..., dist1 sources...] if we enqueue all dist-0 first, then dist-1. Popping dist-0 sources generates dist-2 states appended after dist-1 sources. Then dist-1 sources generate dist-3 states appended after dist-2 states. Order: 0,1,2,3 — non-decreasing. Correct as long as we enqueue all 0-sources before 1-sources. Since each state is assigned distance only when first discovered, and discovery order is non-decreasing in distance, distances are shortest. 

Alternative cleaner method: Dijkstra, but BFS suffices.

Now write the code.

Parsing: N, then N lines each of length N (no separators).

Implementation:

```python
import sys
from collections import deque

def main():
    input = sys.stdin.readline
    N = int(input())
    in_edges = [[] for _ in range(N)]          # in_edges[u] = list of (x, c)
    out_by_letter = [[[] for _ in range(26)] for _ in range(N)]  # out_by_letter[v][c] = list of y
    grid = [input().strip() for _ in range(N)]
    for i in range(N):
        row = grid[i]
        for j in range(N):
            ch = row[j]
            if ch != '-':
                c = ord(ch) - 97
                in_edges[j].append((i, c))       # edge i -> j
                out_by_letter[i][c].append(j)
    INF = -1
    size = N * N
    dist = [-1] * size
    dq = deque()
    # dist 0 sources
    for i in range(N):
        s = i * N + i
        dist[s] = 0
        dq.append(s)
    # dist 1 sources
    for i in range(N):
        row = grid[i]
        base = i * N
        for j in range(N):
            if row[j] != '-':
                s = base + j
                if dist[s] < 0:
                    dist[s] = 1
                    dq.append(s)
    remaining = size
    # count visited
    visited = 0
    for d in dist:
        if d >= 0:
            visited += 1
    while dq and visited < size:
        s = dq.popleft()
        u, v = divmod(s, N)
        nd = dist[s] + 2
        obv = out_by_letter[v]
        for x, c in in_edges[u]:
            for y in obv[c]:
                t = x * N + y
                if dist[t] < 0:
                    dist[t] = nd
                    dq.append(t)
                    visited += 1
    out_lines = []
    for i in range(N):
        base = i * N
        out_lines.append(' '.join(str(dist[base + j]) for j in range(N)))
    sys.stdout.write('\n'.join(out_lines) + '\n')

main()
```

Wait — the early exit `visited < size` only helps when all states reachable. In dense graph all states are sources, so `visited == size` immediately and we skip BFS entirely. 

One more check on BFS correctness with mixed 0/1 sources: enqueued order is all dist-0 then all dist-1. Popping generates dist+2. Sequence in queue: 0...0, 1...1, 2...2, 3...3. Non-decreasing. Each state gets distance at first discovery = shortest. Correct.

Check sample 1 mentally: N=4, edges: 1→1 'a', 1→2 'b', 2→3 'b', 3→4 'a', 4→1 'c'. (1-indexed). A_{1,4}: sources include (1,1) d0, (1,2) d1, (2,3) d1, (3,4) d1, (4,1) d1. Expand (1,1): in-edges of 1: (1,a),(4,c). out of 1: a:[1], b:[2]. x=1,c=a → y∈{1}: (1,1) visited. x=4,c=c → out_1[c] empty. Expand (1,2) d1: in of 1: (1,a),(4,c); out of 2: b:[3]. x=1,a: out_2[a] empty. x=4,c: empty. Expand (2,3) d1: in of 2: (1,b); out of 3: a:[4]. x=1,c=b: y=4? out_3[b] empty. Hmm. Expand (3,4) d1: in of 3: (2,b); out of 4: c:[1]. no match. Expand (4,1) d1: in of 4: (3,a); out of 1: a:[1],b:[2]. x=3,c=a: y∈{1,2} → (3,1) d3, (3,2) d3. Then expand (3,1) d3: in of 3: (2,b); out of 1: a,b. x=2,c=b: y=2 → (2,2) visited d0... wait (2,2) is dist 0, yes. Also y∈ out_1[b] = [2]. So (2,2). Nothing new? Hmm, but expected A_{1,4}=4 via 1→1→2→3→4 "abba". Let's trace: state (1,4) should be reached. From (1,2) [palindrome "b" from 1 to 2], extend with a: in-edge x→1 labeled a: x=1; out-edge 2→y labeled a: none (2→3 is b). Hmm, that doesn't work. Other direction: palindrome "bb"? No.

Path 1→1 (a), 1→2 (b), 2→3 (b), 3→4 (a): string abba. Building from ends: start with middle "bb" from 1→2... wait middle two edges are 1→2 (b) and 2→3 (b): "bb" palindrome from 1 to 3. So state (1,3) dist 2: from source (2,2) dist 0, extend with b: in-edge of 2 labeled b: x=1; out-edge of 2 labeled b: y=3 → (1,3) dist 2. Yes! Expand (2,2): in_edges[2] = [(1,b)], out_by_letter[2][b] = [3] → (1,3) d2. Then expand (1,3) d2: in of 1 labeled a: x=1; out of 3 labeled a: y=4 → (1,4) d4. ✓. My earlier manual BFS just hadn't gotten there. Good.

Also A_{4,1} = 1 (edge c). ✓. A_{3,1} = 3: path 3→4→1? "ac"? not palindrome. Expected 3: 3→4 (a), 4→1 (c), 1→1 (a)? "aca" palindrome, length 3, from 3 to 1. ✓ matches (3,1) d3 found above.

Code looks right. Output formatting: rows joined by spaces, trailing newline fine.

Minor performance: inner loop `for x, c in in_edges[u]: for y in obv[c]:` — fine. Use local variables for dist, dq.append for speed. Also computing `visited` initial count: just compute during source marking.

Edge case N=1: grid single char. If '-': dist[(0,0)]=0, output "0". If letter: dist 0 anyway. Output 0. Correct (empty string palindrome).

I'll finalize the code.

## worker: Write the complete Python solution: parse input, b
- State = ordered pair (u, v) meaning "shortest palindrome-labeled walk from u to v found so far". Flattened to id u*N+v with a -1-initialized dist array.
- Sources: (i,i) at distance 0 (empty string is a palindrome) enqueued first, then (i,j) with an edge i→j at distance 1 (any single character is a palindrome).
- Transition: from (u,v), for every in-edge x→u labeled c and out-edge v→y labeled c, relax (x,y) with +2 (prepend/append the same character, preserving palindromicity). This exactly characterizes palindrome walks: any palindrome of length ≥2 has equal first/last edge labels, and its middle is a shorter palindrome walk.
- BFS validity: every transition costs exactly 2 and all 0-sources precede all 1-sources in the initial queue, so queue order is non-decreasing in distance; first discovery = shortest distance.
- Early exit when all N² states are visited handles dense graphs (where every state is already a distance-≤1 source) to avoid wasteful expansion.
- Complexity: O(N²) states; per-state work is Σ over in-edges (x,u,c) of |out_c(v)|, fine for N ≤ 100 in practice (standard editorial approach for this problem).
- Verified logic against Sample 1 by hand: (1,4) reached at distance 4 via (2,2)→(1,3)→(1,4) building "bb" then "abba"; (3,1)=3 via "aca"; diagonal entries are 0.
