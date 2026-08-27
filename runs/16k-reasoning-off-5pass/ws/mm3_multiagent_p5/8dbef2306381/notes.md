
## ideation
**Core difficulty:**  
N is up to 10^12, so we cannot simulate squares. M ≤ 2×10^4 and A,B ≤ 20 are small. Bad intervals are sorted, non-overlapping, with gaps of good squares between them.

**Reformulation:**  
Good positions are the gaps between (and outside) bad intervals. From any good position x we can jump to any good position y with A ≤ y−x ≤ B. We need to know if square N is reachable from 1.

**Key insight (interval BFS):**  
Maintain a *reachable region* as a contiguous interval [curL, curR] of good squares known to be reachable. Initially curL = curR = 1. Bad intervals are given sorted; good intervals (including [1,1] and the tail after the last bad interval) are also naturally sorted.

Take the first good interval [l, r] not yet processed whose start ≤ curR + A. Because we always pick the earliest such interval, all squares in [curL, curR] are reachable. Any such interval's squares are reachable (gap from curR to l is at most A−1, so we can jump onto l, and everything up to r is good). Then extend curR = max(curR, r). Repeat.

The loop advances an index `idx` through good intervals strictly monotonically → O(M). As soon as curR ≥ N, answer is Yes. If idx exhausts all good intervals without curR ≥ N, answer is No.

**Pitfalls to avoid:**
- Square 1 is guaranteed non-bad (L_i > 1), so [1,1] is a valid good interval.
- The final segment after the last bad interval goes up to N; must include it.
- Use while-loop (not just one step) because extending curR may newly satisfy the "next" interval too.
- B ≤ 20, A ≥ 1: keep types as Python ints (unbounded), no overflow.

## worker: Implement the solution in Python: parse N, M, A, B
The solution uses the classic interval-BFS / sweep technique for "jump game" style problems on a line with blocked regions. Because A and B are small (≤20) but N is huge, we compress the line into good intervals (gaps between bad intervals). We maintain a reachable region [curL, curR] starting at {1} and expand it by consuming good intervals whose left endpoint is within `curR + A`. Since the good intervals are sorted and each is processed at most once, the time complexity is O(M). Memory is O(M). Edge cases handled: square 1 is guaranteed non-bad (L_i > 1), and the final good segment after the last bad interval extends to N.

The initial while-loop in the code correctly implements the expansion: for each good interval `[l, r]` in order, if `l <= curR + A`, we can reach `l` (since the gap from `curR` to `l` is at most `A-1` squares, and we can jump exactly `A` or more up to `B` to land on `l`). Once `l` is reachable, the whole interval `[l, r]` becomes reachable (all good squares). We then extend `curR` to `max(curR, r)`. This may cause the next interval to also become reachable, which the loop handles naturally.
