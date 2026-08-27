import sys

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    M = int(next(it))
    B = []
    W = []
    for _ in range(M):
        x = int(next(it))
        y = int(next(it))
        c = next(it).decode()
        if c == 'B':
            B.append((x, y))
        else:
            W.append((x, y))

    # Black cells form a Ferrers shape anchored at top-left.
    # Let f(y) = number of black cells in column y (0..N), nonincreasing in y.
    # A black cell (x,y) forces f(y) >= x.
    # A white cell (x,y) forces f(y) <= x-1.
    # Feasibility: there exists a nonincreasing integer sequence f(1..N)
    # satisfying all lower/upper bounds at the constrained columns.

    # Collect constraints per column.
    from collections import defaultdict
    lo = defaultdict(int)   # lower bound on f(y), default 0
    hi = defaultdict(lambda: N)  # upper bound on f(y), default N

    for x, y in B:
        if x > lo[y]:
            lo[y] = x
    for x, y in W:
        if x - 1 < hi[y]:
            hi[y] = x - 1

    # Check immediate contradictions per column.
    cols = set(lo) | set(hi)
    for y in cols:
        if lo[y] > hi[y]:
            print("No")
            return

    # Sort constrained columns.
    ys = sorted(cols)

    # We need a nonincreasing integer sequence f over columns 1..N.
    # Between constrained columns, f can be chosen freely (constant or
    # decreasing). Feasibility condition: scanning columns left to right,
    # maintain the feasible range for f at the current column given
    # monotonicity (f can only decrease or stay equal as y increases).
    #
    # Let prev = feasible value range [L, R] at previous constrained column.
    # At the next constrained column y, f(y) must satisfy lo[y] <= f(y) <= hi[y]
    # and f(y) <= f(prev). Since we can decrease arbitrarily between columns,
    # the only requirement is that there exists v in [lo[y], hi[y]] with
    # v <= (chosen previous value). To keep maximum flexibility for the
    # future, we want the largest possible value at each step, but we must
    # ensure we don't go below lo[y].
    #
    # Greedy: maintain cur = maximum feasible value at current column.
    # Initially cur = N (f can start at most N).
    # At each constrained column y (in increasing order):
    #   cur = min(cur, hi[y])   # f can only decrease
    #   if cur < lo[y]: infeasible
    # This greedy is valid because choosing the largest possible value
    # never hurts future feasibility (future constraints only require
    # f to be small enough, and we can always decrease later).

    cur = N
    for y in ys:
        cur = min(cur, hi[y])
        if cur < lo[y]:
            print("No")
            return

    print("Yes")

solve()