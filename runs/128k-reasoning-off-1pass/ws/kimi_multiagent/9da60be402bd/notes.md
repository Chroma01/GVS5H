
## ideation
Core difficulty: We need shortest paths whose edge-label string is a palindrome, for all N² pairs. The key insight is to think of building the palindrome from both ends simultaneously: a palindrome of length L from i to j is either empty (i=j, length 0), a single edge (length 1), or formed by wrapping a shorter palindrome: edge a→u with label c, then a palindrome path u→v, then edge v→b with label c, giving length +2.

State space: dist[u][v] = shortest palindrome-length path from u to v. That's N² = 10⁴ states for N=100. Transitions from (u,v): for each character c, for each in-neighbor a of u via c, for each out-neighbor b of v via c: candidate dist[a][b] = dist[u][v] + 2.

Pitfalls:
- Naive transition scans all N² edge pairs per state → O(N⁴) = 10⁸ operations, borderline/too slow in Python. Must precompute in_edges[v][c] and out_edges[v][c] as lists to only iterate over actual edges.
- BFS correctness: initial states have distances 0 and 1 (mixed parity). Transitions add 2, so parity of distance is invariant per state. A plain queue BFS works if we seed all initial states (dist 0 and dist 1) into the queue upfront, since every relaxation is +2 — a state first reached at distance d can never later be improved (all edge weights positive and BFS processes in nondecreasing order... actually with 0/1 seeds and +2 steps, standard BFS from all seeds is fine because it's equivalent to Dijkstra with uniform weight 2 on a graph whose sources have initial potentials 0/1; a FIFO queue processes seeds first, then distance-2, etc. — order is nondecreasing). Safer alternative: Dijkstra, but BFS with all seeds enqueued initially is correct and faster.
- Answer for (i,i) is 0 (empty palindrome). Unreachable → -1.
- Self-loops: edge i→i gives dist[i][i] = 1 candidate but 0 is smaller; fine.
- Reading input: lines may have no spaces; strip newline.

Complexity: O(N² · Σ_c indeg·outdeg) worst case ~O(N⁴) but with adjacency lists the constant is tiny; well within limits for N=100.

## worker: Write the complete Python solution: parse input, b
- State `dist[u][v]` = shortest palindrome-length path from u to v; seeds are (i,i)=0 and edges=1.
- BFS with all seeds enqueued upfront is correct: all transitions add exactly 2, so states are dequeued in nondecreasing distance order (all 0/1 seeds precede any distance-2 state, etc.). First time a state is set is its minimum.
- Per-character in/out adjacency lists keep transitions proportional to actual edges, avoiding an O(N^4) full scan per state.
- Verified mentally on Sample 1: (1,4): seeds (1,1)=0; wrap with 1->1 'a' and 1->2 'b'? Actually path built: (1,1)=0 → wrap a: in-neighbors of 1 via 'a' = {1}, out-neighbors of 1 via 'a' = {1} → (1,1) stays; wrap 'b': in of 1 via b none... The chain (2,3)=1 via 'b', then wrap with 1->2 'a' and 3->4 'a' gives (1,4)=3? No: (2,3) dist 1, in-neighbors of 2 via 'a' = {1}, out-neighbors of 3 via 'a' = {4} → dist[1][4] = 3? But expected 4. Wait — the palindrome is "abba": outer chars 'a','a', inner "bb". Inner (2,3) via edge 'b' is length 1 = "b", not "bb". Correct chain: (1,2)=1 ("b"? edge 1->2 is 'b'), wrap with 1->1 'a' and 2->3 'b'? That gives "abb"? Let me redo: edges: 1->1 'a', 1->2 'b', 2->3 'b', 3->4 'a', 4->1 'c'. Path 1->1->2->3->4 = "abba". Build: center (2,2)=0, wrap 'b': in of 2 via b = {1}, out of 2 via b = {3} → (1,3)=2 ("bb"). Wrap 'a': in of 1 via a = {1}, out of 3 via a = {4} → (1,4)=4. ✓ Matches sample.
