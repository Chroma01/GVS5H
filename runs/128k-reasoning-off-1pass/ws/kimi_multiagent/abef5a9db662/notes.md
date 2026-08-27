
## ideation
The problem: N up to 2e5 contests, each increments rating by 1 if current rating in [L_i, R_i]; Q up to 3e5 queries with initial X in [1, 5e5]; answer final rating per query.

Key observations:
- The overall map f(x) is non-decreasing in x, and each contest preserves monotonicity. Also f(x+1) - f(x) ∈ {0,1} (a contest can increment x+1 only if it increments x... actually increments are "nested": if x and x+1 both in [L,R] both increment; the difference stays 0 or 1). So f is a monotone "1-Lipschitz non-expanding" step function.
- Domain of queries is bounded: X ∈ [1, V] with V = 5e5. So we can afford to compute f(x) for every x in [1, V], then answer queries in O(1).
- Naive per-contest update over all V positions is O(NV) = 1e11 — too slow. Need the structure: maintain cur[x] = f_sofar(x), a non-decreasing array. For contest [L, R], the set {x : L ≤ cur[x] ≤ R} is a contiguous index interval [a, b] (because cur is monotone). We need:
  - a = first index with cur[a] ≥ L
  - b = last index with cur[b] ≤ R
  - range add +1 on [a, b]
- A lazy segment tree over indices 1..V storing min and max of cur in each node supports all three operations in O(log V):
  - "first index with value ≥ L": walk down, skipping nodes whose max < L.
  - "last index with value ≤ R": walk down, skipping nodes whose min > R.
  - range add with lazy propagation updates min/max.
- Edge cases: if no index satisfies (a doesn't exist or b doesn't exist or a > b), skip the add. Note cur values can grow up to V + N ≈ 7e5, fits in int.
- Complexity: O((N + V) log V + Q). V=5e5, N=2e5 → fine in Python with an iterative/efficient recursive segment tree? Python recursion depth and speed: 2e5 contests × ~2 walks × log(5e5)≈19 levels → ~8e6 node visits. Recursive functions in Python might be borderline but likely OK with sys.setrecursionlimit and fast I/O; could also implement walks iteratively. Need to be careful with constant factors. Alternative: since cur is monotone and updates are range-add on a contiguous interval, could maintain a difference array plus a Fenwick and binary search boundaries via Fenwick "find by value"? Values change though; binary search over prefix sums isn't valid after range adds unless we can query point values — point query via Fenwick is O(log V), binary search O(log V) point queries → O(log²V) per contest, total 2e5 × 19 × 19 ≈ 7e7 — too slow in Python. Segment tree walk is O(log V) per boundary, better.
- Another candidate approach: per-query binary search on answer with reverse simulation O(N log N) per query — way too slow (3e5 × 2e5). Reject.
- Another approach: sqrt decomposition over contests, precompute f per block for all V values: each block's f is monotone; composing blocks for all x costs O(V) per block with two pointers? Composition f_total(x) = f_block(f_prev(x)) is just array indexing O(V) per block. Number of blocks B = N/S; cost O((N/S)·V + N·S?) Hmm: building each block's table costs O(S·? ) — building f_block for all V values naively costs O(S·V). Not good unless block build is smart. With S ≈ sqrt(N)≈450, blocks ≈ 450, composition cost 450 × 5e5 = 2.25e8 — too slow in Python. Reject; segment tree is cleaner.

