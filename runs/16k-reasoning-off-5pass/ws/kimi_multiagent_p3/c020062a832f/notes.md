
## ideation
The core difficulty is that M can be up to 2e5, so recomputing the inversion number from scratch for each k (O(M · N log N)) is far too slow. We need to compute all M answers in roughly O(N log M + M).

Key insight: for a fixed pair (i, j) with i < j, as k varies over 0..M-1, the comparison between B_i = (A_i + k) mod M and B_j = (A_j + k) mod M changes only at the "wrap-around" points. Specifically, adding k mod M preserves the order of two residues unless exactly one of them wraps past M. So each pair contributes to the inversion count either:
- for all k except a contiguous interval (when A_i > A_j), or
- only within a contiguous interval (when A_i < A_j), or
- never (when A_i = A_j).

This means each pair's contribution as a function of k is a piecewise-constant function with at most two breakpoints, so we can use a difference array over k. The base value (k = 0) is the ordinary inversion number of A.

Pitfalls:
- Getting the interval endpoints exactly right (half-open vs closed intervals; k is an integer in [0, M-1]).
- Pairs with A_i = A_j never contribute (B_i = B_j always).
- When A_i > A_j, the pair is an inversion for all k except k in (M - A_i, M - A_j] — need care: at k = M - A_i, B_i = 0 which is ≤ B_j (since B_j = A_j + k < M doesn't wrap, B_j = A_j + M - A_i ≥ ... hmm need to check), so the non-inversion interval is k ∈ [M - A_i, M - A_j - 1]? Let me re-derive carefully.

Let a = A_i, b = A_j, i < j. B_i = (a+k) mod M, B_j = (b+k) mod M. Inversion iff B_i > B_j.

Case a > b: Without wrap, a+k > b+k. B_i wraps when a+k ≥ M i.e. k ≥ M - a. B_j wraps when k ≥ M - b. Since a > b, M - a < M - b. For k in [0, M-a): neither wraps, B_i > B_j → inversion. For k in [M-a, M-b): B_i = a+k-M, B_j = b+k; B_i > B_j iff a - M > b, impossible since a < M and b ≥ 0 → a - M < 0 ≤ b. So no inversion. For k in [M-b, M): both wrap, B_i = a+k-M > b+k-M = B_j → inversion. So inversion holds for k ∈ [0, M-a) ∪ [M-b, M). The "gap" is [M-a, M-b), which is non-empty since a > b.

Case a < b: symmetric — inversion only for k ∈ [M-a, M-b).

Case a = b: never.

So the difference array approach: ans[k] = baseInv + delta[k], where for each pair:
- a > b: it's already counted in baseInv; subtract 1 for k ∈ [M-a, M-b).
- a < b: add 1 for k ∈ [M-a, M-b).

Now the challenge: we must enumerate pairs efficiently. We can't iterate over all pairs. Standard trick: process elements left to right with a Fenwick tree over values. When processing element j with value b = A_j, for each previous value a:
- pairs with a > b contribute a range-subtract on [M-a, M-b).
- pairs with a < b contribute a range-add on [M-a, M-b).

For fixed j, as a varies over values > b, the interval [M-a, M-b) has right endpoint fixed (M-b) and left endpoint M-a varying. So we need, for each distinct value a, the count of previous occurrences, then apply a difference-array update at position M-a (and M-b). We can aggregate: for all a > b with count c_a: diff[M-a] -= c_a, diff[M-b] += c_a. Similarly for a < b: diff[M-a] += c_a, diff[M-b] -= c_a.

If we iterate over all distinct values a per element, that's O(N·M) worst case. Instead, we can process per distinct value of b: group indices by value. For a group with value b and total count c_b (process the whole group's contribution at once — pairs within the group have a = b, no contribution), we need sum of counts over a > b and the distribution of M-a. Hmm, the left endpoints M-a still vary per distinct a.

Alternative: think of it as for each pair of distinct values (a, b) with counts, but that's O(number of distinct pairs) which could be O(min(N, M)^2).

Better approach: process value thresholds with a Fenwick over positions k. Let's think differently. For each element j (value b), the contribution to diff is:
- For each previous a > b: diff[M-a] -= 1, diff[M-b] += 1.
- For each previous a < b: diff[M-a] += 1, diff[M-b] -= 1.

The diff[M-b] parts are easy: diff[M-b] += (count of a > b) - (count of a < b) = computable with Fenwick counts in O(log M).

The diff[M-a] parts require, for each distinct value a, adding ±count(a) at position M-a. If we process elements one at a time, when we encounter value b, we could apply point updates at M-a for all distinct a seen so far — too many.

