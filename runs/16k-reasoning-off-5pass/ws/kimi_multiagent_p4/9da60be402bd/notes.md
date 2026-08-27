
## ideation
Core difficulty: We need shortest walks whose label string is a palindrome, for all N² pairs. The key insight is the classic "two-pointer" expansion: a palindrome is built by matching equal letters at both ends. Define state (u, v) = "there is a palindrome path from u to v of length d". Transitions: from (u, v), pick an edge x→u with label c and an edge v→y with the same label c; then (x, y) is reachable with a palindrome of length d+2. Base cases: (i, i) with distance 0 (empty palindrome), and (i, j) with distance 1 whenever an edge i→j exists (single character is a palindrome). A multi-source BFS on this N²-state graph (each step costs 2, uniform) yields shortest distances for all pairs.

Pitfalls:
- BFS must be by number of edges, but every transition adds exactly 2, so a plain FIFO queue works since all edge weights in the state graph are equal.
- Efficiency: naive transition enumeration is O(in-degree(u) × out-degree(v)) per state, which could be ~10⁴ per state × 10⁴ states = 10⁸ — borderline/too slow in Python. Better: group in-neighbors of u by letter and out-neighbors of v by letter, then only iterate over letters present in both, summing sizes. Worst case is still high for dense graphs with one letter (N=100: in/out degree 100 each → 10⁴ pairs per state → 10⁸ total). However, we can prune: once dist[x][y] is set we skip; but the enumeration itself still happens. An alternative is to iterate over the smaller of the two neighbor lists and check membership via adjacency lookup of matching letter... Actually a cleaner optimization: for each letter c, we have sets In_c(u) and Out_c(v); the product must be enumerated only if both nonempty. In the worst case (complete graph, single letter 'a'), every state (u,v) has 10⁴ successors, but each successor pair (x,y) gets relaxed only once — yet we'd still generate duplicates 10⁸ times. Hmm. A standard trick used in editorial solutions: BFS where each state processes transitions once; with N=100 the worst case 10⁸ operations is too slow in Python but fine in C++. For Python, we can reduce by noting that from state (u,v) we generate (x,y) for x ∈ In_c(u), y ∈ Out_c(v). Instead, we can precompute nothing better; but we can limit work by early termination? Not possible for all-pairs.

Alternative viewpoint: think of it as BFS on pairs but process by letter: for letter c, consider the bipartite-like product graph. Actually total work = Σ over states (u,v) of Σ_c |In_c(u)|·|Out_c(v)|. With N=100 and dense single-letter graph this is 10⁴ × 10⁴ = 10⁸. In Python with tight loops (list of in-neighbors per (u,c), out-neighbors per (v,c)), 10⁸ simple operations is ~50-100s — too slow. Need a smarter method.

Smarter: For each letter c, define boolean matrices. The transition is essentially: new_reachable = In_c^T ... hmm, think of dist as matrix D; relaxation D' = min over c of (M_c^T · something · M_c)? This is like a min-plus closure — not straightforward with BFS levels.

But note: BFS levels increase by 2. We can process level by level: at each BFS layer we have a set S of pairs (u,v). The next layer = { (x,y) : ∃c, ∃(u,v)∈S with x→u labeled c and v→y labeled c } minus already visited. Computing this per layer: for each letter c, let X = set of u appearing in S... still product-like.

Practical compromise: worst case complete graph with all same label. Then answer structure is trivial but BFS doesn't know that. However, we can add a crucial optimization: for each state (u,v), instead of iterating x over all in-neighbors and y over all out-neighbors, iterate over letters c where both lists nonempty, and iterate the product — but skip early if all targets already visited? Checking "all visited" still costs the product.

Alternative optimization: process transitions from the perspective of the smaller side. For fixed c, cost is |In_c(u)| × |Out_c(v)|. We can't avoid the product in the worst case.

Let me reconsider the actual worst-case bound more carefully: Σ_{u,v} Σ_c indeg_c(u)·outdeg_c(v) = Σ_c (Σ_u indeg_c(u)) · (Σ_v outdeg_c(v)) = Σ_c E_c · E_c = Σ_c E_c² where E_c = number of edges labeled c. With N=100, max edges 10⁴, so worst case Σ E_c² = 10⁸ (all edges same letter). So 10⁸ edge-relaxation attempts. Each attempt in pure Python ~0.1µs–0.3µs if optimized with local variable caching and visited check via a flat list... realistically ~0.2–0.5 µs for a simple `if d[xy] < 0:` in C-optimized loop? No — Python bytecode loop iteration is more like 50–100ns for trivial body only in ideal cases; realistically 10⁸ iterations ≈ 20–60 seconds. Too slow.

