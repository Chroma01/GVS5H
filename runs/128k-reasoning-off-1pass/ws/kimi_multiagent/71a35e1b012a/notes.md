
## ideation
This is the AtCoder-style problem "choose per operation: nothing / set interval to 1 / set complement to 1". Since writes only turn 0→1, the final state is all-1s iff every position j is covered by at least one chosen operation, where operation i covers j iff (op=1 and j∈[Li,Ri]) or (op=2 and j∉[Li,Ri]). Cost = number of non-zero operations, so we want the minimum number of operations whose "coverage sets" (each either an interval or a complement-of-interval) cover [1,N].

Key structural facts to verify:
- K=0 impossible (N≥1).
- K=1 possible iff some operation has [Li,Ri]=[1,N] (op1) — op2 of a single operation can never cover [1,N] since complement can't be everything. Actually op2 covers complement of [L,R]; to be all of [1,N] we'd need [L,R] empty, impossible. So K=1 iff ∃i: Li=1, Ri=N.
- K=2 cases: (1,1): union of two intervals = [1,N]; (1,2): interval ∪ complement-of-interval = [1,N] iff the complement's hole [Lj,Rj] ⊆ [Li,Ri]... precisely: op1 on i covers [Li,Ri], op2 on j covers everything except [Lj,Rj]; union = [1,N] iff [Lj,Rj] ⊆ [Li,Ri]. (2,2): complement of [Li,Ri] ∪ complement of [Lj,Rj] = complement of intersection; equals [1,N] iff [Li,Ri] ∩ [Lj,Rj] = ∅.
- K=3: claim — if no solution with K≤2, then K=3 always works? Sample 4 (N=5, [1,3],[2,4]) gives -1, so feasibility isn't automatic. Need to characterize: with 3 operations we can use patterns like op2 on [l,r] (covers [1,l-1]∪[r+1,N]) plus two op1s covering [l,r], i.e., need intervals covering [l,r]. Or op1+op1+op2 patterns. The known solution: answer ∈ {1,2,3,-1}; 3 suffices iff there exist operations i,j,k with... Standard approach: try to find triple (op2 on i, op1 on j, op1 on k) covering [Li,Ri] by [Lj,Rj]∪[Lk,Rk], i.e., Lj ≤ Li, Rj ≥ something, and Lk ≤ ..., Rk ≥ Ri — actually two intervals cover [a,b] iff one has L≤a and R≥a-? Two intervals [l1,r1],[l2,r2] cover [a,b] iff (after sorting l1≤l2) l1≤a, r1≥l2-1... no wait, covering a contiguous target with two intervals requires l1≤a, r2≥b, and r1 ≥ l2 - 1 (no gap). Hmm, but coverage doesn't require contiguity of the union overall — union must ⊇ [a,b], so yes need no gap: r1+1 ≥ l2.

Alternative known characterization (this is AtCoder AGC/ARC?): The answer is min over patterns. Let me think of it as: we need to cover [1,N]. Each op2 covers a prefix+suffix (two rays), each op1 covers an interval. With 3 ops, the useful patterns: (2,1,1): rays from one op + two intervals covering the middle hole; (2,2,1): two ray-pairs + one interval covering the intersection of holes; (1,1,1): three intervals covering [1,N]; (2,2,2): three complements covering [1,N] iff intersection of the three holes is empty.

Pitfall: M,N up to 2e5/1e6, so O(M) or O(M log M) needed. Checking K=2 naively is O(M²) — must be smart:
- (1,1): need i,j with Li=1... union [Li,Ri]∪[Lj,Rj]=[1,N] iff one starts at 1, other ends at N, and they overlap/touch: min L =1, max R = N, and Ri ≥ Lj-1 where Li≤Lj. Check: exists i with Li=1 and j with Rj=N and Ri ≥ Lj-1. Compute for each j with Rj=N, need some i with Li=1 and Ri ≥ Lj-1: just max R among L=1 intervals.
- (1,2): need [Lj,Rj] ⊆ [Li,Ri]: exists pair with Li ≤ Lj and Ri ≥ Rj, i≠j (or same i? If same operation used once, that's K=1; using op1 and op2 on the same operation index isn't allowed — each operation picks exactly one type. So i≠j). Check: for each j, exists i≠j with Li≤Lj, Ri≥Rj. Sweep/sort with segment tree or sort by L and track max R; careful with i≠j (handle ties by keeping top-two max R values).
- (2,2): need [Li,Ri] ∩ [Lj,Rj] = ∅: exists pair with Ri < Lj. Just check min R < max L.

