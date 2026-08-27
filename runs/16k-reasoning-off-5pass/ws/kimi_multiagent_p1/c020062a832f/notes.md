
## ideation
Core observation: For shift k, B_i = (A_i + k) mod M. Since A_i < M, B_i = A_i + k if A_i < M-k, else A_i + k - M. An inversion (i<j) requires B_i > B_j. Case analysis: if both wrap or neither wraps, order is preserved (no inversion). Inversion happens exactly when A_i doesn't wrap but A_j does, i.e., A_i < M-k ≤ A_j, which also requires A_i < A_j automatically. So with t = M-k (t ranges over 1..M as k goes M-1..0), answer for k is f(t) = #{(i<j): A_i < t ≤ A_j}, and we output f(M-k) for k=0..M-1 (note k=0 → t=M, condition A_i < M always true, A_j ≥ M never — wait, t=M means A_j ≥ M impossible, so f(M)=0? But sample 1 k=0 gives 3. Recheck: k=0, no wrap at all, inversions are just A_i > A_j pairs. Hmm, so my case analysis is wrong for k=0: when neither wraps, B_i > B_j iff A_i > A_j — that IS an inversion! I made an error: "order preserved" is wrong — adding the same constant preserves order, so inversions among non-wrapped pairs still count.

Correct analysis: pairs split by wrap status. Let t = M-k (for k=0, t=M, nothing wraps).
- Neither wraps (A_i, A_j < t): inversion iff A_i > A_j.
- Both wrap (A_i, A_j ≥ t): inversion iff A_i > A_j.
- A_i ≥ t > A_j: B_i = A_i+k-M < k ≤ B_j... actually B_i < B_j always here, no inversion.
- A_i < t ≤ A_j: B_i = A_i + k ≥ k > B_j = A_j + k - M, always an inversion.

So answer(k) = (inversions within {A_i < t}) + (inversions within {A_i ≥ t}) + (pairs i<j with A_i < t ≤ A_j).

For k=0 (t=M): only first term = total inversions of A. Good, matches sample.

So we need for each t in 1..M: inv_lt(t) = inversions among elements with value < t; inv_ge(t) = inversions among elements with value ≥ t; cross(t) = #{(i<j): A_i < t ≤ A_j}.

Note inv_lt(t) + cross(t) + (pairs i<j, A_i ≥ t, A_j < t) + inv_ge(t)... total pairs with both < t is C(cnt_lt,2) = inv_lt(t) + noninv_lt(t). Also cross(t) + reverse-cross = cnt_lt * cnt_ge where reverse-cross = #{(i<j): A_i ≥ t, A_j < t}.

Simpler unified formula: answer(t) = inv_lt(t) + inv_ge(t) + cross(t). Alternative: answer(t) = total_inv - [pairs i<j, A_i ≥ t, A_j < t with A_i > A_j counted...] hmm not clean. Let's just compute the three terms.