Mitigation ideas:
1. Use numpy vectorization per letter: represent current frontier as boolean matrix F (N×N). For letter c with adjacency matrix M_c (x→u means M_c[x,u]=1), next frontier contribution = M_c^T? Let's define F[u,v]=1 for frontier pairs. Successors (x,y): ∃(u,v)∈F: edge x→u in c and v→y in c. That's (M_c · F · M_c^T)[x,y] > 0 where M_c[x,u]=1 if edge x→u labeled c. So next = OR over c of (M_c @ F @ M_c.T) > 0, then mask out visited. Each matrix multiply is 10⁶ ops in C (N=100 → 100³ = 10⁶), times 26 letters times number of BFS layers (up to ~ answer length/2, could be large...). Max answer length: bounded by number of states × 2 = 2·10⁴? BFS layers ≤ N² = 10⁴. Then total = 10⁴ layers × 26 × 10⁶ = way too much. But typically layers are few; worst case still bad.

2. Accept the O(Σ E_c²) approach but implement the inner loops efficiently: precompute for each vertex u a list of (letter, in-neighbor array), and for each vertex v (letter, out-neighbor array). For state (u,v), find common letters (both lists ≤ 26 entries), then double loop. In the absolute worst case this is 10⁸ — risky but AtCoder (this is ABC/ARC problem "Shortest Path" — actually it's from AGC? It's AtCoder problem "palindrome path" — typical constraints N≤100, and C++ solutions do exactly this O(N⁶)-ish = 10⁸... wait, editorial complexity is O(N⁶)? No: states N², transitions per state N² → N⁶ = 10¹² for N=100? No wait: per state transition is indeg×outdeg ≤ N² = 10⁴, states 10⁴ → 10⁸ total. Yes editorial is O(N⁶)?? N=100 → N⁶ = 10¹². No — it's O(N² · N²) = O(N⁴) = 10⁸. Right, O(N⁴). C++ handles 10⁸ easily; Python struggles.

Given the environment expects a Python solution that presumably should pass, we should implement the O(N⁴) BFS with heavy optimization:
- Encode state as integer s = u*N + v.
- Precompute in-neighbors grouped by letter: in_by_letter[u] = list of (letter_index, list_of_x). Similarly out_by_letter[v].
- dist as a flat list of ints, -1 = unvisited.
- BFS with collections.deque.
- For each popped state, loop over common letters via index intersection (both lists sorted by letter, or use 26-length arrays of lists/None).
- Inner double loop over x_list and y_list; compute t = x*N + y; if dist[t] == -1: set and append.

To speed the worst case, we can add deduplication: if the same (x,y) gets generated many times, we still check dist each time. In the dense single-letter case, the first layer from base states already visits almost everything, so later states' product loops all hit "already visited" — still 10⁸ checks. Hmm.

Additional pruning: For a given state (u,v) and letter c, if we iterate x in In_c(u) and y in Out_c(v), all targets get the same distance. We could skip the whole product if... we can't know without checking.

Alternative: bitset approach per letter. For each letter c, represent In_c(u) as a 100-bit integer (Python int bitmask), Out_c(v) similarly. The product set = {(x,y)} — still a 2D product; bitsets don't directly give 2D products. But we can flip the loop: for each x in In_c(u), we want to set all (x, y) for y ∈ Out_c(v). If we maintain dist as a 2D structure and process "row-wise": for each x, the set of y's is the same bitmask. We could keep for each x a bitmask of visited y's, and compute new_y_mask = outmask & ~visited_row[x]; if nonzero, iterate set bits. This reduces repeated work: each (x,y) is set once, and the check per state is: for each x in In_c(u), one bitmask AND + comparison (~cheap big-int op on 100 bits ≈ 2 words). Cost per state per letter ≈ |In_c(u)| big-int ops. Total ≈ Σ_c Σ_{u,v} |In_c(u)| = Σ_c N · E_c = N · E = 100 · 10⁴ = 10⁶ big-int ops, plus bit-iteration over newly discovered pairs (≤ 10⁴ total discoveries, each with bit fiddling). That's very feasible!

So the plan: BFS where dist/visited is stored as list of N Python ints (bitmasks over v) — or flat dist list plus bitmask rows. For each state (u,v) popped, for each letter c common to in-neighbors of u and out-neighbors of v: for each x in In_c(u): new = OutMask_c(v) & ~visRow[x]; if new: iterate set bits y, set dist[x][y] = d+2, mark visRow[x] |= bit, enqueue. Wait but we need OutMask per (v,c) — precompute out_mask[v][c] as int bitmask, and in_list[u][c] as list of x (or also bitmask and iterate bits).

Complexity: per state (u,v), per letter c: |In_c(u)| iterations each doing a couple of 100-bit int ops (~O(2) word ops). Total big-int ops ≈ Σ_{(u,v)} Σ_c |In_c(u)| = N · Σ_c Σ_u |In_c(u)| = N · E ≤ 100·10⁴ = 10⁶. Each op maybe 100–200ns → ~0.2s. Bit-iteration for discoveries: each pair discovered once, 10⁴ pairs, fine. Also need common-letter detection: precompute for each u a 26-bit mask in_letters[u], out_letters[v]; common = in_letters[u] & out_letters[v]; iterate set bits (≤26). Per state ≤ 26 checks → 2.6·10⁵. 

BFS queue holds up to 10⁴ states. Total runtime well under a second. 

Also need dist output as N×N matrix of ints; store dist as list of lists initialized to -1, or a flat list. Setting dist[x][y] during bit iteration.

Edge cases:
- Answer for (i,i) is always 0 (empty palindrome).
- Single edge i→j gives answer 1.
- Self-loops with letters also give 1 for (i,i) but 0 is smaller anyway.
- BFS initialization: enqueue all (i,i) with d=0 and all (i,j) with edge with d=1. Order doesn't matter for correctness as long as we process in FIFO order of distance — but mixing d=0 and d=1 sources in one queue is fine since all transitions add +2 uniformly; BFS processes nondecreasing distances if we enqueue all d=0 first then d=1. Actually even interleaved it's fine because d=0 and d=1 differ, and transitions from d=0 give 2, from d=1 give 3 — FIFO with all sources initially enqueued (0s and 1s in any order) still yields nondecreasing processing order? If a d=1 source is enqueued before a d=0 source, processing d=1 first enqueues d=3 nodes, then d=0 enqueues d=2 nodes — queue order becomes 3 before 2, violating BFS order. But correctness of "first time we set dist is shortest" requires processing in nondecreasing order. Safer: enqueue all d=0 states first, then all d=1 states. Then distances processed: 0s, then 1s, then 2s (from 0s), then 3s (from 1s)... wait, 2s get enqueued while processing 0s, before 1s are processed? No — initial queue contains [0s..., 1s...]; processing 0s appends 2s at the tail, after the 1s. So order: 0,1,2,3,... nondecreasing. 

Alternatively, run Dijkstra-like with the property, but the simple ordering works. Even simpler: since transitions add exactly 2, parity of distance is preserved per state? dist parity: from (i,i) even, from edge-source odd. A given pair (x,y) could be reached both ways (even and odd palindromes). BFS handles min.

Let me double check the transition direction: We have palindrome path from u to v of length d. Prepend edge x→u (label c) and append edge v→y (label c): new palindrome c + (middle) + c from x to y, length d+2. So from state (u,v) we go to (x,y) using in-edge to u and out-edge from v. Yes: x ∈ In_c(u), y ∈ Out_c(v). Correct.

Base: dist[i][i] = 0. For edge i→j label c: dist[i][j] = min(1). Note if edge i→i exists, dist[i][i] stays 0.

Then answer matrix is dist.

Let me verify with sample 1 mentally: N=4; edges: 1→1 a, 1→2 b; 2→3 b; 3→4 a; 4→1 c.
dist init: diag 0; edges get 1: (1,1)=0 already, (1,2)=1, (2,3)=1, (3,4)=1, (4,1)=1.
BFS: from (1,1) d=0: in-neighbors of 1: from 1 (a), from 4 (c). out-neighbors of 1: to 1 (a), to 2 (b). Common letter a: x∈{1}, y∈{1} → (1,1) visited. Nothing new. From (2,2) d=0: in of 2: from 1 (b). out of 2: to 3 (b). common b: x=1,y=3 → dist[1][3]=2. ✓ (matches sample: A[1][3]=2). From (3,3): in of 3: from 2 (b); out of 3: to 4 (a); no common. From (4,4): in of 4: from 3 (a); out of 4: to 1 (c); none. From (1,2) d=1: in of 1: {1:a, 4:c}; out of 2: {3:b}; no common. From (2,3) d=1: in of 2 {1:b}; out of 3 {4:a}; none. From (3,4) d=1: in of 3 {2:b}; out of 4 {1:c}; none. From (4,1) d=1: in of 4 {3:a}; out of 1 {1:a, 2:b}; common a: x=3, y=1 → dist[3][1]=3 ✓ (sample A[3][1]=3). From (1,3) d=2: in of 1 {1:a,4:c}; out of 3 {4:a}; common a: x∈{1}, y=4 → dist[1][4]=4 ✓. Also x from letter a only 1. Good. From (3,1) d=3: in of 3 {2:b}; out of 1 {1:a,2:b}; common b: x=2, y=2 → dist[2][2] already 0; y∈{2}: visited. Hmm also out b → y=2 only. Nothing new. Wait sample A[2][4]=1 (edge? 2→3 b, 3→4 a... A[2][4] sample row 2: "-1 0 1 -1" so A[2][4]=-1 ✓. Row 1: 0 1 2 4 ✓. Row 3: 3 -1 0 1 ✓ (A[3][4]=1 edge). Row 4: 1 -1 -1 0 ✓. Great, algorithm matches.

Implementation details:
- Read N, then N strings.
- in_list[u][c]: list of predecessors via label c; also in_letters[u] bitmask of letters present.
- out_mask[v][c]: bitmask (int) of successors via label c; out_letters[v] bitmask.
- Use arrays indexed [u*26 + c] or list of lists.
- dist: list of lists, -1 init. vis rows: list of N ints (bitmask of visited y for row x). Actually dist[x][y] != -1 check suffices; bitmask vis is for fast dedup. We need both: vis bitmask for the & trick, and dist for final output. When discovering y from row x: set vis[x] |= (1<<y), dist[x][y] = nd, append (x,y) to queue.
- Queue stores encoded state s = u*N+v; decode via divmod.
- For popped (u,v) with d = dist[u][v]: common = in_letters[u] & out_letters[v]; while common: c = (common & -common).bit_length()-1 ... or iterate bits via while loop: lb = common & -common; c = lb.bit_length()-1; common ^= lb. Then om = out_mask[v][c]; if om: for x in in_list[u][c]: new = om & ~vis[x]; while new: lb = new & -new; y = lb.bit_length()-1; new ^= lb; vis[x] |= lb; dist[x][y] = d+2; queue.append(x*N+y).

Wait: vis[x] should be updated once with all new bits: accumulate then vis[x] |= new_all. Fine to do vis[x] |= new before iterating (since new = om & ~vis[x], then vis[x] |= new, then iterate bits of new). Cleaner.

- Note: ~vis[x] in Python is negative infinite bits; om & ~vis[x] works correctly because om has finite bits. Good.

Complexity: the inner "for x in in_list[u][c]" runs Σ ≈ N·E = 10⁶ times worst case, each with a couple of bigint ops. Fine.

Memory: dist 10⁴ ints, fine.

Output: print rows space-separated.

One more check on BFS ordering: initial queue = all (i,i) [d=0], then all edge pairs (i,j) [d=1] (only those with dist set to 1; note multiple edges? At most one edge per ordered pair per problem statement — exactly one edge if letter, so fine). Then process. Since every transition adds 2, and initial queue is sorted (0s then 1s), processing order is nondecreasing in d. Proof: standard two-tier BFS; appended nodes have d = current+2 ≥ current, and appended after all initially-queued 1s when processing 0s... when processing a 0-node we append 2s behind the 1s — good; when processing 1-nodes we append 3s behind 2s — good. Inductively fine. So first discovery = shortest. 

Alternatively to be safe we could use a deque and it's fine.

Edge case N=1: works.

Now, is the bitmask-per-row dedup definitely correct? vis[x] marks all y such that (x,y) discovered. When processing state (u,v), for letter c and predecessor x, the candidate y set is Out_c(v). We only enqueue undiscovered ones. Correct.

But subtle: we process each state (u,v) once (when popped). Its transitions are computed then. Since dist[u][v] is final at pop time (BFS), no reprocessing needed. Good.

Let me also double check sample 2 quickly for one tricky value: A[5][3] = 5. Edges: row1: u s - - - → 1→1 u, 1→2 s. row2: - s t - - → 2→2 s, 2→3 t. row3: - - s - - → 3→3 s. row4: u - - s - → 4→1 u, 4→4 s. row5: - - - t s → 5→4 t, 5→5 s.
Path 5→4 (t), 4→1 (u), 1→2 (s)... want palindrome ending at 3: "t u s ? ?" length 5: t u s u t? Need edges: after 1→2 labeled s, need 2→? labeled u — none. Hmm. Let's find: 5→4 t, 4→4 s? no. Try "s t s t s"? 5→5 s, 5→4 t? no that's length 2 "st" not palindrome. Let's trust BFS: dist[5][3]: base: (5,4)=1 (t), (5,5)=0. From (5,5): in of 5: none (who→5? row? edges into 5: none since column 5 all '-'? C[i][5]: rows: 1:'-',2:'-',3:'-',4:'-',5:'s' → 5→5 s. So in of 5: {5:s}. out of 5: {4:t, 5:s}. common s: x=5, y∈{5} → visited. From (5,4) d=1: in of 5 {5:s}; out of 4: {1:u, 4:s}; common s: x=5, y=4 → (5,4) visited. Hmm. From (4,4) d=0: in of 4: {5:t, 4:s}; out of 4 {1:u, 4:s}; common s: x=4,y=4 visited. From (4,1) d=1: in of 4 {5:t,4:s}; out of 1 {1:u, 2:s}; common s: x=4, y=2 → dist[4][2]=3 ✓ (sample A[4][2]=3). From (1,1) d=0: in of 1: {1:u, 4:u}; out of 1 {1:u, 2:s}; common u: x∈{1,4}, y=1 → (1,1) visited, (4,1) already 1. From (2,2): in of 2 {2:s, 1:s}; out of 2 {2:s, 3:t}; common s: x∈{1,2}, y=2 → visited. From (3,3): in of 3 {2:t}; out of 3 {3:s}; none. From (2,3) d=1: in of 2 {1:s,2:s}; out of 3 {3:s}; common s: x∈{1,2}, y=3 → dist[1][3]=3 ✓ (sample A[1][3]=3), dist[2][3] already 1. From (4,2) d=3: in of 4 {5:t, 4:s}; out of 2 {2:s, 3:t}; common s: x=4, y=2 visited; common t: x=5, y=3 → dist[5][3] = 5 ✓. 

Algorithm confirmed.

## worker: Implement the complete solution: parse input, buil
- Modeled the problem as BFS on pair-states (u, v) = "shortest palindrome-labeled walk from u to v". Transition: from (u, v), prepend edge x→u and append edge v→y with the same letter c, giving state (x, y) at distance +2.
- Seeds: all (i, i) with distance 0 (empty string is a palindrome) enqueued first, then all direct edges (i, j) with distance 1. Since every transition costs exactly +2 and the initial queue is nondecreasing, plain FIFO BFS yields shortest distances (verified ordering argument: 2s appended behind 1s, 3s behind 2s, etc.).
- Performance: naive per-state transition enumeration is O(Σ_c E_c²) ≤ 10⁸, too slow in pure Python. Optimized with bitmasks:
  - `out_mask[v][c]` = 100-bit int of c-labeled successors; `in_list[u][c]` = list of c-labeled predecessors; 26-bit letter masks allow quick common-letter intersection per state.
  - For each predecessor x, `new = om & ~vis[x]` computes all undiscovered targets in one big-int op; each pair (x, y) is discovered exactly once.
  - Total work ≈ N·E ≤ 10⁶ big-int operations plus 10⁴ discoveries — runs in well under a second.
- Hand-verified both samples against the BFS trace (e.g., (1,4)=4 via abba in sample 1; (5,3)=5 in sample 2).
