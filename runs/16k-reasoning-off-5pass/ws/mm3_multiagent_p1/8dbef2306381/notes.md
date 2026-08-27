
## ideation
The problem is a reachability question on a huge line (N up to 1e12) with at most 2e4 disjoint bad intervals. Moves are steps i ∈ [A,B] (both ≤ 20) to non‑bad squares. Since N is huge we cannot BFS over individual squares, but the number of good (non‑bad) segments is at most M+1 ≤ 20001. Inside a good segment we can move freely as long as the segment length is at least B (otherwise we might be stuck near its ends). The key observation: once we can land on any square of a good segment, we can reach the whole segment if its length ≥ B; otherwise we must treat the segment as a set of reachable positions (but length < B means at most 19 squares, still manageable). However, a simpler and sufficient approach is to BFS over the **segments** themselves: from a segment [l,r] (good), for each step i ∈ [A,B], the landing position is x+i for some x in the segment. The set of reachable landing positions is the union of intervals [l+i, r+i] intersected with good segments. Since we only care whether we can reach *some* square in a target segment, we can just check if the interval [l+i, r+i] overlaps any good segment. If it does, we can move to that segment (and mark it reachable). Because steps are small (≤20) and segments are few, we can do this efficiently.

Pitfalls:
- Bad intervals are disjoint and sorted (given by constraints). Good segments are: [1, L1-1], [R1+1, L2-1], ..., [RM+1, N].
- Need to handle M=0 (no bad squares): then whole [1,N] is one good segment.
- Segment length may be < A, in which case we cannot make any move from it (except if we are already at N).
- BFS must avoid revisiting segments.
- The answer is Yes iff segment containing N is reachable (or N itself is reachable; N is always good because R_i < N).

Algorithm sketch:
1. Read N, M, A, B.
2. Build list of good segments: start = 1; for each bad interval [L,R], add segment [start, L-1] if start ≤ L-1; then start = R+1. After loop, add [start, N] if start ≤ N.
3. BFS queue of segment indices. Initially reachable = segment containing 1 (which is always the first good segment, since 1 is not bad because L_i > 1).
4. While queue not empty:
   - pop segment idx.
   - let l, r = segments[idx].
   - if this segment contains N: return Yes.
   - for i in range(A, B+1):
       - new_l = l + i, new_r = r + i.
       - find all good segments that intersect [new_l, new_r]. Since segments are disjoint and sorted, we can binary search for the first segment with r >= new_l, then iterate while segments[j].l <= new_r.
       - For each such segment j not yet visited, mark visited and push to queue.
5. If BFS finishes without reaching N, return No.

Complexity: O((M+1) * (B-A+1) * log(M)) for binary search, or O((M+1)*(B-A+1)) with two pointers if we process segments in order. Since M ≤ 2e4 and B-A+1 ≤ 20, this is trivial.

Edge cases:
- N=1? Constraint N≥2, but still handle.
- Segment length < A: then l+i > r+i, but the interval [l+i, r+i] is empty if l+i > r+i? Actually if l > r (empty segment) we shouldn't have it. If length < A, then for any i ≥ A, l+i > r+i? No: l+i ≤ r+i always. But if l+i > N we skip. The interval [l+i, r+i] is valid but may be very short. We still process it normally.
- Bad intervals may cover everything except 1 and N? That's fine.

## worker: Implement the segment BFS in Python, using the goo
- I built the good (non-bad) segments by walking through the disjoint bad intervals. Since 1 is guaranteed to be good (L_i > 1) and N is guaranteed to be good (R_i < N), there is always at least one good segment containing 1 and one containing N.
- BFS is performed over segment indices, not individual squares. From a segment `[l, r]`, trying a step `i` gives the interval `[l+i, r+i]`. I find all good segments intersecting this interval using `bisect` and a forward scan. Because `B ≤ 20` and the number of segments ≤ 20001, the total work is well under a second.
- I included an early `break` when `l + A > N` (since steps are increasing) to avoid useless work.
- The algorithm correctly handles edge cases: `M=0` (one big segment), very small segments, and the start being already at `N` (which would print "Yes" immediately).
- The binary search part is slightly tricky because I need the first segment with `right >= new_l`, but I used `bisect_right` on lefts and then check intersection while scanning forward. This is safe because segments are sorted and disjoint.
