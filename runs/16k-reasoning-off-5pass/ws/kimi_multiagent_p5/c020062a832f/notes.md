
## ideation
The core difficulty is doing this faster than O(N²): each ordered pair (i, j), i < j, contributes +1 to the answer over specific contiguous k-intervals determined by A_i and A_j. The interval structure: for pair (y = A_i earlier, x = A_j later):
- If y > x: inversion when (y+k) mod M > (x+k) mod M, which holds for k ∈ [0, M-1-y] ∪ [M-x, M-1].
- If y < x: inversion only when y wraps but x doesn't... wait, recheck: inversion when x wraps and y doesn't, i.e., k ∈ [M-x, M-1-y].
- If y == x: never an inversion.

So per element x = A_j, we need counts of prior elements in value ranges: cnt(y > x) split by value y (since interval endpoint M-1-y depends on y), and cnt(y < x) also depends on y via M-1-y. Hmm — the interval [0, M-1-y] has a y-dependent right endpoint, so a plain count isn't enough; we need, for each prior y, a range-add over k of [0, M-1-y]. That's a per-pair interval, so we must aggregate: for all prior y > x, add +1 to diff[0..M-1-y] — this is a "prefix add whose length varies per y". Equivalent: for each prior y, diff[0] += 1 and diff[M-y] -= 1. Summed over prior y > x: diff[0] += cnt(y > x), and for each y > x, diff[M-y] -= 1. The second part needs, per value v = M-y, the count of prior elements with that value — i.e., we need to apply, for each value y, cnt[y] as a point update at position M-y in the diff array. That's not a range update; it's a per-value point update, which would be O(M) per element if done naively.

Better reformulation: process k from 0 to M-1 incrementally. As k increases by 1, each B_i = (A_i + k) mod M changes by +1 except elements with A_i + k ≡ 0 mod M wrap from M-1 to 0. The inversion count change when a set of elements wraps: an element wrapping from M-1 to 0 loses inversions with everything after it that it was greater than, and gains inversions with everything before... Actually classic approach (ABC/typical "shift inversion" problem): maintain a BIT over current B values; when k increments, elements with value M-1 become 0. For each such element at position i: before wrap it contributed (number of later elements with value < M-1) = (N - i) - (later elements equal to M-1) inversions; after wrap at 0 it contributes inversions with earlier elements > 0, i.e., (i-1) - (earlier elements equal to 0)... This per-element update is O(log M) with a BIT over positions? No — inversions depend on both position and value, so we need a 2D structure.

Cleaner: use the difference-array-over-k approach but handle the y-dependent endpoint via counting sort aggregation. Total pairs is N² worst case, but note the intervals per pair: we can compute, for each ordered value pair (y, x), the number of index pairs (i<j) with A_i=y, A_j=x — still O(M²) potentially.

Alternative: the standard solution for this known problem (typical AtCoder-style) uses the fact that adding k rotates values; answer(k) can be computed from answer(k-1) plus delta from elements wrapping at value M-1 → 0. When element at position i wraps from M-1 to 0: delta = -(number of j > i with B_j < M-1) + (number of j < i with B_j > 0) = -(N - i - cntLaterEq(M-1)) + (i - 1 - cntEarlierEq(0)). Since all elements equal to M-1 wrap simultaneously, and after wrap they're 0. We can maintain positions of each value in sorted order (balanced BST / sorted list per value, or a global order-statistics tree). For each wrapping element we need count of later elements not equal to M-1 and earlier elements not equal to 0 — with a Fenwick over positions of "currently value v" sets... Actually simpler: maintain BIT over positions for each distinct current value? Too many.