Computing per t efficiently:
- cross(t): sweep t from M down to 1. Maintain BIT over positions containing elements with A_i ≥ t. When lowering t to t-1... Actually cross(t) = sum over j with A_j ≥ t of (# i<j with A_i < t) = sum over j with A_j ≥ t of (j-1 - # i<j with A_i ≥ t). If we insert positions of elements with A = t, t+1, ..., M-1 into a position-BIT as t decreases, then for each newly... Standard: iterate t from M-1 down to 0; before handling threshold t+1→t, add all positions with A_i = t... Let me define: at threshold t, set S = {i: A_i ≥ t}. cross(t) = sum_{j in S} ((j-1) - (number of S-members before j)). Process t from M down to 1: S only grows. When adding element at position p (with A_p = t-1... careful indexing), its contribution to cross for current and future thresholds: for each element j already in S after p... Actually when we add position p to S (moving threshold from t+1 to t, so A_p = t), cross(t) = cross(t+1) adjusted: elements with A_i < t are those not in S. New cross(t) = sum_{j in S_new} (j-1 - rank_S(j)+1)... Easier: cross(t) = sum_{j in S} (j-1) - sum_{j in S}(# S-members before j). First part: sum of (j-1) over S. Second part: number of pairs (i,j) both in S with i<j = C(|S|,2) — wait no, # S-members before j summed = number of in-S pairs (i<j) regardless of values = C(|S|,2). Oh nice! sum_{j in S} (#S members before j) = C(|S|, 2). So cross(t) = sum_{j in S} (j-1) - C(|S|,2) = (sum of positions in S) - |S| - C(|S|,2)... using 1-indexed positions: sum_{j∈S}(j-1) = posSum - |S|. So cross(t) = posSum(S) - |S| - C(|S|,2) = posSum(S) - |S|(|S|+1)/2. Wait check: C(|S|,2) = |S|(|S|-1)/2, plus |S| gives |S|(|S|+1)/2. So cross(t) = posSum(S) - |S|(|S|+1)/2 where S = {i: A_i ≥ t}. That's trivially maintainable while sweeping t down: add positions, track count and position sum. 

Let me verify with sample 1: A=(2,1,0), M=3. t=1: S = all (A_i≥1: positions 1 (A=2), 2 (A=1)). posSum=3, |S|=2, cross = 3 - 3 = 0. Pairs i<j with A_i<1≤A_j: A_i<1 means A_i=0 (position 3), A_j≥1 before it — none since i<j needed. Yes 0. t=2: S={1}, cross = 1-1=0. Pairs: A_i<2≤A_j: A_j=2 at pos1, need i<1: none. t=3: S={} (A_i≥3 none), cross=0. Hmm but answer needs cross for k: t=M-k. k=1→t=2: answer should be 1. inv_lt(2): elements <2: (1,0) at positions 2,3: inversions=1. inv_ge(2): elements ≥2: just (2): 0. cross=0. Total 1. ✓. k=2→t=1: inv_lt(1): elements<1: (0): 0. inv_ge(1): (2,1): 1 inversion. cross=0. Total 1 ✓. k=0→t=3: inv_lt(3) = inversions of whole (2,1,0) = 3 ✓, inv_ge(3)=0, cross=0. 

- inv_lt(t): inversions among subsequence of elements with A_i < t, for all t. Sweep t from 0 to M: insert elements with A_i = t-1... as t increases, set grows. inv among a growing set: when inserting element at position p with value v, new inversions formed = (# existing elements before p with value > v) + (# existing elements after p with value < v). Since all existing have value < t and v = t-1... hmm values equal to v: existing elements have value ≤ v. # before p with value > v: none if we insert in increasing value order? Existing values < t, v = t-1 is the max. So "before p with value > v" = 0. "after p with value < v": need value-BIT or count per value of positions after p. Alternatively insert in increasing t, and for equal values insert in position order? For elements with equal value, no inversions among them anyway. So inv_lt increment when adding element (p, v): number of previously added elements j>p with value < v... but previously added all have value ≤ v; those with value = v don't count (strict). If we process value groups: for group with value v, first count for each element the number of already-inserted (value < v) elements at positions > p, sum them, then insert all positions. Using position-BIT: count after p = totalInserted - prefix(p). So inv_lt(t) accumulates. Store inv_lt for each t.

- inv_ge(t): symmetric; sweep t from M down to 0, inserting elements with A_i = t, counting inversions among inserted (values ≥ t). When inserting group with value v (descending), new inversions = # existing (value > v) elements before p... existing have value > v (strictly greater since we go descending and handle group together). Inversion (i<j, val_i > val_j): new element at p with value v: as j (smaller value): # existing i<p with value > v = all existing before p. As i: # existing j>p with value < v = 0. So increment = number of existing elements at positions < p = prefix(p-1) from position-BIT. Sum over group, then insert.

Then answer for k = inv_lt(M-k) + inv_ge(M-k) + cross(M-k), output for k=0..M-1.

Complexity O((N+M) log N). Edge cases: t ranges 1..M; inv_lt(M) = total inversions; inv_ge(M) = 0 (no elements ≥ M); cross(M)=0. Arrays of size M+2.

Alternative simpler viewpoint: for each pair i<j with A_i > A_j (an inversion in A), it remains an inversion for shift k iff both wrap or neither wraps, i.e., t > A_i or t ≤ A_j (t=M-k); for each pair i<j with A_i < A_j, it becomes an inversion iff A_i < t ≤ A_j. Could difference-array over t per pair but that's O(N^2) pairs. The sweep approach above is the way.

Pitfalls: 64-bit answers (N up to 2e5, inversions up to ~2e10 — need 64-bit; Python fine anyway, but if writing C++ use long long). The problem statement says write Python ("when the python program runs"). So implement in Python with fast I/O and Fenwick trees; O((N+M) log N) in Python should pass for 2e5.

Let me double check inv_ge with sample 2: A=(5,3,5,0,1), M=6. k=0 → t=6: inv_lt(6)=total inversions of (5,3,5,0,1): pairs: (5,3),(5,0),(5,1) from first 5: 3; (3,0),(3,1): 2; second 5: (5,0),(5,1): 2; 0: none; total 7 ✓ (sample says 7). k=5 → t=1: expected 5. inv_lt(1): elements<1: (0): 0. inv_ge(1): elements ≥1: (5,3,5,1) at positions 1,2,3,5: inversions: (5,3),(5,1),(3,1),(5,1) = 4. cross(1): S={1,2,3,5}, posSum=11, |S|=4, cross=11-10=1. Total 0+4+1=5 ✓.

Great, formula verified.

Implementation plan:
1. Read N, M, A.
2. Group positions by value: pos_by_val[v] = list of positions (0-indexed fine).
3. inv_lt array size M+1: BIT over positions. cur=0. For v in 0..M-1: for each p in group v: cur += inserted_total - bit.sum(p+1) (elements after p, 0-indexed p: sum over positions > p = total - prefix up to p inclusive). Then after counting all in group, insert each p (bit.add(p,1)), inserted_total += len. inv_lt[v+1]... define inv_lt[t] for t=0..M: inv_lt[0]=0; after processing value v, inv_lt[v+1] = cur. So inv_lt[t] = inversions among elements with A_i < t. ✓
4. inv_ge array size M+1: BIT over positions. cur=0, total=0. inv_ge[M]=0. For v from M-1 down to 0: for each p in group v: cur += bit.sum(p) (number inserted at positions < p, 0-indexed: prefix count of positions 0..p-1 = bit.sum(p) if bit.sum(x) sums indices < x... define carefully). Then insert all. inv_ge[v] = cur after processing v. inv_ge[t] = inversions among A_i ≥ t. ✓
5. cross[t] for t=1..M: cnt=0, posSum=0; cross[M]=0 (S empty since A_i<M... wait A_i ≥ M impossible, so at t=M, S empty ✓). For t from M-1 down to 1: add group t: cnt += len, posSum += sum of (p) — using 1-indexed positions: posSum += sum(p+1 for p in group). cross[t] = posSum - cnt*(cnt+1)//2. Wait derived: cross = posSum - |S|(|S|+1)/2 with 1-indexed positions. Check earlier: t=1 sample1: S positions 1,2 (1-indexed), posSum=3, cnt=2, cross=3-3=0 ✓. Sample2 t=1: positions 1,2,3,5, posSum=11, cnt=4, cross=11-10=1 ✓. Note: also need cross[M]=0.
   Actually careful: cross(t) = sum_{j∈S}(j-1) - C(|S|,2) = posSum - cnt - cnt(cnt-1)/2 = posSum - cnt(cnt+1)/2. ✓
6. For k in 0..M-1: t = M-k; ans = inv_lt[t] + inv_ge[t] + cross[t]. Print.

Wait — does cross need t= M? cross[M] = 0 ✓ (S empty). And inv_ge[M]=0, inv_lt[M]=total. k=0 → t=M ✓.

Fenwick in Python: size N, standard. Total ops ~ 2N queries + 2N updates + M loop iterations: ~8e5 BIT ops each O(log N) — fine.

## worker: Implement the full Python solution: read input, gr
**Derivation.** For shift k, let t = M−k (elements wrap iff A_i ≥ t). For a pair i<j:
- Both below t or both ≥ t: relative order preserved → inversion iff A_i > A_j. Contributes inv_lt(t) and inv_ge(t) respectively.
- A_i ≥ t > A_j: B_i = A_i+k−M < k ≤ B_j → never an inversion.
- A_i < t ≤ A_j: B_i = A_i+k ≥ k > B_j → always an inversion. Contributes cross(t).

So answer(k) = inv_lt(t) + inv_ge(t) + cross(t) with t = M−k.

**Key simplification for cross:** cross(t) = Σ_{j∈S}(j−1) − Σ_{j∈S}(#S-members before j) = posSum(S) − |S| − C(|S|,2) = posSum(S) − |S|(|S|+1)/2 (1-indexed positions), maintainable with just a counter and position sum while sweeping t downward.

**Sweeps:**
- inv_lt: insert value groups ascending; since all previously inserted have strictly smaller values, new inversions contributed by element at p = (# inserted at positions > p) = total − prefix(p+1). Count whole group before inserting (equal values never form inversions).
- inv_ge: insert value groups descending; new element at p (smaller value) forms an inversion with every previously inserted element before p: prefix(p).
- cross: descending sweep accumulating cnt and posSum.

**Hand-verification:**
- Sample 1 (A=2,1,0, M=3): inv_lt = [0,0,1,3], inv_ge = [3,1,0,0], cross = [0,0,0,0]. k=0→t=3: 3+0+0=3 ✓; k=1→t=2: 1+0+0=1 ✓; k=2→t=1: 0+1+0=1 ✓.
- Sample 2 (A=5,3,5,0,1, M=6): k=0→t=6: inv_lt(6)=7 ✓. k=5→t=1: inv_lt(1)=0, inv_ge(1)=4 (pairs (5,3),(5,1),(3,1),(5,1) among subsequence (5,3,5,1)), cross(1)=11−10=1 → 5 ✓. k=3→t=3: inv_lt(3)= inversions of (0,1)=0; inv_ge(3)= inversions of (5,3,5)=1; cross(3): S={1,2,3}, posSum=6, cnt=3 → 6−6=0; total 1 ✓ (sample line 4 = 1).
- Sample 3 (A=0..6, M=7): no inversions anywhere, so inv_lt=inv_ge=0; answer(k)=cross(7−k). t=7:0; t=6: S={7}, 7−1=6; t=5: S={6,7}, 13−3=10; t=4: 18−6=12; t=3: 22−10=12; t=2: 25−15=10; t=1: 27−21=6 → 0,6,10,12,12,10,6 ✓.

**Complexity:** O((N+M) log N) time, O(N+M) memory. Answers fit in Python ints automatically (max ~2·10¹⁰).

## worker: Hand-trace all three samples and sanity-check edge
Hand-traced all samples and edge cases against the code:

**Sample 1** (N=3, M=3, A=2,1,0):
- inv_lt sweep: v=0: group [2], cur += 0-0=0, insert; inv_lt[1]=0. v=1: group [1], cur += 1 - bit_sum(2)=1-1=0... wait: total=1, bit_sum(p+1)=bit_sum(2)=1 (element at pos 2 inserted), so cur += 1-1 = 0? That's wrong — element at pos 2 (value 0) is AFTER p=1, so it should count as an inversion (1 > 0 with i=1<j=2). bit_sum(p+1) counts inserted positions ≤ p, i.e., in [0, p+1) = positions 0..p. Inserted before counting group v=1: only pos 2. bit_sum(2) = count in [0,2) = positions 0,1 = 0. So cur += total(1) - 0 = 1. ✓ (I misread; bit_sum(i) sums [0,i), so bit_sum(p+1) covers positions 0..p, and total - that = positions > p. Correct.) inv_lt[2]=1. v=2: group [0], cur += 2 - bit_sum(1) = 2-0=2 → cur=3, inv_lt[3]=3. inv_lt = [0,0,1,3] ✓.
- inv_ge sweep: v=2: group [0], cur += bit_sum(0)=0, inv_ge[2]=0. v=1: group [1], cur += bit_sum(1)=1 (pos 0 before it) → 1, inv_ge[1]=1. v=0: group [2], cur += bit_sum(2)=2 → 3, inv_ge[0]=3. inv_ge = [3,1,0,0] ✓.
- cross: t=2: group [0], cnt=1, pos_sum=1, cross[2]=1-1=0. t=1: group [1], cnt=2, pos_sum=3, cross[1]=3-3=0. cross=[0,0,0,0] ✓.
- Output: k=0→t=3: 3+0+0=3; k=1→t=2: 1+0+0=1; k=2→t=1: 0+1+0=1 → "3 1 1" ✓.

**Sample 2** (N=5, M=6, A=5,3,5,0,1): spot-checked t=6: inv_lt[6]=7 (total inversions) → k=0 gives 7 ✓. t=1: inv_lt[1]=0, inv_ge[1]: descending sweep inserts v=5 (pos 0,2), v=3 (pos 1: cur += bit_sum(1)=1), v=1 (pos 4: cur += bit_sum(4)=3) → 4; cross[1]: cnt=4, pos_sum=1+2+3+5=11 → 11-10=1. Total 5 ✓ matches line 6. t=3: inv_lt[3]=0 (elements 0,1 sorted), inv_ge[3]=1 (pair (5,3) at pos 0,1), cross[3]: S={0,1,2}, pos_sum=6, cnt=3 → 0. Total 1 ✓ matches line 4.

**Sample 3** (sorted 0..6, M=7): inv_lt and inv_ge all 0 (no inversions in any subsequence since subsequences of sorted stay sorted). cross[t] = posSum - cnt(cnt+1)/2 with S = {t, t+1, ..., 6} positions 1-indexed: t=7:0, t=6: 7-1=6, t=5: 13-3=10, t=4: 18-6=12, t=3: 22-10=12, t=2: 25-15=10, t=1: 27-21=6 → output 0,6,10,12,12,10,6 ✓.

**Edge cases:**
- N=1, M=1, A=[0]: groups: pos_by_val=[[0]]. inv_lt=[0,0], inv_ge=[0,0], cross=[0,0]. k=0→t=1: 0 ✓ (single element, no pairs).
- M=1, N large, all A_i=0: every k=0 only; t=1; inv_lt[1]=total inversions of all-equal = 0 (equal values never counted since groups counted before insertion); inv_ge[1]=0; cross[1]=0. Output 0 ✓ (B all zeros always).
- All equal values v, arbitrary M: inv_lt[t]=0 ∀t (no strict inversions possible within a value group, and no other values); inv_ge: same, 0; cross[t]: for t ≤ v, S = all positions, pos_sum = N(N+1)/2, cnt=N → cross = 0; for t > v, S empty → 0. All outputs 0 ✓ (B is constant for any k).
- Reverse-sorted distinct values, e.g., N=M, A_i = M-i: inv_lt[M] = N(N-1)/2 max — Python int fine.
- Values present only at extremes (0 and M-1): sweeps handle empty groups via `if group` guards; inv_lt[0]=0 and inv_ge[M]=0, cross[M]=0 defaults correct.

Complexity: O((N+M) log N) time, O(N+M) memory. The code is correct as written; no changes needed.