K=3 construction: if K≤2 fails, find any feasible triple; if none, -1. Need to characterize feasibility of K=3 and construct. Patterns:
- (2,1,1): pick op2 on k, cover [Lk,Rk] with two intervals i,j: need Li ≤ Lk, Ri ≥ Lj-1, Rj ≥ Rk (sort so Li≤Lj). Equivalent: exists i,j,k distinct with Li ≤ Lk, Rj ≥ Rk, Ri ≥ Lj - 1.
- (2,2,1): holes [Li,Ri]∩[Lj,Rj] ⊆ [Lk,Rk]. Intersection = [max(Li,Lj), min(Ri,Rj)] (if nonempty). Need Lk ≤ max(Li,Lj) and Rk ≥ min(Ri,Rj).
- (1,1,1): three intervals cover [1,N]: Li=1 for some, Rj=N for some, and middle bridges: exists i,j,k with Li=1, Rj=N, Ri ≥ Lk-1, Rk ≥ Lj-1... Actually union of 3 intervals = [1,N] iff sorted by L: l1=1, r3=N, r1≥l2-1, r2≥l3-1.
- (2,2,2): intersection of three holes empty: min over... intersection empty iff max L > min R among the three. Equivalent to (2,2) case with... no, three holes can have empty intersection even if every pair intersects (Helly doesn't apply? For intervals on a line, Helly says pairwise intersecting ⇒ total intersection nonempty. So three intervals have empty intersection iff some pair is disjoint!). So (2,2,2) reduces to (2,2) case — covered by K=2 check. Similarly (1,1,1) might not reduce. (2,2,1) doesn't reduce.

Hmm wait — but is the answer always ≤3 when feasible? Feasibility requires every position covered; with unlimited ops we could still fail (sample 4). Claim: if feasible at all, feasible with ≤3. Plausible: consider position coverage; the hardest positions are extremes. Known result for this AtCoder problem (it's ABC 267 Ex? No... it's "HHKB2020"? Actually it's AtCoder "jsc2021"? I recall this is ARC 113 B? Not sure). Anyway, the standard editorial: answer ∈ {1,2,3,-1}, check 1, check 2, check 3, else -1. And 3-feasibility check: exists i,j,k with pattern (2,1,1) or (2,2,1) or (1,1,1). But maybe simpler: answer is 3 iff feasible, and feasibility ⇔ ∃ triple of one of those forms. Also note (1,1,1) might be subsumed: if three intervals cover [1,N], then... could also be done as (2,1,1)? Not necessarily.

Let me reconsider: maybe there's a cleaner unified condition. Think of it as: we need to cover [1,N]. Consider using at most one op2? Patterns with one op2: (2,1,1) and (2,1) [K=2] and (2,1,1) generalizes (2,1). Patterns with two op2: (2,2,1), (2,2). With zero op2: (1,1,1),(1,1),(1). With three op2: reduces to (2,2).

So algorithm:
1. K=1 check: ∃i: Li=1 & Ri=N → output that op as 1.
2. K=2 checks (i≠j):
   a. (1,1): ∃i,j: Li=1, Rj=N, Ri ≥ Lj-1.
   b. (1,2): ∃i≠j: Li ≤ Lj, Ri ≥ Rj.
   c. (2,2): ∃i,j: Ri < Lj.
3. K=3 checks (distinct indices):
   a. (1,1,1): ∃i,j,k: Li=1, Rk=N, Ri ≥ Lj-1, Rj ≥ Lk-1.
   b. (2,1,1): ∃i,j,k: Li ≤ Lk (op2 on k... wait let me re-set: op2 on m, intervals i,j cover [Lm,Rm]: Li ≤ Lm, Rj ≥ Rm, Ri ≥ Lj-1.
   c. (2,2,1): ∃i,j,k: Lk ≤ max(Li,Lj), Rk ≥ min(Ri,Rj) (with max(Li,Lj) ≤ min(Ri,Rj), else K=2 case c applies).

Hmm, this is getting complex with distinctness constraints. Let me think about whether distinctness matters: if i=j in (1,2) check (Li≤Lj, Ri≥Rj always true for i=j), we'd falsely report K=2 when actually K=1 fails. So yes distinctness matters. But note: if (1,2) with i=j were the only solution, then [Li,Ri] ⊇ [Li,Ri] means op1+op2 on same op — not allowed. However, if Li≤Lj and Ri≥Rj for i=j only, that means no other interval contains j's. Handle by tracking top-2.

Simplification idea: For (1,2): sort intervals; for each j, query max R among intervals with L ≤ Lj, excluding j itself. If we process in order of L and maintain max R with the index, exclusion only matters when the max comes from j itself — keep top two (value,index) pairs.

For (2,1,1): for each m, need intervals i,j (≠m, and i≠j) with Li ≤ Lm, Rj ≥ Rm, Ri ≥ Lj-1. Hmm, 3 distinct indices. This is getting heavy. Alternative: think of it as: define A = set of intervals. We need two intervals whose union covers [Lm, Rm]. For two intervals to cover target [a,b]: one must have L ≤ a (call left-cover), one must have R ≥ b (right-cover), and they must connect: R_left ≥ L_right - 1. Note the same interval could serve both roles if it contains [a,b] — but then that's K=2 case (1,2). So for K=3 we can assume i≠j, and also i,j ≠ m. But wait: could i = m? Op2 on m and op1 on m — no, same operation index can't do both. So distinct.

Hmm, but here's a thought: if i=m satisfied Li ≤ Lm and Ri ≥ Lj-1 etc., would using a different interval work? Not necessarily. So we do need distinctness. This makes implementation tricky but doable with care: for pattern (2,1,1), iterate over m; we need:
- best "left interval" i≠m with Li ≤ Lm maximizing Ri.
- best "right interval" j≠m with Rj ≥ Rm minimizing Lj.
- check Ri ≥ Lj - 1, and i≠j (if i=j then that single interval covers [Lm,Rm] → that's actually K=2 pattern (1,2) with m... wait (1,2): op1 on i, op2 on m, need [Lm,Rm]⊆[Li,Ri]. If i=j covers [Lm,Rm] alone, then K=2 works and we'd have already found it. So in K=3 branch, if best-left and best-right are the same index, we need second-best on one side. Ugh.

Alternative cleaner approach: since answer ≤ 3, maybe directly search for the constructive triple with sweeps. Or: think about it differently.

Alternative viewpoint (I recall the editorial trick for this problem — it's AtCoder ABC 241 F? No. It's "Ex - Directed Substring"? No. Let me just derive). Actually I believe this is AtCoder Grand Contest? The problem "x_i all 1, operations interval/complement" — this is AtCoder ABC 197? Hmm, I recall a similar problem: "Snuke's Coloring 2"? Not it. Could be from AIZU or a recent ABC Ex. Regardless, derive from scratch.

Cleaner formulation: We need every point p∈[1,N] covered. Consider the leftmost uncovered structure... Let me think about what makes it infeasible. Sample 4: [1,3],[2,4], N=5. Position 5: covered only by op2 of an interval not containing 5, i.e., op2 of [1,3] (5∉[1,3]) or op2 of [2,4]. Position 1: covered by op1 of [1,3] or op2 of [2,4]. Suppose we use op2 of [2,4] (covers 1 and 5) — then need cover [2,4] with op1s: only [1,3] and [2,4] available; [1,3]∪[2,4]=[1,4] ⊉ [2,4]? It does cover [2,4]! Wait: [1,3]∪[2,4] ⊇ [2,4] yes since [2,4] itself is one of the intervals. But op1 on [2,4] and op2 on [2,4] is the same operation — can't. op1 on [1,3] covers [1,3], missing 4. So with op2 of [2,4] + op1 of [1,3]: covered = {1,5} ∪ [1,3] = {1,2,3,5}, 4 uncovered. op2 of [1,3] covers {4,5}; need [1,3] covered: op1 [1,3] conflicts (same op), op1 [2,4] misses 1. So {4,5}∪[2,4]={2,4,5}, missing 1,3? [2,4] covers 2,3,4. So {2,3,4,5}, missing 1. Three ops: op2[1,3] + op1[2,4] + ? : covered {4,5}∪{2,3,4} = {2,3,4,5}, need 1: op1 [1,3] — that's 3 ops total: op2 on op1-index... indices: op A=[1,3], op B=[2,4]. op2 on A, op1 on B, op1 on A — conflict, A used twice. So infeasible. ✓ matches -1.

So feasibility genuinely requires distinct indices and the checks above. Now, is "feasible ⇒ feasible with ≤3" true? Suppose feasible with some set S of operations. Take any op2 in S with interval [a,b] (covers rays). Positions in [a,b] must be covered by other ops. Hmm, induction: I believe the known result is answer ≤ 3. Let me just trust patterns: any solution can be reduced to ≤3 ops? Consider a solution using only op1s: intervals covering [1,N]. Then there's a chain from 1 to N; a minimal chain has the property that each interval is needed... minimal cover of [1,N] by intervals: sort by L; greedy gives a chain where each consecutive pair overlaps; can a minimal chain need 4+ intervals? Minimal means removing any breaks coverage. E.g., [1,2],[2,3],[3,4],[4,5] covering [1,5]: remove [2,3]: [1,2]∪[3,4]∪[4,5] misses nothing? [1,2],[3,4],[4,5] covers 1,2,3,4,5 — yes covers! So not minimal. In general, covering a line with intervals, minimal cover has ≤ ... hmm, [1,2],[2,100],[2,3],[3,4]? Minimal covers can be reduced: in any cover of [1,N] by intervals, there's a subcover of size ≤ 2? No: [1,2],[2,3],[3,5] covering [1,5]: size 3, no 2-subcover ([1,2]∪[3,5] misses... misses nothing between? misses (2,3) gap? [1,2]∪[3,5]: point 2 covered, 3 covered, but 2.5 not an integer — positions are integers! Integer positions: [1,2]∪[3,5] covers all integers 1..5. Oh wait — gap condition: integer positions, so intervals [1,2] and [3,5] touch (2 and 3 adjacent). So covering [1,N] (integers) with intervals: need chain where consecutive satisfy r ≥ l' - 1. Minimal chain: can we always find ≤2? [1,2],[3,4],[4,5]? [1,2]∪[4,5] misses 3. [1,2],[3,5]? not available. So need 3: [1,2],[3,4],[4,5] — check pairs: [1,2]+[3,4] misses 5; [1,2]+[4,5] misses 3; [3,4]+[4,5] misses 1,2. So (1,1,1) with 3 genuinely needed. Can 4 be needed? [1,2],[3,4],[5,6],[6,7] covering [1,7]: [1,2],[3,4]... [3,4] and [5,6]: 4 and 5 adjacent ok. So [1,2],[3,4],[5,6],[6,7]: is there a 3-subcover? [1,2],[3,4],[6,7] misses 5. [1,2],[5,6],[6,7] misses 3,4. No 3-subcover works! But wait — is this instance feasible with op2s? Only op1s available say. Then answer would be 4, contradicting "≤3". Hmm! But hold on — with only op1 allowed... the problem allows op2 for every operation too. op2 of [3,4] covers [1,2]∪[5,7]. Then op2[3,4] + op1[3,4]? conflict. op2 of [5,6] covers [1,4]∪{7}: combined with op1 [5,6]: conflict. op2[3,4] + op1[5,6] + op1[6,7]? covered: {1,2,5,6,7}∪{5,6}∪{6,7} = {1,2,5,6,7}, misses 3,4. Hmm. op2[5,6] covers {1,2,3,4,7}; + op1[1,2] conflict-free? op1[1,2] adds nothing new; need 5,6: op1[5,6] conflict, op1[3,4] no, op1[6,7] covers 6. So {1,2,3,4,7}+{6} = misses 5. Hmm. op2[3,4] + op2[5,6]: {1,2,5,6,7} ∪ {1,2,3,4,7} = everything! K=2. OK bad example.

Let me think again: is it always ≤3? Suppose all-op1 solution needs ≥4 intervals minimally: [1,2],[3,4],[5,6],[7,8] covering [1,8]. Then op2 of [3,4] covers {1,2,5,6,7,8}; need [3,4]: op1 of [5,6]? no. Hmm op1 [3,4] conflict. So op2[3,4]+op1[?]: nothing covers 3,4 except op1[3,4]. Try op2[5,6]: covers {1,2,3,4,7,8}; need 5,6: op1[5,6] conflict; others no. So this instance: op1s: [1,2],[3,4],[5,6],[7,8], N=8. Feasible? Any op2 leaves its hole uncovered-able only by other op1s that cover the hole. Hole [3,4]: only interval covering 3..4 is [3,4] itself. So op2[3,4] unusable. Similarly each op2 unusable. So must use op1s only: need all 4. Answer 4?! That contradicts my assumption. Let me double check coverage with all 4 op1s: [1,2]∪[3,4]∪[5,6]∪[7,8] = [1,8] ✓. Can 3 ops work? Any op2 has hole containing some position coverable only by... position 3 is covered only by op1[3,4] or op2 of intervals not containing 3: op2[1,2] (3∉[1,2] ✓), op2[5,6], op2[7,8]. Let me retry: op2[1,2] covers [3,8]. Then need 1,2: op1[1,2] conflict; op2[3,4] covers {1,2,5,6,7,8}: so op2[1,2]+op2[3,4] = [3,8]∪{1,2,5,6,7,8} = misses? 3,4 covered by first, 1,2 by second, 5-8 by both. = [1,8]! K=2!! Ugh, right: two complements: holes [1,2]∩[3,4]=∅ ⇒ covers everything. Of course.

OK so complements are powerful. Let me reconsider whether ≤3 always holds. Try to construct a hard instance: intervals arranged so that every op2's hole can only be filled by conflicting ops, and op1-chains are long. Intervals: [1,2],[3,4],[5,6],[7,8],... op2[1,2]+op2[5,6]: holes [1,2]∩[5,6]=∅ ⇒ full cover. Any two disjoint intervals give K=2 via (2,2). So to force long chains, need all intervals pairwise intersecting (nested-ish), but then (1,2) likely applies... If all intervals share common point c, then op2 of any covers rays; hole contains c. To cover hole [a,b]∋c need op1s covering [a,b]. Hmm: intervals all containing c, e.g., c=5, N=9: [1,5],[5,9],[4,6],[3,7]... (1,2): [3,7]⊆? need Li≤3,Ri≥7: none maybe. (2,2): disjoint pair? all contain 5, no. (1,1): L=1 and R=9: [1,5] has L=1, [5,9] has R=9, touch? 5≥5-1 ✓ ⇒ K=2. To avoid, no interval with L=1 touching one with R=N... Let me try: N=10, intervals: [2,5],[6,9],[4,7]. (1,1): no L=1, no R=10. (2,2): disjoint? [2,5]&[6,9]: 5<6 disjoint! ⇒ K=2. Argh.

To prevent (2,2), all pairs intersect ⇒ common point (Helly) ⇒ let c be common point. To prevent (1,2), no interval contains another. To prevent (1,1), no L=1 interval reaches (adjacently) an R=N interval. Now K=3: (2,2,1): two complements + one interval covering intersection of holes. Take two holes [a1,b1],[a2,b2] both containing c; intersection [max a, min b] ∋ c; need an interval ⊇ [max(a1,a2), min(b1,b2)]. Pick the two holes to minimize intersection: the hole with max L and the hole with max R... intersection = [max_i L_i (over two), min_i R_i]. Choose hole1 = interval with largest L (Lmax), hole2 = interval with largest R (Rmax). Intersection = [Lmax, Rmax'] where Rmax' = min(R_of_Lmax, R_of_LmaxR)... hmm getting complicated. Since all intervals contain c: Lmax ≤ c ≤ ... intersection of hole1,hole2 = [max(L1,L2), min(R1,R2)] ∋ c, nonempty. Need third interval ⊇ this. Is there always one? The interval achieving Lmax: call I1=[Lmax, R1]. The interval achieving overall min R? Since no nesting... Consider I1 (max L) and I2 (max R). If I1≠I2: intersection [Lmax, min(R1,R2)]. Any interval containing [Lmax, min(R1,R2)]? Not necessarily. Example: intervals [1,5],[4,9],[5,6]? contains: [5,6]⊆[4,9]? 4≤5,9≥6 yes ⇒ (1,2). Avoid nesting: [1,6],[4,9],[5,7]? [5,7]⊆[4,9] yes. Hmm hard to avoid nesting with all containing c. Three intervals all containing c, no nesting: L's distinct, R's distinct, and L increasing ⇒ R increasing (else nesting). So intervals like [1,5],[3,7],[6,9] — but [1,5]∩[6,9]=∅ ⇒ (2,2). With all containing c, sorted by L, R also sorted (no nesting). I1 = max L = [6?,...] e.g. c=5: [1,5],[2,6],[4,8],[5,9]: check nesting: [1,5]⊆? no. [2,6]⊆[1,?] no. ok no nesting? [4,8] vs [5,9]: fine. (2,2): all contain 5 ⇒ intersect. (1,1): L=1: [1,5]; R=9: [5,9]; 5≥5-1 ✓ K=2. To avoid (1,1): no interval with L=1 OR no interval with R=N OR they don't touch. Say no L=1 and no R=N: [2,5],[3,6],[4,7],[5,8] with N=10. But then position 1: covered only by op2 of intervals not containing 1 — any of them (1∉all). Position 10 similarly. Position 1 and 10: op2 of any single interval covers both 1 and 10 (since 1,10∉[a,b] for all). Then need cover [a,b] with op1s: [2,5] hole: cover with [3,6]? no, misses 2. Hmm: op2[2,5] + op1s covering [2,5]: available [3,6],[4,7],[5,8]: none covers 2. So that fails. op2[5,8]: need [5,8]: [4,7] covers 4-7, [3,6] 3-6, [2,5] 2-5: [4,7]+[2,5]: 4≤5+1 touch? [2,5]∪[4,7]=[2,7] ⊇[5,8]? misses 8. [4,7]+[3,6]: [3,7] misses 8. So need 8: only [5,8] (conflict) — fail. So with these 4 intervals, is it feasible at all?? Positions 1,9,10: only via op2s. Position 1: any op2. Position 9: op2 of interval not containing 9: all of them (max R=8). OK. Let's try op2[2,5] (covers {1}∪[6,10]) + need [2,5]: impossible as shown. op2[3,6]: covers {1,2}∪[7,10]; need [3,6]: [2,5]∪[4,7]=[2,7]⊇[3,6] ✓!! So op2 on [3,6], op1 on [2,5], op1 on [4,7]: covered = {1,2,7,8,9,10} ∪ [2,5] ∪ [4,7] = [1,10] ✓ K=3, pattern (2,1,1). 

So the conjecture "feasible ⇒ ≤3" survives. Indeed intuitively: take any feasible solution. If it uses an op2 with hole [a,b], positions outside [a,b] are done; positions inside need covering by other ops, and any cover of [a,b] by intervals+complements... a complement within [a,b] covers [a,b] minus its hole — recursion. Plausibly minimal solutions are ≤3. I'll trust the known result (this is AtCoder ABC 233? "Ex - ..."? I genuinely recall an AtCoder problem with answer in {1,2,3,-1} and interval/complement operations — yes! It's ABC 197? No — it's "HHKB 2020"? Whatever — I'm fairly confident this is AtCoder ABC 233 Ex or typical where editorial says answer ≤ 3).

Hmm wait, actually I should double-check the (1,1,1) necessity: can (1,1,1) situations always be replaced by (2,·,·)? Earlier example: intervals [1,2],[3,4],[4,5] N=5 — but (2,2): [1,2]∩[4,5]=∅ ⇒ K=2. To force pure (1,1,1): need all intervals pairwise intersecting (common point c), no nesting, no L=1..R=N touching pair, and (2,1,1),(2,2,1) fail. All contain c. (2,1,1): op2 on [a,b], cover [a,b] with two other intervals. (2,2,1): cover [max L, min R] of two holes with one interval. Since all intervals contain c and no nesting, sorted by L = sorted by R. Take holes = two extreme intervals: [L1,R1] (min L) and [Lk,Rk] (max L & max R): intersection = [Lk, R1] (if Lk ≤ R1). Need interval ⊇ [Lk,R1]: any interval with L ≤ Lk and R ≥ R1 — the extremes themselves... a middle interval [Lm,Rm] has L1<Lm<Lk and R1<Rm<Rk, so Lm ≤ Lk? No, Lm < Lk, so Lm ≤ Lk ✓ and Rm ≥ R1 ✓! So [Lm,Rm] ⊇ [Lk, R1] iff Lm ≤ Lk and Rm ≥ R1 — yes since Lm < Lk and Rm > R1. Wait need Lm ≤ Lk: Lm < Lk ✓. Rm ≥ R1 ✓. So (2,2,1) works with holes = extreme intervals and middle interval — as long as there are ≥3 distinct intervals and intersection [Lk,R1] nonempty (Lk ≤ R1). If Lk > R1, holes disjoint ⇒ (2,2) K=2. So with ≥3 intervals all sharing common point, no nesting: is (2,2,1) always available?? Need middle interval distinct from the two extremes — yes if ≥3 intervals. But wait, also need the middle interval's index distinct — yes.

Hold on, that suggests (1,1,1) is NEVER needed when (2,2,1) possible... but (2,2,1) needs the two extreme holes + a middle interval ⊇ intersection. With all intervals containing common point c and no nesting and ≥3 intervals, works. With nesting, (1,2) gives K=2. With disjoint pair, (2,2) gives K=2. So when is (1,1,1) the only option?? Maybe never! Interesting. But careful: "no nesting" — if interval A ⊇ B (A contains B), then (1,2) with op1=A, op2=B gives K=2. Right. So for K≥3 situations: all pairs intersect (common point c by Helly), no containments. Then (2,2,1) works as argued IF there are ≥3 intervals with distinct extremes... What if M=2? Then K≤2 checks cover it. What if all intervals identical? Then containment ⇒ (1,2)? i≠j with Li≤Lj, Ri≥Rj: identical intervals i≠j satisfy ⇒ K=2 (op1 on one, op2 on other: covers [a,b] ∪ complement = everything). ✓.

But wait, the (2,2,1) argument: holes are [L1,R1] and [Lk,Rk] where these are min-L and max-L intervals; but I need max(L1,Lk)=Lk ≤ min(R1,Rk)=R1, i.e., Lk ≤ R1. Since common point c: Lk ≤ c ≤ R1 ✓. Middle interval [Lm,Rm] with L1 < Lm < Lk (exists if ≥3 distinct-L intervals) and R1 < Rm < Rk (no nesting ⇒ same order). Then Lm ≤ Lk ✓, Rm ≥ R1 ✓. So covered. But what if there are only 2 distinct intervals but M≥2... then K=2 via (1,2) if nested/identical, or (2,2) if disjoint, or they intersect without containment: [1,3],[2,5]: (1,1)? L=1: [1,3], R=5=N? if N=5: 3≥2-1 ✓ K=2. If N>5, position N uncovered by op1s; op2s: [1,3] op2 covers 4..N; [2,5] op2 covers {1}∪[6,N]. Both op2: holes intersect [2,3] nonempty ⇒ miss 2,3. op1+op2: (1,2) needs containment — none. So K=2 fails, K=3 needs 3 distinct ops but M=2 ⇒ -1. E.g., N=6, [1,3],[2,5]: position 6: op2[1,3] or op2[2,5]. position 1: op1[1,3] or op2[2,5]. Try op2[2,5] ({1,6}) + op1[1,3] ([1,3]): covered {1,2,3,6}, miss 4,5. op2[1,3] ({4,5,6}) + op1[2,5] ([2,5]): {2,3,4,5,6} miss 1. Both op1: [1,5] miss 6. Both op2: miss 2,3. So -1 ✓ (M=2, can't do 3). Good — so M≥3 needed for K=3, plus distinctness.

So refined understanding:
- K=3 patterns needed: (2,1,1), (2,2,1), (1,1,1)? — from the analysis, (1,1,1) might be subsumed by other patterns when M≥3... but not obviously in all cases (e.g., intervals NOT all sharing a common point but no disjoint pair — impossible by Helly: pairwise intersecting intervals ⇒ common point. But (1,1,1) scenario doesn't require pairwise intersection of ALL intervals, just that no disjoint pair exists... which is pairwise intersection ⇒ Helly ⇒ common point. Hmm but K=2 (2,2) failing means no disjoint pair ⇒ all pairs intersect ⇒ common point c. Then as shown, if no containment (else (1,2)) and ≥3 intervals with distinct... wait need an interval with L strictly between... What if there are intervals but only 2 distinct "extreme" ones and everything else identical to them? Identical ⇒ containment ⇒ (1,2). So fine.

But actually, hmm, (2,2,1) requires a third interval containing [Lk, R1]. I showed a middle interval (by L-order) works. But what if M≥3 but the third interval is, e.g., not containing the intersection? With common point c and no nesting, sorted by L ⇔ sorted by R, any middle one contains [Lk,R1]? Middle interval [Lm,Rm]: Lm ≤ Lk ✓ (Lm<Lk), Rm ≥ R1 ✓ (Rm>R1). Yes contains [Lk,R1]. ✓. So whenever K=2 fails and there are ≥3 intervals (M≥3), (2,2,1) works?! Wait, K=2 failing requires: no [1,N] interval (K=1), no (1,1) chain, no (1,2) containment, no (2,2) disjoint pair. Then all intervals pairwise intersect, common point c, no containment. If M≥3, pick extremes by L and a middle ⇒ (2,2,1) works. But hold on — what about (1,1) failing: that's automatically fine, we don't need it.

Wait, but that would mean the answer is: 1 if ∃[1,N]; else 2 if any of the three K=2 patterns; else 3 if M≥3; else -1. Let me sanity check against sample 4: N=5, [1,3],[2,4], M=2. K=1: no. K=2: (1,1): L=1→[1,3], R=5? none (max R=4≠5). Fail. (1,2): containment? [1,3]⊇[2,4]? 3<4 no. [2,4]⊇[1,3]? no. Fail. (2,2): disjoint? [1,3]∩[2,4]=[2,3]≠∅. Fail. M=2 <3 ⇒ -1 ✓.

Sample 3: N=5, [1,3],[2,5]. K=1: no. (1,1): L=1: [1,3]; R=5: [2,5]; need Ri ≥ Lj-1: 3 ≥ 2-1 ✓ ⇒ K=2, op1 on both. Output "1 1" ✓ matches.

Sample 2: [1,3],[1,5],[2,4],[3,5]. K=1: [1,5] exists ⇒ op1 on op2. Output "0 1 0 0" ✓.

Sample 1: [2,4],[3,5],[1,4],[2,5]. K=1: none. (1,1): L=1: [1,4] (R=4); R=5: [3,5](L=3),[2,5](L=2). Need 4 ≥ L-1: L=3: 4≥2 ✓ ⇒ K=2 with op1 on [1,4] and op1 on [3,5]! But sample output uses K=2 with ops 2 and 1 (op2 on [2,4], op1 on [1,4]): also valid. Our answer: op1 on op3 ([1,4]) and op1 on op2 ([3,5]): covered [1,4]∪[3,5]=[1,5] ✓ K=2. Valid output: "2 / 0 1 1 0". ✓ (any min solution accepted).

Now test my "M≥3 ⇒ 3" claim on a potential counterexample. N=5, intervals: [1,2],[2,3],[4,5]? (2,2): [1,2]∩[4,5]=∅ ⇒ K=2. OK. Need all pairs intersecting: [1,3],[2,4],[3,5] (N=5): common point 3. (1,2): containment? no. (1,1): L=1:[1,3] R=3; R=5:[3,5] L=3; 3≥3-1 ✓ ⇒ K=2! Hmm. Adjust: [1,3],[2,4],[3,5] — to kill (1,1), need R of L=1 interval < L of R=N interval - 1: [1,2]?, but then [1,2]∩[3,5]=∅. Tricky: common point c forces every interval to contain c, so L=1 interval is [1,≥c], R=N interval is [≤c,N]: they touch at c ⇒ (1,1) always succeeds if both extremes exist! So to fail (1,1): no interval with L=1, or none with R=N. Say no L=1: N=6, [2,4],[3,5],[4,6]: common point 4. (1,1): no L=1 ⇒ fail. (1,2): no containment. (2,2): all intersect. K=3 predicted. (2,2,1): extremes: min L: [2,4], max L: [4,6]; intersection of holes = [4,4]; middle [3,5] ⊇ [4,4] ✓. So op2 on [2,4] (covers {1,5,6}), op2 on [4,6] (covers {1,2,3}), op1 on [3,5] ([3,5]): union: 1,2,3 from second; 5,6 first; 4 from third; 3,5 third ⇒ [1,6] ✓ K=3.

Great, so the characterization seems to be:
- ans=1 iff ∃i: [Li,Ri]=[1,N].
- ans=2 iff (not ans 1) and (∃ i≠j with one of: (a) Li=1? wait (1,1) pattern: ∃i,j (distinct) with min... let me define: (a) ∃i≠j: [Li,Ri]∪[Lj,Rj]=[1,N] i.e. min(Li,Lj)=1, max(Ri,Rj)=N, and overlap: if Li≤Lj then Ri≥Lj-1. (b) ∃i≠j: [Li,Ri]⊇[Lj,Rj]. (c) ∃i≠j: [Li,Ri]∩[Lj,Rj]=∅.)
- ans=3 iff (not ans≤2) and M≥3.
- else -1.

Wait, but I should double check the claim "K=2 fails & M≥3 ⇒ K=3 works" more rigorously, especially the distinctness in (2,2,1): holes I1 (min L), I2 (max L), middle I3 — need I3 distinct from I1,I2 and containing [L_{I2}, R_{I1}]. Existence of I3: need an interval with L strictly between L_{I1} and L_{I2}? What if M≥3 but all intervals have only 2 distinct L values, e.g., two copies of [2,4] and one [4,6]? Two copies of [2,4]: containment (equal) ⇒ (1,2) K=2. So duplicates ⇒ K=2. What if intervals are [2,4],[3,4],[4,6]? [3,4]⊆[2,4] ⇒ (1,2). Hmm: common point 4; no nesting ⇒ sorted by L strictly ⇒ sorted by R strictly. With M≥3 and no two nested (in particular no equal L? equal L with different R ⇒ nesting. Equal L equal R ⇒ nesting) ⇒ all L distinct, all R distinct, same order. So with M≥3, pick I1 = min L, I2 = max L, I3 = any other: L_{I1} < L_{I3} < L_{I2}, R_{I1} < R_{I3} < R_{I2}. Then I3 ⊇ [L_{I2}, R_{I1}] since L_{I3} < L_{I2} and R_{I3} > R_{I1}. And [L_{I2}, R_{I1}] nonempty since L_{I2} ≤ c ≤ R_{I1}. ✓✓. Also need I3 ≠ I1, I2 ✓ (M≥3).

But wait — also need to double-check that "no disjoint pair ⇒ common point" (Helly for intervals: pairwise intersecting family of intervals has total intersection nonempty ✓ standard). And pairwise intersection failing = ∃ disjoint pair = (2,2) success. ✓.

Also: what if M≥3 but N... any edge cases? N=1: then any interval is [1,1]=[1,N] ⇒ K=1. Fine.

Hmm, one more subtlety: K=2 pattern (a) (1,1) with i=j? [Li,Ri]∪[Li,Ri]=[1,N] ⇒ [1,N] ⇒ K=1 already. So requiring distinct is fine but if K=1 failed, (1,1) with i=j impossible anyway. For (b) i=j: always true ⇒ must require i≠j strictly. For (c) i=j: intersection nonempty always ⇒ fine. So only (b) needs distinctness care. Actually also (a): if K=1 check done first, no issue, but let's just require distinct everywhere for safety. For (a): i≠j automatically since one has L=1,R<N (K=1 failed ⇒ L=1 interval has R<N) and other has R=N,L>1. Actually L=1 interval could also have R=N — excluded by K=1 check. So distinctness automatic for (a) and (c). For (b), need i≠j: ∃ pair i≠j with Li≤Lj and Ri≥Rj.

Now K=3 construction: find I1 = argmin L (any tie-break), I2 = argmax L, I3 = any index ≠ I1,I2. Wait — need I3 with L strictly between? I argued no-nesting ⇒ all L distinct. But ties in L with equal intervals ⇒ nesting ⇒ K=2. Since we're in K=3 branch, K=2 failed ⇒ no nesting ⇒ all L distinct? Careful: no nesting means no pair with Li≤Lj & Ri≥Rj (i≠j). If Li=Lj and Ri<Rj, that's nesting (j contains i) ⇒ excluded. So all L distinct ✓, and then order by L = order by R (if Li<Lj but Ri>Rj, nesting) ✓. So I1=argmin L, I2=argmax L, any I3≠I1,I2 works (L_{I3} strictly between). Then output: op2 on I1, op2 on I2, op1 on I3. Let me verify coverage: op2 on I1 covers complement of [L1,R1]; op2 on I2 covers complement of [L2,R2]; union of these two = complement of [L1,R1]∩[L2,R2] = complement of [L2, R1] (since L1<L2≤c≤R1<R2, intersection = [L2,R1]). op1 on I3 covers [L3,R3] ⊇ [L2,R1] ✓. Total = everything ✓. 

So the algorithm is remarkably simple:
1. Read N, M, intervals.
2. If ∃i: Li=1 and Ri=N → K=1, output op_i=1.
3. Else check K=2:
   a. (1,1): Let bestR = max Ri over Li=1; bestL = min Li over Ri=N. If bestR ≥ bestL - 1 → K=2. (Need the actual indices: i* = argmax among L=1 of R; j* = argmin among R=N of L; they're distinct as argued.) Output op1 on both.
   b. (1,2): ∃i≠j: Li≤Lj, Ri≥Rj. Equivalent: sort; for each j, max R over i with Li≤Lj; if max achieved by i≠j or second-best works. Simple approach: sort indices by L; sweep; maintain top-2 (R, idx). For each j in order of increasing L... careful: need Li ≤ Lj, so process j and all i with Li ≤ Lj. If we iterate j in sorted order and add i as we go, i and j both from prefix — need to ensure i≠j: when querying for j, j itself may already be in the structure (if we add before query). Add all with Li ≤ Lj including j, query max R; if max R ≥ Rj and argmax ≠ j → found; if argmax == j, check second max ≥ Rj → found. Alternatively: for each j, query structure containing only items with Li ≤ Lj, excluding j — process in order, query before inserting j? But then i with Li = Lj and appearing later in sort order missed — but we query max R ≥ Rj with Li ≤ Lj; if the only containing interval has same L and comes later... we'd miss it when processing j, but when processing that later interval j', j is in structure and if Rj ≥ Rj'... not necessarily. Hmm: containment is symmetric-ish: [a,b]⊇[c,d] with a≤c. If a<c: process in L order, when j=[c,d] queried, i=[a,b] already inserted (a<c ⇒ earlier) ✓ found. If a=c (equal L): then b≥d; i=[a,b] is the container. When processing j=[c,d] (if d<b), need i inserted: tie order by R descending ⇒ i before j ✓. So: sort by (L asc, R desc), sweep inserting into max-structure, but query for j must include items with same L inserted before j — with R desc tie-break, container comes first ✓. And query before inserting j itself? If we query the structure (items before j in sorted order) for max R ≥ Rj: items before j have Li ≤ Lj (and if equal, Ri ≥ Rj by tie-break). max R ≥ Rj ⇔ container exists (i≠j since j not yet inserted) ✓. So: sort by (L asc, R desc); running max of R; for each j in order: if running_max_R ≥ Rj → found pair (argmax index, j). Then update running max with Rj. Wait but running max includes items with L ≤ Lj only if sorted ✓. But careful: running max over all previous = max R among Li ≤ Lj (with tie handling) ✓. This finds container with smallest... any container ✓. O(M log M).
   
   Alternatively even simpler: compute for each j whether ∃i≠j with Li≤Lj, Ri≥Rj via the sweep above. Fine.
   
   c. (2,2): min R < max L → K=2: i* = argmin R, j* = argmax L (distinct since Ri* < Lj*). Output op2 on both.
4. Else if M≥3 → K=3: I1=argmin L (tie-break any, but to be safe pick... since no nesting, L distinct, any tie-break fine — but ties shouldn't happen; still, pick lowest index), I2=argmax L, I3=any index not I1 or I2. Output op2 on I1, op2 on I2, op1 on I3.
   Wait — must double check the tie case doesn't break: if K=2 checks all failed, can there be equal L? Equal L, different R ⇒ nesting ⇒ (1,2) would have succeeded. Equal L equal R (i≠j) ⇒ (1,2) succeeds (Li≤Lj, Ri≥Rj). So in K=3 branch, all L distinct, all good. But defensively, if somehow I3 doesn't cover, answer would be wrong. Also need M≥3 for I3 to exist.
5. Else → -1.

Hold on, wait. I need to double-check step 4's claim once more: "K=2 fails ⇒ all pairs intersect". K=2 fail includes (c) fail: no disjoint pair ✓ ⇒ pairwise intersecting ⇒ common intersection point c (Helly). Every interval contains c. Also (b) fail ⇒ no containment ⇒ L order = R order, strict. I1 = min L, I2 = max L. Common intersection [max L, min R] = [L_{I2}, R_{I1}] ∋ c, nonempty ✓. I3 any other: L_{I1} < L_{I3} < L_{I2} and R_{I1} < R_{I3} < R_{I2} ⇒ [L3,R3] ⊇ [L2,R1] ✓. Output ops: op2(I1), op2(I2), op1(I3). Coverage: comp([L1,R1]) ∪ comp([L2,R2]) ∪ [L3,R3] = comp([L2,R1]) ∪ [L3,R3] = everything since [L3,R3] ⊇ [L2,R1] ✓✓.

Hmm wait, but is it possible that K=2 fails, M≥3, but the answer is actually still impossible because... no, we just constructed a valid K=3. And minimality: K=1,2 checked failed ⇒ 3 is min ✓. And if M≤2 and K≤2 fail ⇒ -1 ✓ (can't do 3 ops with 2 operations... well, K counts non-zero ops; with M=2 we can do at most 2 non-zero ⇒ infeasible ✓).

Edge: M≥3 but maybe K=3 construction picks I1=I2? Only if M=1. M≥3 ⇒ distinct indices exist; argmin L ≠ argmax L since all L distinct (M≥2 distinct values). ✓.

Let me also double check (1,1) condition precisely: need i,j with Li=1? No wait — union [Li,Ri]∪[Lj,Rj] = [1,N] requires min L = 1 and max R = N and no gap. WLOG Li ≤ Lj: need Li=1, Rj=N, Ri ≥ Lj-1. So: i* = interval with Li=1 maximizing Ri; j* = interval with Rj=N minimizing Lj. Condition: Ri* ≥ Lj* - 1. If both exist and condition holds → K=2. Distinct: i* has R<N (else K=1), j* has L>1 (else K=1) ⇒ distinct ✓.

(2,2): i* = argmin R, j* = argmax L; condition Ri* < Lj* ✓ distinct automatically.

(1,2): sweep as described.

Now complexity: O(M log M) fine.

Let me now also verify with sample 1 that we don't accidentally output K=3: K=2 (1,1) check: L=1 intervals: [1,4] R=4. R=5 intervals: [3,5] L=3, [2,5] L=2 → min L = 2. Condition: 4 ≥ 2-1 ✓ → K=2: op1 on [1,4] (index 3), op1 on [2,5] (index 4). Output: ops: [0,0,1,1], K=2. Verify: op1[1,4] → 1,2,3,4; op1[2,5] → 2,3,4,5; union all ✓. 

Another test: N=1, M=1, [1,1]: K=1 → output "1\n1". ✓.

Test: N=3, M=2, [1,1],[3,3]: K=1 no. (1,1): L=1: R=1; R=3(=N): L=3; 1 ≥ 3-1=2? No. (1,2): containment no. (2,2): minR=1 < maxL=3 ✓ → K=2: op2 on [1,1] (covers 2,3), op2 on [3,3] (covers 1,2): union {1,2,3} ✓.

Test K=3 example: N=6, M=3, [2,4],[3,5],[4,6]: K=1 no. (1,1): no L=1 ⇒ no. (1,2): containment? [2,4]⊇? no; [3,5]⊇[4,6]? no; etc. No. (2,2): minR=4, maxL=4; 4<4? No ⇒ fail. M=3 ⇒ K=3: I1=argminL=[2,4] (idx1), I2=argmaxL=[4,6] (idx3), I3=idx2=[3,5]. Ops: op2 on 1: covers {1,5,6}; op2 on 3: covers {1,2,3}; op1 on 2: {3,4,5}. Union: 1,2,3,4,5,6 ✓. K=3.

Test -1: N=5, M=2, [1,3],[2,4] → as computed, -1 ✓.

Test -1 with M≥3? Claim: impossible. M≥3 & K≤2 fail ⇒ K=3 works. So -1 only when M≤2 (and checks fail). Interesting. Actually also M could be ≥3 but... no, construction always valid. Wait, one more constraint check: I3 must be ≠ I1, I2 — M≥3 guarantees some index exists ✓.

Hmm, but wait: what if M≥3, K=2 fails, but there are duplicate intervals? Duplicates ⇒ (1,2) succeeds ⇒ K=2, contradiction. So fine.

Now, the (1,2) sweep: sort indices by (L asc, R desc). Iterate, maintain (maxR, argmax) over previously seen. For current j: if maxR ≥ Rj → pair (argmax, j) found. Then update max with Rj. Note: this checks containers with L ≤ Lj strictly-before-in-order; equal L handled by R desc order (container first). But what about container with equal L and equal R? That's a duplicate; container = duplicate: [a,b] ⊇ [a,b], i≠j: sorted adjacently, first one is "container" for second: maxR ≥ Rj ✓ found ✓.

But careful: container with L < Lj but appearing... all L < Lj come before in sort ✓. Container with L = Lj needs R ≥ Rj ⇒ comes before due to R desc ✓. 

Also (1,2) could also be checked more simply: for each j, exists i≠j with Li ≤ Lj and Ri ≥ Rj. The sweep finds exactly this ✓.

Now also think: do we need to check (1,1) and (2,2) and (1,2) all? Yes, any one suffices for K=2.

Priority: output any minimal. Order of checks: K=1, then K=2 (any pattern), then K=3, else -1.

Implementation details:
- Read input fast (sys.stdin.buffer).
- K=1: scan for Li==1 and Ri==N. Record index.
- Precompute: idx_minL... etc.
- (1,1): among L==1, max R and its index i1; among R==N, min L and its index j1. If both exist and R_i1 ≥ L_j1 - 1 → K=2, ops: op1 on i1, op1 on j1.
- (1,2): sweep.
- (2,2): idx of min R (i2), idx of max L (j2). If R_i2 < L_j2 → K=2, op2 on both.
- K=3: I1 = argmin L (first), I2 = argmax L (first), I3 = first index not in {I1,I2}. Ops: 2 on I1, 2 on I2, 1 on I3.
- Output K and the op list (length M, zeros except chosen).

Wait, one more consideration for K=3: we need to ensure that in the K=3 branch, the constructed triple is valid even if there are ties in L (shouldn't happen, but let's be safe). If ties existed, (1,2) would have caught nesting... unless tie with identical interval — caught. Tie in L with different R — caught (container). So in K=3 branch all L distinct; but code defensively: pick I1 = argmin L, I2 = argmax L; if somehow L_{I1} == L_{I2} (all L equal ⇒ M≥3 identical-L ⇒ nesting ⇒ K=2, unreachable). Fine.

Also double-check (2,2,1) coverage claim once more with actual numbers: I1=[2,4], I2=[4,6], I3=[3,5] done above ✓.

Another K=3 test with more intervals: N=10, intervals [2,5],[3,6],[4,7],[5,8] (earlier example): K=2 checks: (1,1): no L=1. (1,2): no containment (L increasing, R increasing). (2,2): minR=5, maxL=5, 5<5 no. ⇒ K=3: I1=[2,5], I2=[5,8], I3=[3,6] (first index not I1,I2). Ops: op2[2,5] → {1,6,7,8,9,10}; op2[5,8] → {1,2,3,4,9,10}; op1[3,6] → {3,4,5,6}. Union: 1 ✓,2 ✓(op2 I2),3 ✓,4 ✓,5 ✓(op1 I3),6 ✓,7 ✓(op2 I1),8 ✓(op2 I1),9 ✓,10 ✓. [1,10] ✓✓.

Now let me reconsider whether K=2's (1,1) might need i and j such that... also the case where the SAME interval has L=1 and another has R=N — handled. What about (1,1) where the L=1 interval also is the R=N interval? ⇒ K=1. Excluded.

Also potential subtle case: K=2 via (1,2) where container i and contained j — output op1 on i, op2 on j: coverage = [Li,Ri] ∪ comp([Lj,Rj]) = comp([Lj,Rj]) ∪ [Li,Ri]; since [Lj,Rj] ⊆ [Li,Ri], union = everything ✓.

Alright, also verify the problem statement: op2 sets x_j=1 for j NOT in [L,R] ✓ complement. Cost 1 each for op1/op2, 0 for op0. Min total cost = min number of nonzero ops ✓.

Now, is the answer really never >3? We've shown: K=1 check; K=2 three patterns; if all fail and M≥3, K=3 construction; if M<3, -1. The only gap: is "K=2 fail ⇒ (2,2,1) construction valid" fully rigorous? Requirements: (i) all intervals pairwise intersect (from (2,2) fail: min R ≥ max L... wait (2,2) condition was minR < maxL for disjointness. Fail ⇒ minR ≥ maxL ⇒ every interval contains [maxL, minR]... actually ⇒ for all i,j: Ri ≥ Lj, i.e., all pairs intersect, and moreover common intersection ⊇ [maxL, minR] nonempty ✓ even stronger, no Helly needed!). (ii) no containment (from (1,2) fail) ⇒ strict order. (iii) M≥3 ⇒ I3 exists with L strictly between ⇒ R strictly between ⇒ I3 ⊇ [L_{I2}, R_{I1}] ⊇ [maxL, minR]... wait [L_{I2}, R_{I1}] = [maxL, minR] exactly (I2 = argmax L, I1 = argmin... hold on: I1 = argmin L, but min R: is R_{I1} = min R? Since L order = R order (no nesting), argmin L = argmin R ✓. Similarly argmax L = argmax R ✓.) So intersection of all holes ⊇ [L_{I2}, R_{I1}], and I3 ⊇ [L_{I2}, R_{I1}] since L_{I3} < L_{I2} and R_{I3} > R_{I1} ✓. Coverage: comp([L1,R1]) ∪ comp([L2,R2]) = comp([L1,R1]∩[L2,R2]) = comp([max(L1,L2), min(R1,R2)]) = comp([L2, R1]) and [L3,R3] ⊇ [L2,R1] ✓. Total cover ✓. 

So final answer characterization confirmed. Also note: we don't even need the (1,1,1) or (2,1,1) patterns — (2,2,1) always works in the K=3 branch. Neat.

Hmm wait, actually let me double-check the (2,2) fail condition: (2,2) succeeds iff ∃i≠j: Ri < Lj. This is iff minR < maxL? If minR < maxL, then i*=argminR, j*=argmaxL, and i*≠j* automatically (Ri* < Lj* ≤ Rj*... wait need i*≠j*: Ri* < Lj* and Lj* ≤ Rj*; if i*=j* then Ri* < Li* contradiction since Li ≤ Ri always. So distinct ✓). And if minR ≥ maxL, no disjoint pair ✓. So (2,2) check = (minR < maxL) ✓ O(M).

(1,1) check = (∃ L=1 interval) and (∃ R=N interval) and (maxR among L=1) ≥ (minL among R=N) - 1 ✓ O(M).

(1,2) check = sweep O(M log M). Actually can also be O(M): for each j, need max R over {i : Li ≤ Lj} ≥ Rj with i≠j. Sort by L and sweep — sorting is O(M log M) anyway. Fine.

Edge Cases:
- N=1: any interval is [1,1] ⇒ K=1.
- M=1: K=1 if [1,N], else -1 (can't do K=2 or 3). Check: K=2 patterns need pairs — (1,1) needs both an L=1 and R=N interval: with M=1 that single interval would be [1,N] ⇒ K=1 first. (1,2) needs i≠j ⇒ no. (2,2) minR<maxL with one interval: minR=maxL? minR=R1, maxL=L1, R1<L1 impossible ⇒ no. K=3 needs M≥3 ⇒ no. So -1 ✓.
- Large input: fast IO.

Now write the code:

```python
import sys

def main():
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    N = int(next(it))
    M = int(next(it))
    L = [0]*(M+1)
    R = [0]*(M+1)
    for i in range(1, M+1):
        L[i] = int(next(it))
        R[i] = int(next(it))
    
    ans = [0]*(M+1)
    
    # K=1
    for i in range(1, M+1):
        if L[i]==1 and R[i]==N:
            ans[i]=1
            out = [str(1), ' '.join(str(ans[i]) for i in range(1,M+1))]
            sys.stdout.write('\n'.join(out)+'\n')
            return
    
    # K=2 (1,1)
    i1 = -1; bestR = -1
    j1 = -1; bestL = N+2
    for i in range(1,M+1):
        if L[i]==1 and R[i]>bestR:
            bestR=R[i]; i1=i
        if R[i]==N and L[i]<bestL:
            bestL=L[i]; j1=i
    if i1!=-1 and j1!=-1 and bestR >= bestL-1:
        ans[i1]=1; ans[j1]=1
        ...output K=2...
        return
    
    # K=2 (1,2): container exists
    order = sorted(range(1,M+1), key=lambda i: (L[i], -R[i]))
    maxR = -1; argmax = -1
    ci=cj=-1
    for i in order:
        if maxR >= R[i]:
            ci=argmax; cj=i
            break
        if R[i] > maxR:
            maxR=R[i]; argmax=i
    if ci!=-1:
        ans[ci]=1; ans[cj]=2
        output K=2
        return
    
    # K=2 (2,2)
    i2 = argmin R; j2 = argmax L
    if R[i2] < L[j2]:
        ans[i2]=2; ans[j2]=2
        output K=2
        return
    
    # K=3
    if M>=3:
        I1 = argmin L (first occurrence)
        I2 = argmax L (first occurrence)
        I3 = first i not in {I1,I2}
        ans[I1]=2; ans[I2]=2; ans[I3]=1
        output K=3
        return
    
    print(-1)
```

Wait, in (1,2) sweep: I break at first found. But note the check `if maxR >= R[i]` before updating ensures container is a previous index (i≠j) ✓. But subtle: container must satisfy L_container ≤ L_j: all previous in sorted order have L ≤ L_j ✓ (ties: equal L, larger R first ✓; equal L equal R: previous duplicate ✓ i≠j ✓).

Hmm, one concern in (1,2): what if maxR ≥ R[i] but argmax has L > L[i]? Impossible since argmax came earlier in sort ⇒ L ≤ L[i] ✓.

For K=3, argmin/argmax L: use first occurrence; ties impossible in this branch but fine.

Also need to double check: in K=3 branch, is it guaranteed that I3 ≠ I1 and I3 ≠ I2 exists and that I1 ≠ I2? M≥3, and I1=argminL, I2=argmaxL; if I1==I2 then all L equal ⇒ nesting ⇒ (1,2) found earlier ⇒ unreachable. So I1≠I2, pick I3 any other index ✓.

Let me also think again about whether (1,1) check should require i1 ≠ j1: i1 has L=1; if i1==j1 then R[i1]=N and L[i1]=1 ⇒ K=1, unreachable ✓.

Output format: K on first line, then space-separated ops on second line. For -1 just print -1.

Let me trace sample 1 fully: N=5,M=4, intervals: 1:[2,4],2:[3,5],3:[1,4],4:[2,5]. K=1: none (L=1&R=5? no). (1,1): L=1: i=3,R=4 → bestR=4,i1=3. R=5: i=2,L=3; i=4,L=2 → bestL=2,j1=4. 4≥2-1 ✓ ⇒ K=2, ans[3]=1,ans[4]=1 → "0 0 1 1". Verify: op1[1,4]={1,2,3,4}, op1[2,5]={2,3,4,5} ⇒ all ✓. Output "2\n0 0 1 1" — accepted (any optimal).

Sample 2: K=1: i=2 [1,5] ✓ ⇒ "1\n0 1 0 0" ✓ matches.

Sample 3: [1,3],[2,5]: K=1 no. (1,1): i1=1 (R=3), j1=2 (L=2): 3≥1 ✓ ⇒ "2\n1 1" ✓ matches.

Sample 4: [1,3],[2,4]: K=1 no. (1,1): i1=1(R=3); R=N=5: none ⇒ j1=-1 ⇒ skip. (1,2): sorted by (L,-R): i=1 [1,3], i=2 [2,4]: maxR after i1: 3; i=2: maxR=3 ≥ R=4? No. Update maxR=4. End ⇒ none. (2,2): i2=argminR=1 (R=3), j2=argmaxL=2 (L=2): 3<2? No. M=2<3 ⇒ -1 ✓.

All samples pass.

Now complexity: O(M log M), memory O(M). N up to 1e6 but we never allocate by N. M up to 2e5 fine.

One more sanity check on the K=3 correctness claim with a weird case: N=2, M=3, intervals [1,1],[1,1],[2,2]. K=1: no ([1,1]≠[1,2]). (1,1): L=1: bestR=1; R=2: bestL=2; 1 ≥ 2-1=1 ✓ ⇒ K=2: op1[1,1] + op1[2,2] = {1}∪{2} ✓.

N=2, M=2, [1,1],[1,1]: K=1 no. (1,1): R=N=2 interval? none ⇒ no. (1,2): duplicates ⇒ sorted: first [1,1], second: maxR=1≥1 ✓ ⇒ K=2: op1 on i1, op2 on i2: {1} ∪ comp({1})={1}∪{2} ✓ K=2.

N=3, M=3, [1,2],[2,3],[1,3]: K=1: [1,3] ✓ ⇒ K=1.

N=3, M=3, [1,2],[2,3],[2,2]: K=1 no. (1,1): L=1: R=2; R=3: L=2; 2≥1 ✓ K=2 ✓.

N=4, M=3, [1,2],[3,4],[2,3]: (1,1): L=1:R=2; R=4:L=3; 2≥2 ✓ K=2: [1,2]∪[3,4]=[1,4] ✓ (adjacent integers, no gap) ✓.

N=4, M=2, [1,2],[3,4]: (1,1): 2≥3-1=2 ✓ K=2 ✓.

N=4, M=2, [1,2],[4,4]: (1,1): 2≥4-1=3? No. (1,2): no containment. (2,2): minR=2 < maxL=4 ✓ K=2: op2[1,2]={3,4}, op2[4,4]={1,2,3} ⇒ all ✓.

Looks solid. Also large N with M≥3 random — trust the proof.

Wait, I want to reconsider one thing: the (1,2) pattern — I should double check that op1 on container + op2 on contained is indeed valid: op1 on i sets [Li,Ri] to 1; op2 on j sets complement of [Lj,Rj] to 1. Every position p: if p∈[Lj,Rj] then p∈[Li,Ri] (containment) ⇒ set by op1. If p∉[Lj,Rj] ⇒ set by op2 ✓. All covered ✓.

And (2,2): op2 on i, op2 on j, [Li,Ri]∩[Lj,Rj]=∅: every p: if p in both intervals — impossible; so p∉[Li,Ri] or p∉[Lj,Rj] ⇒ covered by one of them ✓.

Now, code details: reading input, 1-indexed arrays. Output join. Let me also handle M=0? Constraints say M≥1. Fine.

Also, for argmin/argmax in (2,2) and K=3, simple loops.

Potential pitfall: in K=3, I3 selection: first index not equal to I1 or I2. Since M≥3 exists ✓.

Let me also double-check the claim "K=2 (1,1) found ⇒ distinct indices": i1: L=1, and since K=1 failed, R[i1]<N. j1: R=N, L[j1]>1. So i1≠j1 ✓.

Also, hmm, what about (1,1) where the L=1 interval and R=N interval are the same index but K=1 failed — impossible as shown ✓.

I think solution is complete. Let me also reflect: is it possible that K=2 is achievable via (1,1) but our specific index choice fails the gap condition while another pair succeeds? We choose max R among L=1 and min L among R=N — this maximizes chance: condition bestR ≥ bestL - 1 is necessary and sufficient for some pair (any L=1 interval i has R ≤ bestR, any R=N interval j has L ≥ bestL ⇒ Ri ≥ Lj-1 requires... if bestR ≥ bestL-1 then pair (i1,j1) works; conversely if some pair works, bestR ≥ Ri ≥ Lj-1 ≥ bestL-1 ✓). ✓ optimal check.

(2,2): minR < maxL necessary & sufficient ✓.

(1,2): sweep checks for each j whether any earlier (in sorted order) interval has R ≥ Rj; this is exactly "∃i≠j: Li≤Lj, Ri≥Rj" — need to confirm the sweep finds it iff it exists: if container i exists with Li<Lj: i before j ⇒ when processing j, maxR ≥ Ri ≥ Rj ✓. If Li=Lj, Ri≥Rj: i before j (R desc) ✓. Conversely if sweep finds, container ✓. ✓.

Everything checks. Also note: we should double check that in (1,2) we don't need Li ≤ Lj strictly or i≠j — handled by processing order (strictly previous) ✓.

Now also think about output size: M up to 2e5, fine.

Let me write final code cleanly.

```python
import sys

def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    N = int(data[idx]); idx+=1
    M = int(data[idx]); idx+=1
    L = [0]*(M+1); R = [0]*(M+1)
    for i in range(1,M+1):
        L[i] = int(data[idx]); R[i] = int(data[idx+1]); idx+=2
    
    ops = [0]*(M+1)
    def output(K):
        ops_str = ' '.join(str(ops[i]) for i in range(1,M+1))
        sys.stdout.write(f"{K}\n{ops_str}\n")
    
    # K = 1
    for i in range(1,M+1):
        if L[i]==1 and R[i]==N:
            ops[i]=1
            output(1)
            return
    
    # K = 2, pattern (1,1)
    i1=-1; bestR=-1
    j1=-1; bestL=N+2
    for i in range(1,M+1):
        if L[i]==1 and R[i]>bestR:
            bestR=R[i]; i1=i
        if R[i]==N and L[i]<bestL:
            bestL=L[i]; j1=i
    if i1!=-1 and j1!=-1 and bestR>=bestL-1:
        ops[i1]=1; ops[j1]=1
        output(2)
        return
    
    # K = 2, pattern (1,2): container
    order = sorted(range(1,M+1), key=lambda i:(L[i], -R[i]))
    maxR=-1; argmax=-1; found=False
    for i in order:
        if maxR>=R[i]:
            ops[argmax]=1; ops[i]=2
            output(2)
            return
        if R[i]>maxR:
            maxR=R[i]; argmax=i
    
    # K = 2, pattern (2,2): disjoint
    i2=1; j2=1
    for i in range(2,M+1):
        if R[i]<R[i2]: i2=i
        if L[i]>L[j2]: j2=i
    if R[i2]<L[j2]:
        ops[i2]=2; ops[j2]=2
        output(2)
        return
    
    # K = 3
    if M>=3:
        I1=1; I2=1
        for i in range(2,M+1):
            if L[i]<L[I1]: I1=i
            if L[i]>L[I2]: I2=i
        I3=1
        while I3==I1 or I3==I2:
            I3+=1
        ops[I1]=2; ops[I2]=2; ops[I3]=1
        output(3)
        return
    
    sys.stdout.write("-1\n")

main()
```

Wait — in K=3, I1 (argmin L) and I2 (argmax L): need I1≠I2. If M≥3 and all L equal... then nesting exists ⇒ (1,2) found ⇒ unreachable. But defensive: if I1==I2 (all L equal), then... unreachable, but code would pick I3 ≠ I1, and ops[I2]=2 overwrites ops[I1]=2 same index — would produce only 2 distinct ops with a wrong claim of K=3. Since unreachable, fine, but let me add safety: not needed.

Hmm, actually wait. Let me reconsider whether all L equal really implies (1,2) found: all L equal = a; intervals [a, R_i]. If any two have different R: container relation ⇒ found. If all identical: duplicates ⇒ found (maxR >= R[i] on second occurrence) ✓. So yes unreachable.

Also in K=3, need I3's interval to satisfy L_{I1} < L_{I3} < L_{I2}: since all L distinct (no nesting), any I3 ≠ I1,I2 has L strictly between min and max ✓.

One more check on (1,2) sweep: after the loop without finding, argmax might be -1 if M=0 — M≥1 fine. Also if found at first iteration? maxR=-1 initially, R[i]≥1 > -1, so no false find ✓.

Now let me test mentally with a K=3 case where (1,2) sweep might false-positive: intervals [3,5],[1,2] N=5: sorted: [1,2] then [3,5]: maxR=2; [3,5]: 2≥5? No. ✓ no false positive. Then (2,2): minR=2 ([1,2]), maxL=3: 2<3 ✓ K=2: op2[1,2]={3,4,5}, op2[3,5]={1,2} ⇒ all ✓.

Test where answer is 3 with N large: N=100, M=3: [10,50],[20,60],[30,70]. K=1 no. (1,1): no L=1, no R=100 ⇒ no. (1,2): sorted: [10,50],[20,60],[30,70]: maxR=50; 50≥60? no; maxR=60; 60≥70? no ⇒ none. (2,2): minR=50, maxL=30: 50<30? no. M=3 ⇒ K=3: I1=[10,50] (idx1), I2=[30,70] (idx3), I3=idx2=[20,60]. Ops: op2 idx1: comp([10,50]) = [1,9]∪[51,100]; op2 idx3: comp([30,70]) = [1,29]∪[71,100]; op1 idx2: [20,60]. Union: [1,9]✓, [10,19] from comp idx3 ([1,29]) ✓, [20,60] ✓, [61,70] from comp idx1 ([51,100]) ✓, [71,100] ✓. All covered ✓✓.

Great. Now also consider: could K=2 be achievable through pattern (1,1) using the same operation twice? Not allowed, and we handled distinctness.

I'm confident. Also note the problem says "print one way with minimum cost" — our K is minimal by the case analysis ✓.

Let me also verify the proof that answer never exceeds 3 once more from a different angle (adversarial): try to make K=2 fail with M≥3 but break the K=3 construction. K=3 construction needs: I3 ⊇ [L_{I2}, R_{I1}]. This required L_{I3} < L_{I2} and R_{I3} > R_{I1}. L_{I3} < L_{I2} since I2 = unique max L ✓. R_{I3} > R_{I1}: I1 = argmin L; is R_{I1} necessarily < R_{I3}? No-nesting: L_{I1} < L_{I3} and if R_{I1} ≥ R_{I3} then I1 contains I3 ⇒ (1,2) ⇒ contradiction ✓. So holds. ✓.

Also [L_{I2}, R_{I1}] nonempty: L_{I2} ≤ R_{I1} since (2,2) failed ⇒ maxL ≤ minR ≤ R_{I1}... wait minR: R_{I1} = min R? I1 = argmin L; no-nesting ⇒ argmin L = argmin R ✓ (if R_{I1} > R_k for some k, then L_k > L_{I1} and R_k < R_{I1} ⇒ I1 contains k ⇒ contradiction). So R_{I1} = minR ≥ maxL = L_{I2} ✓ nonempty ✓.

All good. Final code as above. Let me polish I/O and make it efficient: building output string of M numbers fine.

Also handle the `while I3==I1 or I3==I2` loop: I1,I2 ∈ [1,M], I3 starts at 1, increments at most twice ✓.

One more consideration: recursion/limits not an issue. Sorting key lambda fine for 2e5.

Let me also add a fast path: precompute argmin L etc. in single loops. Fine as is.

Double-check sample outputs format: "2\n2 0 1 0\n" — ours: "2\n0 0 1 1\n" for sample 1 — different but valid.

Now write the final answer with brief explanation? The user wants code enclosed in delimiters. The instruction says "Enclose your code within delimiters as follows" — presumably ```python ... ```. Provide the code.

## worker: Write the final Python solution implementing the d
- Coverage viewpoint: writes only turn 0→1, so the goal is to cover every position of [1,N]; op1 on i covers [Li,Ri], op2 on i covers its complement. Cost = number of nonzero ops.
- K=1 iff some interval equals [1,N] (op2 alone can never cover everything).
- K=2 patterns (all pairs of distinct indices):
  - (1,1): two intervals whose union is [1,N] — need an L=1 interval and an R=N interval that touch: maxR(L=1) ≥ minL(R=N) − 1. Distinctness automatic since K=1 failed.
  - (1,2): op1 on container + op2 on contained: ∃i≠j with Li≤Lj, Ri≥Rj. Found by sorting on (L asc, R desc) and checking a running max R strictly before each element (guarantees i≠j and correct tie handling).
  - (2,2): two complements cover everything iff the holes are disjoint: minR < maxL (indices automatically distinct since L≤R).
- K=3: if all K=2 checks fail, then (2,2)-fail ⇒ every pair intersects ⇒ maxL ≤ minR (common nonempty core); (1,2)-fail ⇒ no containment ⇒ L-order equals R-order, all L distinct. Take I1=argmin L (=argmin R), I2=argmax L (=argmax R), and any third index I3. Then op2(I1) ∪ op2(I2) = complement of [L_I2, R_I1], and [L_I3, R_I3] ⊇ [L_I2, R_I1] because L_I3 < L_I2 and R_I3 > R_I1. So op2,op2,op1 covers [1,N]. Hence answer is 3 whenever M≥3 and K≤2 fails; otherwise (M≤2) it's -1.
- Verified mentally on all four samples: (1) K=2 via op1 on [1,4] and [2,5]; (2) K=1 via [1,5]; (3) K=2 via "1 1"; (4) all checks fail with M=2 → -1.
- Complexity: O(M log M) time (one sort), O(M) memory; N only used for comparisons, so N up to 1e6 is fine.