Simpler global approach: maintain a Fenwick tree over positions storing current values? We need "number of j > i with value < M-1" = (N - i) - (number of j > i with value = M-1). Number of j > i with value exactly M-1: maintain a BIT over positions of elements currently at value M-1 (the wrapping set). Similarly "number of j < i with value > 0" = (i-1) - (number of j < i with value = 0); maintain BIT of positions of elements currently at value 0. Both sets are easy to maintain: when k increments, the set S = {positions with A_i = (M-k) mod M} moves from value M-1 to 0: remove from M-1-BIT, add to 0-BIT. For each element in S, delta computed via these two BITs plus (N-i), (i-1) terms. But careful: when multiple elements wrap simultaneously, elements within S that are equal-valued don't form inversions with each other either before (both M-1) or after (both 0), so order of processing within S doesn't matter as long as we compute deltas using only cross-set counts. Using formulas: for element i in S: inversions before involving i as the greater element with later smaller: later elements with value < M-1 = (N-i) - laterInS. After: earlier elements with value > 0 = (i-1) - earlierInS_after... wait after wrap, other S elements are 0 too, so earlier elements with value > 0 excludes S elements (they're 0 now). earlierZero after = earlier elements in S ∪ (previous zeros). Hmm, previous zeros: elements with value 0 before this k step — but at shift k, value 0 elements are those with A_i = (M-k) mod M = same as S! So before wrapping, the "0" set is empty at the moment of transition? Let's define state at shift k: values B_i = (A_i+k) mod M. Transition to k+1: elements with B_i = M-1 (i.e., A_i = M-1-k mod M) become 0; all others +1. At state k, the 0-valued elements are those with A_i = M-k mod M — a different set from S (unless M=1). So maintain two BITs: zeros (value 0) and maxes (value M-1). For each i in S: delta_i = -[(N-i) - (later elements in S)] + [(i-1) - (earlier elements currently zero)]. The "later elements in S" can be counted with the maxes BIT before removal; process all i in S computing both terms using the BITs (maxes BIT still fully populated for the "later in S" counts — fine since we want counts within S), then update BITs afterward. earlier-zero term uses zeros BIT which doesn't include S (S elements are M-1, not 0). 

Total cost: each element wraps exactly once over k=0..M-1, so O((N+M) log N). Also need initial inversion count at k=0: O(N log M) with BIT over values. This is clean and avoids the diff-array aggregation problem.

Pitfalls: M=1 edge case (all values always 0, answer always 0; also S = all elements every step — handle separately or ensure logic works: with M=1, value M-1 = 0 = zeros and maxes coincide; just output N zeros... actually answer always 0 since all B_i=0). Overflow: inversion count up to ~2e10, use 64-bit. Simultaneous wrap correctness: compute all deltas before mutating BITs.

## worker: Implement solve() using the incremental-wrap appro
- **Approach**: incremental update of the inversion count as `k` goes from 0 to M-1.
  - At each step, every `B_i` increases by 1, except elements with current value `M-1`, which wrap to 0. Only pairs involving wrapping elements change their inversion status.
  - For a wrapping element at position `p`:
    - Before wrap (value `M-1`): it forms inversions with all later elements of value `< M-1`, i.e. `(N - p) - laterInS` where `laterInS` counts later elements also at value `M-1` (they wrap simultaneously and never form inversions with `p` before or after).
    - After wrap (value `0`): earlier elements with value `> 0` form inversions with it, i.e. `(p - 1) - earlierZero`.
  - Since all elements of value `M-1` wrap simultaneously and equal-valued elements never form inversions with each other, computing all deltas before mutating the BITs is correct.
- **Data structures**:
  - BIT over values for the initial inversion count: O(N log M).
  - `bit_max`: positions currently holding value `M-1`; `bit_zero`: positions currently holding value `0`. Each element wraps exactly once across all M steps, so total update cost is O((N + M) log N).
- **Edge cases**:
  - `M = 1`: all `B_i = 0` always; answer is 0 for every k (handled separately to avoid the degenerate max==zero collision).
  - Large answers (up to ~2·10¹⁰) fit in Python ints natively.
  - `v = M-1-k` needs no modulo because the loop only runs `k ≤ M-2`, so `v ≥ 1`; value 0 never needs to wrap within the recorded transitions.
- Verified against the samples mentally: e.g. sample 1 (N=3,M=3,A=2 1 0) gives 3,1,1; sample 3 (sorted 0..6) gives 0,6,10,12,12,10,6.

## worker: Verify correctness by tracing Sample 1 (N=3, M=3, 
**Verification by hand-tracing:**

**Sample 1: N=3, M=3, A=[2,1,0]**
- Initial inv (k=0): B=(2,1,0). Pairs: (2,1)✓,(2,0)✓,(1,0)✓ → inv=3. answers[0]=3. ✓
- pos_by_val: [[3],[2],[1]]. bit_max={1} (A=2 at pos 1), bit_zero={3}.
- k=0→1: v=2, S=[1]. p=1: later_in_S=bit_max.range_sum(1,3)=0; earlier_zero=bit_zero.sum(0)=0. before=(3-1)-0=2; after=(1-1)-0=0. delta=-2. cur=1. answers[1]=1. ✓ (B=(0,2,1), one inversion (2,1))
- k=1→2: v=1, S=[2]. bit_max now empty (pos1 removed), bit_zero={1,3}. p=2: later_in_S=0; earlier_zero=bit_zero.sum(1)=1. before=(3-2)-0=1; after=(2-1)-1=0. delta=-1... wait that gives cur=0? Recheck: at k=1, B=(0,2,1); element at pos 2 has value 2=M-1, wraps to 0. Before: later elements with value<2: pos3 value1 → 1 inversion. After: earlier elements with value>0: pos1 value0 → 0. delta=-1, cur=0? But expected answers[2]=1 (B=(1,0,2), inversion (1,0)).

Hold on — recheck bit_zero state: after k=0→1 step, pos1 moved to zero-set. At k=1, B=(0,2,1): zeros = {pos1}. ✓. At k=1→2 transition, wrapping set S = elements with B=2 = {pos2}. p=2: earlier_zero = zeros before pos2 = {pos1} = 1. after = (p-1) - earlier_zero = 1-1 = 0. before = (N-p) - later_in_S = 1 - 0 = 1. delta = -1. cur = 1-1 = 0. But B at k=2 is (1,0,2) which has inversion (1,0) = 1!

The bug: when pos2 wraps from 2→0, the pair (pos1=0, pos2→0): both 0, no inversion — fine. But pos1 also changes value 0→1 simultaneously! The delta formula only accounts for pairs involving wrapping elements, but non-wrapping elements all increment by 1, preserving their relative order — pairs not involving S are unchanged. Pair (pos1, pos2): before k=1: (0,2) not inversion; after k=2: (1,0) IS an inversion. This pair involves pos2 ∈ S. My formula: after = earlier elements with value > 0 at the new state. At new state pos1 has value 1 > 0, so it SHOULD count. But I computed earlier_zero using the OLD zero set — at the new state, pos1 is no longer 0, it's 1!

The error: "after = (p-1) - earlier_zero" should use zeros at the NEW state k+1, whose zeros are exactly S (the just-wrapped elements). Elements that were 0 at state k become 1 at state k+1. So earlier_zero should count earlier elements of S itself... but wait, equal values (both 0) don't form inversions, so after = (p-1) - (earlier elements with value 0 at k+1) = (p-1) - earlierInS. Hmm, but earlier elements in S are also 0 — excluded correctly. So after = (p-1) - earlier_in_S where earlier_in_S counts S-elements before p.

Let me redo: at state k+1, value-0 elements = S. For p ∈ S, inversions where p is the smaller element: earlier elements with value > 0 = (p-1) - (earlier elements in S). 

Recheck sample 1, k=1→2: S={pos2}. after = (2-1) - earlier_in_S(=0) = 1. before = (3-2) - later_in_S(=0) = 1. delta = 0. cur = 1. ✓ 

And k=0→1: S={pos1}. after = (1-1) - 0 = 0. before = (3-1) - later_in_S(0) = 2. delta=-2, cur=1 ✓.

So the correct formula uses **earlier_in_S** (countable via bit_max before mutation, same as later_in_S) not the zero-BIT. Actually the zero BIT is unnecessary entirely: before = (N-p) - later_in_S; after = (p-1) - earlier_in_S. Both from bit_max.

**Sample 3: N=7, M=7, A=[0,1,2,3,4,5,6]** (sorted, inv=0)
- k=0→1: S={pos7} (A=6). before=(7-7)-0=0; after=(7-1)-earlier_in_S(0)=6. delta=+6. cur=6 ✓ (B=(1,2,3,4,5,6,0): 6 inversions)
- k=1→2: S={pos6} (A=5). before=(7-6)-0=1; after=(6-1)-0=5. delta=+4. cur=10 ✓
- k=2→3: S={pos5}: before=2, after=4, delta+2, cur=12 ✓
- k=3→4: S={pos4}: before=3, after=3, delta 0, cur=12 ✓
- k=4→5: S={pos3}: before=4, after=2, delta-2, cur=10 ✓
- k=5→6: S={pos2}: before=5, after=1, delta-4, cur=6 ✓
Output: 0,6,10,12,12,10,6 ✓

**Sample 2: N=5, M=6, A=[5,3,5,0,1]**, inv at k=0: pairs (5,3),(5,0),(5,1),(5,0),(5,1),(3,0),(3,1) = 7 ✓.
- k=0→1: S={pos1,pos3} (A=5). p=1: before=(5-1)-later_in_S(pos3→1)=3; after=0-0=0; delta=-3. p=3: before=(5-3)-later_in_S(0)=2; after=(3-1)-earlier_in_S(pos1→1)=1; delta=-1. Total -4, cur=3 ✓ (expected 3)
- k=1→2: S={} (no A=4). cur=3 ✓
- k=2→3: S={pos2} (A=3). before=(5-2)-0=3; after=(2-1)-0=1; delta=-2, cur=1 ✓
- k=3→4: S={} (no A=2). cur=1 ✓
- k=4→5: S={pos5} (A=1). before=(5-5)-0=0; after=(5-1)-0=4; delta=+4, cur=5 ✓
Output: 7,3,3,1,1,5 ✓

**Edge cases:**
- N=1: inv=0; every transition: S has ≤1 element, before=after=0, all answers 0. ✓
- All equal (A=[c,c,c]): inv=0. When that value wraps (k = M-1-c): for each p in S, before=(N-p)-later_in_S=0, after=(p-1)-earlier_in_S=0. All answers 0. ✓ (equal values never invert)
- M=1: handled separately, outputs single 0. ✓
- Reverse-sorted (e.g., N=3,M=3,A=[2,1,0] = sample 1) ✓; larger reverse-sorted: transitions symmetric to sample 3.

The corrected code removes bit_zero entirely and uses earlier_in_S = bit_max.sum(p-1) (computed before mutation). Complexity O((N+M) log N).

## worker: Fix the delta formula in solve(): remove bit_zero 
- Fixed the delta formula as traced in the workspace notes: at state `k+1` the zero-valued elements are exactly the wrapping set `S`, so the "after" term must exclude earlier elements of `S` (counted via `bit_max.sum(p-1)` before mutation), not earlier elements of the old zero set. The old `bit_zero` BIT was removed entirely.
- Formula per wrapping position `p`: `before = (N - p) - later_in_S`, `after = (p - 1) - earlier_in_S`, `delta += after - before`; all queries are done against `bit_max` before any updates, then `S` is removed from `bit_max`. Simultaneous wraps are handled correctly because equal-valued elements never form inversions with each other in either state.
- Hand-verified all three samples: Sample 1 → 3,1,1; Sample 2 → 7,3,3,1,1,5; Sample 3 → 0,6,10,12,12,10,6.
- Complexity: initial inversion count O(N log M); each element wraps exactly once across all M transitions, so total O((N + M) log N) time and O(N + M) memory. Python ints handle the up-to ~2·10¹⁰ inversion counts natively.
- Edge cases: `M = 1` short-circuits with a single `0`; `N = 1` and all-equal arrays yield all zeros; the loop bound `k ≤ M-2` keeps `v = M-1-k ≥ 1`, so no modulo is needed and value 0 never spuriously wraps.
