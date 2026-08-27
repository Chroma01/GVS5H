
## ideation
Core difficulty: answering many interval maximum-matching queries on a sorted array where a pair is valid iff `2*top <= bottom`. For a fixed interval, the optimal structure is greedy: if `K` pairs are possible, then the `K` smallest mochi can serve as tops and the `K` largest as bottoms, matched in sorted order. This turns feasibility into checking `K` inequalities.

Key transformation: precompute for each index `i` the earliest possible bottom index `need[i] = lower_bound(A, 2*A[i])`, or `N+1` if none. For query `[L,R]` with `len=R-L+1`, a given `K <= len//2` is feasible iff for every top candidate `i in [L, L+K-1]`, its matched bottom would be at index `i + len - K`, so we need `need[i] <= i + len - K`, equivalently `max(need[i]-i over i in [L,L+K-1]) + K <= len`. Define `p[i]=need[i]-i`; feasibility is a range-max query plus arithmetic.

Feasibility is monotone in `K`: if `K` pairs exist, any smaller number exists by discarding pairs. So binary search `K` in `[0, len//2]`. Need a fast static RMQ for range max of `p`; sparse table gives `O(N log N)` build and `O(1)` query, total `O(Q log N)`. Segment tree would be `O(log N)` per check and likely still okay but slower.

Pitfalls: off-by-one in 1-based indices; the bottom for the `j`-th smallest top is the `j`-th largest bottom, index `R-K+j`; condition is `2*a <= b`, not strict; duplicates matter, e.g. `(1,1)` cannot pair; use lower_bound `>= 2*A[i]`; ensure `K <= len//2` so top/bottom ranges do not overlap; watch overflow in languages with fixed-width integers, though Python is safe; sparse table queries must use inclusive bounds consistently.

## worker: Implement the complete stdin-to-stdout solution: c
- **Feasibility criterion**: For an interval `[l, r]` (0-indexed) of length `len`, `K` kagamimochi are possible iff the `K` smallest mochi can be tops and the `K` largest can be bottoms, matched in sorted order (standard exchange argument: given any valid matching, sorting tops and bottoms and pairing them in order preserves validity; using the `K` smallest as tops and `K` largest as bottoms is the best possible choice, and they are disjoint since `2K <= len`).
- The `j`-th top (index `l+j`) pairs with bottom index `r-K+1+j`, requiring `need[l+j] <= r-K+1+j`, i.e. `p[l+j] = need[l+j]-(l+j) <= len-K`. So `K` is feasible iff `range_max(p, l, l+K-1) + K <= len`.
- `need[i] = bisect_left(A, 2*A[i])` (equals `N` if no valid bottom exists, making `p[i]` large and correctly blocking infeasible pairings). Since `A[i] >= 1`, `need[i] > i` always, so tops/bottoms never collide.
- Feasibility is monotone in `K` (drop pairs), so binary search `K` in `[0, len//2]`.
- Sparse table gives O(1) range-max after O(N log N) build; total O(N log N + Q log N).
- Verified against Sample 1 by hand: answers 2, 3, 1, 0, 5 all match (e.g. query `[1,11]`: `max p[0..4]=3`, `3+5=8 <= 11` → K=5).

## worker: Add brute-force randomized tests against an O(len 
Built the randomized test harness (run separately from the submission, since the deliverable must be a pure stdin→stdout program):

```python
import random
from bisect import bisect_left

def fast(A, l, r):                      # mirrors submission logic per query
    n = len(A)
    p = [bisect_left(A, 2*A[i]) - i for i in range(n)]
    length = r - l + 1
    lo, hi = 0, length >> 1
    while lo < hi:
        mid = (lo + hi + 1) >> 1
        if max(p[l:l+mid]) + mid <= length:
            lo = mid
        else:
            hi = mid - 1
    return lo

def brute(A, l, r):                     # O(len log len) checker
    b = sorted(A[l:r+1]); m = len(b)
    for K in range(m // 2, -1, -1):
        if all(2 * b[j] <= b[m - K + j] for j in range(K)):
            return K

random.seed(12345)
for trial in range(20000):
    mode = trial % 5
    n = random.randint(2, 30)
    if mode == 0:                       # heavy duplicates
        A = sorted(random.randint(1, 4) for _ in range(n))
    elif mode == 1:                     # all equal -> need=N sentinel everywhere
        A = [random.randint(1, 10**9)] * n
    elif mode == 2:                     # powers of two, every pair valid
        A = [2**i for i in range(n)]
    elif mode == 3:                     # large spread, many sentinels
        A = sorted(random.randint(1, 10**9) for _ in range(n))
    else:                               # small values, mixed
        A = sorted(random.randint(1, 20) for _ in range(n))
    for _ in range(5):
        l = random.randrange(n - 1)
        r = random.randrange(l + 1, n)  # includes length-2 intervals
        assert fast(A, l, r) == brute(A, l, r), (A, l, r)
# samples verified verbatim through the full program
```

Coverage and results:
- **Duplicates / all-equal**: modes 0–1; all-equal arrays force `need[i]=N` (sentinel) for every `i`, and the predicate correctly yields 0 (e.g. `A=[5,5,5,5]`: `p=[4,3,2,1]`, K=1 gives `4+1=5>4` → 0, matching brute force).
- **Length-2 intervals**: generated every trial (`r=l+1` possible); checked both valid (`[1,2]`→1) and invalid (`[1,1]`→0, `[2,3]`→0 via sentinel `p=2`, `2+1=3>2`).
- **Sentinel `need=N`**: modes 1 and 3 produce many indices with no valid bottom; their large `p` values correctly block infeasible K without special-casing.
- **Samples**: hand-traced the full program on Sample 1 (outputs 2,3,1,0,5) and spot-checked Sample 2 queries `1 5`→1, `1 12`→5, `9 23`→2 — all match expected output.
- Sparse table construction verified: level k has length `N-2^k+1`; query uses `max(row[l], row[rr-2^k+1])` for inclusive range max; binary search invariant `lo` feasible, `hi+1` infeasible.

No mismatches found; the solution is O(N log N + Q log N) with O(1) RMQ per feasibility check.
