
## ideation
**Core difficulty.** Naively computing M inversion counts costs O(N·M log N) ≈ way too much. Need O(N log N + M): compute the k=0 answer once, then get each next answer by an O(1) incremental update.

**Key structural insight.** Going from shift k to k+1, every element's value increases by 1 except those currently equal to M−1, which wrap to 0. Relative comparisons among all non-wrapping elements are unchanged (both increase by 1), and comparisons among wrapping elements are also unchanged (all equal before, all equal after → contribute 0 inversions either way). So only pairs (wrapping element, non-wrapping element) change. The elements that wrap at step k are exactly those with original value v = (M−1−k) mod M.

**Delta derivation.** Let the wrapping positions (1-indexed) be p_1<…<p_c, c = cnt[v]. Before: value M−1 is the strict max, so element r contributes (N−p_r)−(c−r) inversions as a left element and 0 as a right element. After: value 0 is the strict min, so it contributes 0 as left and (p_r−1)−(r−1) as right (the only zeros are the other wrapped ones). Per-element delta = 2p_r − 2r + c − N. Summing r=1..c:

delta = 2·sumPos[v] − 2·c(c+1)/2 + c² − cN = **2·sumPos[v] − cnt[v] − cnt[v]·N**

where sumPos[v] = sum of 1-indexed positions of elements with A_i = v. Note this depends only on cnt and sumPos per value — no sorting needed beyond one pass.

**Verification on samples (mental check).**
- Sample 1 (N=3,M=3,A=2,1,0): ans0=3; v=2 (pos 1): 2·1−1−3=−2 → 1 ✓; v=1 (pos 2): 4−1−3=0 → 1 ✓.
- Sample 3 (N=7,M=7,A=0..6): ans0=0; deltas for v=6,5,4,3,2,1 are +6,+4,+2,0,−2,−4 → 6,10,12,12,10,6 ✓.

**Pitfalls.**
- Values with cnt=0 give delta 0 (loop must still advance k) — handled automatically by the formula.
- Order of iteration: at step k→k+1 use v = (M−1−k) mod M, i.e. v goes M−1, M−2, …, 1, 0 as k goes 0,1,…; only M−1 deltas are needed.
- Positions must be 1-indexed consistently in the formula.
- Base case inversion count must be over the raw A (k=0), values in [0,M); Fenwick of size M (or coordinate-compressed).
- Edge cases: N=1 → all answers 0; M=1 → single answer 0 (all A_i=0).
- Performance in Python: use fast input reading (sys.stdin.buffer), a flat-list Fenwick tree, and '\n'.join for output; building the M answers as a list of ints then joining.
- Numbers can be ~2·10^10 (fits Python int trivially, but don't use numpy int32).

## worker: Write the complete Python solution in one file: fa
Implemented exactly the planned O(N log N + M) algorithm:

1. **Base case (k=0):** Fenwick tree over value domain [0, M). Scanning left to right, for element A_i the number of previously inserted elements strictly greater than A_i is `i - prefix(A_i)` (with 0-indexed i = count inserted so far). Summing gives the inversion count of A.

2. **Incremental step:** going from shift k to k+1, all elements gain 1 except those with current value M−1 (original value v = M−1−k), which wrap to 0. Pairs among non-wrapping elements are unaffected (both +1); pairs among wrapping elements contribute 0 both before and after (equal values). For the r-th (of c) wrapping element at 1-indexed position p_r: before wrapping it is the strict maximum, contributing (N−p_r)−(c−r) inversions as a left element and 0 as a right element; after wrapping it is the strict minimum (only other wrapped elements share value 0), contributing 0 as left and (p_r−1)−(r−1) as right. Per-element delta = 2p_r − 2r + c − N; summing r=1..c gives
   delta = 2·sumPos[v] − c(c+1) + c² − cN = 2·sumPos[v] − cnt[v] − cnt[v]·N,
   which only needs cnt and sumPos per value (1-indexed positions), computed in one pass.

3. **Loop order:** for k = 0..M−2, v = M−1−k, yielding v = M−1 down to 1 — values with cnt=0 correctly give delta 0.

Sample checks (by hand):
- Sample 1: inv0=3; v=2 → 2·1−1−3=−2 → 1; v=1 → 4−1−3=0 → 1. ✓
- Sample 2: inv0=7; deltas −4, 0, −2, 0, +4 → 7,3,3,1,1,5. ✓
- Sample 3: inv0=0; deltas +6,+4,+2,0,−2,−4 → 0,6,10,12,12,10,6. ✓

Edge cases: M=1 (all A_i=0) → single output line "0" since the loop body doesn't execute and inv=0; N=1 → inv0=0 and all deltas are 2·1−1−1=0 for the single value, 0 otherwise, so all answers are 0. All arithmetic uses Python ints (values up to ~2·10^10), and I/O uses buffered read plus one joined write.
