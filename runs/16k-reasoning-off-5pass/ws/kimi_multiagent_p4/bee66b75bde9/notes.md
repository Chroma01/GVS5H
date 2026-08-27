
## ideation
The core structure: each row is a black-prefix, each column is a black-top-prefix. If we let r[x] = number of black cells in row x (so row x has black cells in columns 1..r[x]), then cell (x,y) is black iff y <= r[x]. The column condition says: for each column y, the set of rows x with y <= r[x] must be a prefix of {1..N}. The set {x : r[x] >= y} being a prefix for every y is exactly equivalent to r being non-increasing: r[1] >= r[2] >= ... >= r[N]. (If r is non-increasing, {x: r[x] >= y} = {x : x <= max index with r >= y}, a prefix. Conversely, if r[x] < r[x+1] for some x, take y = r[x+1]; then row x+1 has black at column y but row x doesn't, violating the top-prefix property for column y.)

So the problem reduces to: find non-increasing sequence r[1..N], 0 <= r[x] <= N, satisfying:
- For each precolored B at (x,y): r[x] >= y.
- For each precolored W at (x,y): r[x] <= y-1.

Per row: L[x] = max y over B's in row x (0 if none), U[x] = min(y-1) over W's in row x (N if none). Need L[x] <= r[x] <= U[x]. If L[x] > U[x] for any row → immediate No.

Feasibility with monotonicity: process rows 1..N, maintain feasible interval [lo, hi] of possible r[x] values given rows so far. Initially before row 1, "previous value" is unbounded above (r[1] can be anything in [L[1],U[1]]). Transition: given previous feasible set is an interval [lo, hi] (it always stays an interval), new feasible set for row x is {v in [L[x], U[x]] : v <= some w in [lo,hi]} = [L[x], min(U[x], hi)] — nonempty iff L[x] <= min(U[x], hi), i.e., L[x] <= U[x] and L[x] <= hi. New interval: lo' = L[x], hi' = min(U[x], hi). Note lo doesn't propagate downward constraints since smaller values are always allowed downward (v can be as low as L[x] regardless). Wait — need to double-check: any v in [L[x], min(U[x],hi)] has some w >= v in [lo,hi]? Since v <= hi, pick w = max(v, lo)... w must be >= v and in [lo,hi]; since v <= hi, w = max(lo, v) <= hi works and >= v. Yes. So the interval invariant holds.

N up to 1e9 but M up to 2e5, so only rows with constraints matter; unconstrained rows have L=0, U=N: transition gives lo'=0, hi' = min(N, hi) = hi — no change. So we only process constrained rows in sorted order. Also rows with constraints: group by x.

Edge cases: N=1 with W → r[1] <= 0 → r[1]=0, fine (sample 3). Sample 2: (1,2) W → r[1] <= 1; (2,2) B → r[2] >= 2. Row1: [0,1], hi=1. Row2: L=2 > hi=1 → No. Correct.

Pitfalls: (a) must verify the equivalence rigorously — done above. (b) Multiple constraints same row — aggregate. (c) Rows must be processed in increasing x order. (d) L[x] > U[x] within a row → No. (e) Off-by-one: W at column y means r[x] <= y-1.

Complexity O(M log M) from sorting/grouping.

## worker: Write final Python solution: read N, M; aggregate 
- Reduced the problem to a non-increasing sequence r[1..N] (black prefix length per row). Column top-prefix condition ⟺ r non-increasing (proof: if r[x] < r[x+1], column y = r[x+1] has black at row x+1 but white at row x, violating prefix; conversely non-increasing r makes {x : r[x] >= y} a prefix for every y).
- Per row: B at (x,y) forces r[x] >= y (L[x] = max such y); W forces r[x] <= y-1 (U[x] = min such y-1).
- Sweep rows in increasing x maintaining hi = max feasible r value from previous rows. Feasible set stays an interval [L[x], min(U[x], hi)]; fail if L[x] > U[x] or L[x] > hi. Unconstrained rows (L=0, U=N) never change hi, so only constrained rows are processed — O(M log M).
- Verified against samples: (1) Yes; (2) row1 hi=1, row2 L=2 > 1 → No; (3) r[1]=0 → Yes; (4) produces No.