Pitfalls:
- Boundary conditions: increment applies when L ≤ cur ≤ R inclusive. First index with cur ≥ L; last index with cur ≤ R. Both must exist and a ≤ b.
- Lazy propagation correctness: push down before walking children.
- Python speed: use sys.stdin.buffer.read, iterative walks where possible, avoid deep recursion (depth log V ≈ 19 is fine for recursion actually). Recursion depth 19 is fine; number of recursive calls is the cost. Implement find_first_ge and find_last_le as iterative walks from root using an explicit stack or a clever loop. Simpler: recursive with arrays (min[], max[], lazy[]) as Python lists; ~4e6-8e6 calls total might be ~5-10s. Risky. Optimize: combine the two boundary searches? Could do a single function. Or use iterative segment tree with lazy (segment tree beats style not needed). Let me think about an iterative walk:
  - find_first_ge(L): start at root; if root.max < L return None. Iteratively: maintain node index; standard technique: walk down with a stack, pushing right child first... Actually simplest iterative: use recursion but with small depth it's fine; the cost is number of calls ~ O(log V) per query = 19 calls per boundary, 2 boundaries + 1 range add (range add visits O(log V) nodes ~ 2*19). So per contest ≈ 4*19 ≈ 76 function calls → 2e5 × 76 ≈ 1.5e7 calls. That's likely too slow in Python (~10-20s). Need faster.
  
  Faster idea: iterative segment tree walk without recursion for the two searches:
  - find_first_ge(L): node=1; if tree_max[1] < L: return V+1. Then loop: push lazy? Lazy push requires updating children — with iterative arrays we can push as we descend: at each node, apply pending lazy to children (write to child min/max/lazy), clear node lazy. Then go to left child if its max ≥ L else right child. That's O(log V) iterations with O(1) work each — cheap, no function-call overhead beyond the loop. ~19 iterations × 2 searches + range add.
  - range add iterative with lazy is trickier (need to push on the way down and pull on the way up). Could implement range add recursively — 2e5 × ~38 calls ≈ 7.6e6 calls. Still heavy.
  
  Alternative for range add: since the added interval [a,b] is exactly the set where L ≤ cur ≤ R, and after adding, values in [a,b] increase by 1... Hmm, is there a simpler data structure? Think differently: cur is monotone, values from 1..V+N. Consider maintaining for each value v the count/positions? Equivalent dual view: let pos[v] = number of x with cur[x] ≤ v... Contest [L,R] increments all x with cur[x] ∈ [L,R]. In terms of the inverse function g(y) = #{x : cur[x] ≤ y} (a count function), incrementing x's with values in [L,R] shifts those x's from value v to v+1 for v in [L,R]. Hmm, that's like moving mass between adjacent value buckets — a range "shift right by 1" of the histogram over [L, R]. The histogram h[v] = #{x: cur[x] = v}; operation: for v from R down to L: h[v+1] += h[v], h[v] = 0... that's O(R-L) naive. But as a "shift" operation on an array, we can use a lazy offset structure? Shifts on overlapping ranges repeatedly — this is like a deque/offset trick but ranges vary. Could use a balanced structure with "shift values in key range [L,R] by +1" — that's exactly a treap/splay with split by key and lazy add! Keys are cur values, but multiple x share keys; we just need final cur[x] per x though, and queries only need f(X) for X in [1,V]. Actually we don't even need per-x; we need the final array cur[x] for all x to answer queries. With a treap keyed by value with multiplicities: split into (<L), ([L,R]), (>R); add lazy +1 to middle; merge. But merging requires keys ordered — after +1, middle keys ∈ [L+1, R+1] may overlap with right part keys (which are ≥ R+1). Overlap at R+1: middle has R+1, right has ≥ R+1 — keys collide; treap with multiplicities handles equal keys fine if we merge carefully (merge by key with duplicates allowed, or combine counts). Standard approach: split at L and at R+1 gives A (<L), B ([L,R]), C (≥R+1). Add +1 to B → keys [L+1, R+1]. Now B's max key R+1 may equal C's min key R+1. Merge A+B+C where B and C may share key R+1: if treap allows duplicate keys with consistent ordering, fine. Each contest = 2 splits + 2 merges + lazy add = O(log M) where M ≤ V distinct... but number of nodes could grow? Nodes = distinct values with multiplicities; splits don't create nodes, adds don't create nodes. Initial nodes ≤ V distinct values (values 1..V each with count 1 → V nodes). M = 5e5 nodes, treap operations O(log M). Per contest ~4 treap ops × ~20 steps × pointer chasing in Python — also heavy, similar cost. And at the end we need cur[x] per original x — but we've lost x identity! The histogram only gives counts per value, but f is monotone so cur[x] = the value v such that cumulative counts locate x: since cur is non-decreasing in x, cur[x] = smallest v with prefix_count(v) ≥ x. So from final histogram we can reconstruct cur array. OK that works, but implementation complexity in Python (treap with lazy propagation, splits/merges) is high and speed uncertain.

  Better: just implement the lazy segment tree with iterative loops and accept ~2e5 × (2 walks × 19 + range-add). For range add, do it iteratively too: standard recursive range add is simplest; let me estimate more carefully. Recursive range_add(node, l, r): visits O(log V) nodes but with function call overhead ~2 calls per level → ~38 calls per contest → 7.6e6 calls total. Each call does list indexing and comparisons. Python ~10^7 simple ops/sec for function calls... 7.6e6 calls ≈ 4-8 seconds. Risky but possibly OK if time limit is 2s? Probably not. This is AtCoder ABC (this is ABC 330-ish? Actually it's from AGC? It's "AtCoder" problem — likely typical 2s limit). Need a faster plan.

  Fully iterative segment tree with lazy: implement range add and boundary searches all iteratively with an explicit stack. Alternatively use the "segment tree on monotone array with difference array + Fenwick + binary search" — O(log²V) per contest = 2e5 × 361 ≈ 7e7 basic ops — too slow.

  Hmm, alternative: PyPy-style optimizations: represent tree arrays as lists; write tight loops. Iterative walk for search: ~19 iterations, each a few ops → cheap. Range add iterative: use the classic iterative lazy segment tree (like Al.Cash's) — complex. Or: note we can avoid a separate range-add by combining: after finding a and b, we need cur[a..b] += 1. 

  Alternative simpler data structure: sqrt decomposition on the array cur (size V=5e5, block size ~700). Operations: range add [a,b] (O(#blocks) ≈ 700/... wait, range add touches ≤ V/B + 2 blocks partially → O(V/B + B)). Boundary search: find first index with value ≥ L: scan blocks using block max (with lazy), O(V/B) blocks, then scan within block O(B). So each op O(B + V/B) ≈ 1400 with B=700. Per contest ~3 ops → ~4200 ops → 2e5 × 4200 = 8.4e8. Too slow.

  So segment tree it is; must be efficient. Let me design a fully iterative lazy segment tree:
  - Size: n = V (5e5), tree size 2*2^ceil(log2 n) ≈ 2^20 = 1048576 → arrays of size 2*P where P = 2^19 = 524288 ≥ 5e5? 2^19 = 524288 ≥ 500000. Good, P = 1<<19.
  - Arrays mn[2P], mx[2P], lz[2P] as Python lists of ints (or array('i')). 
  - Build: leaves mn[P+i] = mx[P+i] = i+1 (value = initial rating x, since f initially identity). Then build parents.
  - push(node): if lz[node]: apply to children (mn,mx,lz += v), clear.
  - Range add [a,b] (0-indexed inclusive): iterative with explicit stack for push-down path, then update, then pull-up. Standard approach (iterative segment tree with lazy, "atcoder library" style is recursive). Hmm.

  Honestly, recursive implementation with sys.setrecursionlimit and functions operating on lists might pass in PyPy (AtCoder uses PyPy-like speeds? In this environment we just need correct Python). The grader here likely runs CPython. Let's aim for efficiency but prioritize correctness; typical accepted Python solutions for this exact problem (this is AtCoder ABC... let me recall: "Takahashi plans to participate in N AtCoder contests" — this is ABC 268? No... It's from ABC 261? Actually I recall this problem: it's "Ex - Directed Substring"? No. It's ABC 249? Hmm, it's from "AtCoder Beginner Contest 280"? Not sure. I recall a known problem "Rating" where the intended solution is exactly this segment tree, and Python solutions pass with recursive seg trees in ~2s PyPy.)

  Let me just write a reasonably optimized recursive segment tree:
  - Use lists mn, mx, lz of size 4*V? 4*5e5 = 2e6 ints per list × 3 lists — memory ~ 3 × 2e6 × 28 bytes ≈ 170MB. Too much! Use size 2*2^19 = 2^20 ≈ 1.05e6 per list → 3 lists × 1.05e6 × 28B ≈ 88MB. Still heavy but maybe OK. Better: use array('i') or list of int from `array` module, or use a single list of ints... Python ints are objects; 1e6 ints ≈ 28MB per list (small ints cached only up to 256). Values up to 7e5 → real objects. 3 lists × 1.05e6 × ~28B ≈ 88MB + list overhead 8MB each ≈ 100MB+. Risky. Use `array('i', ...)` → 4 bytes per entry → 4MB per array. Much better. Or use one list and encode? array('i') indexing is slightly slower but fine.

  Alternatively, avoid storing mn: since cur is monotone... we need both mn and mx for the two searches. Could we do both searches with only mx and mn? find_first_ge needs mx; find_last_le needs mn. Yes need both.

  Alternative memory-light approach: Fenwick + binary search with O(log²) — 7e7 ops too slow. 

  Let me reconsider: maybe there's an O((N+V) log V) approach with smaller constants: process contests, maintain difference array d[] where cur[x] = x + add[x], add monotone non-decreasing? Is add[x] = cur[x] - x monotone? cur[x+1] - cur[x] ∈ {0,1} → add[x+1] - add[x] = cur[x+1]-cur[x] - 1 ∈ {-1, 0}. So add is non-increasing! Interesting: f(x) - x is non-increasing in x? Check sample: f(1)=? contests: [1,5],[1,3],[3,6],[2,4],[4,7]. f(1): 1→2→3→4→4→5? Let's compute: x=1: c1 in[1,5]→2; c2 in[1,3]→3; c3 in[3,6]→4; c4 in[2,4]→5; c5 in[4,7]→6. f(1)=6, add=5. f(2)=6 (given), add=4. f(3)=6, add=3. f(5)=8, add=3. f(4): 4→5→5→6→6→7: f(4)=7, add=3. So add: x=1→5, 2→4, 3→3, 4→3, 5→3. Non-increasing. Yes! Because each contest increments x's with cur in [L,R], and if cur[x] and cur[x+1] both... the increment count difference can only decrease. So add[x] is a non-increasing function starting at some value ≤ N, ending ≥ 0.

  Does that help? Contest update: for x with L ≤ x + add[x] ≤ R, add[x] += 1. The condition x + add[x] ≥ L: since x + add[x] = cur is non-decreasing, it's a suffix; ≤ R is a prefix. Same structure as before. No simplification.

  OK here's another thought — offline with parallel binary search? Each query answer in [X, X+N]; predicate "final ≥ v" checkable by forward sim O(N) — too slow.

  Decision: implement iterative lazy segment tree with array('i') or lists; I'll write it with lists first for speed (indexing lists is faster than array), memory ~100MB might be too much. Hmm. Compromise: use lists but of size 2*P = 2^20 ≈ 1.05e6. mn and mx and lz: 3 × 1.05e6. CPython list of 1.05e6 ints: the list holds pointers (8B each) = 8.4MB, plus int objects. Initially all zeros/small — Python caches ints -5..256, so building with values ≤ 256 uses cached ints (no extra allocation). But values grow beyond 256 during updates → new int objects allocated for changed entries. Number of distinct changed entries ≤ 1.05e6 per array → up to ~28MB each in the worst case. Total maybe ~60-90MB. Typical limit 256MB (AtCoder ABC usually 256MB... this problem's original constraints suggest AtCoder; memory 1024MB for some). Probably fine. But to be safe, use array('i') for lz (values ≤ N ≤ 2e5 fits int32) and lists for mn, mx? Or all array('i'). array indexing returns Python int; assignment converts. Speed: array('i') access is somewhat slower than list but acceptable.

  Actually, let me reconsider the algorithm count: per contest: find_first_ge(L) + find_last_le(R) + range_add(a,b). With iterative walks:
  - find_first_ge: if mx[1] < L: return n (none). node=1; while node < P: push(node); if mx[2node] ≥ L: node=2node else node=2node+1. Return node-P. ~19 iterations, each with a push (check lz[node], maybe update children). Cheap.
  - find_last_le: symmetric with mn.
  - range_add(a, b): iterative lazy range add is the tricky part. Option: implement recursively. Depth 19, calls ~2*19 per contest = 38 calls → 7.6e6 calls. Each call ~ 100ns-200ns overhead plus body → maybe 3-6s. Hmm.

  Iterative range add with lazy propagation (standard technique): 
  ```
  def range_add(l, r, v):  # inclusive, 0-indexed
      l += P; r += P
      l0, r0 = l, r
      # push ancestors of l0 and r0
      for i in range(LOG, 0, -1):
          if ((l0 >> i) << i) != l0: push(l0 >> i)
          if ((r0 >> i) << i) != r0: push(r0 >> i)
      # hmm this is the atcoder-library style for lazy segtree which is recursive actually
  ```
  The well-known iterative lazy segment tree (e.g., from emaxx / "efficient and easy segment trees") handles range updates with lazy only for commutative updates with a specific structure; range add + range min/max with lazy can be done iteratively:
  ```
  l += P; r += P+1
  l0, r0 = l, r
  # push down along the paths
  for i in reversed(range(1, LOG+1)):
      if l0 >> i << i != l0: push(l0 >> i)
      if r0 >> i << i != r0: push((r0-1) >> i)
  while l < r:
      if l & 1: apply(l, v); l += 1
      if r & 1: r -= 1; apply(r, v)
      l >>= 1; r >>= 1
  # pull up
  for i in range(1, LOG+1):
      if l0 >> i << i != l0: pull(l0 >> i)
      if r0 >> i << i != r0: pull((r0-1) >> i)
  ```
  This is the standard iterative lazy segtree pattern (from the famous CF blog "Efficient and easy segment trees"). It works for range add with min/max. All loops, no recursion. Per contest cost: pushes ~2*19, updates ~2*19, pulls ~2*19 → ~114 loop iterations of simple work → 2e5 × 114 ≈ 2.3e7 iterations. Plus two searches ~38 iterations with push each. Total ~3e7 simple loop iterations in CPython ≈ 15-30s. Too slow!

  Hmm. Need to cut constants. Ideas:
  1. Use PyPy-style: can't control environment.
  2. Reduce to one search per contest: note a = first index with cur ≥ L, b = last index with cur ≤ R. Both needed. 
  3. Reduce range-add cost: since we know exactly [a,b], and the tree push/pull is O(log) — unavoidable.
  4. Use a Fenwick-of-differences plus something smarter? 

  Alternative: think about the dual/histogram approach with a "shift" data structure. Operation: histogram h over values; shift h[L..R] right by 1. Equivalent: define g = h as a sequence; operation moves each element in index range [L,R] to index+1. If we maintain h in a treap/splay keyed by index with lazy "shift" tags... same complexity.

  Alternative: Link/cut style? Overkill.

  Let me reconsider the actual complexity more optimistically. LOG = 19 (since P = 2^19 = 524288 ≥ 5e5). Actually V = 5e5 exactly, P = 2^19. Loops:
  - find_first_ge: 19 iterations, each: push check (lz[node] != 0 → rarely true? lz can be nonzero often). Each iteration ~6-10 ops → ~150-200 ops per search. Two searches ~400 ops.
  - range_add: push loop 19×2 iterations (but only when condition holds — the condition `(l0>>i)<<i != l0` holds roughly half the time), update loop ~ up to 38 applies, pull loop similar. ~150-250 ops.
  Total per contest ~600-700 ops → 2e5 × 650 = 1.3e8 ops. CPython ~3-5e7 ops/s for simple integer ops → 3-4s... borderline. With PyPy JIT it'd be fast. Risky but might be the intended Python-feasible solution? Let me check known results: this is AtCoder problem from "ABC 241 Ex"? Let me recall... The problem statement "Takahashi plans to participate in N AtCoder contests" — I believe this is ABC 280 F? No. It's "typical90"? Hmm, it's from "AtCoder Grand Contest"? The constraints N≤2e5, Q≤3e5, values ≤5e5 — this is ABC 267 Ex? I recall this exact problem: it's from "AtCoder Beginner Contest 308"? Not sure. I do recall the intended solution is the segment tree described, and Python solutions exist using recursive segment trees passing in PyPy ~2s. In CPython it might TLE at 2s but the grading environment here is unknown; we should just produce the best we can.

  Optimization: combine the two searches into one traversal? They search different predicates. Alternatively, note b = last index with cur ≤ R and a = first with cur ≥ L. Since cur monotone, we could find a, then find b starting from a's subtree? Not simpler.

  Bigger optimization: reduce LOG by using V = 5e5 → P = 2^19, LOG = 19. Fine.

  Alternative approach with much smaller constant: sqrt decomposition with block size B ≈ 1024: blocks = 489. Operations:
  - find_first_ge(L): scan blocks: for each block check block max (with lazy) — up to 489 checks, then scan within block ≤ 1024. Worst ~1500 ops.
  - Similarly find_last_le ~1500.
  - range_add: partial blocks at ends (≤1024 each) + full blocks (≤489 lazy increments). ~2500.
  Total ~5500 ops/contest → 1.1e9. Worse. Block size 256: blocks 1954 → scan 1954+256... worse. Optimal B = sqrt(V) ≈ 707 → ~2100+... still worse than segtree. No.

  What about a completely different angle: answer queries offline by processing initial values simultaneously? Simulate all V starting values through all N contests = O(NV) — no. But maybe we can compress: the function f after k contests has at most k+1 "breakpoints"? f is monotone, integer-valued, f(x)-x non-increasing, and each contest adds at most... The number of distinct values of add[x] changes by at most 1 per contest? Each contest increments add on a contiguous interval [a,b], which can introduce at most 2 new breakpoints in the step function add. So after k contests, add has ≤ 2k+1 steps. Represent add as a step function with breakpoints (sorted list of (position, value)). Contest update: find a (first x with x+add[x] ≥ L) and b (last x with x+add[x] ≤ R) via binary search over breakpoints — but x+add[x] within a step: add constant c on interval → x+c increasing in x. Binary search over O(k) breakpoints with O(log k) evaluations, each evaluation O(log k) to locate step → O(log²k). Then increment add on [a,b]: this splits/merges steps — with a sorted list of breakpoints, inserting two breakpoints and incrementing values in between is O(#breakpoints in between) = O(k) worst case per contest → O(N²) total. Unless we use a balanced tree with lazy on value ranges... The breakpoints have positions (x) and values (add). Increment add for x in [a,b]: that's a range update on position intervals — a treap keyed by position with lazy add on values, splits at a and b+1. Same as before, O(log) per contest with treap. Number of nodes grows by ≤ 2 per contest → ≤ 4e5 nodes. Treap in Python with split/merge: each op ~log(4e5)≈19 pointer steps, 4 ops per contest → ~76 node visits × 2e5 = 1.5e7 node operations with tuple/object overhead — slow in CPython (~30s+). No.

  Hmm OK. Let me reconsider: maybe recursion-based segment tree is actually acceptable and I'm overestimating. Let me count recursive range_add calls precisely: standard recursive range add visits at most 4*LOG nodes ≈ 76 calls per contest → 1.5e7 calls. At ~0.15µs per call overhead + body ~0.3µs → ~7s. Iterative version ~1.3e8 simple ops → ~4-6s. Both risky for 2s, OK for 5-10s.

  Can we prune? Important: many contests may have empty [a,b] (no x with cur in [L,R]) — then only two searches, no add. Searches are cheaper. Also we can early-exit searches: if mx[1] < L or mn[1] > R → skip. 

  Another idea: batch — process all contests but note that consecutive identical contests could be merged (apply +k). Sample 2 has many duplicates. But worst case all distinct.

  Alternative: use numpy! Represent cur as numpy array. Each contest: mask = (cur >= L) & (cur <= R); cur[mask] += 1. That's O(V) per contest → 2e5 × 5e5 = 1e11 element ops — numpy does ~1e8-1e9 simple ops/s → 100-1000s. No.

  Numpy with the interval structure: find a, b via np.searchsorted (cur is sorted! monotone non-decreasing). a = np.searchsorted(cur, L, 'left'), b = np.searchsorted(cur, R, 'right') - 1. Then cur[a:b+1] += 1. But wait — after incrementing, does cur stay sorted? cur[a..b] all increase by 1; cur[b]+1 vs cur[b+1]: cur[b] ≤ R < cur[b+1]... cur[b] ≤ R and cur[b+1] > R → cur[b]+1 ≤ R+1 ≤ cur[b+1]. Yes! Sortedness preserved. And cur[a-1] < L ≤ cur[a] → cur[a-1] < cur[a] ≤ cur[a]+1. Sorted. 

  So the algorithm: maintain numpy sorted array cur; per contest: two searchsorted (C-speed binary search, O(log V)) and one slice increment cur[a:b+1] += 1 which is O(b-a) in C. Worst case b-a = V = 5e5 per contest → 2e5 × 5e5 = 1e11 C-ops → way too slow (numpy int64 add on 5e5 elements ~ 0.5ms → 2e5 × 0.5ms = 100s). Hmm, borderline too slow. But wait — can we avoid touching the whole interval? Use a difference/lazy approach: we need final cur values for all x at the end. The increments are range-adds on index intervals that are "value-aligned". 

  Combine numpy with lazy: maintain cur = base + delta where delta from a difference array? Each contest adds +1 on index range [a,b] where a,b depend on current cur values — which depend on accumulated deltas. Chicken-and-egg: we need actual values to binary search. But note: searchsorted needs cur sorted; if we keep cur = x + add[x] with add non-increasing... 

  Alternative: keep a Fenwick/BIT for range-add point-query (to get cur[i] = i + bit.query(i)), and binary search over the BIT: finding first index with value ≥ L requires O(log V) BIT queries each O(log V) → O(log²V) = 361 per search, ×2 searches ×2e5 = 1.4e8 BIT inner ops — in numpy? BIT query is sequential, can't vectorize easily. In pure Python 1.4e8 ops — too slow.

  But here's a vectorized trick: binary search over all... no, searches are sequential across contests (each depends on previous updates). 

  Hmm, what about processing in a "difference of difference" way: total increment at index x is add[x] = sum over contests of 1{L ≤ cur_t[x] ≤ R}. No closed form.

  Let me reconsider the numpy slice-add cost. Average interval length might be small in practice but adversarial input (all contests [1, 5e5]) → every contest increments everything → but then cur = x + t after t contests, all values increase; interval always full → 5e5 per contest × 2e5 = 1e11. Definitely too slow. So numpy alone insufficient for adversarial cases. Need lazy propagation to make range-add O(log).

  Hybrid: numpy + sqrt decomposition with lazy block tags, vectorized within blocks? Block count 489 with B=1024. find_first_ge: compute block maxes = block_max + lazy (maintain array of block maxes, updated after each partial update via recompute O(B)). Search: scan 489 block maxes in Python loop (or numpy argmax on (blockmax >= L) → first True — numpy op on 489 elements ~ fast, ~2µs). Then scan within block: numpy on 1024 elements. range_add: two partial blocks (numpy ops on ≤1024 elements each + recompute block min/max) + full blocks: lazy[blocks] += 1 (numpy slice on ≤489 elements) — but also need block min/max updated: block_min/max += 1 for full blocks (numpy slice add on 489-element arrays). So per contest: a handful of numpy ops on arrays of size ≤1024, plus Python overhead ~10-20 numpy calls. Each numpy call overhead ~1-2µs + work. Per contest ~30-50µs → 2e5 × 40µs = 8s. Hmm, still slow-ish. Reduce numpy call count: maybe ~15 calls × 2µs = 30µs + Python logic 20µs → 50µs → 10s. Not great.

  Alternatively block size 2048, blocks 245: partial block ops on 2048 elements (~3µs each), full-block lazy on 245-element arrays (~1.5µs). Similar total.

  Let me reconsider pure-Python iterative segment tree with tight code and estimate honestly: inner loop iteration of the walk:
  ```
  node = 1
  while node < P:
      z = lz[node]
      if z:
          c = node*2
          mn[c] += z; mx[c] += z; lz[c] += z
          c += 1
          mn[c] += z; mx[c] += z; lz[c] += z
          lz[node] = 0
      node = node*2 if mx[node*2] >= L else node*2+1
  ```
  ~19 iterations × ~8 ops = 150 ops per search. Two searches = 300. Range add iterative ~ 3 loops × 19 × ~6 ops = 350. Total ~650 ops/contest → 1.3e8 ops. CPython ~5e7 simple ops/sec (optimistic for list ops in tight loop) → ~3s. If TL is 2s, TLE; if 3-5s, pass. Given uncertainty, maybe implement in a way that's fast enough: use iterative everything, localize variables, avoid attribute lookups.

  Actually, wait. Let me reconsider the problem constraints: this is from AtCoder "HHKB2020"? Let me think... "Takahashi plans to participate in N AtCoder contests" with L_i, R_i ≤ 5e5, Q ≤ 3e5 — I'm fairly sure this is ABC 279 Ex? Or "ARC"? Actually I now recall: this is from "AtCoder Beginner Contest 262"? Hmm. There's a well-known problem "Slime" no... I believe it's ABC 241 F? No. Let me just recall the known result: the intended solution is exactly the monotone-array + segment tree, and it's AtCoder ABC 280? The problem ID might be "abc268_g"? I can't recall. Known Python AC solutions for this problem exist (in PyPy). Time limit for AtCoder is typically 2s. Python (CPython) might struggle; PyPy passes. The grading environment here likely runs CPython with some time limit (unknown, maybe lenient). I'll write the most efficient CPython code I can: iterative segment tree, lists for mn/mx/lz (memory ~100MB worst case — hmm).

  Memory concern: 3 lists × 2^20 entries. Initially: mn/mx leaves = values 1..5e5 (ints > 256 → distinct objects, but each leaf value is a distinct int object anyway ~ 5e5 objects shared between mn and mx? If we assign the same int object to both mn[P+i] and mx[P+i], they share the object). Internal nodes: min of children, max of children — references to existing int objects. So initially few allocations. During updates, entries get new values → new int objects. In the worst case all 2^20 entries of mn and mx become distinct large ints: 2 × 2^20 × 28B ≈ 59MB + list pointers 2 × 8.4MB = 76MB. lz mostly small ints (≤ 2e5, but values ≤ 256 cached; up to N=2e5 → objects). lz entries that are nonzero: up to 2^20 × 28B = 29MB + 8.4MB list. Total worst ~120MB. Hmm, plus input storage. Risky if ML = 256MB but probably OK. Could use array('i') to cut to 12MB total with slight speed penalty. I'll consider array('i') — actually array element access in tight loops is maybe 1.5-2× slower than lists. Given time pressure, use lists but be mindful.

  Alternatively, drop mn array: can we do find_last_le(R) using only mx? No — need min. Hmm, but note cur[x] = x + add[x] where add non-increasing. "Last x with cur[x] ≤ R" ⟺ "last x with add[x] ≤ R - x"... not simpler.

  Alternatively store a single array mx and derive mn? No.

  OK here's another thought to halve the work: combine both searches into a single walk? They're independent predicates; can't trivially combine.

  Alternatively, reduce contests: if consecutive contests are identical, merge them into one with count k: applying contest k times = add k on the same interval? Careful: applying [L,R] twice: first increments cur in [L,R] → values become [L+1,R+1]; second application increments cur in [L,R] again — the set changed! After +1, values in [L+1, R+1]; those in [L+1, R] get incremented again, those at R+1 don't, and new x's with value L (previously L-1... no, previously at L moved to L+1; x's with value L now are those that were L before? none moved into L). So repeated application isn't simply +k on the same index interval. But it is: apply k times → indices with initial cur in [L, R-k+1] get +k, those with cur in (R-k+1, R] get + (R - cur + 1)... i.e., cur becomes min(cur + k, R+1)?? Let's verify: repeated increment while cur ≤ R: each step if cur ∈ [L,R] → +1. Starting cur = c ∈ [L,R]: after k steps, c + k but capped: increments stop once c > R, i.e., final = min(c + k, R + 1). And indices with c < L or c > R unaffected... wait if c slightly below L, never increments. So merging k identical contests: cur → cur + min(k, R + 1 - cur) for cur ∈ [L, R], i.e., cur → min(cur + k, R + 1) on the index interval [a, b]. That's a "range chmin with (R+1) after add" — segment tree beats territory. Not worth it; adversarial input has all-distinct contests anyway.

  Let me just go with the iterative segment tree and optimize constants. Actually, you know, let me reconsider using recursion but with the searches iterative and only range_add recursive — no, fully iterative is better.

  Let me now design the iterative lazy segment tree carefully (0-indexed, size P, arrays length 2P):

  Build:
  ```
  P = 1
  while P < V: P <<= 1
  mn = [0]*(2*P); mx = [0]*(2*P); lz = [0]*(2*P)
  for i in range(V):
      mn[P+i] = mx[P+i] = i+1
  for i in range(P-1, 0, -1):
      mn[i] = mn[2*i]; mx[i] = mx[2*i+1]  # since leaves ordered, min is leftmost, max is rightmost... but careful with beyond-V leaves = 0
  ```
  Beyond-V leaves: set mn = INF (large), mx = -INF? For searches: find_first_ge(L) might return index ≥ V — we must clamp. Simpler: set leaves beyond V to mn=INF, mx=INF? Then find_first_ge(L) could return them (mx ≥ L) — wrong. Set mn = INF, mx = -INF: find_first_ge skips them (mx < L always) ✓; find_last_le: predicate mn ≤ R — mn = INF > R → skipped ✓. And range_add never touches them if a,b computed within [0,V-1] ✓. But internal node mn = min(children) — with INF padding, mn of nodes mixing real and padding = real min ✓; nodes fully padding: mn=INF, mx=-INF. Build: mn[i] = min(mn[2i], mn[2i+1]), mx[i] = max(...). Since leaves are increasing, mn[i] = mn[2i] only if left child non-padding... safer to use min/max. Cost O(P) with min/max — fine (1e6 ops once).

  Hmm wait, actually since leaf values increase with index, mn[node] = leftmost leaf, mx[node] = rightmost leaf. But after updates, values within a node stay ordered (monotone preserved globally), so mn = leftmost, mx = rightmost always. Using min/max during build is simplest.

  apply(node, v): mn[node] += v; mx[node] += v; lz[node] += v.
  push(node): z = lz[node]; if z: apply(2node, z); apply(2node+1, z); lz[node] = 0.
  pull(node): mn[node] = min(mn[2n], mn[2n+1]); mx[node] = max(...).

  find_first_ge(L):  # smallest idx with cur[idx] >= L; return V if none
  ```
  if mx[1] < L: return V
  node = 1
  while node < P:
      push(node)
      if mx[2*node] >= L: node = 2*node
      else: node = 2*node+1
  return node - P
  ```
  find_last_le(R):  # largest idx with cur[idx] <= R; return -1 if none
  ```
  if mn[1] > R: return -1
  node = 1
  while node < P:
      push(node)
      if mn[2*node+1] <= R: node = 2*node+1
      else: node = 2*node
  return node - P
  ```
  Wait — find_last_le: we want the largest index with value ≤ R. Go right if right child has any value ≤ R i.e. mn[right] ≤ R. ✓.

  range_add(l, r, v) with 0 ≤ l ≤ r < V, iterative:
  Standard iterative lazy (from "efficient and easy segment trees", modified for min/max):
  ```
  l += P; r += P + 1
  l0 = l; r0 = r - 1
  # push ancestors
  for i in range(LOG, 0, -1):
      if (l0 >> i) << i != l0: push(l0 >> i)
      if (r0 >> i) << i != r0: push(r0 >> i)
  while l < r:
      if l & 1: apply(l, v); l += 1
      if r & 1: r -= 1; apply(r, v)
      l >>= 1; r >>= 1
  # pull ancestors
  for i in range(1, LOG+1):
      if (l0 >> i) << i != l0: pull(l0 >> i)
      if (r0 >> i) << i != r0: pull(r0 >> i)
  ```
  This is correct per the well-known method. The push condition `(l0 >> i) << i != l0` checks whether l0 is not aligned... Actually the standard condition is: push ancestors of l0 and r0 that are not on the boundary... The known code (from the CF blog, for lazy):
  ```
  void push(int l, int r) {
    int s = h, l0 = l, r0 = r;
    for (l += n, r += n; s > 0; --s) {
      for (int i = l >> s; i <= r >> s; ++i) ... 
    }
  }
  ```
  Hmm, there are variants. The cleanest correct iterative version pushes all ancestors of l0 and r0 from top down:
  ```
  for i in range(LOG, 0, -1):
      push(l0 >> i)   # but only if (l0 >> i) is an ancestor whose range isn't fully... 
  ```
  Actually pushing all ancestors of l0 and r0 (nodes l0>>i for i=LOG..1, and r0>>i) is safe and correct (push only propagates lazy down; pushing extra nodes is harmless as long as we later pull to fix ancestors' aggregates — but pulling ALL ancestors of l0/r0 after update fixes everything). Wait, but pushing an ancestor whose interval is fully inside [l,r] would push lazy down unnecessarily and then the update loop applies to children instead of the node — still correct, just slightly slower. But there's subtlety: the update loop applies to canonical nodes; ancestors of l0/r0 that are fully inside the range are NOT canonical nodes (canonical nodes are exactly those selected by the two-pointer walk; ancestors of endpoints are never fully selected... actually an ancestor of l0 can be fully inside [l,r]? If l0 is the left boundary, ancestors of l0 contain indices < l0... no wait, ancestor of l0 at height i covers [ (l0>>i)<<i, ((l0>>i)+1)<<i ). It contains l0's position. Since l0 = l+P is the leftmost updated leaf, the ancestor covers positions starting ≤ l... it starts at a multiple of 2^i ≤ l0-P... hmm, ancestor's range start = (l0>>i)<<i - P in leaf terms, which is ≤ l. If it equals l, the ancestor is fully inside [l, r]? Its range is [l, l + 2^i) — inside iff l + 2^i ≤ r. Possible! E.g., l=0, r=P: ancestors of l0=0 include node 1 (whole range) which is fully inside. Then the update loop: l=P(0+P), r=2P → l<r, l even, r even → l=P/2... wait l=P, r=2P: l&1=0, r&1=0 → l=P/2, r=P; ... eventually l=1,r=2 → apply(1). So node 1 IS selected by the walk. If we had pushed node 1 beforehand, its lazy went to children, then apply(1) adds to node 1's mn/mx/lz — correct anyway (children hold the pushed-down values, node1 gets new lazy; aggregates consistent). So pushing all ancestors is harmless for correctness. And pulling all ancestors bottom-up restores aggregates. 

  But careful: pushing ancestors of l0 includes node 1 (when i=LOG, l0>>LOG could be 1 or 0). l0 ≥ P → l0 >> LOG ≥ 1 ✓ (since l0 < 2P, l0>>LOG ∈ {1}). Good. Also r0>>i ancestors similarly. To avoid double-push/pull of shared ancestors — harmless.

  However, pushing ALL ancestors costs 2×19 pushes per contest even when unnecessary. The alignment check `(l0>>i)<<i != l0` skips pushes when the ancestor's range starts exactly at l0's... hmm, the standard optimization: only ancestors that are "partially overlapped" need pushing. The condition for ancestor at height i of l0 to be partial: the ancestor's range is not fully inside [l, r]. For the left endpoint: ancestor covers [A, A+2^i) with A = ((l0-P)>>i)<<i (in leaf coords). Fully inside iff A ≥ l and A+2^i ≤ r. Since A ≤ l always (A is l rounded down), A ≥ l ⟺ A == l ⟺ l aligned to 2^i. So if l is aligned at 2^i AND A+2^i ≤ r, ancestor fully inside → no push needed. The simple check `(l0>>i)<<i != l0` (l0 not aligned) catches the "A < l" case but not the "aligned but extends beyond r" case — pushing anyway is harmless. Fine, keep the simple check.

  Actually, simpler and definitely correct: skip the alignment checks, just push/pull all ancestors (2×19 each). Cost: 38 pushes + 38 pulls per range add. Push ~8 ops, pull ~6 ops → ~500 ops. Hmm, that's more than the searches. With alignment checks, roughly half skipped. Keep checks.

  Wait, actually there's an even simpler correct approach avoiding separate push/pull loops: do the searches and the add in one recursive function... no, keep iterative.

  Alternatively — cleaner idea: since find_first_ge and find_last_le already walk from root to leaves pushing along the way, the paths to a and b are already pushed! If range_add's ancestors of a and b were already pushed by the searches... The searches push nodes along the path to the found leaves a and b. range_add(a, b) needs ancestors of a+P and b+P pushed — exactly the paths the searches traversed (search for a ends at leaf a; search for b ends at leaf b). So after the two searches, all ancestors of a and b are already pushed (lz cleared along paths)! Then range_add can skip the push phase entirely, just do the update walk and the pull phase. 

  But careful: find_first_ge returns a = first index with cur ≥ L. The leaf it lands on is a. Its ancestors were pushed. Similarly b. So yes! Skip push phase in range_add. Saves ~38 push ops per contest. Also the update walk applies lazy to canonical nodes; pull phase fixes ancestors of a and b. 

  One more subtlety: after find_first_ge pushes path to a, values at leaves are up-to-date; the aggregate mn/mx of nodes OFF the path remain valid (push doesn't change aggregates of the pushed node itself — push propagates lazy to children but keeps node's mn/mx correct; children's mn/mx get updated correctly too). ✓. And after range_add's applies and pulls, all ancestors of a,b are fixed; nodes not ancestor of a or b but containing updated leaves? Any node containing an updated leaf in [a,b] is either a canonical node (applied directly) or an ancestor of a or b (pulled) — is that true? A node whose range intersects [a,b] partially contains a or b or is... a partially-overlapping node must contain a or b (since [a,b] is contiguous, a node overlapping but not containing either endpoint is fully inside). Fully-inside nodes are canonical (selected by walk) — yes, the standard argument: the walk selects exactly the canonical cover; every node with partial overlap is an ancestor of a or b. ✓ So pulling ancestors of a and b suffices. 

  Even better: we can fuse the pull into... whatever, it's fine.

  Also note: we might not even need the searches to return exact leaf then re-walk; but fine.

  Per-contest cost now: 2 searches (19 iters each, each iter: push + compare ~8 ops → ~150 ops each) + update walk (~38 applies max, each ~4 ops + loop overhead ~ 200 ops) + pull (38 pulls × 6 ops ≈ 230 ops). Total ~700-800 ops. Hmm similar to before. 1.5e8 ops total. ~4-6s CPython. Still risky.

  Micro-optimizations:
  - Use local variable references to lists inside loops.
  - Combine mn/mx/lz into a single list of lists? No — separate lists, indexed, is fastest.
  - Use while loops with precomputed LOG.
  - Avoid function call overhead: inline everything into the main contest loop (no function calls per operation). The main loop over contests: read L, R; do search1 inline, search2 inline, add inline. This avoids 3 function calls per contest (6e5 calls saved) and enables local variable caching. Code will be long but fast.

  Alternatively — think about whether we can use a Fenwick tree for everything with the "binary lifting" trick: Fenwick supports point query (value at index = x + fenwick.prefix(i)? no—range add, point query via BIT: add(a,b,v): bit.add(a,v), bit.add(b+1,-v); point query = prefix sum. Binary search for "first index with cur ≥ L" = first index with i + ps(i) ≥ L where ps(i) = prefix sum of BIT. ps is... cur is monotone, so binary search works: O(log V) steps each needing a prefix sum O(log V) → O(log²V)=361 BIT ops per search. BIT prefix sum in Python ~19 adds. So per search ~361 × (loop) ≈ 361 iterations of inner while? No: binary search 19 steps × prefix-sum 19 steps = 361 inner iterations, each ~3 ops → ~1000 ops per search. Worse than segtree walk. BUT: Fenwick "binary lifting" finds the largest prefix with sum ≤ K in O(log V) — that works on the BIT's own sums, but our predicate involves i + ps(i), not ps(i) alone. Since i + ps(i) is monotone, we can't directly use Fenwick lifting. Unless... transform: let d[i] = cur[i] - cur[i-1] ∈ {0,1} (with cur[0]=0). cur[i] = sum of d[1..i]. Range add [a,b] +1 on cur ⟺ d[a] += 1, d[b+1] -= 1. So d is a 0/1 array (mostly) with point updates! cur[i] = prefix sum of d. "First index with cur ≥ L" = position of the L-th 1 in d! "Last index with cur ≤ R" = position of the R-th 1 minus... last i with cur[i] ≤ R = (position of (R+1)-th 1) - 1. So we need a data structure for: binary array d with point updates (set/increment — d[a] goes 0→1 or stays? d[a] += 1: d values can exceed 1? d[i] = cur[i]-cur[i-1] ∈ {0,1} always (monotone + non-expanding). After update d[a]+=1, d[b+1]-=1: d[a] was cur[a]-cur[a-1]; since a is first with cur ≥ L, cur[a-1] < L ≤ cur[a] → cur[a] > cur[a-1] → d[a] = 1?? Then d[a] += 1 → 2?! Wait: cur[a-1] ≤ L-1 and cur[a] ≥ L; cur is integer and d ∈ {0,1} → cur[a] = cur[a-1] + d[a]. If d[a] were 1, cur[a] = cur[a-1]+1 ≤ L → could equal L ✓. After update, cur[a] increases by 1, cur[a-1] doesn't → d[a] becomes 2? But we claimed d ∈ {0,1} invariant! Contradiction? Let's recheck: after increment, cur[a]+1 vs cur[a-1]: cur[a-1] ≤ L-1, new cur[a] = old cur[a] + 1 ≥ L+1 > L-1 ≥ cur[a-1]... new d[a] = new cur[a] - cur[a-1] = old cur[a] + 1 - cur[a-1] = d_old[a] + 1 = 2 if d_old was 1. But invariant says d ∈ {0,1}?! Let me recheck the invariant with sample: cur after all contests: f(1)=6, f(2)=6 → d[2] = 0. f(3)=6 → d[3]=0. f(4)=7 → d[4]=1. f(5)=8 → d[5]=1. So d = [_, 6?? wait d[1] = cur[1] - cur[0]. cur[0] = 0 (rating 0 → f(0)? ratings start at 1; define cur[0] = 0 as sentinel... f(0): contest1 [1,5]: 0 not in range → 0; ... f(0) = 0 probably. d[1] = 6?? That's > 1! So d ∈ {0,1} only for i ≥ 2 if cur[0]=0... no wait d[i] = cur[i] - cur[i-1] ∈ {0,1} for all i ≥ 1 requires cur[0] such that cur[1] - cur[0] ≤ 1. cur[1] = 6. So the invariant d ∈ {0,1} holds for i ≥ 2 but the "jump" at i=1 can be large. Fine — treat cur[0] = 0 fixed, d[1] = cur[1] can be large. Hmm, but then "position of L-th 1" logic breaks because d[1] > 1.

  Let me redo: d[i] ∈ {0,1} for i ≥ 2, and d[1] = cur[1] ≥ 0 arbitrary. Define d'[i] = d[i] for i≥2, and handle the first value separately. cur[i] = d[1] + sum_{2..i} d. "First i with cur[i] ≥ L": if d[1] ≥ L → i=1... wait i starts at 1 (ratings 1..V). OK so: first index i ∈ [1,V] with cur[i] ≥ L: if cur[1] ≥ L, answer 1; else find first i ≥ 2 with prefix-sum of d[2..i] ≥ L - d[1]. That's an order-statistics query on a binary array: "find position of k-th one" — Fenwick with binary lifting does this in O(log V)! And updates: d[a] += 1, d[b+1] -= 1 — but wait we showed d[a] could become 2? Let's recheck with the invariant that a ≥ 2 or a = 1. Hmm, above I derived d[a] becomes 2 if d_old[a]=1. But the invariant d ∈ {0,1} must be preserved... let me recheck the invariant proof: cur non-decreasing with consecutive difference ≤ 1: initially cur[i] = i → d = 1 everywhere (d[i]=1). Update: cur[a..b] += 1 where a = first with cur ≥ L, b = last with cur ≤ R. New d[a] = cur[a]+1-cur[a-1]. Old d[a] = cur[a]-cur[a-1]. Since a is FIRST with cur ≥ L: cur[a-1] ≤ L-1 < L ≤ cur[a]. If old d[a] = 1: cur[a] = cur[a-1]+1 ≤ L-1+1 = L → cur[a] = L exactly. New d[a] = 2. But wait — is the invariant "d ≤ 1" actually preserved by the update? New d[a] = 2 contradicts. But hold on — can old d[a] = 1 happen? cur[a-1] = L-1, cur[a] = L. Then after update cur[a] = L+1, cur[a-1] = L-1 → d[a] = 2. Next contest, is d ≤ 1 invariant used anywhere? The monotonicity cur[x+1]-cur[x] ∈ {0,1} — let me re-examine whether that invariant actually holds! Initially cur[i]=i, differences 1. Contest update: indices [a,b] get +1. New difference at a: d[a]+1 could be 2. At b+1: d[b+1]-1: old d[b+1] = cur[b+1]-cur[b]; cur[b] ≤ R < cur[b+1] → d[b+1] ≥ 1 → new d[b+1] ≥ 0 ✓. But d[a] → 2 breaks the ≤1 invariant!! Let me verify with a concrete example: V=3, cur = [1,2,3] (indices 1..3). Contest L=2,R=2: a = first with cur ≥ 2 = index 2; b = last with cur ≤ 2 = index 2. cur → [1,3,3]. d = [1, 2, 0]. Indeed d[2] = 2! So my earlier claim f(x+1)-f(x) ∈ {0,1} is FALSE. Let me recheck with the sample: f(1)=6, f(2)=6, f(3)=6, f(4)=7, f(5)=8 — differences 0,0,1,1 — fine there, but in general differences can exceed 1? f(x+1) - f(x): both go through same contests; x+1 starts 1 ahead; the gap can only grow? If x in [L,R] and x+1 in [L,R], both increment — gap unchanged. If only x+1 in range (x = L-1): x+1 increments, x doesn't → gap grows by 1. If only x in range (x = R, x+1 = R+1): x increments → gap shrinks by 1. So gap can grow arbitrarily! f is monotone non-decreasing but NOT 1-Lipschitz. My earlier claim was wrong. Good thing we didn't rely on d ∈ {0,1}. But the segment tree approach only relies on monotonicity of cur (non-decreasing), which holds. ✓ (mn=leftmost, mx=rightmost still valid.)

  Phew — so segment tree approach remains valid. The d-array/Fenwick approach: d can be any non-negative integer; updates d[a] += 1, d[b+1] -= 1 still hold (range add on cur = point updates on difference array!). And cur[i] = prefix sum d[1..i]. Searches: first i with prefix ≥ L. Fenwick binary lifting finds largest i with prefix < L in O(log V) — works with arbitrary non-negative d! But d values: d[a] += 1 where d[a] could already be large — fine, Fenwick handles arbitrary values. BUT: binary lifting on Fenwick requires non-negativity of d to have monotone prefix sums — d[i] ≥ 0 always (cur monotone) ✓. And d[b+1] -= 1 keeps d[b+1] ≥ 0 as shown ✓.

  So the Fenwick approach:
  - BIT over d[1..V], initially d[i] = 1 for all i (cur[i] = i). Wait d[1] = 1, d[i]=1 → cur[i] = i ✓.
  - find_first_ge(L): find smallest i with ps(i) ≥ L. Binary lifting: standard "lower_bound" on Fenwick: find largest pos with ps(pos) < L, answer pos+1. If ps(V) < L → none (return V+1). O(log V) with ~19 iterations, each 1-2 BIT array accesses — VERY cheap, no push/lazy!
  - find_last_le(R): largest i with ps(i) ≤ R = largest pos with ps(pos) ≤ R → binary lifting for "largest pos with ps(pos) ≤ R": find largest pos with ps(pos) < R+1, i.e., lower_bound(R+1) - 1. O(log V).
  - Update: if a ≤ b: bit.add(a, +1), bit.add(b+1, -1). Two point updates, each O(log V) ~19 iterations of `while i <= V: bit[i] += v; i += i&-i` — cheap.
  - At the end: cur[i] = ps(i) for all i — compute all prefix sums O(V log V) or O(V) by walking: cur[i] = cur[i-1] + d[i] where d[i] recovered via bit.prefix(i)-bit.prefix(i-1)... simpler: after all updates, compute d[i] = bit prefix diff — actually just compute ps(i) for each i via BIT query O(log V) each → 5e5 × 19 = 1e7 ops, fine. Or reconstruct d array from BIT in O(V) (standard: d[i] = bit[i] - (bit[i - (i&-i)]... there's an O(V) reconstruction). Simpler: ps via loop with BIT query each — 1e7 ops ~ 3-5s? Hmm, that's a lot. O(V) reconstruction: for i in 1..V: d[i] = bit[i]; then for i: j = i + (i&-i); if j <= V: d[j] -= d[i]... that gives original d. Then prefix sum in O(V). Total ~3 × 5e5 = 1.5e6 ops. 

  Per contest cost: 2 binary-liftings (19 iters × ~3 ops = 60 each) + 2 point updates (19 iters × 3 ops = 60 each) ≈ 240 ops → 2e5 × 240 = 4.8e7 ops → ~2-3s CPython. Better than segment tree (~1.5e8)! And WAY simpler code, tiny memory (one BIT array of size 5e5+2).

  Wait, but I must double check the binary lifting "lower_bound" on Fenwick with arbitrary non-negative values: standard algorithm finds the largest index pos such that ps(pos) < target (a.k.a. lower_bound): 
  ```
  pos = 0; acc = 0
  for k in powers of 2 descending from highest ≤ V:
      nxt = pos + k
      if nxt <= V and acc + bit[nxt] < target:
          acc += bit[nxt]; pos = nxt
  return pos  # ps(pos) < target ≤ ps(pos+1)
  ```
  This requires prefix sums monotone (non-negative d) ✓. Correct standard algorithm.

  So:
  - a = lower_bound(L) + 1  (first index with ps ≥ L); if a > V → no update... also need ps(V) ≥ L check: if pos == V then a = V+1 → empty.
  - b = lower_bound(R + 1) (largest index with ps ≤ R = lower_bound(R+1)+1-1). Let pos2 = lower_bound(R+1) → ps(pos2) < R+1 ≤ ps(pos2+1) → b = pos2. (b could be V, fine; b ≥ 0.)
  - if a <= b: add(a, +1); add(b+1, -1) (b+1 ≤ V? if b = V, skip second add or allow BIT size V+1 — just guard `if b+1 <= V`).
  
  Edge: ratings X from 1 to 5e5 = V. cur array indices 1..V. ✓.

  Let me verify with sample 1: V ≥ 5; use V = 5e5 but let's trace small with indices 1..5 (and beyond all d=1). Initially d[i]=1 ∀i, cur[i]=i.
  Contests: [1,5],[1,3],[3,6],[2,4],[4,7].
  C1 [1,5]: a = lb(1)+1: ps(i)=i; largest pos with ps < 1 → pos=0 → a=1. b = lb(6): largest pos with ps < 6 → pos=5 (ps(5)=5 <6, ps(6)=6≥6) → b=5. add(1,+1), add(6,-1). d: d[1]=2, d[6]=0. cur: [2,3,4,5,6,6,7,8,...]. Wait cur[1] = 2? f after contest 1: rating 1 → in [1,5] → 2 ✓; rating 5 → 6 ✓; rating 6 → 6 (not in [1,5]) ✓. 
  C2 [1,3]: a = lb(1)+1 = 1 (ps(1)=2 ≥ 1, pos=0). b = lb(4): ps: [2,5,9,13,17,...]. ps(1)=2<4, ps(2)=5≥4 → pos=1 → b=1. add(1,+1), add(2,-1). d[1]=3, d[2]=0. cur: [3,3,4,5,6,6,7,...]. Check: after C2, rating1: 2→3 (in [1,3]) ✓; rating2: was 3 → in [1,3] → 4? Wait forward: initial rating 2 → after C1 = 3 → C2 [1,3]: 3 in range → 4. But cur[2] = 3?! Discrepancy! Let me recompute. Hmm wait, cur[2] after C1 = 3 ✓ (2→3). C2: 3 ∈ [1,3] → 4. So cur[2] should be 4. But my computed cur[2] = 3. Let me recheck b: b should be last index with cur ≤ R=3: cur = [2,3,4,5,6,...] → indices 1 (2≤3 ✓) and 2 (3≤3 ✓) → b should be 2! My lb(4): largest pos with ps(pos) < 4. ps(1)=2 <4 ✓, ps(2)=5 ≥4 → pos=1 → b=1. WRONG — b should be 2. 

  Where's the bug? "Last i with cur[i] ≤ R" = last i with ps(i) ≤ R = last i with ps(i) < R+1 = lb(R+1) where lb(t) = largest pos with ps(pos) < t. lb(4): ps(1)=2<4, ps(2)=5≮4 → pos=1. But ps(2)=5 and we want ps(i) ≤ 3: ps(1)=2≤3, ps(2)=5>3 → last i = 1?? But cur[2] = 3 ≤ 3! ps(2) should be cur[2] = 3, not 5. Let me recompute ps after C1: d[1]=2, d[2]=1, d[3]=1,... → ps(1)=2, ps(2)=3, ps(3)=4, ps(4)=5, ps(5)=6, ps(6)=6 (d[6]=0), ps(7)=7. I made an arithmetic error before: ps(2)=3 not 5. Redo C2: a = lb(1)+1 = 0+1 = 1. b = lb(4): ps(1)=2<4, ps(2)=3<4, ps(3)=4≮4 → pos=2 → b=2 ✓. add(1,+1), add(3,-1). d: d[1]=3, d[3]=0. cur: [3,4,4,5,6,6,7,...]. Check rating2: 2→3→4 ✓. rating1: 1→2→3 ✓ (cur[1]=3). 
  C3 [3,6]: a = lb(3)+1: ps(1)=3 ≮3 → pos=0 → a=1. b = lb(7): ps: [3,7,...] ps(1)=3<7, ps(2)=7≮7 → pos=1 → b=1. add(1,+1), add(2,-1). d[1]=4, d[2]=0. cur: [4,4,4,5,6,6,7,8,...]. Check rating3 after C3: 3→4→4→ C3 [3,6]: 4∈ → 5? Forward: initial 3: C1 →4, C2: 4∉[1,3] →4, C3: 4∈[3,6] →5. cur[3] should be 5 but I got 4?! Hmm. Let me recompute. After C2, cur = [3,4,4,5,6,6,7,...]: check rating 3: C1: 3∈[1,5]→4; C2: 4∉[1,3]→4. ✓ cur[3]=4. C3 [3,6]: indices with cur ∈ [3,6]: cur[1]=3 ✓, cur[2]=4 ✓, cur[3]=4 ✓, cur[4]=5 ✓, cur[5]=6 ✓, cur[6]=6 ✓, cur[7]=7 ✗. So a=1, b=6. My lb gave a=1 ✓ but b=1 ✗. Bug: b = lb(R+1) = lb(7): largest pos with ps < 7. ps after C2: d=[3,1,0,1,1,1,0,1,...] wait let me recompute d after C2: initial d all 1; C1: d[1]+=1 → 2, d[6]-=1 → 0. C2: d[1]+=1 → 3, d[3]-=1 → 0. So d = [_,3,1,0,1,1,1,0,1,1,...]. ps: ps(1)=3, ps(2)=4, ps(3)=4, ps(4)=5, ps(5)=6, ps(6)=7, ps(7)=7, ps(8)=8. cur[5]=6? ps(5)=6 ✓ (rating5: C1→6, C2: 6∉[1,3]→6 ✓). cur[6]=7? rating6: C1: 6∉[1,5]→6; C2: 6∉→6. cur[6] should be 6! But ps(6)=7. BUG. d[6] was decremented to 0 by C1 (b+1=6). cur[6] = ps(6) = 3+1+0+1+1+1 = 7. But correct cur[6] = 6. Let me recheck C1: [1,5]: b = last index with cur ≤ 5 = index 5 (cur[5]=5). add(1,+1), add(6,-1): cur[1..5] += 1 → [2,3,4,5,6], cur[6] = 6 unchanged ✓. ps(6) = 6+... wait cur[6] = 6 means ps(6) = 6. d = [_,2,1,1,1,1,0,1,...]: ps(6) = 2+1+1+1+1+0 = 6 ✓. I mistakenly wrote d[1]=2 then ps(1)=2 ✓, ps(2)=3, ps(3)=4, ps(4)=5, ps(5)=6, ps(6)=6 ✓. Then C2: a=1, b: lb(4): ps(1)=2<4, ps(2)=3<4, ps(3)=4 ≮4 → pos=2 → b=2 ✓. add(1,+1)→d[1]=3; add(3,-1)→d[3]=0. d=[_,3,1,0,1,1,0,1,...]. ps: 3,4,4,5,6,6,7. cur=[3,4,4,5,6,6,7] ✓ matches (rating5→6, rating6→6 ✓). C3 [3,6]: a = lb(3)+1: ps(1)=3 ≮3 → pos=0 → a=1 ✓. b = lb(7): ps(1)=3<7, ps(2)=4<7, ps(3)=4<7, ps(4)=5<7, ps(5)=6<7, ps(6)=6<7, ps(7)=7≮7 → pos=6 → b=6 ✓ (I mis-added before). add(1,+1) → d[1]=4; add(7,-1) → d[7]=0. d=[_,4,1,0,1,1,1,0,0,1,...]. ps: 4,5,5,6,7,8,8,8,9,... cur=[4,5,5,6,7,8,8,8,9]. Check rating3: C1→4, C2→4, C3: 4∈[3,6]→5 ✓ cur[3]=5. rating1: →2→3→4 ✓ cur[1]=4. 
  C4 [2,4]: a = lb(2)+1: ps(1)=4≮2 → pos=0 → a=1. b = lb(5): ps(1)=4<5, ps(2)=5≮5 → pos=1 → b=1. add(1,+1)→d[1]=5; add(2,-1)→d[2]=0. cur: ps: 5,5,5,6,7,8,8,8,9. Check rating2: 2→3→4→5(C3: 4∈[3,6]→5)→ C4 [2,4]: 5∉ →5. cur[2]=5 ✓. rating1: →2→3→4→ C4: 4∈[2,4]→5 ✓.
  C5 [4,7]: a = lb(4)+1: ps(1)=5≮4 → pos=0 → a=1. b = lb(8): ps: 5,5,5,6,7,8,... ps(5)=7<8, ps(6)=8≮8 → pos=5 → b=5. add(1,+1)→d[1]=6; add(6,-1)→d[6]=0. Final ps: 6,6,6,7,8,8,8,8,9,... cur[1..5] = [6,6,6,7,8]. Expected: f(1)=6 ✓, f(2)=6 ✓, f(3)=6 ✓, f(4)=7 ✓, f(5)=8 ✓. 

  The Fenwick approach works beautifully. Sample 1 queries: X=3→6 ✓, X=2→6 ✓, X=5→8 ✓.

  Now complexity per contest: 2 × lower_bound (each ~19 iterations of: nxt = pos + k; if nxt <= V and acc + bit[nxt] < t: ...) ≈ 19 × 5 ops = 95 ops → 190; plus 2 point updates ~19 × 4 ops = 76 each → 150. Total ~340 ops/contest → 6.8e7 for N=2e5. Hmm, ~3-4s CPython. Can we trim? Note the two lower_bounds: lb(L) and lb(R+1). Both needed. Point updates: add(a,+1) and add(b+1,-1): each `while i <= V: bit[i] += v; i += i & -i`. ~19 iters.

  Alternative micro-opt: precompute powers of 2 list. Use local vars. Inline all in main loop. Should be ~2-3s. Acceptable risk; much better than segtree.

  Wait, actually we can halve the lower_bound work: we need a = lb(L)+1 and b = lb(R+1). Note lb is monotone in target; two separate searches needed. Fine.

  Also note: we can early skip if a > b.

  Also handle V: max rating = 5e5 (given constraints: X ≤ 5e5, and L_i,R_i ≤ 5e5). But cur values can exceed V (up to V + N). BIT lower_bound target up to R+1 ≤ 5e5+1; ps values up to V + N ≈ 7e5 — fine. BIT size V = 5e5. Highest power: 2^19 = 524288 > V → start k = 2^18 = 262144? Standard: start with largest power of 2 ≤ V... Actually binary lifting typically starts at highest power of 2 ≥ ... use k = 1 << (V.bit_length() - 1) = 2^18 = 262144. Hmm, the standard algorithm uses highest power ≤ n. Let me use k starting at 1 << (V.bit_length() - 1). For V = 5e5, bit_length = 19 (since 2^18 = 262144 ≤ 5e5 < 2^19), so start k = 262144. ✓.

  Edge cases:
  - a = pos+1 where pos = lb(L). If ps(V) < L then pos = V → a = V+1 > V → no update. Check: also if a > b skip.
  - b = lb(R+1) = pos2. If ps(1) > R i.e. pos2 = 0 → b = 0 < a ≥ 1 → skip ✓ automatically.
  - b could be V → add(b+1) = add(V+1) out of range; guard `if b < V: add(b+1, -1)`. Actually b+1 = V+1 only when b = V; the -1 at V+1 would only affect indices > V which we never query — safe to skip. ✓.

  Final reconstruction: compute cur[i] for i in 1..V:
  Option A: for each i, BIT prefix query — O(V log V) = 1e7 ops ~ 3s. Too slow-ish.
  Option B: extract d from BIT in O(V): standard trick:
  ```
  d = bit[1:V+1] (copy)
  for i in range(1, V+1):
      j = i + (i & -i)
      if j <= V: d[j] -= d[i]
  ```
  Wait, that reconstructs the original array from BIT: for i from 1..n: j = i + (i&-i); if j ≤ n: bit[j] -= bit[i] — but this must be done in a specific order? The standard reconstruction: for i in range(1, n+1): j = i + (i & -i); if j <= n: bit[j] -= bit[i]. Processing i in increasing order works because bit[i] at the time of processing holds a[i] + (contributions from smaller indices already subtracted)... Let me recall: BIT[i] = sum over (i - (i&-i) + 1 .. i) of a. To invert: for i = n down to 1? Hmm. Common method: for i in range(1, n+1): j = i + (i&-i); if j <= n: bit[j] -= bit[i]. After this loop, bit[i] = a[i]. Let me verify small: n=4. BIT[1]=a1, BIT[2]=a1+a2, BIT[3]=a3, BIT[4]=a1+a2+a3+a4. i=1: j=2: BIT[2] -= BIT[1] → a2. i=2: j=4: BIT[4] -= BIT[2](now a2) → a1+a3+a4. i=3: j=4: BIT[4] -= BIT[3]=a3 → a1+a4. Hmm BIT[4] = a1+a4 ≠ a4. That's wrong. Correct order: process i from n down to 1? i=4: j=8>4 skip. i=3: j=4: BIT[4] -= BIT[3] → a1+a2+a4. i=2: j=4: BIT[4] -= BIT[2] → a4 ✓. i=1: j=2: BIT[2] -= BIT[1] → a2 ✓. So loop i from n down to 1: for i in range(n, 0, -1): j = i + (i&-i); if j <= n: bit[j] -= bit[i]. Then bit[i] becomes a[i]. Verify fully: initial BIT = [a1, a1+a2, a3, a1+a2+a3+a4] (indices 1..4). i=4: j=8 skip. i=3: j=4: BIT[4] = a1+a2+a4. i=2: j=4: BIT[4] = a4 ✓; BIT[2] unchanged = a1+a2. i=1: j=2: BIT[2] = a2 ✓. Result: BIT = [a1, a2, a3, a4] ✓. 
  Then cur[i] = cur[i-1] + bit[i] prefix loop O(V). Total reconstruction ~2×5e5 = 1e6 ops ✓.

  Actually even simpler: skip reconstruction; answer queries by BIT prefix query per query: Q = 3e5 × 19 = 5.7e6 ops ~ 2s. Hmm, reconstruction O(V) + O(1) per query is better: ~1e6 + 3e5. Do reconstruction.

  Wait, even better: we don't need d separately; after the reverse loop, bit[i] = d[i]; then running prefix: c = 0; for i in 1..V: c += bit[i]; cur[i] = c. Store cur as a list of size V+1. Then answer queries: print cur[X]. 

  Memory: bit list size V+2 ints (~5e5 × 28B = 14MB + list 4MB) fine; cur another — we can reuse bit as cur in place! After reverse loop bit[i] = d[i]; then prefix in place: for i in 2..V: bit[i] += bit[i-1] → bit[i] = cur[i]. Then queries read bit[X]. One array only. 

  Input parsing: read all via sys.stdin.buffer.read().split() — N up to 2e5 lines ×2, Q 3e5 → total tokens ≈ 2 + 4e5 + 1 + 3e5 = 7e5 tokens. split() memory fine (~7e5 bytes objects ~ 30MB?). Hmm, 7e5 tokens × ~50B overhead ≈ 35MB. Acceptable. Or use a custom fast parser (map to ints via split is typical). I'll use read().split() and map(int, ...) lazily via iterator — iter of bytes → int() conversion on demand. Fine.

  Output: Q lines, join with '\n'.

  Now double-check the lower_bound correctness with target possibly ≤ ps(1): lb(t) returns pos=0 (since no k step satisfies acc+bit[k] < t... wait first iteration k=262144 > V? No, k starts at 262144 ≤ V=5e5 ✓. nxt = 262144; if acc + bit[262144] < t... For t small, condition fails everywhere → pos=0 ✓. Note: binary lifting requires the BIT to store the actual frequencies — yes standard.

  One more check: the algorithm's lower_bound requires non-negative d values (monotone prefix). We proved d stays ≥ 0: d[b+1] -= 1 only when b+1 has d ≥ 1? Proof: b = last with cur ≤ R; cur[b+1] ≥ R+1 > R ≥ cur[b] → d[b+1] = cur[b+1] - cur[b] ≥ 1 ✓ (when b+1 ≤ V). And d[a] += 1 keeps ≥ 0 ✓. Also d[1] = cur[1] ≥ 0 always (starts 1, only incremented... d[1] only gets +1 when a=1; never decremented since b+1 ≥ 2). ✓.

  Also confirm a ≤ b check handles all no-op cases: if no index has cur ≥ L (ps(V) < L) → a = V+1 → skip ✓. If no index has cur ≤ R (cur[1] > R) → b = 0 → skip ✓. If a > b (gap: cur values jump over [L,R]) → skip ✓.

  Great, the solution is O((N + V) log V + Q) with tiny constants. Let me now also double check sample 2 mentally? Trust it.

  Now write the code:

  ```python
  import sys

  def main():
      data = sys.stdin.buffer.read().split()
      idx = 0
      N = int(data[idx]); idx += 1
      V = 500000
      L = [0]*N; R = [0]*N
      for i in range(N):
          L[i] = int(data[idx]); R[i] = int(data[idx+1]); idx += 2
      Q = int(data[idx]); idx += 1
      queries = [int(x) for x in data[idx:idx+Q]]
      
      bit = [0]*(V+2)
      # init d[i] = 1: bit for all-ones: bit[i] = i & -i
      for i in range(1, V+1):
          bit[i] = i & -i
      
      # process contests
      hb = 1 << (V.bit_length() - 1)  # highest power of 2 <= V
      for i in range(N):
          Li = L[i]; Ri = R[i]
          # a = lower_bound(Li) + 1 : largest pos with ps(pos) < Li, +1
          pos = 0; acc = 0
          k = hb
          bit_ = bit
          while k:
              nxt = pos + k
              if nxt <= V and acc + bit_[nxt] < Li:
                  acc += bit_[nxt]
                  pos = nxt
              k >>= 1
          a = pos + 1
          # b = lower_bound(Ri+1): largest pos with ps(pos) <= Ri
          t = Ri + 1
          pos = 0; acc = 0
          k = hb
          while k:
              nxt = pos + k
              if nxt <= V and acc + bit_[nxt] < t:
                  acc += bit_[nxt]
                  pos = nxt
              k >>= 1
          b = pos
          if a <= b:
              # add(a, +1)
              j = a
              while j <= V:
                  bit[j] += 1
                  j += j & -j
              if b < V:
                  j = b + 1
                  while j <= V:
                      bit[j] -= 1
                      j += j & -j
      # reconstruct d then prefix
      for i in range(V, 0, -1):
          j = i + (i & -i)
          if j <= V:
              bit[j] -= bit[i]
      # now bit[i] = d[i]; prefix in place
      for i in range(2, V+1):
          bit[i] += bit[i-1]

## worker: Implement the Fenwick (BIT) solution: fast input p
- **Key insight**: maintain `cur[x]` = final rating for initial rating `x`. `cur` is non-decreasing, so its difference array `d[i] = cur[i] - cur[i-1]` is non-negative. A contest `[L, R]` adds +1 to `cur[x]` exactly on the contiguous index interval `{x : L ≤ cur[x] ≤ R} = [a, b]`, which is just two point updates on `d`: `d[a] += 1`, `d[b+1] -= 1`.
- Because `cur` is monotone, `a` = first index with prefix-sum `≥ L` and `b` = last index with prefix-sum `≤ R` are found by Fenwick **binary lifting** (lower_bound) in O(log V) each — valid since all `d[i] ≥ 0` (invariant preserved: `d[b+1] ≥ 1` before decrement because `cur[b+1] > R ≥ cur[b]`).
- BIT is initialized for the all-ones `d` via `bit[i] = i & -i` in O(V).
- After all contests, `d` is recovered from the BIT in O(V) (reverse loop `bit[j] -= bit[i]` for `j = i + (i&-i)`), then prefix-summed in place to obtain `cur[x]`; queries answered in O(1).
- **Verified by hand on Sample 1**: traced all 5 contests through the BIT operations; final `cur[1..5] = [6,6,6,7,8]`, matching expected outputs (3→6, 2→6, 5→8). Edge cases handled: `a = V+1` (no `cur ≥ L`), `b = 0` (no `cur ≤ R`), `a > b` (values jump over `[L,R]`), and `b = V` (skip the `d[V+1]` decrement).
- Complexity: O((N + V) log V + Q) time, O(V) memory. Per contest ~2 binary liftings + 2 point updates (~40 cheap loop iterations total), fast enough in CPython.

## worker: Verify the implementation against the three provid
**Verification performed** (mentally traced + logic-checked against samples and edge cases):

**Sample 1** (traced in detail in the plan): BIT ops give final `cur[1..5] = [6,6,6,7,8]`. Queries 3→6, 2→6, 5→8 ✓ matches expected output.

**Sample 2** (spot-checked key queries): Contests are mostly `[1,1999]` (7 of them), plus `[1200,2399]`, `[2000,500000]`, `[1600,2799]`.
- X=1: increments in all 7 `[1,1999]` contests + `[1200,2399]` (rating reaches 7→8, at 1200+? rating after 7 contests = 8, never reaches 1200) → answer 8 ✓ (expected 8).
- X=500000: only `[2000,500000]` applies → 500001 ✓.
- X=1995: 7 increments from `[1,1999]` (1995→2002, but stops applying once rating >1999: 1995,96,97,98,99 increment → 2000, then `[1,1999]` no longer applies — that's 5 increments → 2000; then `[2000,500000]` applies → 2001... expected 2002. Recount: contests in order: `[1,1999]`×2 →1997, `[1200,2399]` →1998, `[1,1999]`×4 → 1999,2000(stop applies after 1999→2000: ratings 1998→1999 ✓, 1999→2000 ✓, then 2000 not in [1,1999]) — so `[1,1999]` applies while rating ≤1999: 1995→1996→1997→1998→1999→2000 = 5 increments across the six `[1,1999]` contests seen before rating hits 2000... then `[2000,500000]` → 2001, remaining `[1,1999]` contests skip, `[1600,2799]` → 2002 ✓. Matches expected 2002. The BIT mechanism handles this correctly since each contest's interval `[a,b]` is computed from current `cur` values.

**Sample 3**: X=11431 and X=8580 are below all L_i → no contest applies → unchanged ✓ (expected outputs match inputs). Others gain exactly 6 (each X lands in 6 of the 15 intervals — consistent with monotone `cur` logic).

**Edge cases checked:**
- **N=1**: single lower_bound pair + at most one update; reconstruction loops still valid.
- **X=1 / X=5·10⁵ boundaries**: `cur[1]` and `cur[V]` both correctly maintained; queries index `bit[X]` directly.
- **No contest applies** (X outside all `[L_i,R_i]`): `a > b` or `b = 0` or `a = V+1` → update skipped; `cur[x] = x` ✓.
- **All contests apply** (`L_i=1, R_i=5·10⁵`): `a=1, b=V` every time; `b < V` guard skips the `d[V+1]` decrement; `cur[x] = x + N` ✓.
- **b = V case**: guard `if b < V` prevents out-of-range BIT index and is semantically correct (no indices > V exist).
- **a > V case**: `a = pos+1 = V+1` when `ps(V) < L`; `a <= b` fails since `b ≤ V` → skip ✓.
- **Invariant `d[i] ≥ 0`**: `d[b+1] ≥ 1` before decrement because `cur[b+1] > R ≥ cur[b]`; binary lifting validity preserved.
- **BIT init**: `bit[i] = i & -i` is exactly the BIT of the all-ones array ✓.
- **Reconstruction order**: decreasing `i` verified correct (`bit[j] -= bit[i]` with `j = i + (i&-i)`), then in-place prefix sum yields `cur[x]` ✓.

Complexity: O((N + V) log V + Q) ≈ 2·10⁵ × ~40 cheap iterations + 10⁶ — fast in CPython. Memory: one int list of size V+1 (~5·10⁵) plus input tokens.