Alternative: swap roles. Process j from left to right; maintain a Fenwick over values for counts. Also maintain a second structure: for the "diff[M-a] ±= count" part, note that when a new element with value a is processed (as the left element i), it will pair with all future elements. For a future element with value b < a: diff[M-a] -= 1 and diff[M-b] += 1. For a future element with value b > a: diff[M-a] += 1 and diff[M-b] -= 1.

So when we insert value a (as a left endpoint), we could defer: we need data structures supporting "for all future b, apply updates depending on comparison". 

Cleaner formulation: total answer[k] = sum over pairs of indicator. Let's define for each ordered pair of values. Alternatively, compute ans[k] directly via convolution-like structure? Let's think.

ans[k] = #{(i,j): i<j, (A_i+k) mod M > (A_j+k) mod M}.

Alternative known approach for this problem (it's AtCoder ABC/ARC problem "Shift and Inversions" — typical solution): The intended solution is exactly the difference array with per-pair intervals, implemented by iterating over pairs of values using a Fenwick tree where we process elements and for each element update ranges. Let me reconsider complexity: for element j with value b, we need:
- sum over distinct a > b of count(a) applied at position M-a: this is like a "range of values" mapped to "range of positions" — since a > b maps to M-a < M-b, i.e., positions [0, M-b-1]... wait M-a for a > b means M-a ≤ M-b-1, so positions in [M - (M-1), M-b-1] = [1, M-b-1] roughly. But the update at each position is -count(a), which depends on a, not uniform. So it's not a uniform range update.

Hmm, but we can maintain a Fenwick tree F over positions p = M - a, where when we insert an element with value a, we do point update F.add(M - a, 1). Then for element j with value b:
- subtract contributions: for a > b, positions p = M-a ∈ [M-(M-1), M-b-1] = [1, M-b-1]; we want diff[p] -= 1 for each p where there's a prior element — but that's applying -1 at each occupied position, i.e., diff[p] -= F.point(p)? No — diff array updates are per pair, and we want diff[p] -= count of prior elements with M-a = p. That's exactly: for all p in range, diff[p] -= cnt_at_position(p). This is not a standard range update because the amount varies per position.

So instead of materializing diff updates per pair, we can compute ans[k] differently: ans[k] = baseInv + sum_k corrections, where corrections involve prefix sums of diff. Let's compute the total correction C[k] = sum over pairs of f_pair(k), where f_pair(k) = -1 if a > b and k ∈ [M-a, M-b), +1 if a < b and k ∈ [M-a, M-b), else 0.

C[k] = sum over pairs (i<j, a=A_i, b=A_j) of g(a, b, k) where g = +1 if a < b ≤ ... let me re-derive: for a < b: +1 when M-a ≤ k ≤ M-b-1, i.e., a ≥ M-k and b ≤ M-k-1. Wait: M-a ≤ k means a ≥ M-k; k ≤ M-b-1 means b ≤ M-k-1. But a < b and a ≥ M-k, b ≤ M-k-1 gives M-k ≤ a < b ≤ M-k-1, contradiction! Let me recheck.

For a < b: inversion when k ∈ [M-a, M-b). Since a < b, M-a > M-b, so [M-a, M-b) is empty! I made an error. Let me redo.

Case a < b: B_i wraps when k ≥ M-a; B_j wraps when k ≥ M-b. Since a < b, M-a > M-b. For k ∈ [0, M-b): neither wraps, B_i = a+k < b+k = B_j, no inversion. For k ∈ [M-b, M-a): B_j wraps: B_j = b+k-M, B_i = a+k. B_i > B_j iff a > b - M, i.e., a + M > b, always true. So inversion! For k ∈ [M-a, M): both wrap, B_i = a+k-M < b+k-M, no inversion. So inversion iff k ∈ [M-b, M-a). Good — non-empty.

Case a > b: inversion iff k ∈ [0, M-a) ∪ [M-b, M) as derived. Equivalently, NOT inversion iff k ∈ [M-a, M-b).

So:
- a > b (inversion at k=0): subtract 1 on k ∈ [M-a, M-b).
- a < b (not inversion at k=0): add 1 on k ∈ [M-b, M-a).

Both intervals are non-empty and of form [M-max(a,b), M-min(a,b)). Nice symmetry: for the pair with values lo = min(a,b), hi = max(a,b), the "flip interval" is k ∈ [M-hi, M-lo). If the left element is the larger (a=hi, inversion at k=0), we subtract; if the left element is smaller (a=lo), we add.

Now C[k] = sum over pairs with a < b of [M-b ≤ k < M-a] - sum over pairs with a > b of [M-a ≤ k < M-b].

Let's define for each pair (i<j): lo, hi. The indicator [M-hi ≤ k ≤ M-lo-1].

C[k] = Σ_{pairs, a<b} 1{k ∈ [M-b, M-a)} - Σ_{pairs, a>b} 1{k ∈ [M-a, M-b)}.

Compute via difference array diff[0..M]: for pair a<b: diff[M-b] += 1, diff[M-a] -= 1. For pair a>b: diff[M-a] -= 1, diff[M-b] += 1.

Now efficient computation: process j from 1..N, b = A_j. Maintain Fenwick cnt over values (counts of previous elements). For the pair contributions with previous elements:

For a < b: diff[M-b] += count(a<b) — aggregate via cnt.prefix_sum(b-1). And diff[M-a] -= 1 for each a < b: this is per-value, amount = count(a) at position M-a.

For a > b: diff[M-b] += count(a>b) — aggregate. And diff[M-a] -= 1 for each a > b: per-value amounts.

The per-value parts: we need, for each distinct value a with count c among previous elements, diff[M-a] -= c (regardless of whether a < b or a > b — interesting, in both cases diff[M-a] -= 1 per pair!). Indeed: a<b case has diff[M-a] -= 1; a>b case has diff[M-a] -= 1. And a=b: no contribution. So for element j: for every previous element with value a ≠ b, diff[M-a] -= 1, and diff[M-b] += (number of previous elements with a ≠ b).

Wait check a<b: diff[M-b] += 1, diff[M-a] -= 1. a>b: diff[M-a] -= 1, diff[M-b] += 1. Yes! Both cases: diff[M-a] -= 1, diff[M-b] += 1. Beautiful simplification: for each pair (i<j) with A_i ≠ A_j: diff[M - A_i] -= 1 and diff[M - A_j] += 1.

So total: diff[M - v] += (number of pairs with A_j = v, j later, A_i ≠ v) - (number of pairs with A_i = v, i earlier, A_j ≠ v).

For each index t with value v = A_t: as a right endpoint, contributes diff[M-v] += (# previous elements with value ≠ v) = (t-1) - (previous count of v). As a left endpoint, contributes diff[M-v] -= (# later elements with value ≠ v) = (N - t) - (later count of v).

So for each index t (1-based) with value v: diff[M-v] += [(t-1) - preCnt_v] - [(N-t) - postCnt_v], where preCnt_v = occurrences of v before t, postCnt_v = occurrences after t.

That's O(N) after computing pre/post counts! Then ans[k] = baseInv + prefixSum of diff up to k. Wait, need to double check the diff semantics: diff[p] with p = M - v, and intervals [M-hi, M-lo) correspond to diff[start] += x, diff[end] -= x. Let me re-verify with the per-pair rules:

Pair a<b (left smaller): add +1 on [M-b, M-a): diff[M-b] += 1, diff[M-a] -= 1. ✓ (matches diff[M-A_j] += 1, diff[M-A_i] -= 1)
Pair a>b (left larger): subtract 1 on [M-a, M-b): diff[M-a] -= 1, diff[M-b] += 1. ✓ (diff[M-A_i] -= 1, diff[M-A_j] += 1)

Great, unified: for pair with A_i ≠ A_j: diff[M-A_i] -= 1, diff[M-A_j] += 1.

Then ans[k] = baseInv + Σ_{p ≤ k} diff[p]. Let me sanity check with sample 1: A = [2,1,0], M=3, N=3. baseInv = 3.

Pairs: (2,1): diff[3-2=1] -=1, diff[3-1=2] +=1. (2,0): diff[1] -=1, diff[3-0=3] +=1 — but index 3 is out of range [0, M-1]; we can use diff array of size M+1 and only prefix up to M-1. (1,0): diff[2] -=1, diff[3] +=1.

diff[1] = -2, diff[2] = +1-1 = 0, diff[3] = +2 (ignored beyond M-1 but fine).

prefix: k=0: 0 → ans 3. k=1: -2 → ans 1. k=2: -2 → ans 1. Expected: 3,1,1. ✓

Check sample 3: A = [0,1,2,3,4,5,6], M=7, N=7. baseInv = 0. All pairs a<b. Pair (a,b): diff[7-b] += 1, diff[7-a] -= 1.

For each t (1-based), v = t-1: diff[7-v] += (t-1) - (N-t) = (t-1) - (7-t) = 2t - 8. Positions p = 7-v = 8-t. t=1: p=7, += -6. t=2: p=6, += -4. t=3: p=5, += -2. t=4: p=4, += 0. t=5: p=3, += 2. t=6: p=2, += 4. t=7: p=1, += 6.

diff[1]=6, diff[2]=4, diff[3]=2, diff[4]=0, diff[5]=-2, diff[6]=-4, diff[7]=-6.

prefix sums: k=0: 0 → 0 ✓. k=1: 6 → 6 ✓. k=2: 10 → 10 ✓. k=3: 12 → 12 ✓. k=4: 12 → 12 ✓. k=5: 10 → 10 ✓. k=6: 6 → 6 ✓. Matches expected output 0,6,10,12,12,10,6. 

So the algorithm:
1. Compute baseInv = inversion number of A via Fenwick, O(N log M).
2. Compute for each value v: total count tot[v]. Iterate t from 1..N maintaining running count c[v] (occurrences so far including current). pre = c[v]-1, post = tot[v] - c[v]. diff[M - A_t] += (t-1 - pre) - (N - t - post).
3. Prefix sum diff over k = 0..M-1, add baseInv, print.

All O(N + M) after inversion count. Very simple. Edge cases: M - A_t can be M (when A_t = 0), so diff array size M+1; prefix only up to index M-1. Note k ranges 0..M-1 and p = M - A_i ∈ [1, M], so diff[0] is always 0 — consistent with ans[0] = baseInv.

Let me double check sample 2 quickly: N=5, M=6, A=[5,3,5,0,1]. baseInv: pairs: (5,3)✓,(5,5)✗,(5,0)✓,(5,1)✓,(3,5)✗,(3,0)✓,(3,1)✓,(5,0)✓,(5,1)✓,(0,1)✗ → 7. Expected first line 7 ✓.

tot: 5→2, 3→1, 0→1, 1→1.
t=1, v=5: pre=0, post=1. (t-1-pre) - (N-t-post) = 0 - (4-1) = -3. diff[6-5=1] += -3.
t=2, v=3: pre=0, post=0. (1) - (3) = -2. diff[3] += -2.
t=3, v=5: pre=1, post=0. (2-1) - (2-0) = 1-2 = -1. diff[1] += -1 → diff[1] = -4.
t=4, v=0: pre=0, post=0. (3) - (1) = 2. diff[6] += 2.
t=5, v=1: pre=0, post=0. (4) - (0) = 4. diff[5] += 4.

diff: index1: -4, index3: -2, index5: 4, index6: 2.
prefix: k=0: 0 → 7 ✓. k=1: -4 → 3 ✓. k=2: -4 → 3 ✓. k=3: -6 → 1 ✓. k=4: -6 → 1 ✓. k=5: -2 → 5 ✓. Expected: 7,3,3,1,1,5. ✓

The plan is solid. Implementation details: use sys.stdin.buffer.read for fast input, array of ints for diff (Python ints fine), Fenwick for inversions or use a simpler O(N log N) via sorted coordination — values already in [0, M), so Fenwick over M directly.

One more consideration: inversion count can be up to N(N-1)/2 ≈ 2e10, fits in Python int trivially.

## worker: Write the complete Python solution: fast stdin par
- Derivation: for a pair (i<j) with values a=A_i, b=A_j:
  - a > b: inversion for k ∈ [0, M-a) ∪ [M-b, M), i.e. subtract 1 on k ∈ [M-a, M-b).
  - a < b: inversion only for k ∈ [M-b, M-a), i.e. add 1 there.
  - a = b: never an inversion.
  - Both non-equal cases unify to: diff[M-a] -= 1, diff[M-b] += 1.
- Therefore each index t (0-based) with value v contributes diff[M-v] += (t - pre_v) - ((n-1-t) - post_v), where pre_v/post_v are occurrences of v before/after t. Computed in one O(N) pass with running counts.
- ans[k] = baseInv + prefix sum of diff up to k. diff has size M+1 because A_i = 0 gives index M (sentinel, never included in prefix over k ∈ [0, M-1]).
- Verified mentally against all three samples (e.g. sample 2 gives diff[1]=-4, diff[3]=-2, diff[5]=4, diff[6]=2 → 7,3,3,1,1,5 ✓).
- Edge cases: N=1 → baseInv=0, diff all zero, prints M zeros. M=1 → all A_i=0, no unequal pairs, prints 0. All-equal values → no contributions, answer constant = baseInv = 0.
- Complexity: O(N log M + M) time, O(N + M) memory. Values up to ~2e10 fit Python ints.
